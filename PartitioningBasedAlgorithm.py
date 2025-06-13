import random as rd
import pymetis
import itertools

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

def closestLocation(loc, availLocs):
    # Find closest location to a set of locations
    minDist =  float("inf")
    minLoc = [i for i in availLocs][0]
    for locCoord in availLocs:
        dist = ((float(locCoord[0] - loc[0]))**2 + ((float(locCoord[1] - loc[1])**2)))**0.5
        if dist < minDist:
            minLoc = locCoord
            minDist = dist
    return minLoc

def createParts(nodes, locs, nParts, nodeConnections, locations, scaling):
    # Uses pyMetis to divide the social network and locations into communities
    nodeSet = {i for i in nodes}
    adjncyList = []
    xadjList = []
    count = 0

    nodesToMetis = [i for i in nodes]
    nodes = [i for i in range(len(nodes))]

    for n in nodes:
        xadjList.append(count)
        [adjncyList.append(nodesToMetis.index(i)) for i in nodeConnections[nodesToMetis[n]] if i in nodeSet]
        count += len([i for i in nodeConnections[nodesToMetis[n]] if i in nodeSet])
    xadjList.append(len(adjncyList))

    n_cuts, membership = pymetis.part_graph(nParts, xadj=xadjList, adjncy=adjncyList)

    locToParts = [i for i in locs]
    locAdjncyList = []
    locXadjList = [i for i in range(0, (len(locs)-1)**2+len(locs), len(locs)-1)]
    for loc in locs:
        [locAdjncyList.append(locToParts.index(j)) for j in locs if j !=loc]

    # Weights of location network are determined by distance
    eWeights = []
    for loc in locs:
        dists = []
        loc = locations[loc]
        for nLoc in locs:
            nLoc = locations[nLoc]
            if loc != nLoc:
                dist = ((nLoc[0] - loc[0])**2 + ((nLoc[1] - loc[1])**2))**0.5
                dist = int((1/dist)*scaling)
                dists.append(dist)
        [eWeights.append(d) for d in dists]
    

    locCuts, locMembership = pymetis.part_graph(nParts, xadj=locXadjList, adjncy=locAdjncyList, eweights=eWeights)
    
    nodesInPart = []
    for i in range(nParts):
        nodesInPart.append([nodesToMetis[idx] for idx,n in enumerate(membership) if n==i])

    locNodesInPart = []
    for i in range(nParts):
        locNodesInPart.append([locToParts[idx] for idx,n in enumerate(locMembership) if n==i])
    
    return nodesInPart, locNodesInPart

def matchParts(nodesInPart, locNodesInPart, nParts, nodeConnections, locations, distances, scaling, leftoverLocs, leftoverNodes, nodesToLoc):
    # Matches social network parts to location parts that minimizes distances between connected nodes
    partCounts = {}
    for nodes in nodesInPart:
        if len(nodes) not in partCounts:
            partCounts[len(nodes)] = 1
        else:
            partCounts[len(nodes)] = partCounts[len(nodes)]+1

    locPartCounts = {}
    for nodes in locNodesInPart:
        if len(nodes) not in locPartCounts:
            locPartCounts[len(nodes)] = 1
        else:
            locPartCounts[len(nodes)] = locPartCounts[len(nodes)]+1

    availNodeParts = [i for i in range(nParts)]
    availLocParts = [i for i in range(nParts)]

    connectionsBetweenParts = {}
    for i in range(nParts):
        for j in range(nParts):
            count = 0
            if j!=i:
                for node in nodesInPart[i]:
                    for neighbor in nodeConnections[node]:
                        if neighbor in nodesInPart[j]:
                            count+=1
                connectionsBetweenParts[(i, j)] = count
    
    partCoords = {}
    for i, locs in enumerate(locNodesInPart):
        xAvg = sum([locations[loc][0] for loc in locs])/len(locs)
        yAvg = sum([locations[loc][1] for loc in locs])/len(locs)
        partCoords[i] = (xAvg, yAvg)

    posMatches = set()
    for i in range(len(availNodeParts)):
        for j in range(len(availLocParts)):
            if len(nodesInPart[availNodeParts[i]]) == len(locNodesInPart[availLocParts[i]]):
                posMatches.add((availLocParts[i], availNodeParts[j]))

    posCombinations = []
    permut = itertools.permutations(availNodeParts, len(availLocParts))

    for comb in permut:
        zipped = zip(comb, availLocParts)
        posCombinations.append(list(zipped))

    minTotalDistance = float("inf")
    minCombination = []
    for posMatch in posCombinations:
        graphDist = 0
        for nodeMatch in posMatch:
            if nodeMatch not in posMatches:
                break
        for i in posMatch:
            for j in posMatch:
                if i != j:
                    dist = ((partCoords[i[1]][0] - partCoords[j[1]][0])**2 + ((partCoords[i[1]][1] - partCoords[j[1]][1])**2))**0.5
                    dist= dist*connectionsBetweenParts[(i[0], j[0])]
                    graphDist += dist
        if graphDist <minTotalDistance:
            minTotalDistance = graphDist
            minCombination = posMatch
    
    
    for i in minCombination:
        newNParts = len(nodesInPart[i[0]])//15
        locParts = len(locNodesInPart[i[1]])//15
        if newNParts > 10:
            newNParts = 10
        if newNParts > 1 and locParts > 1:
            nLocations = locNodesInPart[i[1]]
            nNodesInPart, nLocNodesinPart  = createParts(nodesInPart[i[0]], nLocations, newNParts, nodeConnections, locations, scaling)
            leftoverLocs, leftoverNodes, nodesToLoc = matchParts(nNodesInPart, nLocNodesinPart, newNParts, nodeConnections, locations, distances, scaling, leftoverLocs, leftoverNodes)
        else:
            for idx, node in enumerate(nodesInPart[i[0]]):
                nodesToMatch = set()
                locsToMatch = set()
                if idx < len(locNodesInPart[i[1]]):
                    nodesToMatch.add(node)
                    locsToMatch.add(locations[locNodesInPart[i[1]][idx]])
                else:
                    leftoverNodes.append(node)
                nodesToLoc = matchNodesinPart(nodesToMatch, locsToMatch, nodeConnections, nodesToLoc, distances)
            if len(nodesInPart[i[0]]) < len(locNodesInPart[i[1]]):
                [leftoverLocs.append(n) for n in locNodesInPart[i[1]][len(nodesInPart[i[0]]):]]
    return leftoverLocs, leftoverNodes, nodesToLoc

def matchNodesinPart(nodes, locs, nodeConnections, nodesToLoc, distances):
    # Matches nodes to locations in a matched part. The node with the highest degree is assigned
    # to the medoid, and its neighbors are assigned to the locations close to it.
    while nodes:
        currentNode = 0
        maxLen = 0
        for node in nodes:
            if len(nodeConnections[node]) > maxLen:
                maxLen = len(nodeConnections[node])
                currentNode = node
        currentLoc = findMedoid(locs, distances)
        nodesToLoc[currentNode] = currentLoc
        nodes.remove(currentNode)
        locs.remove(currentLoc)
        for n in nodeConnections:
            if n in nodes:
                closeLoc = closestLocation(currentLoc, locs)
                nodesToLoc[n] = closeLoc
                nodes.remove(n)
                locs.remove(closeLoc)
    return nodesToLoc

def metisLeftover(leftoverLocs, leftoverNodes, nodeConnections, locations, nodesToLoc):
    # Matches nodes to locations that are left over when the size of location parts and social
    # network parts are not the same
    while leftoverNodes:
        currentNode = 0
        maxLen = 0
        for node in leftoverNodes:
            if len(nodeConnections[node]) > maxLen:
                maxLen = len(nodeConnections[node])
                currentNode = node
        avgNeighborCoordX = 0
        avgNeighborCoordY = 0
        nCount = 0
        for neighbor in nodeConnections[node]:
            if neighbor in nodesToLoc:
                nCount += 1
                avgNeighborCoordX += nodesToLoc[neighbor][0]
                avgNeighborCoordY += nodesToLoc[neighbor][1]
        if nCount == 0:
            currentNode = leftoverLocs[0]
            leftoverLocs = locations[leftoverLocs[1:]]
        else:
            avgNeighborCoordX = avgNeighborCoordX/nCount
            avgNeighborCoordY = avgNeighborCoordY/nCount
            minDist =  float("inf")
            minLoc = leftoverLocs[0]
            for loc in leftoverLocs:
                locCoord = locations[loc]
                dist = ((float(locCoord[0] - avgNeighborCoordX))**2 + ((float(locCoord[1] - avgNeighborCoordY)**2)))**0.5
                if dist < minDist:
                    minLoc = loc
                    minDist = dist
            nodesToLoc[currentNode] = locations[minLoc]
            leftoverLocs.remove(minLoc)
        leftoverNodes.remove(currentNode)
    return [locations[i] for i in leftoverLocs], nodesToLoc

def matchDisconnected(availableNodes, availableLocations, nodesToLoc):
    # Match nodes that have a degree of zero
    rd.shuffle(availableNodes)
    rd.shuffle(availableLocations)
    for i, n in enumerate(availableNodes):
        nodesToLoc[n] = availableLocations[i]
    return nodesToLoc

def partitioning(matrix, locations, knownLocations):
    # Input:
    #   matrix: adjacency matrix with all nodes in the network
    #   locations: list of the coordinates of the possible locations
    #   knownLocations: dictionary which maps nodes to known locations
    # Output:
    #   Dictionary which maps nodes to the given locations

    pop = len(locations)

    nodeConnections = {}
    disconnected = []
    for n, row in enumerate(matrix):
        nodeConnections[n] = {i for i, j in enumerate(row) if j}
        if not nodeConnections[n]:
            disconnected.append(n)

    distances = {}
    scaling = 0
    for loc in locations:
        if ((float(loc[0]))**2 + (float(loc[1]))**2)**0.5 > scaling:
                scaling = ((float(loc[0]))**2 + (float(loc[1]))**2)**0.5

    parts = pop//10
    if parts > 10:
        parts = 10

    nodes = [i for i in nodeConnections if i not in knownLocations and i not in disconnected]
    locs = [i for i, loc in enumerate(locations) if loc not in knownLocations.values()]
    rd.shuffle(nodes)
    rd.shuffle(locs)

    nodesInPart, locNodesInPart = createParts(nodes, locs, parts, nodeConnections, locations, scaling)
    
    leftoverLocs = []
    leftoverNodes = []
    nodesToLoc = {}
    for i in knownLocations:
        nodesToLoc[i] = knownLocations[i]

    leftoverLocs, leftoverNodes, nodesToLoc = matchParts(nodesInPart, locNodesInPart, parts, nodeConnections, locations, distances, scaling, leftoverLocs, leftoverNodes, nodesToLoc)
    leftoverLocs, nodesToLoc = metisLeftover(leftoverLocs, leftoverNodes, nodeConnections, locations, nodesToLoc)
    nodesToLoc = matchDisconnected([i for i in disconnected if i not in nodesToLoc], leftoverLocs, nodesToLoc)
    
    return nodesToLoc