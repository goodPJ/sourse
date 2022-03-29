/* behavioral simulation of IBM S/360 subset for CPSC 3300 at Clemson
 *
 */

#define INST_LR  0
#define INST_CR  1
#define INST_AR  2
#define INST_SR  3
#define INST_LA  4
#define INST_BCT 5
#define INST_BC  6
#define INST_ST  7
#define INST_L   8
#define INST_C   9

#include<stdio.h>
#include<stdlib.h>

int halt      = 0,
    pc        = 0,
    cond_code = 0,
    reg[16]   = {0},
    result;

unsigned opcode,
         r1,
         r2,
         b2,
         eff_addr,
         inst_addr;

unsigned char memory[4096] = {0};

int byte_count;  /* indicates how many memory words to display at end */
int verbose = 0; /* flag to control printing of cycle-by-cycle results */

/* dynamic execution counters */
int inst_fetch_cnt = 0,
    inst_cnt[10] = {0},
    bct_taken_cnt = 0,
    bc_taken_cnt = 0,
    mem_read_cnt = 0,  /* for this simple machine, equals L+C inst cnt */
    mem_write_cnt = 0; /* for this simple machine, equals ST inst cnt */


/* initialization routine to read in memory contents */

void load_memory(){
  int i = 0;
  unsigned input_value;

  if( verbose ){
    printf( "initial contents of memory arranged by bytes\n" );
    printf( "addr value\n" );
  }
  while( scanf( "%x", &input_value ) != EOF ){
    if( i >= 4096 ){
      printf( "program file overflows available memory\n" );
      exit( -1 );
    }
    memory[i] = input_value;
    if( verbose ) printf( "%03x: %02x\n", i, memory[i] );
    i++;
  }
  byte_count = i;
  if( verbose ) printf( "\n" );
}

void print_registers(){
  printf( "instruction address = %06x, ", pc );
  printf( "condition code = %x\n", cond_code );
  printf( "R0 = %08x, R4 = %08x, R8 = %08x, RC = %08x\n",
    reg[0], reg[4], reg[8], reg[12] );
  printf( "R1 = %08x, R5 = %08x, R9 = %08x, RD = %08x\n",
    reg[1], reg[5], reg[9], reg[13] );
  printf( "R2 = %08x, R6 = %08x, RA = %08x, RE = %08x\n",
    reg[2], reg[6], reg[10], reg[14] );
  printf( "R3 = %08x, R7 = %08x, RB = %08x, RF = %08x\n",
    reg[3], reg[7], reg[11], reg[15] );
}

void alignment_error( unsigned multiple, unsigned inst_addr,
  unsigned addr ){
  if( multiple == 2 ){
    printf( "\ninstruction fetch alignment error at %x to %x\n",
      inst_addr, addr );
  }else if( multiple == 4 ){
    printf( "\ndata access alignment error at %x to %x\n",
      inst_addr, addr );
  }else{
    printf( "\nunknown alignment error of %x at %x to %x\n)",
      multiple, inst_addr, addr );
  }
  exit( -1 );
}



/* main program */

int main( int argc, char **argv ){
  int i;

  if( argc > 1 ){
    if( ( argv[1][0] == '-' ) &&
        (( argv[1][1] == 'v' ) || ( argv[1][1] == 'V' )) ){

      verbose = 1;

    }else{
      printf( "usage: either %s or %s -v with input taken from stdin\n",
        argv[0], argv[0] );
      exit( -1 );
    }
  }
      

  printf( "\nbehavioral simulation of S/360 subset\n" );
  if( verbose ){
    printf( "\n(memory is limited to 4096 bytes in this simulation)\n" );
    printf( "(addresses, register values, and memory values are shown " );
    printf( "in hexadecimal)\n\n" );
  }

  load_memory();

  if( verbose ){
    printf( "initial pc, condition code, " );
    printf( "and register values are all zero\n\n" );
    printf( "updated pc, condition code, and register " );
    printf( "values are shown after\n" );
    printf( " each instruction has been executed\n" );
  }

  while( !halt ){

    if( pc > 0xffe ){
      printf( "\nout of range instruction address %x\n", pc );
      exit( -1 );
    }
    inst_addr = pc;
    opcode = memory[pc];
    r1 = (memory[pc+1] >> 4) & 0xf;
    r2 =  memory[pc+1]       & 0xf;
    pc = (pc + 2) & 0xffffff;
    if( opcode != 0 ) inst_fetch_cnt++;

    if( opcode > 0x20 ){
      b2 = (memory[pc] >> 4) & 0xf;
      eff_addr = memory[pc] & 0xf;
      eff_addr = (eff_addr << 8) | memory[pc+1];
      pc = (pc + 2) & 0xffffff;
      if( r2 != 0 ) eff_addr += reg[r2];
      if( b2 != 0 ) eff_addr += reg[b2];
      eff_addr = eff_addr & 0xffffff;
    }

    switch( opcode ){

      case 0:
        if( verbose ) printf( "\nHalt encountered\n" );
        halt = 1;
        break;

      case 0x18:                                 /* LR */
        if( verbose ){
          printf( "\nLR instruction, " );
          printf( "operand 1 is R%x, ", r1 );
          printf( "operand 2 is R%x\n", r2 );
        }
        reg[r1] = reg[r2];
        inst_cnt[INST_LR]++;
        break;

      case 0x19:                                 /* CR */
        if( verbose ){
          printf( "\nCR instruction, " );
          printf( "operand 1 is R%x, ", r1 );
          printf( "operand 2 is R%x\n", r2 );
        }
        result = reg[r1] - reg[r2];
        if( result == 0 )     cond_code = 0;
        else if( result < 0 ) cond_code = 1;
        else                  cond_code = 2;
        inst_cnt[INST_CR]++;
        break;

      case 0x1a:                                 /* AR */
        if( verbose ){
          printf( "\nAR instruction, " );
          printf( "operand 1 is R%x, ", r1 );
          printf( "operand 2 is R%x\n", r2 );
        }
        reg[r1] = reg[r1] + reg[r2];
        if( reg[r1] == 0 )     cond_code = 0;
        else if( reg[r1] < 0 ) cond_code = 1;
        else                   cond_code = 2;
        inst_cnt[INST_AR]++;
        break;

      case 0x1b:                                 /* SR */
        if( verbose ){
          printf( "\nSR instruction, " );
          printf( "operand 1 is R%x, ", r1 );
          printf( "operand 2 is R%x\n", r2 );
        }
        reg[r1] = reg[r1] - reg[r2];
        if( reg[r1] == 0 )     cond_code = 0;
        else if( reg[r1] < 0 ) cond_code = 1;
        else                   cond_code = 2;
        inst_cnt[INST_SR]++;
        break;

      case 0x41:                                 /* LA */
        if( verbose ){
          printf( "\nLA instruction, " );
          printf( "operand 1 is R%x, ", r1 );
          printf( "operand 2 at address %06x\n", eff_addr );
        }
        reg[r1] = eff_addr;
        inst_cnt[INST_LA]++;
        break;

      case 0x46:                                 /* BCT */
        if( verbose ){
          printf( "\nBCT instruction, " );
          printf( "operand 1 is R%x, ", r1 );
          printf( "branch target is address %06x\n", eff_addr );
        }
        reg[r1]--;
        if( reg[r1] != 0 ){
          if( (eff_addr & 1) != 0 ) alignment_error( 2, inst_addr, eff_addr );
          pc = eff_addr;
          bct_taken_cnt++;
        }
        inst_cnt[INST_BCT]++;
        break;

      case 0x47:                                            /* BC */
        if( verbose ){
          printf( "\nBC instruction, " );
          printf( "mask is %x, ", r1 );
          printf( "branch target is address %06x\n", eff_addr );
        }
        if( ( ( r1 & 8 ) && ( cond_code == 0 ) ) ||
            ( ( r1 & 4 ) && ( cond_code == 1 ) ) ||
            ( ( r1 & 2 ) && ( cond_code == 2 ) ) ||
            ( ( r1 & 1 ) && ( cond_code == 3 ) )    ){
          if( (eff_addr & 1) != 0 ) alignment_error( 2, inst_addr, eff_addr );
          pc = eff_addr;
          bc_taken_cnt++;
        }
        inst_cnt[INST_BC]++;
        break;

      case 0x50:                                            /* ST */
        if( verbose ){
          printf( "\nST instruction, " );
          printf( "operand 1 is R%x, ", r1 );
          printf( "operand 2 at address %06x\n", eff_addr );
        }
        if( (eff_addr & 3) != 0 ){
          alignment_error( 4, inst_addr, eff_addr );
        }
        if( eff_addr > 0xffc ){
          printf( "\nout of range data address\n" );
          exit( -1 );
        }
        memory[eff_addr]   = (reg[r1] >> 24) & 0xff;
        memory[eff_addr+1] = (reg[r1] >> 16) & 0xff;
        memory[eff_addr+2] = (reg[r1] >>  8) & 0xff;
        memory[eff_addr+3] =  reg[r1]        & 0xff;
        inst_cnt[INST_ST]++;
        mem_write_cnt++;
        break;

      case 0x58:                                            /* L */
        if( verbose ){
          printf( "\nL instruction, " );
          printf( "operand 1 is R%x, ", r1 );
          printf( "operand 2 at address %06x\n", eff_addr );
        }
        if( (eff_addr & 3) != 0 ){
          alignment_error( 4, inst_addr, eff_addr );
        }
        if( eff_addr > 0xffc ){
          printf( "\nout of range data address\n" );
          exit( -1 );
        }
        reg[r1] = memory[eff_addr];
        reg[r1] = (reg[r1] << 8) | memory[eff_addr+1];
        reg[r1] = (reg[r1] << 8) | memory[eff_addr+2];
        reg[r1] = (reg[r1] << 8) | memory[eff_addr+3];
        inst_cnt[INST_L]++;
        mem_read_cnt++;
        break;

      case 0x59:                                            /* C */
        if( verbose ){
          printf( "\nC instruction, " );
          printf( "operand 1 is R%x, ", r1 );
          printf( "operand 2 at address %06x\n", eff_addr );
        }
        if( (eff_addr & 3) != 0 ){
          alignment_error( 4, inst_addr, eff_addr );
        }
        if( eff_addr > 0xffc ){
          printf( "\nout of range data address\n" );
          exit( -1 );
        }
        result = memory[eff_addr];
        result = (result << 8) | memory[eff_addr+1];
        result = (result << 8) | memory[eff_addr+2];
        result = (result << 8) | memory[eff_addr+3];
        result = reg[r1] - result;
        if( result == 0 )     cond_code = 0;
        else if( result < 0 ) cond_code = 1;
        else                  cond_code = 2;
        inst_cnt[INST_C]++;
        mem_read_cnt++;
        break;

      default:
        printf( "\nunknown opcode %x at %x\n", opcode, inst_addr );
        exit( -1 );
    }

    if( verbose) print_registers();
  }

  if( verbose ){
    printf( "\nfinal contents of memory arranged by words\n" );
    printf( "addr value\n" );
    for( i = 0; i < byte_count; i = i + 4 ){
      result =   (memory[i]   << 24) | (memory[i+1] << 16)
               | (memory[i+2] << 8)  |  memory[i+3];
      printf( "%03x: %08x\n", i, result );
    }
  }

  printf( "\nexecution statistics\n" );
  printf( "  instruction fetches = %d\n", inst_fetch_cnt );
  printf( "    LR  instructions  = %d\n", inst_cnt[INST_LR] );
  printf( "    CR  instructions  = %d\n", inst_cnt[INST_CR] );
  printf( "    AR  instructions  = %d\n", inst_cnt[INST_AR] );
  printf( "    SR  instructions  = %d\n", inst_cnt[INST_SR] );
  printf( "    LA  instructions  = %d\n", inst_cnt[INST_LA] );
  printf( "    BCT instructions  = %d", inst_cnt[INST_BCT] );
  if( inst_cnt[INST_BCT] > 0 ){
    printf( ", taken = %d (%.1f%%)\n", bct_taken_cnt,
      100.0*((float)bct_taken_cnt)/((float)inst_cnt[INST_BCT]) );
  }else{
    printf("\n");
  }
  printf( "    BC  instructions  = %d", inst_cnt[INST_BC] );
  if( inst_cnt[INST_BC] > 0 ){
    printf( ", taken = %d (%.1f%%)\n", bc_taken_cnt,
      100.0*((float)bc_taken_cnt)/((float)inst_cnt[INST_BC]) );
  }else{
    printf("\n");
  }
  printf( "    ST  instructions  = %d\n", inst_cnt[INST_ST] );
  printf( "    L   instructions  = %d\n", inst_cnt[INST_L] );
  printf( "    C   instructions  = %d\n", inst_cnt[INST_C] );
  printf( "  memory data reads   = %d\n", mem_read_cnt );
  printf( "  memory data writes  = %d\n", mem_write_cnt );

  return 0;
}

