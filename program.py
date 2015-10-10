"""
This file deals with:
    Accepting input
    Running the generated code
    Dealing with the output
A file called temp.py is created from the inputs.
A file called temp.out is created after running (redirected stdout)
We'll grab the corresponding the input file and correct output file from some folder and use those.
"""

import sys
import filecmp
import os

class Buffer:

    id = 0 # Tracker between different games

    def __init__(self, problem_name):
        self.problem_name = problem_name
        self.file_name = "t" + str(Buffer.id)
        self.file = open(self.file_name + ".py", "w")
        Buffer.id = (Buffer.id + 1) % 10000000
        
    """
    Takes in string PROBLEM and finds the corresponding input file.
    Uses temp.py to run the program with input and produce temp.out
    """
    def readFile(self):
        # Dig out input file.
        inFile = open("inputs/" + self.problem_name + ".in", "r")
        sys.stdin = inFile

        # Initialize temp.out
        output = open(self.file_name + ".out", "w")
        sys.stdout = output
        
        # Read the file
        self.file.close()
        try:
            module = __import__(self.file_name)
        except Exception as e:
            print(e)
            
        # Redirect I/O to normal, close file
        sys.stdin = sys.__stdin__
        sys.stdout = sys.__stdout__
        inFile.close()
        output.close()

    """
    Check if the outputed file and correct answer are equal.
    """
    def checkFile(self):
        return filecmp.cmp(self.file_name + ".out", "outputs/" + self.problem_name + ".out")
    
    """
    Accepts a character input. Probably doesn't support newline/tab.
    """
    def accept(self, character):
        assert len(character) <= 2
        self.file.write(character)
        
    """
    Does garbage collection.
    """
    def close(self):
        self.file.close()
        os.remove(self.file_name + ".py")
        os.remove(self.file_name + ".out")
    
"""
Global code for debugging purposes.
"""

"""
buffer = Buffer("sum")
while True:
    s = input()
    if s == "`":
        break
    buffer.accept(s)
buffer.readFile()
print(buffer.checkFile())
buffer.close()
"""