import subprocess
import random
import os
import string
#variable fileName is the name of the .cpp file in the test/ directory
def compileC(fileName: str, testType:str):
    compile_result = subprocess.run(["g++", fileName, "-o", f"{testType}.exe"], capture_output=True, text=True, cwd="test")

    if compile_result.returncode != 0:
        print(f"Compilation of {testType} failed:")
        print(compile_result.stderr)
        print("\nProcess terminated due to abnormal compilation")
        exit()
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
    allowedTypes = ['int', 'string']
    #variables[i][x] i is index, x when 0 is type, if type is string 1 is length, else 1 is range from, 2 is range to
    for i in range(0,amountOfVariables):
        line = f.readline()
        type = line.split(" ")[0]
        if type not in allowedTypes:
            print(f"Unexpected type '{type}'. Only supported types are so far 'int' and 'string'\n")
            print("Terminating process")
            exit()
        start = int(line.split(" ")[1])
        if type != "string":
            end = int(line.split(" ")[2])
        else:
            end = 0
        variables.append((type, start, end))
    f.close()
    output = open("test/data.txt", "w")
    output.write(f"{amountOfTestsForFile}\n")
    for i in range(0,amountOfTestsForFile):
        for j in range(0, amountOfVariables):
            if variables[j][0] == "string":
                writeVariable = ''.join(random.choices(string.ascii_letters, k=variables[j][1]))
            elif variables[j][0] == "int":
                writeVariable = random.randint(variables[j][1], variables[j][2])
            else:
                print(f"Unexpected type {variables[j][0]}. Only supported types are so far int and string")
                break
            output.write(f"{writeVariable}")
            if j != amountOfVariables:
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
        print("\n Process terminated due to abnormal execution of test")
        exit()
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