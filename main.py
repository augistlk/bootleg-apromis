import subprocess
import random
#variable "test" is path to the .cpp file
def compileC(test: str):
    compile_result = subprocess.run(["g++", test, "-o", "hello"], capture_output=True, text=True)

    if compile_result.returncode != 0:
        print(f"Compilation of {test} failed:")
        print(compile_result.stderr)
    else:
        print(f"Compilation {test} successful!")

def inputGenerator():
    f = open("test/args.txt")
    amountOfTests: int = int(f.readline())
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

inputGenerator()