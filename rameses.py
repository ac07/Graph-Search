## APPROACH/FORMULATION:
## To solve Ramses, we are employing Alpha Beta Pruning with MiniMax algorithm. On the basis of the experiments run, we found out
## that roughly, 80-85% time was consumed in exploring the state space on the basis of the provided input. Therefore, for implementing
## the time limit, we attribute 80% of the total time for generating state-space. Thus the depth being explored is contingent on the
## given time.
## SUCCESSOR FUNCTION:
## Here, the successor function is determines the next move which is the potential location of the next pebble.
## HEURISTIC:
## The evaluation function being used here quantifies the possibility of terminal states after each move. States which lead towards
## terminal states have a higher cost. 



import sys
import sched, time
import numpy
import datetime
from numpy import matrix
from sys import maxsize
import Queue


class Node(object):
	def __init__(self,initialState):
		self.state = initialState
		self.terminal = False
		self.childNodes	= []

	def CreateChildNodes(self,q,giventime):
		count=1
		player = 2#consider second level as a player 2
		totalcount=0
		st = datetime.datetime.now()
		depth = 0
		
		while float((datetime.datetime.now()-st).total_seconds()*1000) <= giventime and not q.empty() and count != 0 :
			initialState = q.get()
			if not initialState.terminal:
				nextMove = numpy.where(numpy.asarray(initialState.state) == 0)
				for i in range(len(nextMove[0])):
					newState = matrix(initialState.state)
					newState[nextMove[0][i],nextMove[1][i]] = player
		 			node = Node(newState)
		 			a = numpy.asarray(node.state)
		 			#Check for terminal state
					if  0 not in a[nextMove[0][i]] or 0 not in a[:,[nextMove[1][i]]] or 0 not in numpy.diag(a) or 0 not in numpy.diag(numpy.fliplr(a)) :
						node.terminal = True 
					q.put(node)
		 			initialState.childNodes.append(node)
				count = count -1
				totalcount = totalcount + len(initialState.childNodes)
				#change player as per depth level
				if count == 0:
					if player == 1:
						player = 2
					else:
						player = 1
					count = totalcount
					totalcount=0
					depth = depth+1
		
	
#Evaluate possible terminal states for both players by assigning waitage to different sequences.
#Get heuristic of maximum empty places and higher waitage of win.
def EvaluationFunc(node,player):
	count = 0
	pl1Count = 0
	pl2Count = 0
	sizeOfMatrix = len(node.state)
	a = numpy.asarray(node.state)
	if node.terminal and player == 2:
		return 0

	for i in range(sizeOfMatrix-1):
		#Check diagonals
		if sum(numpy.diag(a) == 1) == i+1 and 2 not in numpy.diag(a) :
			pl1Count = i+1 + pl1Count
		if sum(numpy.diag(numpy.fliplr(a))  == 1) == i+1 and 2 not in numpy.diag(numpy.fliplr(a))  :
			pl1Count = i+1 + pl1Count
		if sum(numpy.diag(a) == 2) == i+1 and 1 not in numpy.diag(a) :
			pl2Count = i+1 + pl2Count
		if sum(numpy.diag(numpy.fliplr(a))  == 2) == i+1 and 2 not in numpy.diag(numpy.fliplr(a))  :
			pl2Count = i+1 + pl2Count
		#check rows and columns
		if sum(a[i] == 1) == i+1 and 2 not in a[i]:
			pl1Count = i+1 + pl1Count
		if sum(a[i] == 2) == i+1 and 1 not in a[i]:
			pl2Count = i+1 + pl1Count
		if sum(a[:,[i]] == 1) == i+1 and 2 not in a[:,[i]]:
			pl1Count = i+1 + pl1Count
		if sum(a[:,[i]] == 2) == i+1 and 1 not in a[:,[i]]:
			pl2Count = i+1 + pl2Count

	return pl1Count - pl2Count

#MiniMax with Alpha-Beta pruning 
def miniMax(node,depth,alpha,beta,player):
	if depth == 0 or node.terminal :
		return EvaluationFunc(node,player)
	if player == 1:
		bestValue1 = -maxsize
		for node in node.childNodes:
			bestValue1 = max(bestValue1	,miniMax(node,depth-1,alpha,beta,2))
			if node.terminal == False:
				if bestValue1 in nodeDict:
					del nodeDict[bestValue1]
				nodeDict[bestValue1]=node.state
			alpha = max(alpha,bestValue1)
			if beta <= alpha:
				break
		return bestValue1
	else:
		bestValue2 = maxsize
		for node in node.childNodes:
			bestValue2 = min(bestValue2,miniMax(node,depth-1,alpha,beta,1))
			if node.terminal == False:
				if bestValue2 in nodeDict:
					del nodeDict[bestValue2]
				nodeDict[bestValue2]=node.state
			beta = min(beta,bestValue2)
			if beta <= alpha:
				break
		return bestValue2

def ramses(boardSize,boardState,givenTime):
	go = datetime.datetime.now()
	givenTime  = float(givenTime) * 1000
	t = float(givenTime) * 0.1
	totalTime = float(givenTime) - (float(givenTime) * 0.1)
	timeForTree = totalTime - (float(totalTime) * 0.2)
	
	boardState = boardState.replace("x","1")
	boardState = boardState.replace(".","0")
	size = int(boardSize)
	boardState = ";".join(boardState[i:i+size] for i in range(0,len(boardState),size))
	boardState = " ".join(boardState[i] for i in range(0,len(boardState),1))
	initialState = matrix(boardState).reshape(size,size)
		
	print "Wait!Let me think...."
	node = Node(initialState)
	q = Queue.Queue()
	q.put(node)
	node.CreateChildNodes(q,timeForTree)																																																																																																																																																																																																																																																																																																																  
	d = miniMax(node,4,-maxsize,maxsize,1 )
	if not nodeDict:
		print "No place for yor pebble.You lost!"
	else:	
		nextMove = numpy.where(numpy.asarray(nodeDict[d]) == 2)
		print "Here you go! place your pebble at row",nextMove[0][0] + 1,", column",nextMove[1][0] + 1,"."
		print "New board:"
		s = ""
		initialState[nextMove[0][0],nextMove[1][0]]=2
		for i in numpy.asarray(initialState):
			s = s + str(i).replace('1','x').replace('2','x').replace('0','.').replace(" ","").replace('[','').replace(']','')
		print s,
	

nodeDict={}
ramses(sys.argv[1],sys.argv[2],sys.argv[3]) 