from queue import PriorityQueue
import sys
from random import random
import render
from render import VideoBuilder
from PIL import Image
import math

#---Video Output Options---
makeVid = False #generate output video

#---Image Input Options---
descale = 1 #reduce input image size by this factor

edgeWeights = {}

#load imput image
im = Image.open("weight.jpg")
width, height = im.size

#resize Input
im = im.resize((int(width / descale), int(height / descale)))
width, height = im.size

grayscale = im.convert("L")

# size of grid
if(len(sys.argv) == 2):
        gridWidth = int(sys.argv[1])
        gridHeight = int(sys.argv[1])
elif(len(sys.argv) == 3):
        gridWidth = int(sys.argv[1])
        gridHeight = int(sys.argv[2])
else:
        gridWidth = int((width - 1) / 2)
        gridHeight = int((height - 1) / 2)

if makeVid:
    #create instance of VideoBuilder
    vid = VideoBuilder(gridWidth * 2 + 1, gridHeight * 2 + 1)
    #add entrance to gif
    vid.add_frame(0, 1)

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
fromNode = dict()

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
if makeVid:
    vid.add_frame(1, 1)

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
            #find node already in treeNodes
            originNode = (0, 0)
            for node in edge[1] - frozenset({endpointNode}):
                originNode = node

            # add edge to treeEdges
            treeEdges.add(edge[1])
            # Add the new node to the tree
            treeNodes.add(endpointNode)

            #Store previous node
            fromNode[endpointNode] = originNode

            if makeVid:
                #add video frames
                #average origin and new node co-ords to find edge position
                vid.add_frame(originNode[0] + endpointNode[0] + 1, originNode[1] + endpointNode[1] + 1)
                #add new node
                vid.add_frame(endpointNode[0] * 2 + 1, endpointNode[1] * 2 + 1)

            #print progress percent
            print(len(treeNodes)/(gridWidth * gridHeight))

            # explore the new node for edges
            neighbors = getNeighbors(endpointNode)

            for neighbor in neighbors:
                if not neighbor in treeNodes:
                    newEdge = frozenset({endpointNode, neighbor})
                    openEdges.put((edgeWeights[newEdge], newEdge))

if makeVid:
    #add exit to movie
    vid.add_frame(gridWidth * 2, gridHeight * 2 - 1)

#Find solution path
path = []
path.append((gridWidth - 1, gridHeight - 1))

while path[-1] != (0, 0):
    path.append(fromNode[path[-1]])

path.reverse()

#---Generate Pixel Data---

#holds data to be written to bitmap
pixelData = []

#add upper edge
for i in range(0, gridWidth * 2 + 1):
        pixelData.append((0, 0, 0))

for j in range(0,gridHeight):

    #Left border
    if j == 0:
        pixelData.append((255, 255, 255))
    else:
        pixelData.append((0, 0, 0))

    #right edges
    for i in range(0,gridWidth):

        #add pixel for each node
        pixelData.append((255, 255, 255))

        #add pixel for each right edge in treeEdges
        if j == gridHeight - 1 and i == gridWidth - 1:
            #maze exit
            pixelData.append((255, 255, 255))
        else:
            if frozenset({(i, j),(i+1,j)}) in treeEdges:
                pixelData.append((255, 255, 255))
            else:
                pixelData.append((0, 0, 0))

    # Left border
    pixelData.append((0, 0, 0))

    #add pixel for each down edge in treeEdges
    for i in range(0, gridWidth):

        if frozenset({(i, j),(i,j+1)}) in treeEdges:
            pixelData.append((255, 255, 255))
        else:
            pixelData.append((0, 0, 0))

        pixelData.append((0, 0, 0))

#save and display maze image
render.show_maze(pixelData, gridWidth * 2 + 1, gridHeight * 2 + 1, "maze.png")

#Generate solution image
pixelData[gridWidth * 2 + 1] = (255, 0, 0)

for i in range(0, len(path) - 1):
    #colour node
    pixelData[(path[i][1] + 1) * (gridWidth * 2 + 1) * 2 - (gridWidth * 2 + 1) + (path[i][0] * 2 + 1)] = (255, 0, 0)

    #colour edge
    edgeCoord = ((path[i][0] + path[i + 1][0]) / 2, (path[i][1] + path[i + 1][1]) / 2)
    pixelData[int((edgeCoord[1] + 1) * (gridWidth * 2 + 1) * 2 - (gridWidth * 2 + 1) + (edgeCoord[0] * 2 + 1))] = (255, 0, 0)

pixelData[(path[-1][1] + 1) * (gridWidth * 2 + 1) * 2 - (gridWidth * 2 + 1) + (path[-1][0] * 2 + 1)] = (255, 0, 0)
pixelData[(path[-1][1] + 1) * (gridWidth * 2 + 1) * 2 - (gridWidth * 2 + 1) + (path[-1][0] * 2 + 1) + 1] = (255, 0, 0)

render.show_maze(pixelData, gridWidth * 2 + 1, gridHeight * 2 + 1, "solution.png")

if makeVid:
    #close ffmpeg processs
    vid.release()

print(path)
