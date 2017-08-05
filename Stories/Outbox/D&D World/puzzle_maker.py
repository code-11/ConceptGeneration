class Tile(object):
	x=None
	y=None
	val=None
	def __init__(self,x,y,val):
		self.x=x
		self.y=y
		self.val=val

	def __str__(self):
		if self.val==3.5:
			return "o"
		else:
			return str(self.val)

class Chunk(object):
	tiles={}
	sizeX=0
	sizeY=0

	def __init__(self,sizeX,sizeY):
		for x in range(sizeX):
			for y in range(sizeY):
				self.tiles[(x,y)]=Tile(x,y,0)
		self.sizeX=sizeX
		self.sizeY=sizeY

	def gen_puzz():
		o=3.5
		lay=  [[o,o,o,o,o,o,o],
			   [4,5,6,1,8,8,8],
			   [5,0,1,8,8,8,8],
			   [8,8,2,7,6,8,8],
			   [8,3,3,8,5,4,8],
			   [8,2,8,8,7,8,8],
			   [o,o,o,o,o,o,o]]
		new_puzz=Chunk(7,7)
		for y,line in enumerate(reversed(lay)):
			for x,point in enumerate(line):
				new_puzz.tiles[(x,y)]=Tile(x,y,point)
		return new_puzz

	def up(self,tile):
		return self.tiles[(tile.x,tile.y+1)]

	def down(self,tile):
		return self.tiles[(tile.x,tile.y-1)]

	def left(self,tile):
		return self.tiles[(tile.x-1,tile.y)]

	def right(self,tile):
		return self.tiles[(tile.x+1,tile.y)]

	def __str__(self):
		over_str=""
		for y in reversed(range(self.sizeY)):
			line_str=""
			for x in range(self.sizeX):
				line_str+=str(self.tiles[(x,y)])
			over_str+=line_str+"\n"
		return over_str

class Agent(object):
	tile=None
	name=""
	def __init__(self,name,tile):
		self.tile=tile
		self.name=name

	def crash(self,agent):
		return agent.tile==self.tile

class State(object):
	def __init__(self,agents,chunk):
		self.agents=agents
		self.chunk=chunk

	def gen_puzz():
		chunk=Chunk.gen_puzz()
		agent1=Agent("A",chunk.tiles[(1,0)])
		agent2=Agent("B",chunk.tiles[(4,0)])
		return State([agent1,agent2],chunk)

	def is_solved(self):
		solved=True
		for agent in self.agents:
			solved=solved and (agent.tile.y==self.chunk.sizeY-1)
		return solved

	def agent_pos(self):
		if self.agents==None:
			return "?"
		return ((self.agents[0].tile.x,self.agents[0].tile.y),(self.agents[1].tile.x,self.agents[1].tile.y))

	def new_state_on_move(self,agent,move):
		try:
			new_pos=move(agent.tile)
		except KeyError as e:
			return None #illegal move
		new_agent=Agent(agent.name,new_pos)
		other_agents=self.agents[:] #copy list
		other_agents.remove(agent)
		return State([new_agent].extend(other_agents),self.chunk)

	def new_state_on_up(self,agent):
		return self.new_state_on_move(agent,self.chunk.up)

	def new_state_on_down(self,agent):
		return self.new_state_on_move(agent,self.chunk.down)

	def new_state_on_left(self,agent):
		return self.new_state_on_move(agent,self.chunk.left)

	def new_state_on_right(self,agent):
		return self.new_state_on_move(agent,self.chunk.right)

	def new_state_on_sit(self,agent):
		return self.new_state_on_move(agent,lambda x: x)

	def agent_str_at_pos(self,tile):
		for agent in self.agents:
			if agent.tile==tile:
				return agent.name+" "
		return "  "

	def __str__(self):
		over_str=""
		for y in reversed(range(self.chunk.sizeY)):
			line_str=""
			for x in range(self.chunk.sizeX):
				tile=self.chunk.tiles[(x,y)]
				line_str+=(str(tile)+self.agent_str_at_pos(tile))
			over_str+=line_str+"\n"
		return over_str

	def __repr__ (self):
		return self.agent_pos()

class Solver(object):
	states=[]
	history=[]
	def __init__(self,initial_state):
		self.states.append(initial_state)
		self.history.append(initial_state)

	def new_states_from_one_agent(cur_state,agent):
		new_states=[]
		new_up_state=cur_state.new_state_on_up(agent)
		new_down_state=cur_state.new_state_on_down(agent)
		new_left_state=cur_state.new_state_on_left(agent)
		new_right_state=cur_state.new_state_on_right(agent)
		new_sit_state=cur_state.new_state_on_sit(agent)
		if new_up_state!=None:
			new_states.append(new_up_state)

		if new_down_state!=None:
			new_states.append(new_down_state)

		if new_left_state!=None:
			new_states.append(new_left_state)

		if new_right_state!=None:
			new_states.append(new_right_state)
		
		if new_sit_state!=None:
			new_states.append(new_sit_state)
		print(new_states)

	# def 

	# def solve(self):
	# 	while len(self.states)>0:
	# 		#check rules on collision and 7 here as well as end state
	# 		seed_state=states.pop(0)
	# 		cur_states=[seed_state]
	# 		while len(cur_states)>0:
	# 			cur_state=cur_states.pop(0)
	# 			while len(cur_state.agents)>0:
	# 				cur_agent=cur_state.agents.pop(0)





solver=Solver(State.gen_puzz())
Solver.new_states_from_one_agent(solver.states[0],solver.states[0].agents[0])
# a=Chunk(4,4)
# print(a)
# print(a.down(a.right(a.right(a.tiles[(1,2)]))))