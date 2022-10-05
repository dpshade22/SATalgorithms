import pandas as pd
import csv


def cnfToDict(fileName: str) -> dict[int, str]:
    clauseDict = {}
    start = True
    numVars = -1
    numClauses = -1

    with open(fileName, "r") as cnf:
        lines = cnf.readlines()

        for i, line in enumerate(lines):
            if line[0] == "p":
                elem = line.split(" ")
                numVars = int(elem[2])
                if len(elem) <= 4:
                    numClauses = int(elem[3])
                else:
                    numClauses = int(elem[4])
                start = False
                lenStart = i
                continue
            elif start:
                continue
            elif line[0] == "%" or line[0] == "c":
                break

            line = line.strip("\n 0")
            line = line.split(" ")

            clauseDict[i - lenStart] = [int(x) for x in line]

    return clauseDict


def isInCol(csvName, colName, value):
    fileNameValuesDF = pd.read_csv(csvName)[colName].values

    return value in fileNameValuesDF


def logData(csvName, row):
    with open(csvName, "a", newline="\n") as f:
        writer = csv.writer(f)

        writer.writerow(row)
