import copy
import random

def matchingMPDA(edgesPref, devsPref, isRandom=False):
    deviceDict = devsPref.copy()
    edgeDict = edgesPref.copy()
    matchedDevs = {}
    matchedEdges = {}

    matchingGraph = []

    unmatchedDev = list(devsPref)


    while unmatchedDev:
        #print("unmatched:", unmatchedDev)
        if isRandom:
            random.shuffle(unmatchedDev)
        tempDevID = unmatchedDev.pop(0)
        tempDevPref = deviceDict[tempDevID]
        preferredServID = tempDevPref[0]

        # case1: decided to use cloud
        if preferredServID == 'c0':
            matchingGraph.append((tempDevID,'c0'))

        # case2: both are unmatched
        elif preferredServID not in matchedEdges:
            matchedDevs[tempDevID] = preferredServID
            matchedEdges[preferredServID] = tempDevID
            # update preference list
            tempDevPref.pop(0)

        # case3: Edge is matched
        else:
            tempEdgePref = edgeDict[preferredServID]
            oldDevID = matchedEdges[preferredServID]

            # case3.1: new device is more preferred
            if tempEdgePref.index(tempDevID) < tempEdgePref.index(oldDevID):
                # update new matching
                matchedDevs[tempDevID] = preferredServID
                matchedEdges[preferredServID] = tempDevID
                # remove old device from matchedDevs
                matchedDevs.pop(oldDevID, None)
                # send old device to unmatched list
                unmatchedDev.append(oldDevID)

            # case3.2: edge rejects this device's matching request
            else:
                # send this device back to the first position in unmacthedDev
                unmatchedDev.insert(0, tempDevID)

            # update preference list
            tempDevPref.pop(0)

        tempMatchingGraph = matchingGraph + list(matchedDevs.items())
        #print("matching graph:", tempMatchingGraph)
    #print("-----------------------Done---------------------")

    # update matching graph
    matchingGraph = matchingGraph + list(matchedDevs.items())
    return matchingGraph

def matchingOptimal(mySim):
    edgeList = list(mySim.Edges.keys())
    devList = list(mySim.Devices.keys())

    # [matchingGraph, fairness, totalLatency]
    fairMatching = [[], 0, -1]
    lowLatencyMatching = [[], -1, float('inf')]

    allMatchingGraphs = generateAllMatching(devList, edgeList, [[]])
    print("Num of allMatchingGraphs:", len(allMatchingGraphs))

    for eachGraph in allMatchingGraphs:
        #print("eachGraph:",eachGraph)
        mySim.assign_links(eachGraph)
        tempFairIndex, tempTotalLatency = mySim.compute_fairness()
        #print("tempFairIndex:", tempFairIndex)

        if tempFairIndex > fairMatching[1]:
            fairMatching = [eachGraph, tempFairIndex , tempTotalLatency]
        if tempTotalLatency < lowLatencyMatching[2]:
            lowLatencyMatching = [eachGraph, tempFairIndex , tempTotalLatency]

    return fairMatching, lowLatencyMatching








def generateAllMatching(listA, listB, tempSol):
    options = len(listA)
    finalSol = []
    updatedSol = []
    for j in range(options):
        tempSolCopy = copy.deepcopy(tempSol)
        updatedSol += tempSolCopy

    if options == 1:
        newPair = (listA[0], listB[0])
        updatedSol[0].append(newPair)
        return updatedSol

    for i in range(options):
        newPair = (listA[0], listB[i])
        updatedSol[i].append(newPair)
        newListA = listA.copy()
        newListB = listB.copy()
        del newListA[0]
        del newListB[i]

        newTempSol = [updatedSol[i].copy()]

        tempResult = generateAllMatching(newListA, newListB, newTempSol)
        finalSol += tempResult

    return finalSol