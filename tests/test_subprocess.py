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
        fib = subprocess.Popen(["gcc sim.c -o sim.out"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        errors = fib.stderr.read().strip().decode('utf-8')
        fib.kill()
        fib.terminate()

        # Another artificial delay
        sleep(1)
        
        # Display errors if there are any
        if errors != "":
            msg = "Unable to cleanly compile program.\n"
            msg += "Compilation errors are as follows:\n"
            msg += errors
            raise AssertionError(msg)

# This class should contain any "normal" test cases - basically anything that you want to run AFTER compilation
# Note: the only way to impact the order that test cases run is by putting them in new classes that are alphabetically sorted.
# Any test cases that are put in the same class as each other should be fully independent and should not rely on each other.
class Test02_Execution(unittest.TestCase):
    @number("2")
    @weight(5)
    def test_1(self):
        """test case: bad_bct, non verbose"""
        # Run program with "q" as the only input.
        # Make sure that "\n" follows every input item, as that represents pressing enter
        # If you wanted to enter "a", then "b", then "c", you would do txtContents="a\nb\nc\n"
        
        inputFile = open("bad_bct.txt", "r")
        inputString = inputFile.read()
        submission = runProgram(txtContents=inputString)

        # Array of expected strings
        expectedFile = open("bad_bct_output.txt", "r")
        expectedString = expectedFile.read()
        expectedArr = expectedString.split("\n")

        # Error message
        errorMsg = f"Failed at test case: bad_bct.in(non verbose), recheck your output. -5pts\n{submission.output}"
        
        # Iterate through every expected string. If it isn't present in the submission's output, display the error message
        for expected in expectedArr:
            # MAKE SURE YOU USE THE `clean()` function!
            # This function removes all whitespace and capitalization from the string that is passed in
            # You want to use clean on `expected` and the submission's output to ensure students aren't penalized for whitespace or capitalization
            if clean(expected) not in clean(submission.output):
                raise AssertionError(errorMsg)
    
    @number("3")
    @weight(5)
    def test_2(self):
        """test case: bad_load, non verbose"""
        # Run program with "q" as the only input.
        # Make sure that "\n" follows every input item, as that represents pressing enter
        # If you wanted to enter "a", then "b", then "c", you would do txtContents="a\nb\nc\n"
        
        inputFile = open("bad_load.txt", "r")
        inputString = inputFile.read()
        submission = runProgram(txtContents=inputString)

        # Array of expected strings
        expectedFile = open("bad_load_output.txt", "r")
        expectedString = expectedFile.read()
        expectedArr = expectedString.split("\n")

        # Error message
        errorMsg = f"Failed at test case: bad_load.in(non verbose), recheck your output. -5pts\n{submission.output}"
        
        # Iterate through every expected string. If it isn't present in the submission's output, display the error message
        for expected in expectedArr:
            # MAKE SURE YOU USE THE `clean()` function!
            # This function removes all whitespace and capitalization from the string that is passed in
            # You want to use clean on `expected` and the submission's output to ensure students aren't penalized for whitespace or capitalization
            if clean(expected) not in clean(submission.output):
                raise AssertionError(errorMsg)

    @number("4")
    @weight(15)
    def test_3(self):
        """test case: compare, verbose"""
        # Run program with "q" as the only input.
        # Make sure that "\n" follows every input item, as that represents pressing enter
        # If you wanted to enter "a", then "b", then "c", you would do txtContents="a\nb\nc\n"
        

        inputFile = open("compare.txt", "r")
        inputString = inputFile.read()
        submission = runProgram(txtContents=inputString, args=['-v'])

        # Array of expected strings
        expectedFile = open("compare_verbose.txt", "r")
        expectedString = expectedFile.read()
        expectedArr = expectedString.split("\n")

        # Error message
        errorMsg = f"Failed at test case: compare.in(verbose), recheck your output. -15pts\n{submission.output}"
        
        # Iterate through every expected string. If it isn't present in the submission's output, display the error message
        for expected in expectedArr:
            # MAKE SURE YOU USE THE `clean()` function!
            # This function removes all whitespace and capitalization from the string that is passed in
            # You want to use clean on `expected` and the submission's output to ensure students aren't penalized for whitespace or capitalization
            if clean(expected) not in clean(submission.output):
                raise AssertionError(errorMsg)

    @number("5")
    @weight(5)
    def test_4(self):
        """test case: oor_pc, verbose"""
        # Run program with "q" as the only input.
        # Make sure that "\n" follows every input item, as that represents pressing enter
        # If you wanted to enter "a", then "b", then "c", you would do txtContents="a\nb\nc\n"
        

        inputFile = open("oor_pc.txt", "r")
        inputString = inputFile.read()
        submission = runProgram(txtContents=inputString, args=['-v'])

        # Array of expected strings
        expectedFile = open("oor_pc_verbose.txt", "r")
        expectedString = expectedFile.read()
        expectedArr = expectedString.split("\n")

        # Error message
        errorMsg = f"Failed at test case: oor_pc.in(verbose), recheck your output. -5pts\n{submission.output}"
        
        # Iterate through every expected string. If it isn't present in the submission's output, display the error message
        for expected in expectedArr:
            # MAKE SURE YOU USE THE `clean()` function!
            # This function removes all whitespace and capitalization from the string that is passed in
            # You want to use clean on `expected` and the submission's output to ensure students aren't penalized for whitespace or capitalization
            if clean(expected) not in clean(submission.output):
                raise AssertionError(errorMsg)

    @number("6")
    @weight(25)
    def test_5(self):
        """test case: regular_loop, verbose"""
        # Run program with "q" as the only input.
        # Make sure that "\n" follows every input item, as that represents pressing enter
        # If you wanted to enter "a", then "b", then "c", you would do txtContents="a\nb\nc\n"
        

        inputFile = open("regular_loop.txt", "r")
        inputString = inputFile.read()
        submission = runProgram(txtContents=inputString, args=['-v'])

        # Array of expected strings
        expectedFile = open("regular_loop_verbose.txt", "r")
        expectedString = expectedFile.read()
        expectedArr = expectedString.split("\n")

        # Error message
        errorMsg = f"Failed at test case: regular_loop.in(verbose), recheck your output. -25pts\n{submission.output}"
        
        # Iterate through every expected string. If it isn't present in the submission's output, display the error message
        for expected in expectedArr:
            # MAKE SURE YOU USE THE `clean()` function!
            # This function removes all whitespace and capitalization from the string that is passed in
            # You want to use clean on `expected` and the submission's output to ensure students aren't penalized for whitespace or capitalization
            if clean(expected) not in clean(submission.output):
                raise AssertionError(errorMsg)

    @number("7")
    @weight(15)
    def test_6(self):
        """test case: simple_add, verbose"""
        # Run program with "q" as the only input.
        # Make sure that "\n" follows every input item, as that represents pressing enter
        # If you wanted to enter "a", then "b", then "c", you would do txtContents="a\nb\nc\n"
        

        inputFile = open("simple_add.txt", "r")
        inputString = inputFile.read()
        submission = runProgram(txtContents=inputString, args=['-v'])

        # Array of expected strings
        expectedFile = open("simple_add_verbose.txt", "r")
        expectedString = expectedFile.read()
        expectedArr = expectedString.split("\n")

        # Error message
        errorMsg = f"Failed at test case: simple_add.in(verbose), recheck your output. -15pts\n{submission.output}"
        
        # Iterate through every expected string. If it isn't present in the submission's output, display the error message
        for expected in expectedArr:
            # MAKE SURE YOU USE THE `clean()` function!
            # This function removes all whitespace and capitalization from the string that is passed in
            # You want to use clean on `expected` and the submission's output to ensure students aren't penalized for whitespace or capitalization
            if clean(expected) not in clean(submission.output):
                raise AssertionError(errorMsg)

    @number("8")
    @weight(20)
    def test_7(self):
        """test case: simple_loop, verbose"""
        # Run program with "q" as the only input.
        # Make sure that "\n" follows every input item, as that represents pressing enter
        # If you wanted to enter "a", then "b", then "c", you would do txtContents="a\nb\nc\n"
        

        inputFile = open("simple_loop.txt", "r")
        inputString = inputFile.read()
        submission = runProgram(txtContents=inputString, args=['-v'])

        # Array of expected strings
        expectedFile = open("simple_loop_verbose.txt", "r")
        expectedString = expectedFile.read()
        expectedArr = expectedString.split("\n")

        # Error message
        errorMsg = f"Failed at test case: simple_loop.in(verbose), recheck your output. -20pts\n{submission.output}"
        
        # Iterate through every expected string. If it isn't present in the submission's output, display the error message
        for expected in expectedArr:
            # MAKE SURE YOU USE THE `clean()` function!
            # This function removes all whitespace and capitalization from the string that is passed in
            # You want to use clean on `expected` and the submission's output to ensure students aren't penalized for whitespace or capitalization
            if clean(expected) not in clean(submission.output):
                raise AssertionError(errorMsg)

    @number("9")
    @weight(10)
    def test_8(self):
        """test case: simple_loop, non verbose"""
        # Run program with "q" as the only input.
        # Make sure that "\n" follows every input item, as that represents pressing enter
        # If you wanted to enter "a", then "b", then "c", you would do txtContents="a\nb\nc\n"
        
        inputFile = open("simple_loop.txt", "r")
        inputString = inputFile.read()
        submission = runProgram(txtContents=inputString)

        # Array of expected strings
        expectedFile = open("simple_loop_output.txt", "r")
        expectedString = expectedFile.read()
        expectedArr = expectedString.split("\n")

        # Error message
        errorMsg = f"Failed at test case: simple_loop.in(non verbose), recheck your output. -10pts\n{submission.output}"
        
        # Iterate through every expected string. If it isn't present in the submission's output, display the error message
        for expected in expectedArr:
            # MAKE SURE YOU USE THE `clean()` function!
            # This function removes all whitespace and capitalization from the string that is passed in
            # You want to use clean on `expected` and the submission's output to ensure students aren't penalized for whitespace or capitalization
            if clean(expected) not in clean(submission.output):
                raise AssertionError(errorMsg)