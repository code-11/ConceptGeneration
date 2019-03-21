from queue import Queue
from queue import PriorityQueue
import math
import numpy
from numpy.random import randint as rand
import matplotlib.pyplot as pyplot

def graph1():
	return {'A':{'B','D','F'},
	   'B':{'A','D','C','I','E'},
	   'C':{'B','I'},
	   'D':{'A','B','E','F'},
	   'E':{'B','D','F','G'},
	   'F':{'A','D','E','G'},
	   'G':{'F','E','H'},
	   'H':{'G','I'},
	   'I':{'B','C','H'}}

def graph2():
	return {'A':{('B',4),('D',5),('F',3)},
	   'B':{('A',4),('D',2),('C',8),('I',15),('E',3)},
	   'C':{('B',8),('I',4)},
	   'D':{('A',5),('B',2),('E',1),('F',1)},
	   'E':{('B',3),('D',1),('F',4),('G',2)},
	   'F':{('A',3),('D',1),('E',4),('G',6)},
	   'G':{('F',6),('E',2),('H',2)},
	   'H':{('G',2),('I',2)},
	   'I':{('B',15),('C',4),('H',2)}}   

def graph3():
	height=50
	width=80
	Z = numpy.zeros((height,width), dtype=bool)
	Z[20:29,35]=1
	Z[29,20:36]=1
	graph=bin2graph(Z)
	return Z,graph

def graph4():
	return {(3,3):{(6,9),(10,6),(12,2)},
	   (6,9):{(3,3),(10,6),(9,12),(11,12),(13,7)},
	   (9,12):{(6,9),(11,12)},
	   (10,6):{(3,3),(6,9),(13,7),(12,2)},
	   (13,7):{(6,9),(10,6),(12,2),(22,3)},
	   (12,2):{(3,3),(10,6),(13,7),(22,3)},
	   (22,3):{(12,2),(13,7),(19,11)},
	   (19,11):{(22,3),(11,12)},
	   (11,12):{(6,9),(9,12),(19,11)}}

def BFS(graph,start,goal):
	visited={start}
	queue=Queue()
	queue.put([start])

	while not queue.empty():
		path=queue.get()
		cur_pos=path[-1]
		#Check for goal
		if cur_pos==goal:
			return path
		#loop through neighbors
		for n in graph[cur_pos]:
			if n not in visited:
				visited.add(n)
				queue.put(path+[n])
	return None

def descipher_dijkstra(prev_map,goal):
	path=[goal]
	while prev_map.get(path[0]):
		path.insert(0,prev_map.get(path[0]))
	return path

def Dijkstra(graph,start,goal):
	distTo= {key: float('inf') for key in graph.keys()}
	distTo[start]=0
	prev={}
	unvisited = set(graph.keys())

	while unvisited: #while not empty
		u=min(unvisited,key= lambda x:distTo[x])
		unvisited.remove(u)
		if u==goal:
			#returns the path given prev map
			return descipher_dijkstra(prev,goal)
		for n,weight in graph[u]:
			altDist=distTo[u] + weight
			if altDist < distTo[n]:
				distTo[n]=altDist
				prev[n]=u
	return None

#Finds cumulative distance between a list of points
def accum_map_dist(map_dist,path):
	accum_dist=0
	if len(path)>1:
		#breaks down [A,B,C,D] into [(A,B),(B,C),(C,D)]
		for p1,p2 in zip(path,path[1:]):
			accum_dist+=map_dist(p1,p2)
	return accum_dist

#Distance formula
def map_dist(p1,p2):
	return math.hypot(float(p2[0]-p1[0]),float(p2[1]-p1[1]))

#A star with normal euclidean distance
def MapAStar(graph,start,goal):
	estimate= lambda pos: map_dist(pos,goal)
	dist_func= lambda path: accum_map_dist(map_dist,path)
	return AStar(graph,start,goal,dist_func,estimate)

#A star with manhattan distance
def ManhattanAStar(graph, start, goal):
	estimate = lambda pos: (abs(pos[0]-goal[0])+abs(pos[1]-goal[1]))
	#Shortcut. All moves are one away so the cumulative distance is just the length-1
	dist_func= lambda path: (len(path)-1)
	return AStar(graph, start,goal,dist_func,estimate)

#accum_dist_func is g(n) and heuristic is h(n)
def AStar(graph, start, goal,accum_dist_func, heuristic):
	visited={start}
	#f(n)=g(n)+h(n)
	priority_func= lambda path: accum_dist_func(path)+heuristic(path[-1])
	queue=PriorityQueue()
	queue.put((priority_func([start]),[start]))

	while not queue.empty():
		priority,path=queue.get()
		cur_pos=path[-1]
		#Check for goal
		if cur_pos==goal:
			return path
		#loop through neighbors
		for n in graph[cur_pos]:
			if n not in visited:
				visited.add(n)
				queue.put((priority_func(path+[n]),path+[n]))
	return None

#From wikipedia: https://en.wikipedia.org/wiki/Maze_generation_algorithm#Cellular_automaton_algorithms
def maze(width=81, height=51, complexity=.75, density=.75):
    numpy.random.seed(43)
    # Only odd shapes
    shape = ((height // 2) * 2 + 1, (width // 2) * 2 + 1)
    # Adjust complexity and density relative to maze size
    complexity = int(complexity * (5 * (shape[0] + shape[1]))) # number of components
    density    = int(density * ((shape[0] // 2) * (shape[1] // 2))) # size of components
    # Build actual maze
    Z = numpy.zeros(shape, dtype=bool)
    # Fill borders
    Z[0, :] = Z[-1, :] = 1
    Z[:, 0] = Z[:, -1] = 1
    # Make aisles
    for i in range(density):
        x, y = rand(0, shape[1] // 2) * 2, rand(0, shape[0] // 2) * 2 # pick a random position
        Z[y, x] = 1
        for j in range(complexity):
            neighbours = []
            if x > 1:             neighbours.append((y, x - 2))
            if x < shape[1] - 2:  neighbours.append((y, x + 2))
            if y > 1:             neighbours.append((y - 2, x))
            if y < shape[0] - 2:  neighbours.append((y + 2, x))
            if len(neighbours):
                y_,x_ = neighbours[rand(0, len(neighbours) - 1)]
                if Z[y_, x_] == 0:
                    Z[y_, x_] = 1
                    Z[y_ + (y - y_) // 2, x_ + (x - x_) // 2] = 1
                    x, y = x_, y_
    return Z


def add_tup(tup1,tup2):
	x1,y1=tup1
	x2,y2=tup2
	return (x1+x2,y1+y2)

#Turns a binary 2d array into a dictionary representing edges in a graph
#Actually a bit broken
def bin2graph(bin_map):
	graph={}
	for x in range(bin_map.shape[1]-1):
		for y in range(bin_map.shape[0]-1):
			if not bin_map[y,x]:
				graph[(x,y)]=set()
				for direction in [(0,1),(1,0),(0,-1),(-1,0)]:
					nx,ny= add_tup((x,y),direction)
					if nx>=0 and nx<bin_map.shape[1]-1 and ny>=0 and ny<bin_map.shape[0]-1 and not bin_map[ny,nx]:
						graph[(x,y)].add((nx,ny))
	return graph

#Very unoptimized code to double check my graph creation function
#May or may not flip the y axis by accident
def graph_check(graph,path=None):
	for key,value in graph.items():
		x,y=key
		pyplot.plot(x,y,'ro')
		for edge in value:
			nx,ny=edge
			pyplot.plot([x,(x+nx)/2],[y,(y+ny)/2],'k-')

	if(path):
		xs,ys=zip(*path)
		pyplot.plot(xs,ys,'b-')

	pyplot.show()

def map_check(bin_map,path):
	pyplot.figure(figsize=(10, 5))
	pyplot.imshow(bin_map, cmap=pyplot.cm.binary, interpolation='nearest')
	xs,ys=zip(*path)
	pyplot.plot(xs,ys,'k-')
	pyplot.xticks([]), pyplot.yticks([])
	pyplot.show()


if __name__=="__main__":
	#TEST 1
	# print(BFS(graph1(),'A','I'))
	
	#TEST 2
	# print(Dijkstra(graph2(),'A','I'))

	#TEST 3
	# bin_map,graph3=graph3()
	# path=ManhattanAStar(graph3,(2,2),(40,40))
	# map_check(bin_map,path)

	#Test 4 
	path=MapAStar(graph4(),(12,2),(9,12))
	graph_check(graph4(),path)


