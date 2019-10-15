from infoTheory import mostImportant

class node(object):
    def __init__(self, att, children, isLeaf, remainingDict, guess, attVal):
        self.att = att
        self.children = children
        self.isLeaf = isLeaf
        self.remainingDict = remainingDict
        self.guess = guess
        self.attVal = attVal

    def __str__(self, level=0):
        if(self.att == 'final'):
            ret = "\t"*level+repr("Attri:" + self.att)+" "+repr("Value: " + self.attVal)+" "+repr("Guess: " + self.guess)+"\n"
        else:
            ret = "\t"*level+repr("Attri:" + self.att)+" "+repr("Parent Value: " + self.attVal)+" "+repr("Guess: " + self.guess)+"\n"            
        for child in self.children:
            if(child.att != 'final'):
                ret2 = child.__str__(level+1)
                ret += ret2
            else:
                ret += child.__str__(level+1)
        return ret

    def __repr__(self):
        return '<tree node representation>'

def sameLabel(data):
    if(len(data) == 0):
        return False
    prev = data[0]['final']
    for i in range(len(data)):
        if(data[i]['final'] != prev):
            return False
    return True

def collectData(data, attName, val):
    attData = []
    for i in data:
        if (i[attName] == val):
            attData.append(i)
    return attData

def mostFeqLabel(data):
    p = 0
    e = 0
    for i in data:
        if i["final"] == 'p':
            p += 1
        else: 
            e += 1
    if(max(p, e) == p):
        return 'p'
    else: return 'e'

def DecisionTreeTrain(data, remainingF, parent_guess, attVal, heuristic):
    guess = mostFeqLabel(data)
    if((sameLabel(data)) or (len(remainingF) == 0)):
        return node('final', [], True, data, guess, attVal)
    elif(len(data) == 0):
        return node('final', [], True, data, parent_guess, attVal)
    else:
        f = mostImportant(heuristic, data, remainingF)
        tempAtt = remainingF[f]
        branchRoot = node(f, [], False, remainingF.pop(f), guess, attVal)
        for i in tempAtt:
            newData = collectData(data, f, i)
            sub = DecisionTreeTrain(newData, remainingF, guess, i, heuristic)
            branchRoot.children.append(sub)
        return branchRoot

            
            


    

