from queueandstack import PriorityQueue
from queueandstack import PriorityStack
import time

def BFS(graph,start,end):
	#go = time.time()
	q = PriorityQueue()
	trackPath = [start]
	q.enqueue(trackPath)
	while q.IsEmpty() == False:
		trackPath = q.dequeue()
		node_sate = trackPath[len(trackPath)-1]
		if node_sate == end:
			trackPath = trackPath + CalculateTimeAndDistance(trackPath,graph)
			#print "Time for BFS:",time.time() - go
			return trackPath
		node_stateobj = graph.getVrts(node_sate)	
	
		for node in sorted(node_stateobj.nxtcty):
			if node not in trackPath:
				newEdges = []
				newEdges = trackPath + [node]
				q.enqueue(newEdges)
	
	return trackPath
	
def DFS(graph,start,end):
	#go = time.time()
	s= PriorityStack()
	trackPath = [start]
	visited=[start]
	s.push(trackPath)

	while s.isEmpty() == False:
		trackPath = s.pop()
		node_state = trackPath[len(trackPath)-1]
		if node_state == end:
			trackPath = trackPath + CalculateTimeAndDistance(trackPath,graph)
			#print "Time for BFS:",time.time() - go
			return trackPath
		node_stateobj = graph.getVrts(node_state)	
		nodeList=[]
		for node in sorted(node_stateobj.nxtcty):
			if node not in trackPath:
				newEdges = []
				newEdges = trackPath + [node]
				nodeList.insert(0,newEdges)
		for n in nodeList:
			s.push(n)
	#print "Time for DFS:",time.time() - go	
	return trackPath

def CalculateTimeAndDistance(path,g):
	i=0
	totalDistance=0
	totalTime=0
	distanceAndTime=[]
	pathWithHighway=""
	highway=""
	distance=""
	time= ""
	for p in range(len(sorted(path))):
		city=path[p]
		node_stateobj = g.getVrts(path[p])
		if len(path)-1>p and path[p+1] in sorted(node_stateobj.nxtcty):
			highway= node_stateobj.nxtcty[path[p+1]][2] 
			
			pathWithHighway=pathWithHighway + ' ' + city+'~'+time+'~'+distance+' '+highway
			time=str(float(node_stateobj.nxtcty[path[p+1]][0])/float(node_stateobj.nxtcty[path[p+1]][1]))
			distance=str(float(node_stateobj.nxtcty[path[p+1]][0]))
			totalDistance = totalDistance + float(node_stateobj.nxtcty[path[p+1]][0])
			totalTime = totalTime + float(time)#float(node_stateobj.nxtcty[path[p+1]][0])/float(node_stateobj.nxtcty[path[p+1]][1])
	pathWithHighway=pathWithHighway +' '+ path[p]+'~'+time+'~'+distance
	distanceAndTime=[totalDistance,totalTime,pathWithHighway]

	return distanceAndTime

