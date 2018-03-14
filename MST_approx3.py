"""
Nearest Neighbor implementation for the Travelling Salesman Problem
Project Group 31
"""
import math
import sys
import heapq
import time

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
	cities = distances[1]
	v = len(cities)
	parent = [-1 for x in range(v)]
	key = [[x+1, -1, float('inf')] for x in range(v)]
	key[v-1] = [0, -1, 0]
	i = 0
	#sumMST = 0
	while key:
		#print(key)
		p = key.pop()
		#print(p)
		parent[p[0]] = p[1]
		#sumMST += p[2]
		m = 0
		while m < len(key):
			d = getDistance(cities[p[0]], cities[key[m][0]])
			if d < key[m][2]:
				key[m][1] = p[0]
				key[m][2] = d
			if m != 0:
				if key[m-1][2] <= key[m][2]:
					key[m-1], key[m] = key[m], key[m-1]
			m += 1
	#print("\nParent:")
	#print(parent)
	#print("MST NEW: " + str(sumMST))
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
	

#calculates cycle distance (add's distance from last city in list to first city)
def getTotDist(cycle, cities):
	sum = 0
	i = 1
	while i < len(cycle):
		#print("from: " + str(cycle[i-1]) + "  to: " + str(cycle[i]) + "  Dist: " + str(getDistance(cities[cycle[i-1]], cities[cycle[i]])))
		sum += getDistance(cities[cycle[i-1]], cities[cycle[i]])
		i += 1
	sum += getDistance(cities[cycle[i-1]], cities[cycle[0]])
	return sum


def opt_2(tour, cities):
	size = len(tour)
	i = 0
	best_dist = getTotDist(tour, cities)
	print("Length pre 2-opt: " + str(best_dist))						
	while i < 2:
		j = 0
		while j < size - 1:
			k = j+1
			while k < size:
				new_tour = []
				#swap_slice(j, k, tour, new_tour)
				swap(j, k, tour, new_tour)
				new_dist = getTotDist(new_tour, cities)
				if new_dist < best_dist:
					i = 0
					tour = new_tour
					best_dist = new_dist
					#print("Current Best: " + str(best_dist))
				k += 1
			j += 1
		i += 1
	return [best_dist, tour]



#def swap_slice(one, two, tour, new_tour):
#	size = len(tour)
#	print(tour)
#	if one != 0:
#		new_tour.extend(tour[:one])
#	count = 0
#	i = one
#	while i <= two:
#		new_tour.append(tour[two-count])
#		count += 1
#		i += 1
#	if two != size:
#		new_tour.extend(tour[(two+1):])


def swap(one, two, tour, new_tour):
	size = len(tour)
	i = 0
	while i < one:
		new_tour.append(tour[i])
		i += 1	
	count = 0
	i = one
	while i <= two:
		new_tour.append(tour[two-count])
		count += 1
		i += 1
	i = two + 1
	while i < size:
		new_tour.append(tour[i])
		i += 1


def solve(inputFile, outputfile):
	data = getCityData(inputFile)
	pList = primMST(data)
	mst = primAdj(pList)
	cycle = getCycle(mst)
	if len(cycle) < 300:
		new_tour = opt_2(cycle, data[1])
		outputTour(new_tour, outputfile)
		print("Tour Distance: " + str(new_tour[0]))
	else:
		dist = getTotDist(cycle, data[1])
		outputTour([dist, cycle], outputfile)
		print("Tour Distance: " + str(dist))


#function from nearest neighbor (written by Nathan Bennet)
def main():
    if len(sys.argv) < 3:
        print('Input must be in the form of "python3 nearest_neighbor_test.py [input file] [output file]"')
    else:
        inputFile = sys.argv[1]
        outputFile = sys.argv[2]
        start = time.time()
        solve(inputFile, outputFile)
        end = time.time()
        print("Run Time: " + str(end-start))


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

