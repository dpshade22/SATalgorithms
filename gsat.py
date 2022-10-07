import os, time, random
from helpers import isInCol, cnfToDict, logData


def numSatisfies(currStateList, cnfDict):
    smallerStateList = []

    flipSatisfactionsDict = {}
    for boolNdx, state in enumerate(currStateList[1:]):
        numSatisfies = 0

        for _, values in cnfDict.items():
            x1 = (
                currStateList[values[0]]
                if values[0] > 0
                else not currStateList[abs(values[0])]
            )
            x2 = (
                currStateList[values[1]]
                if values[1] > 0
                else not currStateList[abs(values[1])]
            )
            x3 = (
                currStateList[values[2]]
                if values[2] > 0
                else not currStateList[abs(values[2])]
            )

            clauseBools = [x1, x2, x3]

            if clauseBools == [False, False, False] and boolNdx in values:
                numSatisfies += 1

        flipSatisfactionsDict[boolNdx] = numSatisfies

    mostSatisfied = max(flipSatisfactionsDict, key=flipSatisfactionsDict.get)
    return [mostSatisfied, flipSatisfactionsDict[mostSatisfied]]


def currStateFitness(currStateList, cnfDict):
    fitness = 0

    for _, value in cnfDict.items():
        x1 = (
            currStateList[value[0]]
            if value[0] > 0
            else not currStateList[abs(value[0])]
        )
        x2 = (
            currStateList[value[1]]
            if value[1] > 0
            else not currStateList[abs(value[1])]
        )
        x3 = (
            currStateList[value[2]]
            if value[2] > 0
            else not currStateList[abs(value[2])]
        )

        if x1 or x2 or x3:
            fitness += 1

    return fitness


def generateRandomGenome(nClauses):
    return [-1] + [random.choice([True, False]) for _ in range(nClauses)]


def gSat(cnfDict, maxTries):

    state = generateRandomGenome(len(cnfDict))
    fitnessDict = {}
    for _ in range(maxTries):
        toFlip = numSatisfies(state, cnfDict)[0]
        state[toFlip] = not state[toFlip]
        fitnessDict[tuple(state)] = currStateFitness(state, cnfDict)

    maxFitness = max(fitnessDict.values())

    return maxFitness


myDict = cnfToDict(f"./CNF Formulas/uf50-01.cnf")

for file in os.listdir("CNF Formulas"):
    if isInCol("gSat.csv", "fileName", file):
        continue

    print(file)
    lastProcess = time.process_time()

    currSAT = cnfToDict(f"./CNF Formulas/{file}")

    fitness = gSat(currSAT, 10)

    currProcess = time.process_time()
    totalTime = currProcess - lastProcess

    logData("gSat.csv", [file, totalTime, fitness])

for file in os.listdir("HARD CNF Formulas"):
    if isInCol("gSat.csv", "fileName", file):
        continue

    print(file)
    lastProcess = time.process_time()

    currSAT = cnfToDict(f"./HARD CNF Formulas/{file}")

    fitness = gSat(currSAT, 10)

    currProcess = time.process_time()
    totalTime = currProcess - lastProcess

    logData("gSat.csv", [file, totalTime, fitness])
