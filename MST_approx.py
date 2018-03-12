"""
Nearest Neighbor implementation for the Travelling Salesman Problem
Project Group 31
"""
import math
import sys
import heapq

#function written by Nathan Bennet
def outputTour(tourData, fileName):
    size = tourData[0]
    tour = tourData[1]

    f = open(fileName, "w")     
    
    # Write tour distance to file
    f.write(str(size) + "\n")
    
    # Write tour path to file
    for cityId in tour:
        f.write(str(cityId) + "\n")

    f.close()
 
 
#function written by Nathan Bennet
def getCityData(fileName):
    cityData = [] # Contains both unvisited cities and distances
    unvisited = set() # City id's
    distances = [] # x and y locations for each city

    with open(fileName) as f:
        for line in f:
            city = []

            # Split each line into an array
            lineArr = line.split()
            lineArr = list(map(int, lineArr))
            
            # Build x and y data
            city.append(lineArr[1])
            city.append(lineArr[2])
            city = list(map(int, city))
            
            # Append to distances
            distances.append(city)
            
            # Add city id to unvisited set
            unvisited.add(lineArr[0])

    cityData.append(unvisited)
    cityData.append(distances)
    return cityData


#function written by Nathan Bennet
def getDistance(city1, city2):
	x = (city1[0] - city2[0])**2
	y = (city1[1] - city2[1])**2
	distance = round(math.sqrt(x + y))
	return distance


#gets minimum spanning tree using prim's algorithm
#returns a list of parents corresponding with the index as the child city
def primMST(distances):
	visited = distances[0]
	cities = distances[1]
	v = len(distances[1])
	key = [(float('inf'), x, -1) for x in range(v)]
	parent = [-1 for x in range(v)]
	key[0] = (0, 0, -1)
	heapq.heapify(key)
	while key:
		p = heapq.heappop(key)
		parent[p[1]] = p[2]
		newHeap = []
		while key:
			currN = heapq.heappop(key)
			d = getDistance(cities[p[1]], cities[currN[1]])
			if d < currN[0]:
				newN = (d, currN[1], p[1])
				heapq.heappush(newHeap, newN)
			else:
				heapq.heappush(newHeap, currN)
		key = newHeap
	return parent


#transforms parent list into an adjacency list
def primAdj(pairsList):
	v = len(pairsList)
	tree = [[x] for x in range(v)]
	i = 1
	while i < v:
		tree[pairsList[i]].append(i)
		i += 1
	return tree
	

#gets a cycle from the MST
def getCycle(mst):
	cycle = []
	stack = []
	stack.append(0)
	while stack:
		temp = stack.pop()
		cycle.append(temp)
		i = 1
		while i < len(mst[temp]):
			stack.append(mst[temp][i])
			i += 1
	#cycle.append(0)
	return cycle
	

#calculates cycle distance
def getTotDist(cycle, cities):
	sum = 0
	i = 1
	while i < len(cycle):
		#print("from: " + str(cycle[i-1]) + "  to: " + str(cycle[i]) + "  Dist: " + str(getDistance(cities[cycle[i-1]], cities[cycle[i]])))
		sum += getDistance(cities[cycle[i-1]], cities[cycle[i]])
		i += 1
	sum += getDistance(cities[cycle[i-1]], cities[cycle[0]])
	return sum


def solve(inputFile, outputfile):
	test = getCityData(inputFile)
	pList = primMST(test)
	mst = primAdj(pList)
	cycle = getCycle(mst)
	dist = getTotDist(cycle, test[1])
	outputTour([dist, cycle], outputfile)
	print("Cycle Distance: " + str(dist))


#function from nearest neighbor (written by Nathan Bennet)
def main():
    if len(sys.argv) < 3:
        print('Input must be in the form of "python3 nearest_neighbor_test.py [input file] [output file]"')
    else:
        inputFile = sys.argv[1]
        outputFile = sys.argv[2]
        solve(inputFile, outputFile)

main()

#######################################################
####### Unusued nearest neighbor functions ############
#######################################################


# def getSmallest(cityData, currentId):
#     nearestCityId = -1
#     shortestDistance = sys.maxsize
#     unvisited = cityData[0] # Set of city id's
#     distances = cityData[1] # List of city x and y values
#     
#     for cityId in unvisited:
#         travelDistance = getDistance(distances[currentId], distances[cityId])
# 
#         if travelDistance < shortestDistance and travelDistance > 0:
#             shortestDistance = travelDistance
#             nearestCityId = cityId
# 
#     return [nearestCityId, shortestDistance]
# 
# def removeCity(cityData, index):
#     unvisited = cityData[0] # Set of city id's
#     unvisited.remove(index)
#     return index
# 
# def nearestNeighbor(cityData, startingId):
#     path = []
#     unvisited = cityData[0] # Set of city id's
#     distances = cityData[1] # List of city x and y values
#     distance = 0
# 
#     # Remove starting city and add to path
#     path.append(removeCity(cityData, startingId))
#     
#     # Iterate through unvisited cities
#     while unvisited:
#         smallest = getSmallest(cityData, path[-1])
#         distance += smallest[1]
#         
#         # Append nearest city id to path, remove from unvisited city set
#         path.append(removeCity(cityData, smallest[0]))
#     
#     # Add distance from last city to first city, complete cycle
#     distance += getDistance(distances[path[0]], distances[path[-1]])
# 
#     return [distance, path]
# 
# def solve(inputFile, outputFile):
#     cityData = getCityData(inputFile)
#     unvisited = cityData[0] # Set of city id's
#     distances = cityData[1] # List of city x and y values
#     tourLength = len(distances)     
#     bestDistance = sys.maxsize
#     bestTour = None
#     
#     # Run Nearest Neighbor with each city as starting point for more optimal solution for smaller input files
#     if tourLength < 500:
#         for i in range(tourLength):
#             unvisitedCopy = set(unvisited) # Copy unvisited set since data is removed with each iteration
#             cityDataCopy = [unvisitedCopy, distances]
# 
#             path = nearestNeighbor(cityDataCopy, i)
#             if path[0] < bestDistance:
#                 bestDistance = path[0]
#                 bestTour = path
#                 print("Best distance so far is: {}".format(path[0]))
#     else:
#         bestTour = nearestNeighbor(cityData, 0)
#     
#     outputTour(bestTour, outputFile)
#     print("Distance: {}".format(bestTour[0]))
#     print("Cities visited: {}".format(len(bestTour[1])))

