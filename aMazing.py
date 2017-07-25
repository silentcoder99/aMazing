from random import random
from queue import PriorityQueue
import render

edgeWeights = {}

# size of grid
gridSize = 25

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
	if x > 0:
		nodes.add((x-1, y))
	if y > 0:
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

	# Check the two endpoints for new nodes
	for endpointNode in edge[1]:
		if not endpointNode in treeNodes:
			# add edge to treeEdges
			treeEdges.add(edge[1])
			# Add the new node to the tree
			treeNodes.add(endpointNode)

			# explore the new node for edges
			neighbors = getNeighbors(endpointNode)

			for neighbor in neighbors:
				if not neighbor in treeNodes:
					edge = frozenset({endpointNode, neighbor})
					openEdges.put((edgeWeights[edge], edge))

#holds data to be written to bitmap
pixelData = []

#add upper edge
for i in range(0, gridSize * 2 + 1):
		pixelData.append(0)

for j in range(0,gridSize):

	#Left border
	if j == 0:
		pixelData.append(1)
	else:
		pixelData.append(0)

	#right edges
	for i in range(0,gridSize):

		#add pixel for each node
		pixelData.append(1)

		#add pixel for each right edge in treeEdges
		if j == i == gridSize - 1:
			pixelData.append(1)
		else:
			if frozenset({(i, j),(i+1,j)}) in treeEdges:
				pixelData.append(1)
			else:
				pixelData.append(0)

	# Left border
	pixelData.append(0)

	#add pixel for each down edge in treeEdges
	for i in range(0, gridSize):

		if frozenset({(i, j),(i,j+1)}) in treeEdges:
			pixelData.append(1)
		else:
			pixelData.append(0)

		pixelData.append(0)

print(len(pixelData))
render.show_maze(pixelData, gridSize * 2 + 1, 1)
