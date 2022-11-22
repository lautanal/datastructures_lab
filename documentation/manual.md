# User manual

## Download

Download [release](https://github.com/lautanal/tiralabra/releases/tag/Final).

## Installation

The program is copied to a user defined folder.

A virtual environment is created:

$ poetry install

## Running

The program is run in the installation folder using the following command:

$ poetry run python3 src/bestroute.py

## User interface

The program is run and controlled through a user interface :

<img src="png/ui3.png" width="750">

The user chooses the start and end points with a mouse left click.  After choosing the start and end point, the user can mark the blocked nodes with a mouse left click.  Start and end points and blocked nodes can be erased with a mouse right click.

The algorithm is chosen with a keyboard command m.

Route calculation starts with a keyboard command s.

## Commands

### Keyboard commands:

s : start, start calculating the best route

c : clear, clear start and end points

r : reset, erase the calculated route

m : method, Dijkstra / A* / IDA* / JPS

d : diagonal, orthogonal or diagonal toggle

a : animointi, animation on/off toggle

n: new, generates a new random map (weighted nodes)

g: generate, generates a new map without weights (all nodes equal)

t : test, program test 10 random maps (koko 100 x 100)

\+ : increase node count 10% in both directions and generate a new map

\- : decrease node count 10% in both directions and generate a new map

1 : load map 1.map (from folder data/maps)

2 : load map 2.map (from folder data/maps)

w : write, save map into file f.map (folder data/maps)

f : file, load map from file f.map (folder data/maps)

### Mouse commands:

A left click chooses the start point (if it does not exist)

A left click chooses the end point (when start point is chosen and end point does not exist)

A left click chooses the a blocked node (when start point and end point are already chosen)

A right click erases a node (start point, emnd point or a blocked node)

In edit mode a left click increases the node cost, a right click decreases the node cost





