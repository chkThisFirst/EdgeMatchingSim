#import Node
#import Link
import math
import random

# run this first: 
#!pip install networkx
import networkx as nx
import matplotlib.pyplot as plt


class Simulator:
    def __init__(self, posUpper, numEdge, numDev, taskRange, compRange, BWRange, fileRange):
        """
        :param posUpper: a positive integer
        :param numEdge: a positive integer
        :param numDev: a positive integer
        :param taskRange: (lower_bound, upper_bound) two positive integers
        :param compRange: (lower_bound, upper_bound) two positive integers
        :param BWRange: (lower_bound, upper_bound) two positive integers
        """
        xList = random.sample(range(posUpper * -1, posUpper), numEdge + numDev)
        yList = random.sample(range(posUpper * -1, posUpper), numEdge + numDev)
        self.edgeIDs = []
        self.deviceIDs = []

        # By default, there is only one cloud with infinite computing power
        self.Cloud = Node('Cloud', 'c0', (0, 0), 0, float("inf"), 0)

        # generate a list of Edge nodes
        self.Edges = {}
        for i in range(numEdge):
            tempID = 'e' + str(i)
            self.edgeIDs.append(tempID)
            tempPos = (xList[i], yList[i])
            # tempTask = random.randint(taskRange[0], taskRange[1])
            tempComp = random.randint(compRange[0], compRange[1])
            tempEdge = Node('Edge', tempID, tempPos, 0, tempComp, 0)
            self.Edges[tempEdge.getID()] = tempEdge

        # generate a list of Device nodes
        self.Devices = {}
        for j in range(numDev):
            tempID = 'd' + str(j)
            self.deviceIDs.append(tempID)
            tempPos = (xList[numEdge + j], yList[numEdge + j])
            tempTask = random.randint(taskRange[0], taskRange[1])
            tempFile = random.randint(fileRange[0], fileRange[1])
            # tempComp = random.randint(compRange[0], compRange[1])
            tempDev = Node('Device', tempID, tempPos, tempTask, 0, tempFile)
            self.Devices[tempDev.getID()] = tempDev

        # initialize links between Cloud and Edges
        self.Links = {}
        for h in range(numEdge):
            tempEdgeID = self.edgeIDs[h]
            tempBW = float('inf')
            tempLink = Link(tempEdgeID, 'c0', tempBW)
            self.Links[tempLink.getStartID()] = tempLink

        # initialize links from Devices with empty Edge
        for k in range(numDev):
            tempDevID = self.deviceIDs[k]
            tempBW = random.randint(BWRange[0], BWRange[1])
            tempLink = Link(tempDevID, 'none', tempBW)
            self.Links[tempLink.getStartID()] = tempLink


    # TODO-compute fairness
    def compute_fairness(self):
        e2eLatencyList = []

        # latency = task/comp + file*2/link.speed + distance
        for eachDev in self.Devices:
            tempDevice = self.Devices[eachDev]
            tempTask = tempDevice.task
            tempFile = tempDevice.file
            tempLink = self.Links[tempDevice.ID]

            if tempLink.endID != 'c0':
                tempServ = self.Edges[tempLink.endID]
            else:
                tempServ = self.Cloud

            tempSpeed = tempLink.speed
            tempComp = self.Edges[tempLink.endID].comp
            tempDistance = math.sqrt((tempDevice.pos[0] - tempServ.pos[0])**2 +
                                     (tempDevice.pos[0] - tempServ.pos[0])**2)

            tempLatency = tempTask/tempComp + tempFile*2/tempSpeed + tempDistance

            e2eLatencyList.append(tempLatency)

        totalLatency = sum(e2eLatencyList)
        #print('totalLatency: ', totalLatency)
        #print('e2eLatencyList: ', e2eLatencyList)

        # compute final fairness
        upper = 0
        for i in e2eLatencyList:
            upper += i/totalLatency
        upper = upper ** 2

        lower = 0
        for j in e2eLatencyList:
            lower += (j/totalLatency) ** 2
        lower = lower * len(e2eLatencyList)

        latencyFairness = upper/lower
        return latencyFairness


    # assign Edges and Devices' preferences
    def assign_preference(self, edgesPref, devsPref):
        """
        :param edgesPref: a dict of preferences for Edges. i.e {'e1':['d1','d2','d3'],'e2':['d2','d3','d1']}
        :param devsPref: a dict of preferences for Devices. i.e {'d1':['e1','e2','e3'],'d2':['e2','e3','e1']}
        :return:
        """
        for e_key, eachEdge in self.Edges.items():
            eachEdge.set_preference(edgesPref[e_key])

        for d_key, eachDevice in self.Devices.items():
            eachDevice.set_preference(devsPref[d_key])

    # execute matching
    def assign_links(self, matchingGraph):
        """
        :param matchingGraph: a list of tuples. i.e [('d1','e2'),('d2','e1')] must be (device,edge)
        :return:
        """
        for eachGraph in matchingGraph:
            self.Links[eachGraph[0]].setEndID(eachGraph[1])

    # print network
    def print_network(self):
        self.Cloud.print_self()
        for i, eachEdge in self.Edges.items():
            eachEdge.print_self()
        for j, eachDev in self.Devices.items():
            eachDev.print_self()
        for k, eachLink in self.Links.items():
            eachLink.print_self()

    # print preference
    def print_preference(self):
        for i, eachEdge in self.Edges.items():
            print(eachEdge.ID, " 's preference:")
            eachEdge.print_preference()
        for j, eachDev in self.Devices.items():
            print(eachDev.ID, " 's preference:")
            eachDev.print_preference()


    # generate a figure for the network with all links issued
    def generate_fig(self):
        G = nx.Graph()
        
        # add nodes, colors, positions, and labels
        positions = {self.Cloud.ID: self.Cloud.pos}
        node_labels = {self.Cloud.ID: self.Cloud.nType + "\n" + str(self.Cloud.ID)}
        node_colors = ['red']
        G.add_node(self.Cloud.ID)
        
        for i, eachEdge in self.Edges.items():
            positions[eachEdge.ID] = eachEdge.pos
            node_labels[eachEdge.ID] = "ID: " + str(eachEdge.ID) + "\ncomp: " + str(eachEdge.comp)
            G.add_node(eachEdge.ID)
            node_colors.append('#FF8F00')
            
        for j, eachDev in self.Devices.items():
            positions[eachDev.ID] = eachDev.pos
            node_labels[eachDev.ID] = "ID: " + str(eachDev.ID) + "\ntask: " + str(eachDev.task)
            G.add_node(eachDev.ID)
            node_colors.append('#00d700')
        
        # add edges and edges styles
        edge_styles = []
        edges = []
        for k, eachLink in self.Links.items():
            tempLink = (eachLink.getStartID(), eachLink.getEndID())
            edges.append(tempLink)
            
            # set edge style
            # if cloud -> edge: solid
            # if edge -> device: dashed
            if (eachLink.getEndID() == self.Cloud.ID):
                edge_styles.append('solid')
            else:
                edge_styles.append('dotted')
            
        G.add_edges_from(edges)
        
        # create a plot to view the network
        plt.figure(figsize=(12,12))
        nx.draw_networkx(G, positions, labels=node_labels,
                         with_labels=True, node_size=800, alpha=0.85,
                         node_color=node_colors, style=edge_styles,
                         font_size=12, font_weight=600, width=1.5,
                         verticalalignment='bottom')
                
        plt.title("Network Graph",
                  {'color':'black', 'fontsize':16})
        plt.show()
            
class Node:
    def __init__(self, nType, ID, pos, task, comp, file):
        avaiableNodes = ['Cloud','Edge','Device']
        if nType in avaiableNodes:
            self.nType = nType
            self.ID = ID
            self.pos = pos
            self.task = task
            self.comp = comp
            self.file = file
            self.preference = []
        else:
            raise ValueError("Invalid nType input!")

    def set_preference(self, preference):
        self.preference = preference

    def print_preference(self):
        print(self.preference)

    def getID(self):
        return self.ID

    def print_self(self):
        print('nType:',self.nType,' ID:', self.ID,' pos:', str(self.pos),' task:', str(self.task),
              ' comp:', str(self.comp), ' file:', str(self.file))

class Link:
    def __init__(self, startID, endID, speed):
        """
        :param startID: Always follow device->edge->cloud. That means startID must be from higher level tier. i.e startID can never be from cloud
        :param endID: Always follow device->edge->cloud. That means endID must be from higher level tier. i.e endID can never be from device
        :param speed:
        """
        self.startID = startID
        self.endID = endID
        self.speed = speed

    def getStartID(self):
        return self.startID

    def setEndID(self, newEndID):
        self.endID = newEndID

    def getEndID(self):
        return self.endID
    
    def print_self(self):
        print('startID:',self.startID,' endID:', self.endID,' speed:', str(self.speed))
