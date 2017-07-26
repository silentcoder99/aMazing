from min_heap import MinHeap
from queue import PriorityQueue
import sys
from random import random
import render
from PIL import Image

edgeWeights = {}

# size of grid
if(len(sys.argv) == 2):
        gridWidth = sys.argv[1]
        gridHeight = sys.argv[1]
elif(len(sys.argv) == 3):
        gridWidth = sys.argv[1]
        gridHeight = sys.argv[2]
else:
        gridWidth = 300
        gridHeight = 300

#image scale (1 - 1:1 pixel ratio)
scale = 8

im = Image.open("weight.jpg")
width, height = im.size
grayscale = im.convert("L")

def getWeight(position):
        return grayscale.getpixel(position)


# Generate random edge weights
for i in range(0,gridWidth):
	for j in range(0,gridHeight):
		if i != gridWidth - 1:
			edgeWeights[frozenset({(i, j), (i + 1, j)})] = getWeight((2 * i + 1, 2 * j))
		if j != gridHeight - 1:
			edgeWeights[frozenset({(i, j), (i, j + 1)})] = getWeight((2 * i, 2 * j + 1))

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
	if x < gridWidth - 1:
		nodes.add((x + 1, y))
	if y < gridHeight - 1:
		nodes.add((x, y+1))
	return nodes

startNode = (0,0)
# Add our first node to the tree
treeNodes.add(startNode)

# Discover neighbors from that node
rootNeighbors = getNeighbors(startNode)

# Add those neighbors
for rootNeighbor in rootNeighbors:
	rootEdge = frozenset({startNode, rootNeighbor})
	openEdges.put((edgeWeights[rootEdge],rootEdge))

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
					newEdge = frozenset({endpointNode, neighbor})
					openEdges.put((edgeWeights[newEdge], newEdge))

#holds data to be written to bitmap
pixelData = []

#add upper edge
for i in range(0, gridWidth * 2 + 1):
		pixelData.append(0)

for j in range(0,gridHeight):

	#Left border
	if j == 0:
		pixelData.append(1)
	else:
		pixelData.append(0)

	#right edges
	for i in range(0,gridWidth):

		#add pixel for each node
		pixelData.append(1)

		#add pixel for each right edge in treeEdges
		if j == i == gridWidth - 1:
			pixelData.append(1)
		else:
			if frozenset({(i, j),(i+1,j)}) in treeEdges:
				pixelData.append(1)
			else:
				pixelData.append(0)

	# Left border
	pixelData.append(0)

	#add pixel for each down edge in treeEdges
	for i in range(0, gridWidth):

		if frozenset({(i, j),(i,j+1)}) in treeEdges:
			pixelData.append(1)
		else:
			pixelData.append(0)

		pixelData.append(0)

print(len(pixelData))
render.show_maze(pixelData, gridWidth * 2 + 1, scale)
