"""
TODO- method 1: Generate preference for Devices using euclidean distance only, and
generate preferences for Edges using Devices' task size only

TODO- method 2: Generate preferences for Devices based on computing power within X euclidean distance, and
generate preferences for Edges using Devices' task size only

TODO- method 3..: other possible preferences
"""
import operator

# TODO- method 1
def distance_only(Devices, Edges):
    edgesPref = {}
    devsPref = {}
    devices = list(Devices.values())
    edges = list(Edges.values())

    for eachEdge in edges:
        task_dic = {}
        for eachDev in devices:            
            task_dic[eachDev] = eachDev.task
        sorted_task = dict(sorted(task_dic.items(), key=operator.itemgetter(1)))
        tempEdgePref = list(sorted_task.keys())
            
        edgesPref[eachEdge] = tempEdgePref

        
        
    for eachDev in devices:
        distance_dic = {}
        device_x = eachDev.pos[0]
        device_y = eachDev.pos[1]
        for eachEdge in edges:            
            distance = (eachEdge.pos[0] - device_x) ** 2 + (eachEdge.pos[1] - device_y) ** 2
            distance_dic[eachEdge] = distance
        sorted_distance = dict(sorted(distance_dic.items(), key=operator.itemgetter(1)))
        tempDevPref = list(sorted_distance.keys())

        devsPref[eachDev] = tempDevPref



    return edgesPref, devsPref


# TODO- method 2
def distance_max(Devices, Edges, max_dis):
    edgesPref = {}
    devsPref = {}
    devices = list(Devices.values())
    edges = list(Edges.values())
    max_dis_sq = max_dis ** 2

    for eachEdge in edges:
        task_dic = {}
        for eachDev in devices:            
            task_dic[eachDev] = eachDev.task
        sorted_task = dict(sorted(task_dic.items(), key=operator.itemgetter(1)))
        tempEdgePref = list(sorted_task.keys())
        
            
        edgesPref[eachEdge] = tempEdgePref

        
        
    for eachDev in devices:
        distance_dic = {}
        device_x = eachDev.pos[0]
        device_y = eachDev.pos[1]
        for eachEdge in edges:            
            distance = (eachEdge.pos[0] - device_x) ** 2 + (eachEdge.pos[1] - device_y) ** 2
            if max_dis_sq >= distance:
                distance_dic[eachEdge] = distance
            
        sorted_distance = dict(sorted(distance_dic.items(), key=operator.itemgetter(1)))
        tempDevPref = list(sorted_distance.keys())

        devsPref[eachDev] = tempDevPref

    return edgesPref, devsPref
