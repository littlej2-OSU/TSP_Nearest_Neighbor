import math

def getContent(fileName):
    allCities = []
    with open(fileName) as f:
        for line in f:

            # Split each line into array, convert to int
            city = line.split()
            city = list(map(int, city))
            city.pop(0)
            allCities.append(city)

    return allCities

def getDistance(city1, city2):
    test = math.sqrt(city1[0] + city2[0])    
    print(test)

def buildAdjacencyMatrix(data):
    matrix = []
    print (data)

cities = getContent("./TSP_Files-1/tsp_example_1.txt")
getDistance(cities[0], cities[1])
