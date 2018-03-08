import math
import sys

def getContentAsList(fileName):
    allCities = []
    with open(fileName) as f:
        for line in f:

            # Split each line into array, convert to int
            city = line.split()
            city = list(map(int, city))
            city.pop(0)
            allCities.append(city)

    return allCities

def getContent(fileName):
    allCities = {}

    with open(fileName) as f:
        for line in f:
            city = []

            # Split each line into array
            lineArr = line.split()
            lineArr = list(map(int, lineArr))
            
            # Build x and y data
            city.append(lineArr[1])
            city.append(lineArr[2])
            city = list(map(int, city))

            allCities[lineArr[0]] = (city)

    return allCities

def getDistance(city1, city2):
    x = (city1[0] - city2[0])**2
    y = (city1[1] - city2[1])**2
    distance = round(math.sqrt(x + y))
    return distance

# This is inefficient 
def buildAdjacencyMatrix(data):
    myMatrix = []

    for i in range(len(data)):
        city = []
        for y in range(len(data)):
            city.append(getDistance(data[i], data[y]))
        myMatrix.append(city)

    print(myMatrix)
    return myMatrix

def getSmallest(allCities, city):
    smallestId = -1
    smallest = sys.maxsize
    
    # TODO: Iteration by index won't work.
    for i in allCities:
        distance = getDistance(city, allCities[i])
        if distance < smallest and distance > 0:
            smallest = distance
            smallestId = i

    path = [smallestId, smallest]
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
        currentKey = -1
        current = path[len(path) - 1]
        
        # Get id from current city
        for key in current:
            currentKey = key

        smallest = getSmallest(cities, current[currentKey]) 
        distance += smallest[1]
        path.append(removeCity(cities, smallest[0]))
    
    # TODO: Add distance from last city to first city
    return [distance, path]

def deleteAll(cities):
    i = 0
    while cities:
        removeCity(cities, i)
        print(cities)
        i += 1

cities = getContent("./TSP_Files-1/tsp_example_2.txt")
path = getPath(cities, 0)
print(path)
