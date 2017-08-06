import pprint

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

	def gen_puzz2():
		o=3.5
		lay=  [[o,o,o],
			   [3,8,4],
			   [5,8,2],
			   [o,o,o]]
		new_puzz=Chunk(3,4)
		for y,line in enumerate(reversed(lay)):
			for x,point in enumerate(line):
				new_puzz.tiles[(x,y)]=Tile(x,y,point)
		return new_puzz

	def up(self,tile):
		try:
			return self.tiles[(tile.x,tile.y+1)]
		except:
			return None

	def down(self,tile):
		try:
			return self.tiles[(tile.x,tile.y-1)]
		except:
			return None

	def left(self,tile):
		try:
			return self.tiles[(tile.x-1,tile.y)]
		except:
			return None

	def right(self,tile):
		try:
			return self.tiles[(tile.x+1,tile.y)]
		except:
			return None

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

	def value(self):
		return self.tile.val

	def __str__(self):
		return self.name+":"+"("+str(self.tile.x)+","+str(self.tile.y)+")"

	def __repr__(self):
		return self.__str__()

class State(object):
	def __init__(self,agents,chunk,prior_history):
		self.agents=sorted(agents,key=lambda x:x.name)
		self.chunk=chunk
		temp=prior_history[:]
		temp.append(self.agent_pos())
		self.history=temp

	def gen_puzz():
		chunk=Chunk.gen_puzz()
		agent1=Agent("A",chunk.tiles[(1,0)])
		agent2=Agent("B",chunk.tiles[(4,0)])
		return State([agent1,agent2],chunk,[])

	def gen_puzz2():
		chunk=Chunk.gen_puzz2()
		agent1=Agent("A",chunk.tiles[(0,0)])
		agent2=Agent("B",chunk.tiles[(2,0)])
		return State([agent1,agent2],chunk,[])

	def is_solved(self):
		solved=True
		for agent in self.agents:
			solved=solved and (agent.tile.y==self.chunk.sizeY-1)
		return solved

	def agent_pos(self):
		if self.agents==None:
			return "?"
		agents_str=""
		for i,agent in enumerate(self.agents):
			agents_str+=str(agent)+("" if i==(len(self.agents)-1) else ",")
		return agents_str
		# return ((self.agents[0].tile.x,self.agents[0].tile.y),(self.agents[1].tile.x,self.agents[1].tile.y))

	def is_agent_crash(self):
		for agent in self.agents:
			for other_agent in self.agents:
				if agent==other_agent:
					continue
				elif agent.crash(other_agent):
					return True
		return False

	def is_numerically_valid(self):
		running_sum=0
		for agent in self.agents:
			running_sum+=agent.value()
		return running_sum==7

	def new_state_on_move(self,agent,move):
		new_pos=move(agent.tile)
		if new_pos==None:
			return None
		# 	return None #illegal move
		new_agent=Agent(agent.name,new_pos)

		other_agents=self.agents[:] #copy list
		other_agents.remove(agent)
		new_agents=[new_agent]
		new_agents.extend(other_agents)
		return State(new_agents,self.chunk,self.history)

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
		over_str+=str(self.history)+"\n"
		return over_str

	def __repr__ (self):
		# return self.__str__()
		return str("<state>"+self.agent_pos())+", "+str(self.history)+" </state>"

class Solver(object):
	states=[]
	seen=set()
	def __init__(self,initial_state):
		self.states.append(initial_state)
		self.seen.add(initial_state)

	def is_seen_state(self,state):
		return state.agent_pos in self.seen

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
		return new_states

	def turn(self,seed_state):
		agents_to_go=seed_state.agents[:]
		states_to_go=[seed_state]
		while len(agents_to_go)>0:
			cur_agent=agents_to_go.pop(0)
			states_to_go_for_agent=states_to_go[:]
			new_states_to_go=[]
			while len(states_to_go_for_agent)>0:
				cur_state=states_to_go_for_agent.pop(0)
				new_states=Solver.new_states_from_one_agent(cur_state,cur_agent)
				# print("considering agent:"+str(cur_agent)+" for state:\n"+str(cur_state)+" makes "+str(new_states))
				new_states_to_go.extend(new_states)
			states_to_go=new_states_to_go
		return states_to_go

	def solve(self):
		while len(self.states)>0:
			cur_state=self.states.pop(0)
			if cur_state.is_solved():
				return cur_state
			elif cur_state.is_agent_crash():
				continue
			elif not cur_state.is_numerically_valid():
				continue
			elif self.is_seen_state(cur_state):
				continue
			else:
				#if we get here, its a valid, non-goal state
				self.seen.add(cur_state.agent_pos)
				self.states.extend(self.turn(cur_state))
		return None

# left left
# left right
# left up
# left sit
# right left
# right right
# right up
# right sit
# up left
# up right
# up up
# up sit
# sit left
# sit right
# sit up
# sit sit 


pp = pprint.PrettyPrinter(indent=4)
solver=Solver(State.gen_puzz())
print(solver.states[0])
# pp.pprint(solver.turn(solver.states[0]))
print(solver.solve())
# a=Chunk(4,4)
# print(a)
# print(a.down(a.right(a.right(a.tiles[(1,2)]))))