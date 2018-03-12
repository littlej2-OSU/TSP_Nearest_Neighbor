import math
import sys

import kruskal
import oddfellow
import perfectmatch

def generate_vertices(file_name):
    cities = dict()

    with open(file_name) as i:
        for line in i:
            location = []
            data = list(map(int, line.split()))
            location += [data[1], data[2]]

            cities[data[0]] = location

    return cities

def generate_edges(cities):
    # Edge in the form [origin, destination, cost]
    edges = []
    for origin in cities:
        for destination in cities:
            if origin is not destination:
                distance = generate_distance(cities[origin], cities[destination])
                edges.append(tuple([str(origin), str(destination), distance]))

    return edges

def generate_distance(city_a, city_b):
    x = (city_a[0] - city_b[0])**2
    y = (city_a[1] - city_b[1])**2
    return round(math.sqrt(x + y))

def christofy(input_file):
    vertices = generate_vertices(input_file)
    edges = generate_edges(vertices)
    mst_vertices, mst_edges = kruskal.generate_mst(vertices, edges)
    odd_vertices, odd_edges = oddfellow.generate_odd_degree_subgraph(mst_vertices, mst_edges)
    step_vertices, mst_edges = perfectmatch.min_weight_matching(odd_vertices, odd_edges, mst_edges)

def main():
    if len(sys.argv) < 3:
        print('Input must be in the form of "python3 nearest_neighbor_test.py input_file output_file"')
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        christofy(input_file)

main()
