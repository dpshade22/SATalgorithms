import random, os, time
from helpers import cnfToDict, logData, isInCol

# solve_dpll(cnf):
#     while(cnf has a unit clause {X}):
#         delete clauses contatining {X}
#         delete {!X} from all clauses
#     if null clause exists:
#         return False
#     if CNF is null:
#         return True
#     select a literal {X}
#     cnf1 = cnf + {X}
#     cnf2 = cnf + {!X}
#     return solve_dpll(cnf1)+solve_dpll(cnf2)


def cnfHasClauseWithX(cnfDict, x):
    toDel = set()
    for key, values in cnfDict.items():
        if x in values:
            toDel.add(key)
        if -x in values:
            values.remove(-x)

    for key in toDel:
        del cnfDict[key]

    return cnfDict


def mostPopularLiteral(cnfDict):
    literalsDict = {}
    for key, values in cnfDict.items():
        for value in values:
            if literalsDict.get(abs(value)) is None:
                literalsDict[abs(value)] = 1
            else:
                literalsDict[abs(value)] += 1

    return max(literalsDict, key=literalsDict.get)


def nullClauses(cnfDict):
    nullClauses = 0
    for key, values in cnfDict.items():
        if not values:
            nullClauses += 1

    return (False, nullClauses) if nullClauses == 0 else (True, nullClauses)


def dpll(cnfDict):
    newLiteral = mostPopularLiteral(cnfDict)
    cnfDict = cnfHasClauseWithX(cnfDict, newLiteral)
    fitness = 0

    while nullClauses(cnfDict)[0] and cnfDict != {}:
        newLiteral = mostPopularLiteral(cnfDict)
        cnfDict = cnfHasClauseWithX(cnfDict, newLiteral)

    hasNullClause, numNulls = nullClauses(cnfDict)

    if not hasNullClause:
        fitness = len(cnfDict) - numNulls
    elif cnfDict == {}:
        fitness = len(cnfDict)

    return fitness


# def dpll(cnfDict, literal, model=[]):
#     cnfDict = cnfHasClauseWithX(cnfDict, literal)
#     model.append(literal)

#     if nullClauses(cnfDict)[0]:
#         return False, nullClauses(cnfDict)[1]
#     if cnfDict == {}:
#         return True, 0

#     newLiteral = mostPopularLiteral(cnfDict)

#     return dpll(cnfDict, newLiteral) or dpll(cnfDict, not newLiteral)


for file in os.listdir("CNF Formulas"):
    if isInCol("dpll.csv", "fileName", file):
        continue

    print(file)
    lastProcess = time.process_time()

    currSAT = cnfToDict(f"./CNF Formulas/{file}")

    fit = dpll(currSAT)

    currProcess = time.process_time()
    totalTime = currProcess - lastProcess

    logData("dpll.csv", [file, totalTime, fit])

for file in os.listdir("HARD CNF Formulas"):
    if isInCol("dpll.csv", "fileName", file):
        continue

    print(file)
    lastProcess = time.process_time()

    currSAT = cnfToDict(f"./HARD CNF Formulas/{file}")

    fit = dpll(currSAT)

    currProcess = time.process_time()
    totalTime = currProcess - lastProcess

    logData("dpll.csv", [file, totalTime, fit])
