import os
from shutil import copyfile
from time import sleep
import subprocess

# Return string with no whitespace and converted entirely to lowercase
def clean(s: str) -> str:
    return ''.join(s.split()).lower()

# Gets the location of the `autograder` folder
# Isn't actually necessary to run on Gradescope, but it allows for easier testing on local machines
# where /autograder/ may not be a valid path.
def getAutograderDir() -> str:
    return '/'.join(__file__.split('/')[:-3])

# Finds the location of any file located in the `source` folder that ends in ".out" - this is assumed
# to be the student's submission. Returns `None` if the file can't be found
def findExecutable() -> str:
    sourceDir = getAutograderDir() + '/source'
    outFile = [x for x in os.listdir(sourceDir) if '.out' in x]

    return None if len(outFile)==0 else sourceDir+'/'+outFile[0]

# Checks if all the expected files are present, and raises an error if any of them are missing
# Is used by the `test_checkFiles` test case
def checkFiles(files: list):
    autograderDir = getAutograderDir()
    submissionDir = autograderDir + '/submission/'

    # Array containing the full path location for every submitted file. Typically is `/autograder/submission/myFile`,
    # but this is written to be more robust to allow for easier local testing
    allFiles = [os.path.join(dp, f) for dp, dn, filenames in os.walk(submissionDir) for f in filenames]

    # Array containing the full path to every file that the student submitted that was *expected*
    # In other words, this array discards any files submitted that weren't expected to be submitted
    submittedFiles = [i for i in allFiles if i.split('/')[-1] in files]

    # This seems weird - it should yield the exact same array as `submittedFiles`, unsure why this exists lol
    filesSubmitted = list()
    for file in files:
        for fileDir in submittedFiles:
            if fileDir.split('/')[-1] == file:
                filesSubmitted.append(fileDir.split('/')[-1])

    # Get list of expected files that are missing from submission
    filesMissing = [file for file in files if file not in filesSubmitted]

    # If any files are missing, throw an error and display the missing files
    if len(filesMissing) != 0:
        raise AssertionError("ERROR: You are missing the following files:\n{}".format(' '.join(filesMissing)))

# Copies specified files from the `submission` folder to the `source` folder
def copyFiles(files: list):
    autograderDir = getAutograderDir()
    submissionDir = autograderDir + '/submission/'
    sourceDir = autograderDir + '/source/'

    # Get all files in `submission` folder
    allFiles = [os.path.join(dp, f) for dp, dn, filenames in os.walk(submissionDir) for f in filenames]

    # Get all files from `allFiles` that are specified in the function's input
    validFiles = [i for i in allFiles if i.split('/')[-1] in files]
    
    # Copy each file to the `source` directory
    for file in validFiles:
        copyfile(file, sourceDir+file.split('/')[-1])

# Class used to represent the result of a student's submission
class Submission:
    """
    output - string containing the program's output (stdout)
    errors - string containing the program's errors (stderr)
    timedout - True if the submission timed out during execution, False otherwise
    """
    output: str
    errors: str
    timedout: bool

    def __init__(self, output: str, errors:str, timedout: bool):
        self.output = output
        self.errors = errors
        self.timedout = timedout

# Runs the program
def runProgram(executable: str = None, inputFile: str = None, txtContents: str = None, timeout: float = 0.1) -> str:
    """
    Run the specified executable with given input and return its output

    executable - string containing the name of the executable to run. If not specified,
                    the first file that ends in ".out" will be executed. Default is `None`
    inputFile -  string containing the name of a text file containing user input, separated by newlines.
                    Default is `None`
    txtContents - string containing the user input, separated by newlines. Default is `None`.
    timeout - float specifying how many seconds to wait before terminating the program. Default is 0.1
    """

    # If there is no specified .out file, find the .out file in the `source` dir
    # If no executable is found, throw an error
    if executable is None:
        executable = findExecutable()
        if executable is None:
            raise AssertionError(".out file does not exist - your program may have failed to compile.")

    try:
        # Get user input as a stream of bytes, either from file specified by `inputFile` or from `txtContents`
        if inputFile:
            with open(inputFile, 'r') as f:
                txtContents = bytes(f.read(), 'ascii')
        elif txtContents:
            txtContents = bytes(txtContents, 'ascii')

        
        sleep(1) # Sometimes, not having this would result in test cases being unable to access the executable,
                    # presumably because another test case was still running.

        # Run the code submission, use txtContents to serve as user input, and timeout after `timeout` seconds
        # `subprocess.run()` returns a `CompletedProcess` object which contains the stdout and stderr
        results = subprocess.run([executable], 
                        stdout=subprocess.PIPE,
                        timeout=timeout,
                        input=txtContents)
        timedout = False

    # If submission times out, the TimeoutExpired object still contains the stdout and stederr,
    # so we can simply use the exception object as we would the CompletedProcess object
    except subprocess.TimeoutExpired as e:
        results = e
        timedout = True

    # If unexpected input is piped to program, stdout can often contain information in memory that goes past
    # the bounds of the file. To filter this out, we split the bytes string based on the location of ELF,
    # and only keep everything that was before ELF. This should result in only the submission's actual output
    # being displayed. This is not an issue with stderr.
    stdout = '' if results.stdout is None else results.stdout.split(b'\x7fELF')[0].decode('utf-8')
    stderr = '' if results.stderr is None else results.stderr.decode('utf-8')
    
    # If the standard output or error are longer than 1500 chars, truncate them
    truncationMessage = '\n\n** The output exceeded 1500 characters, so it was truncated **'
    if len(stdout) > 1500:
        stdout = stdout[:1500] + truncationMessage
    if len(stderr) > 1500:
        stderr = stderr[:1500] + truncationMessage

    # Create a `Submission` object containing the results of the program's execution and return it
    submission = Submission(stdout, stderr, timedout)
    return submission