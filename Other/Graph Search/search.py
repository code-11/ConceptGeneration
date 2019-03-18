from queue import Queue
graph1={'A':{'B','D','F'},
	   'B':{'A','D','C','I'},
	   'C':{'B','I'},
	   'D':{'A','B','E','F'},
	   'E':{'B','D','F','G'},
	   'F':{'A','D','E','G'},
	   'G':{'F','E','H'},
	   'H':{'G','I'},
	   'I':{'B','C','H'}}

graph2={'A':{('B',4),('D',5),('F',3)},
	   'B':{('A',4),('D',2),('C',8),('I',15)},
	   'C':{('B',8),('I',4)},
	   'D':{('A',5),('B',2),('E',1),('F',1)},
	   'E':{('B',3),('D',1),('F',4),('G',2)},
	   'F':{('A',3),('D',1),('E',4),('G',6)},
	   'G':{('F',6),('E',2),('H',2)},
	   'H':{('G',2),('I',2)},
	   'I':{('B',15),('C',4),('H',2)}}   

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

def descipher_dijkstra(prev_map,goal):
	path=[goal]
	while prev_map.get(path[0]):
		path.insert(0,prev_map.get(path[0]))
	return path

if __name__=="__main__":
	# print(BFS(graph1,'A','I'))
	print(Dijkstra(graph2,'A','I'))
