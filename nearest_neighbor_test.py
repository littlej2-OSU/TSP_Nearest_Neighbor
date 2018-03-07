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

def getSmallest(cities, cityId):
    smallestId = -1
    smallest = sys.maxsize

    for i in range(len(cities)):
        distance = getDistance(cities[cityId], cities[i])
        if distance < smallest and distance > 0:
            print(distance)
            smallest = distance
            smallestId = i

    path = [smallestId, smallest]
    return path

def removeCity(cities, index):
    city = {index: cities[index]}
    del cities[index]
    return city

def getPath(cities):
    path = []
    
    path.append(removeCity(cities, 0))
    print(path)

    while cities:
        smallest = -1
        current = path[len(path) - 1]
        for key in current:
            current = key

def deleteAll(cities):
    i = 0
    while cities:
        removeCity(cities, i)
        print(cities)
        i += 1

cities = getContent("./TSP_Files-1/tsp_example_1.txt")
getPath(cities)
