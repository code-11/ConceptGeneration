class Tile(object):
	x=None
	y=None
	val=None
	def __init__(self,x,y,val):
		self.x=x
		self.y=y
		self.val=val

	def __str__(self):
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
		lay=  [[4,5,6,1,8,8,8],
			   [5,0,1,8,8,8,8],
			   [8,8,2,7,6,8,8],
			   [8,3,3,8,5,4,8],
			   [8,2,8,8,7,8,8]]
		new_puzz=Chunk(7,5)
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
print(Chunk.gen_puzz())
# a=Chunk(4,4)
# print(a)
# print(a.down(a.right(a.right(a.tiles[(1,2)]))))