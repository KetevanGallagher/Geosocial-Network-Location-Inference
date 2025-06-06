import random as rd

def findMedoid(availableLocations, distances):
    # Find the medoid given locations
    minDistances = {}
    for loc in availableLocations:
        distanceSum = 0
        for toLoc in availableLocations:
            if loc != toLoc:
                dist = distances[(loc, toLoc)]
                distanceSum+= dist
        minDistances[loc] = distanceSum
    denseLoc = min(minDistances, key=lambda k: minDistances[k])
    return denseLoc

def closestLocation(loc, availLocs, maxDist):
    # Find closest location to a set of locations
    minDist =  maxDist*2
    minLoc = [i for i in availLocs][0]
    for locCoord in availLocs:
        dist = ((float(locCoord[0] - loc[0]))**2 + ((float(locCoord[1] - loc[1])**2)))**0.5
        if dist < minDist:
            minLoc = locCoord
            minDist = dist
    return minLoc

def matchDisconnected(availableNodes, availableLocations, nodesToLoc):
    # Match nodes that have a degree of zero
    rd.shuffle(availableNodes)
    rd.shuffle(availableLocations)
    for i, n in enumerate(availableNodes):
        nodesToLoc[n] = availableLocations[i]
    return nodesToLoc

def findStartingNode(nodeConnections, matchedNodes, availableNodes):
    # Find the node with the most connections to matched nodes
    # and is connected to available nodes
    maxLen = 0
    maxID = -1
    maxDeg = 0
    for n in availableNodes:
        deg = len([i for i in nodeConnections[n] if i in availableNodes])
        if maxLen < len([i for i in nodeConnections[n] if i in matchedNodes]):
            maxLen = len([i for i in nodeConnections[n] if i in matchedNodes])
            maxID = n
            maxDeg = deg
        elif maxLen == len([i for i in nodeConnections[n] if i in matchedNodes]):
            if deg > maxDeg:
                maxID = n
                maxDeg = deg
    return maxID
    
def findNeighborCentroid(neighbors):
    # Find the centroid between locations
    neighborX = sum([l[0] for l in neighbors])/len(neighbors)
    neighborY = sum([l[1] for l in neighbors])/len(neighbors)
    return (neighborX, neighborY)

def greedyMatchNodesToLoc(denseLoc, availableNodes, availableLocations, startingSet, known, nodeConnections, distances, nodesToLoc):
    closestLocations = [denseLoc]
    nodeSetsToProcess = [startingSet]

    while nodeSetsToProcess:
        nodeNeighbors = nodeSetsToProcess.pop()
        denseLoc = closestLocations.pop()

        # Sort the neighbors of the starting node by highest degree and remove them from available nodes
        sortedNodeNeighbors = []
        toRemove = []
        for n in nodeNeighbors:
            if n in availableNodes:
                availableNodes.remove(n)
            else:
                toRemove.append(n)
        [nodeNeighbors.remove(n) for n in toRemove]
        if not nodeNeighbors:
            continue
        
        for n in nodeNeighbors:
            if known:    
                sortedNodeNeighbors.append((n, len([i for i in nodeConnections[n] if i in nodesToLoc])))
            else:
                sortedNodeNeighbors.append((n, len([i for i in nodeConnections[n] if i in availableNodes])))
        sortedNodeNeighbors.sort(key=lambda x: x[1], reverse=True)

        
        # Find the locations closest to the current dense location
        locationSet = []
        for loc in availableLocations:
            dist = distances[(denseLoc, loc)]
            if not locationSet:
                locationSet.append((dist, loc))
            else:
                index = len(nodeConnections) + 1

                for i, d in enumerate(locationSet):
                    if d[0] >dist:
                        index = i
                        break
                if index <= len(locationSet):
                    locationSet.insert(index, (dist, loc))
                    if len(locationSet) > len(nodeNeighbors):
                        locationSet.pop()
                else:
                    if len(locationSet) < len(nodeNeighbors):
                        locationSet.append((dist, loc))

        # Match nodes with higher degrees to closer locations
        for i in range(len(sortedNodeNeighbors)):
            node = sortedNodeNeighbors[i][0]
            location = locationSet[i][1]
            nodesToLoc[node] = location
            availableLocations.remove(location)

        # If any of the recently matched nodes have neighbors, process those
        for n in sortedNodeNeighbors[::-1]:
            node = n[0]
            newNodeSet = {i for i in nodeConnections[node] if i in availableNodes}
            if newNodeSet:
                nodeSetsToProcess.append(newNodeSet)
                closestLocations.append(nodesToLoc[node])

    return availableNodes, availableLocations, nodesToLoc

def greedy(matrix, locations, knownLocations):
    # Input:
    #   matrix: adjacency matrix with all nodes in the network
    #   locations: list of the coordinates of the possible locations
    #   knownLocations: dictionary which maps nodes to known locations
    # Output:
    #   Dictionary which maps nodes to the given locations

    nodeConnections = {}
    for n, row in enumerate(matrix):
        nodeConnections[n] = {i for i, j in enumerate(row) if j}

    distances = {}
    maxDist = 0
    for loc in locations:
        for nLoc in locations:
            if loc != nLoc:
                dist = ((nLoc[0] - loc[0])**2 + ((nLoc[1] - loc[1])**2))**0.5
                distances[(loc, nLoc)] = dist
                if dist > maxDist:
                    maxDist = dist
    
    nodesToLoc = {}
    for i in knownLocations:
        nodesToLoc[i] = knownLocations[i]

    availableNodes = {i for i in nodeConnections if i not in knownLocations}
    availableLocations = {loc for loc in locations if loc not in knownLocations.values()}

    # Find starting node:
    #   if there are known locations, the starting node is the node that has the 
    #   greatest connections to nodes with known locations and has available nodes.
    #   Otherwise, it is the node with the highest degree.
    maxID = 0

    if knownLocations:
        maxID = findStartingNode(nodeConnections, knownLocations, availableNodes)
    else:
        maxLen = 0
        maxID = 0
        for n in nodeConnections:
            if maxLen < len(nodeConnections[n]):
                maxLen = len(nodeConnections[n])
                maxID = n

    # Find starting location
    #   If there are known locations, the starting location is the location closest to the
    #   centroid of the locations the starting node is connected to.
    #   Otherwise, the starting location is the medoid.
    if knownLocations:
        knownNeighbors = [knownLocations[i] for i in nodeConnections[maxID] if i in knownLocations]
        neighborCentroid = findNeighborCentroid(knownNeighbors)
        denseLoc = closestLocation(neighborCentroid, [loc for i, loc in enumerate(locations) if i not in knownLocations], maxDist)
    else:
        denseLoc = findMedoid([loc for i, loc in enumerate(locations) if i not in knownLocations])

    nodesToLoc[maxID] = denseLoc
    startingSet = {i for i in nodeConnections[maxID] if i not in knownLocations}
    availableLocations.remove(denseLoc)
    availableNodes.remove(maxID)

    
    known = False
    if knownLocations:
        known = True

    availableNodes, availableLocations, nodesToLoc = greedyMatchNodesToLoc(denseLoc, availableNodes, availableLocations, startingSet, known, nodeConnections, distances, nodesToLoc)
    
    # Repeat matching process until all nodes are matched
    while availableNodes:
        maxID = findStartingNode(nodeConnections, nodesToLoc, availableNodes)
        if maxID == -1:
            maxLen = 0
            for n in availableNodes:
                if maxLen < len([i for i in nodeConnections[n] if i in availableNodes]):
                    maxLen = len([i for i in nodeConnections[n] if i in availableNodes])
                    maxID = n
        if maxID == -1:
            matchDisconnected([i for i in availableNodes], [i for i in availableLocations], nodesToLoc)
            availableLocations, availableNodes = set(), set()
        else:
            startingSet = {i for i in nodeConnections[maxID] if i not in nodesToLoc}
            assignedNeighbors = [nodesToLoc[i] for i in nodeConnections[maxID] if i in nodesToLoc]
            denseLoc = closestLocation(findNeighborCentroid(assignedNeighbors), availableLocations, maxDist)
            nodesToLoc[maxID] = denseLoc
            availableNodes.remove(maxID)
            availableLocations.remove(denseLoc)
            availableNodes, availableLocations, nodesToLoc = greedyMatchNodesToLoc(denseLoc, availableNodes, availableLocations, startingSet, known, nodeConnections, distances, nodesToLoc)
        
    return nodesToLoc