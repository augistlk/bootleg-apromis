import subprocess
import random
import os
#variable fileLocation is path to the .cpp file
def compileC(fileLocation: str, test: int, testType:str):
    compile_result = subprocess.run(["g++", fileLocation, "-o", "test/a.exe"], capture_output=True, text=True)

    if compile_result.returncode != 0:
        print(f"Compilation of {testType} #{test} failed:")
        print(compile_result.stderr)
    else:
        print(f"Compilation {testType} #{test} successful!")

def inputGenerator():
    f = open("test/args.txt")
    global amountOfTests
    amountOfTests = int(f.readline())
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
    output.write(f"{amountOfTests}\n")
    for i in range(0,amountOfTests):
        for j in range(0,amountOfVariables):
            output.write(f"{random.randint(variables[j][0], variables[j][1])}")
            if j != amountOfVariables:
                output.write(" ")
        output.write("\n")
    output.close()

#testType must be either "Test" or "User"
def compileAndRun(fileLocation: str, testNumber: int, testType: str):
    compileC(fileLocation, testNumber, testType)
    executableLocation = fileLocation.split("/")[0] + "/a.exe"
    runResult = subprocess.run([executableLocation])
    if runResult.returncode !=0:
        print(f"{testType} #{testNumber} didn't return 0")
    if testType == "Test":
            os.replace("result.txt", "test/testResult.txt")
    else:
        os.replace("result.txt", "test/result.txt")
        

def runAndCompareResults():
    global amountOfTests
    for i in range(0, amountOfTests):
        compileAndRun("test/test.cpp", i+1, "Test")
        compileAndRun("test/user.cpp", i+1, "User")
        testResult = open("test/testResult.txt", "r")
        userResult = open("test/result.txt", "r")
        if testResult.read() == userResult.read():
            print(f"Test #{i+1} passed")
        else:
            print(f"Test #{i+1} failed")
        testResult.close()
        userResult.close()

def main():
    inputGenerator()
    runAndCompareResults()

main()