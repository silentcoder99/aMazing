from min_heap import MinHeap
from random import random
edgeWeights = {}

# size of grid
gridSize = 8

for i in range(0,gridSize):
	for j in range(0,gridSize):
		if i != gridSize - 1:
			edgeWeights[frozenset({(i, j), (i + 1, j)})] = random()
		if j != gridSize - 1:
			edgeWeights[frozenset({(i, j), (i, j + 1)})] = random()

print edgeWeights
