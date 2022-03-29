from re import sub
import unittest
import subprocess
from time import sleep
from gradescope_utils.autograder_utils.decorators import weight, number

from utils import *


# Put this class in all of your autograders. This class handles checking that the required files
# exist, and it also handles compilation. Make sure all your classes begin with `Test`, and can
# be sorted alphabetically so that this class runs first. `pytest`, the library that works in the
# background to make all of this possible, runs classes that begin with `Test` in alphabetical order,
# and you want this class to run first so that any file or compilation errors can be handled BEFORE
# any of the other test cases.
class Test01_Setup(unittest.TestCase):
    # Array of all the expected file names
    files = ['sim.c']

    # Unused function. According to the Gradescope docs, this function is supposed to run before
    # any of the other functions in this class, but doesn't act as an actual test case. Just leaving
    # this here in case you find any use for it.
    def setUp(self):
        pass
    
    # Use `number` to set the display order for test cases on Gradescope. Does not affect execution order.
    # Use `weight` to specify how many points you want this test case to be worth.
    @number("0")
    @weight(0)
    def test_checkFiles(self):
        """Ensure all required files are present"""
        
        checkFiles(self.files)
        sleep(1) # Honestly, don't remember what this was for - I think there were some weird errors
                 # that could happen when compiling if there wasn't an artificial delay put here, but
                 # I unfortunately don't remember the details. Feel free to remove and do some testing yourself.


    @number("1")
    @weight(0)
    def test_Compile(self):
        """Clean Compile"""
        
        # Copies the files located in the `submission` directory to the `source` directory
        copyFiles(self.files)

        #can change the make command here if necessary
        fib = subprocess.Popen(["gcc sim.c -o sim.out"], shell = True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #fib = subprocess.Popen(["gcc", "-c",  "sim.c"], stdout=subprocess.PIPE, stderr=subprocess.PIPE )
        errors = fib.stderr.read().strip().decode('utf-8')
        fib.kill()
        fib.terminate()

        # Another artificial delay
        sleep(1)
        
        # Display errors if there are any
        if errors != "":
            msg = "Unable to cleanly compile program. Try compiling with the \"-Wall\" flag and see if any errors occur.\n"
            msg += "Compilation errors are as follows:\n"
            msg += errors
            raise AssertionError(msg)

# This class should contain any "normal" test cases - basically anything that you want to run AFTER compilation
# Note: the only way to impact the order that test cases run is by putting them in new classes that are alphabetically sorted.
# Any test cases that are put in the same class as each other should be fully independent and should not rely on each other.
class Test02_Execution(unittest.TestCase):
    @number("2")
    @weight(25)
    def test_Menu(self):
        """Check that prompt exists"""
        # Run program with "q" as the only input.
        # Make sure that "\n" follows every input item, as that represents pressing enter
        # If you wanted to enter "a", then "b", then "c", you would do txtContents="a\nb\nc\n"
        submission = runProgram(inputFile='simple_loop.in')
        #print(submission.output)
        # Array of expected strings
        expectedFile = open("simple_loop.output", "r")
        expectedArr = expectedFile.read().split("\n")

        # Error message
        errorMsg = f"failed at case:   , - 100 { submission.output}"        
        # Iterate through every expected string. If it isn't present in the submission's output, display the error message
        for expected in expectedArr:
            # MAKE SURE YOU USE THE `clean()` function!
            # This function removes all whitespace and capitalization from the string that is passed in
            # You want to use clean on `expected` and the submission's output to ensure students aren't penalized for whitespace or capitalization
            if clean(expected) not in clean(submission.output):
                raise AssertionError(errorMsg)