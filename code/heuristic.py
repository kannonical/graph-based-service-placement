import networkx as nx
import random
from itertools import islice
from networkx.classes.function import path_weight
import matplotlib.pyplot as plt

def find_all_paths(graph, start, end, path=[]):
	path = path + [start]
	if start == end:
		return [path]
	if start not in graph:
                print("Start node not in graph")
                return []
	paths = []
	for node in graph[start]:
		if node not in path:
			newpaths = find_all_paths(graph, node, end, path)
			for newpath in newpaths:
				paths.append(newpath)
#	print paths
	return paths 

#def min_path(graph, start, end):
#    paths=find_all_paths(graph,start,end)
#    mt=10**99
#    mpath=[]
#    print '\tAll paths:',paths
#    for path in paths:
#        t=sum(graph[i][j] for i,j in zip(path,path[1::]))
#        print '\t\tevaluating:',path, t
#        if t<mt: 
#            mt=t
#            mpath=path

#    e1=' '.join('{}->{}:{}'.format(i,j,graph[i][j]) for i,j in zip(mpath,mpath[1::]))
#    e2=str(sum(graph[i][j] for i,j in zip(mpath,mpath[1::])))
#    print 'Best path: '+e1+'   Total: '+e2+'\n'  


#paths = find_all_paths(graph,'D1','C2')
#print paths
	

if __name__ == "__main__":
    graph = nx.barabasi_albert_graph(10,5)
    graph.nodes[0]['compute'] = 150
    graph.nodes[1]['compute'] = 500
    graph.nodes[2]['compute'] = 100
    graph.nodes[3]['compute'] = 250
    graph.nodes[4]['compute'] = 200
    graph.nodes[5]['compute'] = 350      
    graph.nodes[6]['compute'] = 400
    graph.nodes[7]['compute'] = 300
    graph.nodes[8]['compute'] = 450
    graph.nodes[9]['compute'] = 550

# setting edge weights to all the graph edges, in our case it is joint CCP of the edges (which is multiples of node CCPs)
for s,t in graph.edges():
	graph[s][t]['weight'] = random.random()
#        graph[s][t]['weight'] = 
#	graph = {'D1': {'D2':1, 'C1':1},
#             'D2': {'C2':10, 'D1':1},
#             'C1': {'C2':1, 'B1':1, 'D1':1},
#             'C2': {'D2':1, 'C1':1, 'B2':1},
#             'B1': {'C1':1, 'B2':1},
#             'B2': {'B1':1, 'A2':1, 'C2':1},
#             'A2': {'B2':1, 'A1':1},
#             'A1': {'A2':1}}
##	min_path(graph,'D1','A1')
#paths = find_all_paths(graph,start,end)
#print paths
end_node = 2
paths = find_all_paths(graph,1,end_node)
def k_shortest_paths(graph,start, end, k,weight=None):
	return list(islice(nx.shortest_simple_paths(graph,start,end,weight='weight'),k))

#printing only those paths whose weight is greater than a value 
path_store=[]

# the greater than 1 is to ensure that all paths with much lesser CCP are not considered

for path in k_shortest_paths(graph,1,2,6):
	if path_weight(graph,path,weight="weight") > 1:
		print(path,path_weight(graph,path,weight="weight"))
	path_store = path_weight(graph,path,weight="weight")
#min = path_store.sort()
#print(min[0])
##print(paths)

# attempt to find larget path!
largest_path = None
largest_path_weight= 0

for p in paths:
	for _ in range(len(p)):
		pairs = zip(p,p[1:])
		product = 1
		for pair in pairs:
			an_edge = graph.get_edge_data(pair[0], pair[1])
			
			product *= an_edge['weight']
	if product > largest_path_weight:
		largest_path = p
		largest_path_weight = product

#display
print("largest path", largest_path)
print("weight", largest_path_weight)

for s,t in graph.edges():
        graph[s][t]['weight'] = random.randint(10,100)



service_graph = nx.Graph()
service_graph.add_edges_from([(0,1),(1,2),(2,3)])
service_graph.add_node(0, compute_requirement=20)
service_graph.add_node(1, compute_requirement=10)
service_graph.add_node(2, compute_requirement=0)
service_graph.add_node(3, compute_requirement=0)

for s,t in service_graph.edges():
        service_graph[s][t]['weight'] = random.randint(1,50)

positions = {0:[0,0],1:[1,0],2:[2,0],3:[3,0]}
nx.draw_networkx(service_graph,pos=positions)
#plt.savefig("path.png")
#plt.show()
M = [] 
place = 0
total = 0 
#service_placement(largest_path,graph,service_graph)
map = {}
map1 = {}
def service_placement(paths,largest_path,graph,service_graph):
    total=0
    sum_edge = 0
#    print("test")
    for path in paths: 
#        for j,i in zip(range(len(path)),service_graph):        #zip is running for shorter or longer of the two lists? If there are only two paths, the problem is service 
        for i,l,d in service_graph.edges(data=True):
            for j,k,f in graph.edges(data=True):
                if (d['weight'] < f['weight']):
                    d['weight'] = d['weight'] - f['weight']
                    service_graph[i][l]['new'] = 1
#                    sum = 0
                    sum_edge += service_graph[i][l]['new']
#                    if (sum_edge == '4'):
#                        break
#                    values1= map1.values()
#                    total1 = sum(values1)
                    if (sum_edge ==4):
                        break
                else:
                    continue
                break
            else:
                continue
            break
        if (sum_edge == 4):     
            for j in range(len(path)):
#         for j,k in graph.edges():
#        for j in path:
                for i in service_graph:
#       for i in largest_path:
#        for i in service_graph:
#            print(path)
#                print("j \& i",j,i)
                    while(j<4): # start node != end_node
                        place=0
                        j = j + 1
#                print("Value of i at the beggining of while loop %s" %(i) )
                        if (service_graph.nodes[i]['compute_requirement'] < graph.nodes[j]['compute']):
#                        print("Node graph",path[j])
                            graph.nodes[j]['compute'] = service_graph.nodes[i]['compute_requirement'] - graph.nodes[j]['compute']
                            i = i + 1    
                            map[i,j] = 1 
                            values = map.values()
                            total = sum(values)
                            if total == 4:
#                            print("path %s failed" %(path))
                                break              
                               
            if total < 4:
                print("path %s failed" %(path))
                break 
##                    if (total ==3):
##                        print("Success on  %s path" % (j))
##                        break
##                    else: 
##                        print("No success on %s path" %(j))      
#                else:
#                    print("No path found")
#                    continue
#            print("Failed service placement on %s path" % (j))
    if(total == 4):
        print("Successful service at path %s" %(path))
    else:
        print("Failed service")                         
    print("map value is",map)
    values = map.values()
    total = sum(values)
    print("Total value here",total)
#    place = place+1
#                if(total==3):
#                   print("2")
#                   break
              		
#    if(total==3):
#        print(map)
#        break
#    if(total==3):
#      
    for i,l,d in service_graph.edges(data=True):
        for j,k,f in graph.edges(data=True):
            if (d['weight'] < f['weight']):
                d['weight'] = d['weight'] - f['weight']
                

service_placement(paths,largest_path,graph,service_graph)
