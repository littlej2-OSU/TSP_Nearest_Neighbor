class GraphManager(object):
	def __init__(self, vertices, edges):
		self.vertices = vertices
		self.edges = edges
		self.build_edge_dict()

	def build_edge_dict(self):
		self.edge_dict = {}
		for vertex in self.vertices:
			self.edge_dict[vertex] = {}
			self.edge_dict[vertex]["neighbors"] = set()
		for edge in self.edges:
			self.edge_dict[edge[0]][edge[1]] = edge[2]
			self.edge_dict[edge[0]]["neighbors"].add(edge[1])

	def get_vertices(self):
		return self.vertices

	def get_edges(self):
		return self.edges

	def get_neighbors(self, vertex):
		return self.edge_dict[vertex]["neighbors"]

	def get_edge_cost(self, origin, destination):
		return self.edge_dict[origin][destination]

	def del_vertex(self, vertex):
		for neighbor in self.edge_dict[vertex]["neighbors"]:
			self.edge_dict[neighbor]["neighbors"].remove(vertex)
		del self.edge_dict[vertex]

	def del_edge(self, edge):
		del self.edge_dict[edge[0]][edge[1]]
		del self.edge_dict[edge[1]][edge[0]]

	def add_vertex(self, vertex, edges):
		self.edge_dict[vertex] = {}
		for edge in edges:
			self.edge_dict[vertex][edges[1]] = edges[2]


	

