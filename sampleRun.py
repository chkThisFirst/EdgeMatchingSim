from Sim import Simulator
import random
from generatePreference import distance_only
from generatePreference import distance_max
from generatePreference import limited_distance
from generateMatching import mpda
from generateMatching import mpda_random
from generateMatchingV2 import matchingMPDA

def random_preference(deviceIDs, edgeIDs):
    edgesPref = {}
    tempEdgePref = deviceIDs.copy()
    for eachEdge in edgeIDs:
        random.shuffle(tempEdgePref)
        edgesPref[eachEdge] = tempEdgePref

    devsPref = {}
    tempDevPref = edgeIDs.copy()
    for eachDev in deviceIDs:
        random.shuffle(tempDevPref)
        devsPref[eachDev] = tempDevPref

    return edgesPref, devsPref


def random_matching(sim):
    deviceList = sim.deviceIDs.copy()
    edgeList = sim.edgeIDs.copy()
    matchingGraph = []

    for d, e in zip(deviceList,edgeList):
        matchingGraph.append((d,e))

    return matchingGraph


def main():
    mySim = Simulator(20, 5, 5, (50, 200), (5, 10), (10, 50))
##    # generate random preference for all edges and devices
##    edgesPref, devsPref = random_preference(mySim.deviceIDs, mySim.edgeIDs)
##    mySim.assign_preference(edgesPref, devsPref)
##    # generate random matching between edges and devices. For simple demo, this DID NOT use preference
##    matchingGraph = random_matching(mySim)
##    mySim.assign_links(matchingGraph)
##
##    mySim.print_network()

    # generate method #1 for all edges and devices
#    print(type(mySim.Devices))
    edgesPref_1, devsPref_1 = distance_only(mySim.Devices, mySim.Edges)
##    print(edgesPref_1)
##    print(devsPref_1)
    edgesPref_2, devsPref_2 = distance_max(mySim.Devices, mySim.Edges, 20)
##    print(edgesPref_1)
##    print(devsPref_1)
    mySim.assign_preference(edgesPref_1, devsPref_1)
##    print(mySim.Edges)
    matchingGraph_1 = mpda(edgesPref_1, devsPref_1)
##    print(matchingGraph_1)
    mySim.assign_links(matchingGraph_1)
    mySim.print_network()
    mySim.generate_fig()
    
    matchingGraph_2 = mpda_random(edgesPref_1, devsPref_1)
##    print(matchingGraph_2)
    mySim.assign_links(matchingGraph_2)
    mySim.print_network()
    mySim.generate_fig()
##    mySim.assign_preference(edgesPref_2, devsPref_2)
##    

def testMatching():
    mySim = Simulator(20, 6, 6, (50, 200), (5, 10), (10, 50))
    edgesPref_1, devsPref_1 = distance_only(mySim.Devices, mySim.Edges)
    mySim.assign_preference(edgesPref_1, devsPref_1)
    matchingGraph_1 = mpda(edgesPref_1, devsPref_1)
    mySim.assign_links(matchingGraph_1)
    mySim.print_network()
    mySim.generate_fig()

    matchingGraph_2 = mpda_random(edgesPref_1, devsPref_1)
    mySim.assign_links(matchingGraph_2)
    mySim.print_network()
    mySim.generate_fig()


def testPrefV2MatchingV2():
    betterCount = 0
    worseCount = 0
    for i in range(100):
        mySim = Simulator(20, 5, 5, (50, 200), (5, 10), (10, 50), (200, 500))
        edgesPref_1, devsPref_1 = distance_only(mySim.Devices, mySim.Edges)
        #edgesPref_1, devsPref_1 = limited_distance(mySim.Devices, mySim.Edges, 20)
        mySim.assign_preference(edgesPref_1, devsPref_1)
        mySim.print_preference()
        matchingGraph_0 = mpda(edgesPref_1, devsPref_1)
        mySim.assign_links(matchingGraph_0)
        #print('graph 0:', mySim.compute_fairness())
        fair0 = mySim.compute_fairness()
        matchingGraph_1 = matchingMPDA(edgesPref_1, devsPref_1,False)
        mySim.assign_links(matchingGraph_1)
        fair1 = mySim.compute_fairness()
        if fair1 > fair0:
            betterCount += 1
        else:
            worseCount += 1
        #print('graph 1:', mySim.compute_fairness())
        # mySim.print_network()
        # mySim.print_preference()
        # mySim.generate_fig()
    print ('betterCount:',betterCount,'worseCount:',worseCount)



def testFairness():
    fairnessList = []
    for i in range(5):
        print('Simulation #', i)
        mySim = Simulator(20, 5, 5, (50, 200), (5, 10), (10, 50), (200, 500))
        edgesPref_1, devsPref_1 = distance_only(mySim.Devices, mySim.Edges)
        mySim.assign_preference(edgesPref_1, devsPref_1)
        matchingGraph_1 = mpda(edgesPref_1, devsPref_1)
        mySim.assign_links(matchingGraph_1)
        mySim.print_preference()
        mySim.generate_fig()
        fairnessList.append(mySim.compute_fairness())
        print('Simulation #', i, " ends")

    print("fairnessList: ", fairnessList)
    print("avg fairness: ", sum(fairnessList)/len(fairnessList))


if __name__ == "__main__":
    #main()
    #testMatching()
    #testFairness()
    testPrefV2MatchingV2()
