import sys
import random
import math
import operator
import copy
import csv
from infoTheory import infoTheory, counting
from trainingTree import node, DecisionTreeTrain, mostFeqLabel

### Tests the rest of the data for accuracy
def testing(shroomTotData, trainingTree):
    currNode = trainingTree
    correct = 0
    for shroom in shroomTotData:
        while( currNode.att != 'final'):
            currAtt = 0
            while currNode.children[currAtt].attVal != shroom[currNode.att]:
                currAtt += 1
            currNode = currNode.children[currAtt]
        if(currNode.guess == shroom['final']):
            correct += 1
        currNode = trainingTree
    return correct, len(shroomTotData)

def iteration(shroomTotData, increment, attDict, attName, heuristic):
    ### Gets the increment of the training data
    incrementM = []
    for i in range(increment):
        incrementM.append(shroomTotData[i])
    ### Adjust att based on incrementM
    for i in incrementM:
        for j in attName:
            attDict[j][i[j]] += 1
    guess = mostFeqLabel(shroomTotData)
    root = DecisionTreeTrain(incrementM, attDict, guess, '', heuristic)
    return root

def main():
    tSize = int(input("Please enter a training set size (a positive multiple of 250 that is <= 1000): "))
    increment = int(input("Please enter a training increment (either 10, 25, or 50):"))
    assert(increment == 25 or increment == 10 or increment == 50),"Need to input 10, 25, or 50"
    heuristic = input("Please enter a heuristic to use (either [C]ounting-based or [I]nformation theoretic): ")
    assert(heuristic == 'C' or heuristic == 'I'), "Need to input C or I"
    
    print('Loading Property Information from file.')
    with open(sys.argv[1], 'r') as fp:
        attList = fp.readline()
        attDict = dict()
        attName = []
        while attList:
            attList = attList[:-1]
            line = attList.split(':')
            attDict[line[0]] = dict()
            attName.append(line[0])
            for j in line[1].split(' ')[1:]:
                attDict[line[0]][j] = 0
            attList = fp.readline()
        attDict["final"] = {'e' : 0, 'p': 0}
        attName.append("final")
    tempDict = copy.deepcopy(attDict)
        
            
    print('Loading Data from database.')
    ### Stores a list of shroomObj
    with open(sys.argv[2], 'r') as fp2:
        shroomTotData = []
        inputData = fp2.readline()
        while(inputData):
            shroomAtt = inputData.replace(' ', '')
            shroomObj = dict()
            for j in (range(len(shroomAtt)-1)):
                shroomObj[attName[j]] = shroomAtt[j]
            shroomObj["final"] = shroomAtt[-2:-1]
            shroomTotData.append(shroomObj)
            inputData = fp2.readline()

    print('Collecting set of 250 training examples.')
    ### Gets the training set size of the data
    tSet = []
    numRan = random.sample(range(0, len(shroomTotData)), tSize)
    for i in numRan:
        tSet.append(shroomTotData[i])
    
    ### Removes the training set from the data
    removeData = []
    for i in numRan:
        removeData.append(shroomTotData[i - 1])
    for i in removeData:
        shroomTotData.remove(i)
    
    ### Save results
    result = []

    ### Iterate until it reaches the training size
    start = increment
    for i in range(start, tSize + increment, increment):
        print('Running with %i examples in training set\n' % i)
        root = iteration(tSet, i, attDict, attName, heuristic)
        attDict.clear()
        attDict = copy.deepcopy(tempDict)
        correct, tot = testing(shroomTotData, root)
        print("Given current tree, there are %i correct classifications out of %i possible (a success rate of %0.4f percent).\n" %(correct, tot, correct/tot))
        result.append((i, correct / tot))
        if(i != tSize):
            root = None

    ### Prints final tree 

    print('FINAL TREE\n')       
    print(root)
    print('\n')

    print('STATISTICS\n')
    for i in result:
        print("Training set size: %i Success: %0.4f percent."%(i[0], i[1] * 100))

    ### For printing into csv files
    # with open('size%i_increment%i_%s.csv'%(tSize, increment, heuristic), mode='w') as csv_file:
    #     fieldnames = ['size', 'Accuracy']
    #     writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    #     writer.writeheader()
    #     print('STATISTICS\n')
    #     for i in result:
    #         print("Training set size: %i Success: %0.4f percent."%(i[0], i[1] * 100))
    #         writer.writerow({'size': i[0], 'Accuracy': i[1]})

    

if __name__== "__main__" :
	main()

