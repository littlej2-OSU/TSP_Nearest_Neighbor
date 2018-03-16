"""
Nearest Neighbor implementation for the Travelling Salesman Problem
Project Group 31
"""
import sys
import time
import math

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

def getDistance(city1, city2):
    x = (city1[0] - city2[0])**2
    y = (city1[1] - city2[1])**2
    distance = round(math.sqrt(x + y))
    return distance

def getSmallest(cityData, currentId):
    nearestCityId = -1
    shortestDistance = sys.maxsize
    unvisited = cityData[0] # Set of city id's
    distances = cityData[1] # List of city x and y values
    
    for cityId in unvisited:
        travelDistance = getDistance(distances[currentId], distances[cityId])

        if travelDistance < shortestDistance and travelDistance > 0:
            shortestDistance = travelDistance
            nearestCityId = cityId

    return [nearestCityId, shortestDistance]

def removeCity(cityData, index):
    unvisited = cityData[0] # Set of city id's
    unvisited.remove(index)
    return index

def nearestNeighbor(cityData, startingId):
    path = []
    unvisited = cityData[0] # Set of city id's
    distances = cityData[1] # List of city x and y values
    distance = 0

    # Remove starting city and add to path
    path.append(removeCity(cityData, startingId))
    
    # Iterate through unvisited cities
    while unvisited:
        smallest = getSmallest(cityData, path[-1])
        distance += smallest[1]
        
        # Append nearest city id to path, remove from unvisited city set
        path.append(removeCity(cityData, smallest[0]))
    
    # Add distance from last city to first city, complete cycle
    distance += getDistance(distances[path[0]], distances[path[-1]])

    return [distance, path]


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

def opt_2(tour, cities):
    size = len(tour)
    i = 0
    best_dist = getTotDist(tour, cities)
    print("Starting Length: " + str(best_dist))                     
    while i < 2:
        j = 0
        while j < size - 1:
            k = j+1
            while k < size:
                new_tour = []
                #swap_slice(j, k, tour, new_tour)
                swap(j, k, tour, new_tour)
                #print(new_tour)
                #print('\n')            
                new_dist = getTotDist(new_tour, cities)
                if new_dist < best_dist:
                    i = 0
                    tour = new_tour
                    best_dist = new_dist
                    print("Current Best: " + str(best_dist))                        
                k += 1
            j += 1
        i += 1
    return [best_dist, tour]


def getTotDist(cycle, cities):
    sum = 0
    i = 1
    while i < len(cycle):
        #print("from: " + str(cycle[i-1]) + "  to: " + str(cycle[i]) + "  Dist: " + str(getDistance(cities[cycle[i-1]], cities[cycle[i]])))
        sum += getDistance(cities[cycle[i-1]], cities[cycle[i]])
        i += 1
    sum += getDistance(cities[cycle[i-1]], cities[cycle[0]])
    return sum

def solve(inputFile, outputFile):
    cityData = getCityData(inputFile)
    unvisited = cityData[0] # Set of city id's
    distances = cityData[1] # List of city x and y values
    tourLength = len(distances)     
    bestDistance = sys.maxsize
    bestTour = None
    visited = 0

    # Run Nearest Neighbor with each city as starting point for more optimal solution for smaller input files
    if tourLength <= 5000:
        tourRange = 0
        
        # Run nearest neighbor starting on only a portion of the first cities
        if tourLength < 500:
            tourRange = tourLength
        elif tourLength < 1000:
            tourRange = 200
        elif tourLength < 2000:
            tourRange = 80
        elif tourLength < 5000:
            tourRange = 25
        else:
            tourRange = 3
        
        for i in range(tourRange):
            unvisitedCopy = set(unvisited) # Copy unvisited set since data is removed with each iteration
            cityDataCopy = [unvisitedCopy, distances]

            path = nearestNeighbor(cityDataCopy, i)
            if path[0] < bestDistance:
                bestDistance = path[0]
                bestTour = path
                print("Best distance so far is: {} and {} solutions have been tried".format(path[0], visited))

            visited += 1
    else:
        bestTour = nearestNeighbor(cityData, 0)
    
    if tourLength < 500:
        bestTour = opt_2(bestTour[1], cityData[1])
    
    outputTour(bestTour, outputFile)
    print("Distance: {}".format(bestTour[0]))
    print("Cities visited: {}".format(len(bestTour[1])))

def main():
    start_time = time.time() # Start timer

    if len(sys.argv) < 2:
        print('Input must be in the form of "python3 nearest_neighbor_test.py [input file]"')
    else:
        inputFile = sys.argv[1]
        outputFile = inputFile + ".tour"
        solve(inputFile, outputFile)
    
    # Get elapsed time in seconds
    elapsedTime = (time.time() - start_time)
    print("Elapsed seconds: {}".format(math.floor(elapsedTime)))

main()
