import math
import time
class Vert:

    def __init__(self, key):
        self.key = key
        self.spatial = []
        self.nxtcty = {}

    def addSpatial(self,spatial):
        self.spatial = spatial

    def addNxt(self, cty, cst, spdlmt, hghwy):
        self.nxtcty[cty] = [cst, spdlmt, hghwy]

    def __str__(self):
	for x in self.nxtcty:
        	return str(self.key) + str(self.spatial) + str([x.key for x in self.nxtcty])

    def getNcty(self):
        return self.nxtcty.keys()

    def getNctyObj(self):
        return self.nxtcty

    def getCcty(self):
        return self.key

    def getSpatial(self):
        return self.spatial

#Graph creates a dictionary of all city nodes. Key-> city name(str), Value-> city Object

class Graph:

    def __init__(self):
        self.vrtlst = {}
        self.numvrts = 0

    def addVrts(self, key):
        nvrt = Vert(key)
        self.vrtlst[key] = nvrt
        self.numvrts += 1
        return nvrt

    def getVrts(self,key):
	
        if key in self.vrtlst:
            return self.vrtlst[key]
        else:
            return None

    def __contains__(self,key):
	return key in self.vrtlst

    def addncty(self, f, t, cst, spdlmt, hghwy):
        if f not in self.vrtlst:
            fvrt = self.addVrts(f)
        if t not in self.vrtlst:
            tvrt =  self.addVrts(t)
        self.vrtlst[f].addNxt(self.vrtlst[t], cst, spdlmt, hghwy)

    def getAVrts(self):
	return self.vrtlst.keys()
		
    def __iter__(self):
	return iter(self.vrtlst.values())
		
    def getGraph(self):
	g = Graph()

	#ParseNodes
	r  = open('city-gps.txt', 'r')
	for line in r:
	    l = line.split()
	    if l[0]:
		x = g.addVrts(l[0])
	    if l[1] and l[2]:
		y = [l[1],l[2]]
		x.addSpatial(y)
	r.close()

	#ParseEdges
	r  = open('road-segments.txt', 'r')
	for line in r:
	    #Replace blanks in raw data with '0'
	    if ('  ' in line) == True:
		line = line.replace('  ', ' 0 ')
	    #Add cities and their children, if not already present
	    l = line.split()
	    if g.getVrts(l[0]):
		x = g.getVrts(l[0])
		x.addNxt(l[1],l[2],l[3],l[4])
	    else:
		c = g.addVrts(l[0])
		c.addNxt(l[1],l[2],l[3],l[4])
	    #Point chidren to parents
	    if not g.getVrts(l[1]):
		g.addVrts(l[1])
	    z = g.getVrts(l[1])
	    if x.key in z.getNcty():
		pass
	    else:
		z.addNxt(l[0],l[2],l[3],l[4])

	r.close()
	return g
#Retreive Final Path
def txtprcss(rndmwrd):
	rndmwrd = rndmwrd.split(' ')
    	rndmwrd = rndmwrd.pop()
    	return rndmwrd


#Setting up the Graph
def AStar(g,s_node,g_node,metric):
	#																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																	go = time.time()
	#INPUT PARAMETERS
	h_prev = None
	prior_q = {} #distance priority queue
	bst_cnode = s_node  #reference index for accessing path costs
	path_c = {bst_cnode: 0}
	timepq_c = {}
	time_c = {bst_cnode: 0}
	edge_c = {}
	v_nodes = []
	g_cst = 0  #Path Costs till present node
        #s_node=g.getVrts(s_node)
	if s_node in g.vrtlst:
	    s_node = g.getVrts(s_node)
	else:
	    print "Original State not available"

	
	if g_node in g.vrtlst:
	    g_node = g.getVrts(g_node)
	
	else:
	    print "Goal State not available"
	    

	count = 1

	if s_node and g_node:

	    c_node = s_node

	    while c_node.key != g_node.key:
		if c_node.key not in v_nodes:
		    v_nodes.append(c_node.key)
		    nxtc = c_node.getNctyObj()
		    if c_node.spatial != []:
		         h_pmhtx = ( float(c_node.spatial[0]) - float(g_node.spatial[0]) )**2
                         h_pmhty = ( float(c_node.spatial[1]) - float(g_node.spatial[1]) )**2
                         h_pmht = h_pmhtx + h_pmhty
                         h_prev = math.sqrt(h_pmht)
		    else: pass
		    ccty = c_node.key
 		    dct_k = bst_cnode
                    ncty_dct = nxtc
                    #############################################################################################
		    
		    g_cst = path_c[dct_k]
	
	    	    #global h_prev
	    	    for i in ncty_dct:
			if i in v_nodes:
		    		pass
			if i not in v_nodes:
			    h_mhtn = None
			    i_node = g.getVrts(i)
			    tp_cst = 0
			    #Calculate Manhattan Distance to Goal
			    if i_node.spatial != []:
				 h_mhtx = ( float(i_node.spatial[0]) - float(g_node.spatial[0]) )**2
                		 h_mhty = ( float(i_node.spatial[1]) - float(g_node.spatial[1]) )**2
                                 h_mht = h_mhtx + h_mhty
                                 h_mhtn = math.sqrt(h_mht)
			    else:
				h_mhtn = h_prev
				if h_mhtn == None and h_prev == None:
				    h_mhtn = 1000
			    #Cost for each Child City
			    nctyspcs = ncty_dct[i]
			    p_cst = nctyspcs[0]
			    p_cst = float(p_cst)
			    tp_cst = g_cst + p_cst
			    #Update referencing index
			    i = dct_k + ' ' + i
			    #Maintain the route path
			    path_c[i] = tp_cst
			    
			    #Compute time required
			    t_cst = float(nctyspcs[1])
			    if t_cst == 0:
				h_mhtn = 1000
				t_cst = 1
			    #Compute and Maintain the Priority Queue when Distance-Cost
			    if metric == 'd':
				gp_cst = tp_cst + h_mhtn
				prior_q[i] = gp_cst
			    #Maintain the time req to arrive at each city.
			    time_c[i] = time_c[dct_k] + p_cst/t_cst
			    #Compute and Maintain the Priority Queue when Time-Cost
			    if metric == 't':
				timepq_c[i] = time_c[dct_k] + p_cst/t_cst + h_mhtn

			    #Compute and Maintain the Priority Queue when Edge-Cost
			    if metric == 'e':
				edgs_ln = i.split(' ')
				e_cst = len(edgs_ln)-1
				ef_cst = e_cst + h_mhtn
				edge_c[i] = ef_cst
			#############################################################################################

		    if metric == 'd':
		        bst_cnode = min(prior_q, key = lambda k: prior_q[k])
		        del prior_q[min(prior_q, key = lambda k: prior_q[k])]
		        c_node = txtprcss(bst_cnode)
		        c_node = g.getVrts(c_node)
		    elif metric == 't':
		        bst_cnode = min(timepq_c, key = lambda k: timepq_c[k])
		        del timepq_c[min(timepq_c, key = lambda k: timepq_c[k])]
		        c_node = txtprcss(bst_cnode)
		        c_node = g.getVrts(c_node)
		    elif metric == 'e':
		        bst_cnode = min(edge_c, key = lambda k: edge_c[k])
		        del edge_c[min(edge_c, key = lambda k: edge_c[k])]
		        c_node = txtprcss(bst_cnode)
		        c_node = g.getVrts(c_node)
		else:
		    if metric == 'd':
		        bst_cnode = min(prior_q, key = lambda k: prior_q[k])
		        del prior_q[min(prior_q, key = lambda k: prior_q[k])]
		        c_node = txtprcss(bst_cnode)
		        c_node = g.getVrts(c_node)
		    elif metric == 't':
		        bst_cnode = min(timepq_c, key = lambda k: timepq_c[k])
		        del timepq_c[min(timepq_c, key = lambda k: timepq_c[k])]
		        c_node = txtprcss(bst_cnode)
		        c_node = g.getVrts(c_node)
		    elif metric == 'e':
		        bst_cnode = min(edge_c, key = lambda k: edge_c[k])
		        del edge_c[min(edge_c, key = lambda k: edge_c[k])]
		        c_node = txtprcss(bst_cnode)
		        c_node = g.getVrts(c_node)

		count += 1

	    #OUTPUT:
            cty_lst = bst_cnode.split(' ')
	    finalOutPut={}
	    finalOutPut={'disatnce':path_c[bst_cnode],'totalTime':time_c[bst_cnode],'path':bst_cnode,'noOfEdges':len(cty_lst)-1}
	    #print "Time for Astar:",time.time() - go
	    return finalOutPut



