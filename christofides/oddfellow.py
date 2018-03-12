def generate_odd_degree_subgraph(vertices, edges):
	vertices = set(vertices)
	vertices_count = {}
	for vertex in vertices:
		vertices_count[int(vertex)] = 0
	for edge in edges:
		vertices_count[int(edge[0])] += 1

	odd_vertices = set()
	for vertex in vertices:
		if vertices_count[int(vertex)] % 2 != 0:
			odd_vertices.add(vertex)

	odd_edges = set()
	for edge in edges:
		if int(edge[0]) in odd_vertices and int(edge[1]) in odd_vertices:
			odd_edges.add(edge)

	return odd_vertices, odd_edges

	