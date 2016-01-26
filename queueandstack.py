class PriorityQueue:
	
	def __init__(self):
		self.items = []
		
	def enqueue(self,val):
		self.items.append(val)
		#self.items.insert(0,val)
		#print "Q: ",self.items
		
	def dequeue(self):
		val = None
		val = self.items[0]
		if len(self.items) == 1:
			self.items = []
		else:
			self.items = self.items[1:]	
		return val	
	def peek(self):
		return self.items[0]
		
	def IsEmpty(self):
		return self.items==[]

class PriorityStack:
	def __init__(self):
		self.items=[]
	def isEmpty(self):
		return self.items==[]
	def push(self,item):
		self.items.append(item)
	def pop(self):
		return self.items.pop()
	def peek(self):
		return self.items[len(self.items)-1]
	def size(self):
		return len(self.items)

