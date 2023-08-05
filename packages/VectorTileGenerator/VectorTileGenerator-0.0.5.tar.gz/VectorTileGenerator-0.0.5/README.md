# VectorTileGenerator

A python package to automatically generate a list of all possible tiles options between two zoom levels and a bounding box.

## Install
`pip install VectorTileGenerator`

## How to use
```
from VectorTileGenerator import generator

tileGeneration = generator.GenerateTiles(1, 5, [-118, 34, -84, 50])

# Demo of generating tiles
print(tileGeneration.generate())
```