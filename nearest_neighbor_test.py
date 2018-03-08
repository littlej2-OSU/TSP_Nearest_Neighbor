"""
Nearest Neighbor implementation for the Travelling Salesman Problem
Project Group 31
"""
import math
import sys

def getCityData(fileName):
    allCities = {}

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

            allCities[lineArr[0]] = (city)

    return allCities

def outputTour(size, tour, fileName):
    f = open(fileName, "w")     
    
    f.write(str(size) + "\n")

    for city in tour:
        for id in city:
            f.write(str(id) + "\n")    

    f.close()

def getDistance(city1, city2):
    x = (city1[0] - city2[0])**2
    y = (city1[1] - city2[1])**2
    distance = round(math.sqrt(x + y))
    return distance

def getSmallest(allCities, city):
    smallestId = -1
    smallestPath = sys.maxsize
    
    for i in allCities:
        distance = getDistance(city, allCities[i])
        if distance < smallestPath and distance > 0:
            smallestPath = distance
            smallestId = i

    path = [smallestId, smallestPath]
    return path

def removeCity(cities, index):
    city = {index: cities[index]}
    del cities[index]
    return city

def getPath(cities, startingId):
    path = []
    distance = 0
    
    # Remove starting city and add to path
    path.append(removeCity(cities, startingId))
    
    # Iterate through unvisited cities
    while cities:
        smallest = []
        currentKey = None
        current = path[len(path) - 1]
        
        # Get id from current city
        for key in current:
            currentKey = key

        smallest = getSmallest(cities, current[currentKey]) 
        distance += smallest[1]
        path.append(removeCity(cities, smallest[0]))
    
    # Add distance from last city to first city to total distance
    firstCity = path[0][startingId]
    lastCity = path[len(path) - 1]
    lastCityId = None
    
    # Get city id of last city visited 
    for key in lastCity:
        lastCityId = key
    
    # Complete the cycle, add last distance to total distance
    distance += getDistance(firstCity, lastCity[lastCityId])

    return [distance, path]

def solve(fileName):
    cities = getCityData(fileName)
    tourLength = len(cities)     
    bestDistance = sys.maxsize
    bestTour = None
    
    # Run Nearest Neighbor with each city as starting point for more optimal solution for smaller input files
    if tourLength < 500:
        for i in range(tourLength):
            citiesCopy = dict(cities)
            path = getPath(citiesCopy, i)
            if path[0] < bestDistance:
                bestDistance = path[0]
                bestTour = path
                print("Best distance so far is: {}".format(path[0]))
    else:
        bestTour = getPath(cities, 0)
    
    outputTour(bestTour[0], bestTour[1], "test")
    # print("Distance: {}".format(bestTour[0]))
    # print("Cities visited: {}".format(len(bestTour[1])))

fileName = "./TSP_Files-1/tsp_example_1.txt"
solve(fileName)
