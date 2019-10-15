import sys
import random
import math
import operator


### Finds entropy of one att
def entropy(pPos, pNeg):
    hEx = 0
    if(pPos == 0 or pNeg == 0 or (pPos + pNeg)== 0):
        # print('zero')
        return hEx
    p = 0
    n = 0
    p = pPos / (pPos + pNeg)
    n = pNeg / (pPos + pNeg)
    hEx = -1 * (p * math.log(p, 2) + n * math.log(n, 2))
    return hEx


## Finds remainder of one att
def remainder(incrementM, attDict, attName):
    currDict = dict()
    for i in attDict[attName]:
        currDict[i] = {'pPos': 0, 'pNeg' : 0}
    for j in incrementM:
        if(j["final"] == 'p'):
            currDict[j[attName]]['pPos'] += 1
        else:
            currDict[j[attName]]['pNeg'] += 1
    runningTot = 0
    temp = 0
    totalSize = len(incrementM)

    for i in currDict:
        temp = currDict[i]['pPos'] + currDict[i]['pNeg']
        runningTot += (temp / totalSize) * entropy(currDict[i]['pPos'], currDict[i]['pNeg'])
    return runningTot


### Finds most important att using infoTheory
def infoTheory(incrementM, attDict):
    attRank = {}
    poisonous = 0
    ediable = 0
    for i in incrementM:
        if(i["final"] == 'p'):
            poisonous += 1
        else:
            ediable += 1
    pPos = poisonous / (poisonous + ediable)
    pNeg = ediable / (poisonous + ediable)
    OverallEntropy = entropy(pPos, pNeg)

    for i in attDict: 
        if(i != 'final'): attRank[i] = OverallEntropy - remainder(incrementM, attDict, i)
    attRank = sorted(attRank.items(), key=lambda x:x[1], reverse=True)
    return (attRank[0][0])

### Gets all the mushrooms with that attName and att value specified
def attShrooms(data, attName, val):
    shroomsVal = []
    for i in data:
        if i[attName] == val:
            shroomsVal.append(i)
    return shroomsVal

### Finds the number correct per attName
def numCorrect(data, attName, attVal):
    numRight = 0
    p = 0
    e = 0
    maxLabel = 0
    for i in attVal:
        currData = attShrooms(data, attName, i)
        for j in currData:
            if j["final"] == 'p':
                p += 1
            else:
                e += 1

        if p > e:
            maxLabel = p
        else: 
            maxLabel = e
        numRight += maxLabel
        p = 0
        e = 0
    return numRight

### Finds most important att using counting method
def counting(incrementM, attDict):
    ranking = dict()
    for i in attDict:
        ranking[i] = numCorrect(incrementM, i, attDict[i].keys())
    ranking.pop('final')
    ranking = sorted(ranking.items(), key=lambda x:x[1], reverse=True)
    return ranking[0][0]

def mostImportant(heuristic, incrementM, attDict):
    if(heuristic == 'I'):
        return infoTheory(incrementM, attDict)
    else:
        return counting(incrementM, attDict)

