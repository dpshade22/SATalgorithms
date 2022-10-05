from random import choices, randint, random
from helpers import cnfToDict, logData, isInCol
import os, time, csv
import pandas as pd

Genome = list[int]
CnfDict = dict[int, list[int]]


class Individual:
    def __init__(self, genome=None, cnfDict=None) -> None:
        self.boolStates: Genome = []
        self.cnfDict: CnfDict = cnfDict
        self.fit = 0

    def generateGenome(self):
        self.boolStates = choices([True, False], k=len(self.cnfDict.values()))
        self.boolStates.insert(0, -1)

        return self

    def fitness(self):
        fitness = 0

        for key, value in self.cnfDict.items():
            x1 = (
                self.boolStates[value[0]]
                if value[0] > 0
                else not self.boolStates[abs(value[0])]
            )
            x2 = (
                self.boolStates[value[1]]
                if value[1] > 0
                else not self.boolStates[abs(value[1])]
            )
            x3 = (
                self.boolStates[value[2]]
                if value[2] > 0
                else not self.boolStates[abs(value[2])]
            )

            if x1 or x2 or x3:
                fitness += 1
        self.fit = fitness
        return fitness


Population = list[Individual]


def generatePopulation(satDict):
    return [Individual(None, satDict).generateGenome() for _ in range(len(satDict))]


def selectPair(population: Population):
    return choices(
        population=population,
        weights=[genome.fitness() for genome in population],
        k=2,
    )


def singlePointCross(a: Individual, b: Individual, satDict):
    p = randint(1, len(a.boolStates))

    return (
        Individual(a.boolStates[:p] + b.boolStates[p:], satDict).generateGenome(),
        Individual(b.boolStates[:p] + a.boolStates[p:], satDict).generateGenome(),
    )


def mutation(genome: Individual, num: int = 1, probability: float = 0.5):
    for _ in range(num):
        ndx = randint(1, len(genome.boolStates) - 1)
        genome.boolStates[ndx] = (
            genome.boolStates[ndx]
            if random() > probability
            else not genome.boolStates[ndx]
        )

    return genome


def evolution(
    populationFunc,
    selectFunc,
    crossoverFunc,
    mutationFunc,
    generationLimit: int,
    satDict,
):
    population: Population = populationFunc(satDict)

    for i in range(generationLimit):
        population = sorted(
            population, key=lambda genome: genome.fitness(), reverse=True
        )

        if population[0].fit == len(satDict):
            return population[0]

        nextGeneration = population[:2]

        for j in range(int(len(population) / 2) - 1):
            parents = selectFunc(
                population,
            )

            childA, childB = crossoverFunc(parents[0], parents[1], satDict)
            childA = mutationFunc(childA)
            childB = mutationFunc(childB)

            nextGeneration += [childA, childB]

        population = nextGeneration

    return population[0]


for file in os.listdir("CNF Formulas"):
    if (
        "rcnf" in file
        or "op" in file
        or "README" in file
        or isInCol("geneticAlgo.csv", "fileName", file)
    ):
        continue

    print(file)
    lastProcess = time.process_time()

    currSAT = cnfToDict(f"./CNF Formulas/{file}")

    fit = evolution(
        generatePopulation, selectPair, singlePointCross, mutation, 10, currSAT
    ).fit

    currProcess = time.process_time()
    totalTime = currProcess - lastProcess

    logData("geneticAlgo.csv", [file, totalTime, fit])

for file in os.listdir("HARD CNF Formulas"):
    if (
        "rcnf" in file
        or "op" in file
        or "README" in file
        or isInCol("geneticAlgo.csv", "fileName", file)
    ):
        continue

    print(file)
    lastProcess = time.process_time()

    currSAT = cnfToDict(f"./HARD CNF Formulas/{file}")

    fit = evolution(
        generatePopulation, selectPair, singlePointCross, mutation, 10, currSAT
    ).fit

    currProcess = time.process_time()
    totalTime = currProcess - lastProcess

    logData("geneticAlgo.csv", [file, totalTime, fit])
