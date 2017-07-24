from min_heap import MinHeap
from random import random
from Queue import PriorityQueue

edgeWeights = {}

# size of grid
gridSize = 8

# Generate random edge weights
for i in range(0,gridSize):
	for j in range(0,gridSize):
		if i != gridSize - 1:
			edgeWeights[frozenset({(i, j), (i + 1, j)})] = random()
		if j != gridSize - 1:
			edgeWeights[frozenset({(i, j), (i, j + 1)})] = random()

treeNodes = set()
treeEdges = set()
openEdges = PriorityQueue()

def getNeighbors(point):
	nodes = set()
	x = point[0]
	y = point[1]
	if x > 1:
		nodes.add((x-1, y))
	if y > 1:
		nodes.add((x, y-1))
	if x < gridSize - 1:
		nodes.add((x + 1, y))
	if y < gridSize - 1:
		nodes.add((x, y+1))
	return nodes

# Add our first node to the tree
treeNodes.add((0,0))

# Discover neighbors from that node
neighbors = getNeighbors((0,0))

# Add those neighbors
for neighbor in neighbors:
	edge = frozenset({(0,0), neighbor})
	openEdges.put((edgeWeights[edge],edge))

# Do it for the rest
while not openEdges.empty():
	edge = openEdges.get()

	# add edge to treeEdges
	treeEdges.add(edge[1])

	# Check the two endpoints for new nodes
	for endpointNode in edge[1]:
		if not endpointNode in treeNodes:
			# Add the new node to the tree
			treeNodes.add(endpointNode)
			
			# explore the new node for edges
			neighbors = getNeighbors(endpointNode)

			for neighbor in neighbors:
				if not neighbor in treeNodes:
					edge = frozenset({endpointNode, neighbor})
					openEdges.put((edgeWeights[edge], edge))

print len(treeNodes)
print treeEdges
