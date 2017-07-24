from min_heap import MinHeap
from queue import PriorityQueue
import random
import sys

edgeWeights = {}

# size of grid
if(len(sys.argv) == 2):
        gridWidth = sys.argv[1]
        gridHeight = sys.argv[1]
elif(len(sys.argv) == 3):
        gridWidth = sys.argv[1]
        gridHeight = sys.argv[2]
else:
        gridWidth = 90
        gridHeight = 60

# Generate random edge weights
for i in range(0,gridWidth):
	for j in range(0,gridHeight):
		if i != gridWidth - 1:
			edgeWeights[frozenset({(i, j), (i + 1, j)})] = random.uniform(0,1)
		if j != gridHeight - 1:
			edgeWeights[frozenset({(i, j), (i, j + 1)})] = random.uniform(0,1)

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


block = "\u2588"
# create header
header = ""
for i in range(0, gridWidth * 2 + 1):
	header += block

# Print the maze
print(header)
for j in range(0,gridHeight):

	# Left borders
	firstRow = block
	secondRow = block
	for i in range(0,gridWidth):

		# Print right edges
		if frozenset({(i, j),(i+1,j)}) in treeEdges:
			firstRow += "  "
		else:
			firstRow += " " + block
		# print bottom edges
		if frozenset({(i, j),(i,j+1)}) in treeEdges:
			secondRow += " " + block
		else:
			secondRow += block + block
	# print constructed rows
	print (firstRow)
	print (secondRow)
