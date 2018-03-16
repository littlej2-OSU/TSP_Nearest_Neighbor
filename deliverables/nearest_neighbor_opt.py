"""
Nearest Neighbor implementation for the Travelling Salesman Problem
Project Group 31
"""
import sys
import time
import math

#This function takes the input file as a parameter
#Returns a set of cities (ex: {0, 1, 2}) and an array
#of x, y corrdinates for each city (ex: [[5, 8], [6, 9], [10, 15]])
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

#takes a array of tour data where the first element
#is the total distance, and the second is an array of
#cities in visited order.  The second element is the output
#filename.  Function writes to ouput file, putting the distance
#on the first line and then each city on subsequent lines in the 
#order that they are visited in.
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

#Takes to cities as parameters
#calculates and then returns the distance between the two cities.
def getDistance(city1, city2):
    x = (city1[0] - city2[0])**2
    y = (city1[1] - city2[1])**2
    distance = round(math.sqrt(x + y))
    return distance

#takes what is returned from getCityData() and the current location
#finds the next closest city and returns it's id and the distance
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

#takes what is returned from getCityData() and the index of the
#city to be removed from the unvisited list in cityData.
#removes city from list and then returns which city was removed.
def removeCity(cityData, index):
    unvisited = cityData[0] # Set of city id's
    unvisited.remove(index)
    return index

#takes what is returned from getCityData() and as starting city
#as parameters.  Finds the shortest tour for visiting every city once
#that it can by visiting the next closest city.  (Greedy approach)
#returns and array where the first value is the total distance, and the
#second is an array that contains the tour.
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


#function takes in two cities, the current tour and an empty new_tour
#it then creates a new_tour by swapping two edges
def swap(one, two, tour, new_tour):
    size = len(tour)
    #adds all cities from tour to new_tour up to one
    i = 0
    while i < one:
        new_tour.append(tour[i])
        i += 1  
    count = 0
    #adds cities from two going backwards until it adds one
    i = one
    while i <= two:
        new_tour.append(tour[two-count])
        count += 1
        i += 1
    i = two + 1
    #adds the rest of the cities to new_tour until the end of tour
    while i < size:
        new_tour.append(tour[i])
        i += 1

#Function takes in a tour and a list of city coordinates
#goes through tour swaping two edges at a time and checking to see if
#it returns a better distance.  If the distance improves it keeps the new
#tour and continues swapping until no more improvements can be made.
def opt_2(tour, cities):
    size = len(tour)
    i = 0
    best_dist = getTotDist(tour, cities)

    #while loop cycles until no improvements are made for a full loop cycle
    #can increase 2 to have to check for improvements for more iterations
    while i < 2:
        j = 0
        #loops through each city
        while j < size - 1:
            k = j+1
            #for each city swap edges to that city with every edge to the end of 
            #the current tour.  if an improvement is found, reset i to 0
            while k < size:
                new_tour = []
                swap(j, k, tour, new_tour)
                new_dist = getTotDist(new_tour, cities)

                #keep new tour if it's better
                if new_dist < best_dist:
                    i = 0
                    tour = new_tour
                    best_dist = new_dist

                k += 1
            j += 1
        i += 1
    return [best_dist, tour]

#takes a tour and a list of city coordinates
#returns the total distance of the tour
def getTotDist(cycle, cities):
    sum = 0
    i = 1
    while i < len(cycle):
        sum += getDistance(cities[cycle[i-1]], cities[cycle[i]])
        i += 1

    sum += getDistance(cities[cycle[i-1]], cities[cycle[0]])
    return sum

#Function to solve TSP.  Takes in an inputfile name and an output file name
#Determins best method for finding a TSP tour based on number of cities
#outputs the distance and tour to a file.
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

            visited += 1
    else:
        bestTour = nearestNeighbor(cityData, 0)
    
    if tourLength < 500:
        bestTour = opt_2(bestTour[1], cityData[1])
    
    outputTour(bestTour, outputFile)
    print("Distance: {}".format(bestTour[0]))

#main function gets input file name, creates output file name
#and times how long it takes to run the algorithm.
def main():
    start_time = time.time() # Start timer

    if len(sys.argv) < 2:
        print('Input must be in the form of "python3 opt.py [input file]"')
    else:
        inputFile = sys.argv[1]
        outputFile = inputFile + ".tour"
        solve(inputFile, outputFile)
    
    # Get elapsed time in seconds
    elapsedTime = (time.time() - start_time)
    print("Elapsed seconds: {}".format(math.floor(elapsedTime)))

main()
