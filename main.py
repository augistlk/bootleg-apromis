import subprocess
import random
import os
#variable fileName is the name of the .cpp file in the test/ directory
def compileC(fileName: str, testType:str):
    compile_result = subprocess.run(["g++", fileName, "-o", f"{testType}.exe"], capture_output=True, text=True, cwd="test")

    if compile_result.returncode != 0:
        print(f"Compilation of {testType} failed:")
        print(compile_result.stderr)
    else:
        print(f"Compilation {testType} successful!")

#amountOfTestsForFile is 

def inputGenerator():
    f = open("test/args.txt")
    global amountOfTests
    amountOfTests = int(f.readline())
    amountOfTestsForFile = int(f.readline())
    amountOfVariables: int = int(f.readline())
    variables = []
    #variables[x][y]  x is variable number, y is range(1 is from, 2 is to)
    for i in range(0,amountOfVariables):
        line = f.readline()
        start = int(line.split(" ")[0])
        end = int(line.split(" ")[1])
        variables.append((start, end))
    f.close()
    output = open("test/data.txt", "w")
    output.write(f"{amountOfTestsForFile}\n")
    for i in range(0,amountOfTestsForFile):
        for j in range(0,amountOfVariables):
            output.write(f"{random.randint(variables[j][0], variables[j][1])}")
            if j != amountOfVariables-1:
                output.write(" ")
        output.write("\n")
    output.close()

def initializer():
    f = open("test/args.txt")
    global amountOfTests
    amountOfTests = int(f.readline())
    f.close()

#testType must be either "test" or "user"
def runTest(testNumber: int, testType: str):
    executableFilename = f"test/{testType}.exe"
    runResult = subprocess.run([executableFilename], cwd="test")
    if runResult.returncode !=0:
        print(f"{testType} #{testNumber} didn't return 0")
    if testType == "test":
            os.replace("test/result.txt", "test/testResult.txt")
        

def runAndCompareResults():
    global amountOfTests
    compileC("test.cpp", "test")
    compileC("user.cpp", "user")
    testLog = open("testLog.txt", "w")
    for i in range(0, amountOfTests):
        inputGenerator()
        runTest(i+1, "test")
        runTest(i+1, "user")
        testResult = open("test/testResult.txt", "r")
        userResult = open("test/result.txt", "r")
        if testResult.read() == userResult.read():
            print(f"Test #{i+1} passed")
            testLog.write(f"Test #{i+1} passed\n")
        else:
            print(f"Test #{i+1} failed")
            testLog.write(f"Test #{i+1} failed\n")
        testResult.close()
        userResult.close()
    testLog.close()

def main():
    initializer()
    runAndCompareResults()

main()