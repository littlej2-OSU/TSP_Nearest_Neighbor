# Inspired by Geeks for Geeks
# https://www.geeksforgeeks.org/greedy-algorithms-set-2-kruskals-minimum-spanning-tree-mst/

def find_set(master_set, vertex):
    # Determine if two vertices are within the same set.
    if master_set[int(vertex)] == vertex:
        return vertex
    return master_set[int(vertex)]

def union_set(master_set, rank, a, b):
    root_a = find_set(master_set, a)
    root_b = find_set(master_set, b)

    if rank[root_a] > rank[root_b]:
        master_set[root_a] = root_a
    else:
        master_set[root_a] = root_b
        if rank[root_a] == rank[root_b]:
            rank[root_b] += 1

def generate_mst(vertices, edges):
    master_set = {}
    rank = {}

    for vertex in vertices:
        master_set[vertex] = vertex
        rank[vertex] = 0

    result_vertices = set()
    result_edges = set()
    edges.sort(key=lambda x: x[2]) # sort by distance

    for edge in edges:
        origin, destination, cost = edge
        if find_set(master_set, origin) != find_set(master_set, destination):
            union_set(master_set, rank, origin, destination)
            result_edges.add(edge)
            result_vertices.add(origin)
            result_vertices.add(destination)

    return result_vertices, result_edges