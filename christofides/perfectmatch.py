import random
import graphmanager

def min_weight_matching(vertices, edges, mst_edges):
	graph = graphmanager.GraphManager(vertices, edges)

	vertices = random.shuffle(list(vertices))
	while vertices:
		this_vertex = vertices.pop()
		cost = float("inf")
		nearest_neighbor = None
		for vertex in vertices:
			if (vertex != this_vertex
			and graph.get_edge_cost(this_vertex, vertex) < cost):
				cost = graph[this_vertex][vertex]
				nearest_neighbor = vertex

		mst_edges.append(this_vertex, vertex, cost)
		vertices.remove(nearest_neighbor)

	return vertices, mst_edges

