############################################################################################################################################
#1. Formulation of problem:
#
#       a) Formulation of the search problem: 
#
#               State-Space representation: For this problem-set, we created a graph which comprises a dictionary containing key-value pairs #               of city names and city objects. Each city object has the properties: city name, co-ordinates and a dictionary of child-cities.
#               Each child-city dictionary has the key as the name of the child-city and values comprise a list of distance, speed-limit and #               highway name.
# 
#               Algorithm implementation: For BFS and DFS, we have used a queue and stack datastructure respectively. For A-star, we are #               using dictionaries for priority queues. For all algorithms, we are using dictionaries to store the paths travesed and time #               required for all paths and distance covered with each path  
#
#       b) State Space: The state space is represented by a the total number of cities provided in the input files
#
#       c) Successor Function: Successor function is the action of moving from a city (object) to any of its child nodes (other city object).
#          Successor function chooses the next state basis the routing algorithm being implemented
#
#       d) Edge Weights: For A-Star, the edge weights can be the distance between consecutive cities, or the time required to travel or can be #          uniform if number of edges are to be considered
#  
#       e) Heuristic Function: Here, we have chosen Euclidean distance as our heuristic function. We found it to yield more accurate results 
#          as compared to manhattan distance. 
#
#       f) Heuristic Admissibility: Euclidean distance, is the shortest path from the start state to the goal state (straight line).
#          Therefore, it will always be equal or less than the optimal path cost. Therefore, it is an admissible heuristic 
#
#2. Assumptions/Design Decisions:        
#
#       a. For junctions, since co-ordinates are not present, we are using the heuristic for the parent city
#       b. Traversing consecutive junctions is made possible
#	c. Junction nodes cannot be goal-states since they do not have co-ordinates
#       d. Travelling on edges with null speed limits is de-incentivized using a greater heuristic for these paths 
#       e. For A-Star, dictionary is used for a priority queue
#       f. For maintaining path costs and time costs which are required for A-Star, dictionaries are used where the key being used
#          is a string comprising the actual path
#           
#3. Analysis of results: 
#
# 	a) Best algorithm for routing options:
#		A-star is the best algorithm for routing, generally it peforms far better than BFS and DFS. In terms of computation time
#               over longer distances, the # performance of A-star is acceptable as both BFS and DFS will take a very long time. BFS will     
#               outperform A-Star only over very short distances. Performance of DFS is acceptable only in case the goal-node is 
#               very close to the start-node.  
#         		
#       b) Fastest in terms of computing time and how much:
#               For shorter distances,BFS is faster than A-Star. BFS runs 2-3 times as fast for cities up to two nodes away. But as we increase
#               the distance to goal cities, time performance of A-Star increases exponentially relative to BFS. DFS behaves similar to BFS  #               but only for goal nodes that are very close to the starting node both alphabetically and in terms of node depth. For a #               goal-state at a greater depth, DFS will return a faster result only if it is alphabetically sorted. 
#               
#               Find a snapshot of the average times for computation required here:
#                    Bloomington-Cincinnati:   0.00034 sec(A-Star_dist) | 0.00010 sec(BFS) |  0.0001 sec(DFS) 
#                    Bloomington-Cloverdale:   0.00090 sec(A-Star_dist) | 0.00044 sec(BFS) |  (lot of time)(DFS)
#                    Bloomington-Indianapolis: 0.0012  sec(A-Star_dist) | 0.00047 sec(BFS) |  (lot of time)(DFS)
#                    Bloomington-Chicago:      0.24    sec(A-Star_dist) | (1min +)(BFS)    |  (lot of time)(DFS)
#		     Bloomington-Seattle:      4.12    sec(A-Star_dist) | (1min +)(BFS)    |  (lot of time)(DFS)
#
#       c) Hueristic function used and how to make it better:
#               Heuristic being used here is the Euclidean distance. We preferred it over Manhattan distance since it yielded more accuracy.  
#               We think that since this heuristic is admissible and is suitable to the graph search being performed it is quite optimal.      
#               One way of improving the heuristic can be including the element of orthogonality over greater distances like San-Diego to 
#               Nova Scotia. So, the heuristic of a Great-Circle Distance may be used in case of larger distances while Euclidean distance is #               used over shorter ones. 
	
#################################################################################################################################################
import sys
import algo1
import algo2
from algo2 import Graph
from algo2 import Vert

class Route:
	
	def start(self,argv):
		if len(argv) > 5:
			print "too many arguments!"
			return
		if len(argv)>=2:
			startCity=sys.argv[1]
			endCity=sys.argv[2]
			g=Graph()
			gr=g.getGraph()
		if "bfs" or "dfs" or "astar" in sys.argv[3]:
			routingAlgo=sys.argv[3]
		if len(sys.argv)==5:
			routingOption=sys.argv[3]
			routingAlgo=sys.argv[4]
		if routingAlgo.lower()=="bfs":
			print(route.BFS(startCity,endCity,gr))
		elif routingAlgo.lower()=="dfs":
			print(route.DFS(startCity,endCity,gr))
		elif routingAlgo.lower()=="astar":
			metric=''
			if routingOption == "segments":
				metric='e'
			elif routingOption == "distance":
				metric='d'
			elif routingOption == "time":
				metric='t'
			else:
				print "Wrong routing-option provided"
				return
			print(route.ASTAR(startCity,endCity,metric,gr))
		else:
			print "Wrong Algorithm!"
			return
			
	def BFS(self,start,end,gr):
		pathFound=algo1.BFS(gr,start,end)
		return route.ShowResult(pathFound)
		 
	def DFS(self,start,end,gr):
		pathFound=algo1.DFS(gr,start,end)
		return route.ShowResult(pathFound)

	def ASTAR(self,start,end,metric,gr):
		if start not in gr.vrtlst:
			return "Invalid start city name"
		if end not in gr.vrtlst:
			return "Invalid destination or destination has no coordinates"

		result={}
		result=algo2.AStar(gr,start,end,metric)
		cty_lst = result['path'].split(' ')
		pathl=[]
		for c in cty_lst:
			pathl.append(c)
		completePath = route.GetPathWithHighwayName(cty_lst,gr)
		for i in completePath:
			pathl.append(i)
		if metric == 'e':
			print "No Of edges are: ",result['noOfEdges'] 
		return route.ShowResult(pathl)
		
	def GetPathWithHighwayName(self,path,g):
		i=0
		totalDistance=0
		totalTime=0
		distanceAndTime=[]
		pathWithHighway=""
		highway=""
		distance=""
		time= ""
		for p in range(len(path)):
			#print "Path:",path[p]
			city=path[p]
			node_stateobj = g.getVrts(path[p])
			if len(path)-1>p and path[p+1] in sorted(node_stateobj.nxtcty):
				highway= node_stateobj.nxtcty[path[p+1]][2] 
				pathWithHighway=pathWithHighway + ' ' + city+'~'+time+'~'+distance+' '+highway
				if float(node_stateobj.nxtcty[path[p+1]][1]) == 0.0:
					node_stateobj.nxtcty[path[p+1]][1]=1.0
				time=str(float(node_stateobj.nxtcty[path[p+1]][0])/float(node_stateobj.nxtcty[path[p+1]][1]))

				distance=str(float(node_stateobj.nxtcty[path[p+1]][0]))
				totalDistance = totalDistance + float(node_stateobj.nxtcty[path[p+1]][0])
				totalTime = totalTime + float(time)
		pathWithHighway=pathWithHighway +' '+ path[p]+'~'+time+'~'+distance
		distanceAndTime= [totalDistance,totalTime, pathWithHighway]
		
		return distanceAndTime
	
	def ShowResult(self, pathFound):
		finalPath=""
		pathAndTime=[]
		if len(pathFound)>0:

			completepath= pathFound[len(pathFound)-1].split()
			pathAndTime=completepath[0].split('~')
			direction = '\nFrom '+ pathAndTime[0]+', '
			for p in range(1,len(completepath)-1):
				if p%2 != 0:
					direction = direction +'Take '+ completepath[p] 
				else:
					pathAndTime=completepath[p].split('~')
					x=pathAndTime[1]
					direction = direction + ' To: '+ pathAndTime[0] + '\n' + 'Distance:'+ pathAndTime[2]+' | ' + 'Estimated Time:'+x[:5]+' hrs'+ ',\n'
 			
 			x=str(pathFound[len(pathFound)-2])
			print direction + "\nYay! You reached " + completepath[p+1].split('~')[0] + ' | '+ 'Total time:' + x[:5] + ' hrs'+' | '+'Total Distance:'+ str(pathFound[len(pathFound)-3]) + '\n\n'
		
			for path in pathFound[0:len(pathFound)-3]:
				finalPath = finalPath + ' ' + path + ' '
		else: 
			finalPath='No path found!'
		return str(pathFound[len(pathFound)-3]) + ' ' + str(pathFound[len(pathFound)-2]) + finalPath
				
			
		


route=Route()
route.start(sys.argv)

