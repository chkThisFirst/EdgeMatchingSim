from Sim import Simulator
import random
from generatePreference import distance_only
from generatePreference import distance_max

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
    print(edgesPref_1)
    print(devsPref_1)
    edgesPref_1, devsPref_1 = distance_max(mySim.Devices, mySim.Edges, 20)
    print(edgesPref_1)
    print(devsPref_1)




if __name__ == "__main__":
    main()
