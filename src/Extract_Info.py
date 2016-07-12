import ast
import datetime
import json
 
class Node():
    #node class; stores information about the actor, target and time
    def __init__(self, actor):
        self.actor = actor
    def get_actor(self):
        return self.actor
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False
    def __hash__(self):
        return hash(self.actor)
    def __str__(self):
        node_rep = [self.actor]
        return str(node_rep)
    def __repr__(self):
        node_rep = [self.actor]
        return str(node_rep)
    
    
class Graph():
    #graph class for adding nodes and edges; also returns the maximum time stamp of the nodes in the graph
    def __init__(self, nodes, max_time):
        self.nodes = {}
        self.max_time = max_time
    def add_node(self, node):
        self.nodes[node] = []
    def remove_node(self, node):
        self.nodes.pop(node, None)
        for i in self.nodes:
            if node in self.nodes[i]:
                self.nodes[i].remove(node)
    def add_edge(self, node1, node2):
        self.nodes[node1].append(node2)
        self.nodes[node2].append(node1)
    def delete_edge(self, node1, node2):
        self.nodes[node1].remove(node2)
        self.nodes[node2].remove(node1)
    def get_degree_node(self,node):
        return len(self.nodes[node])
    def get_nodes(self):
        return self.nodes
    def get_maximum_time(self):
        return self.max_time
    def change_max_time(self, newmax):
        self.max_time = newmax
    def __str__(self):
        return str(self.nodes)
    
#for testing purposes to form testlist
mindate = datetime.datetime(year= datetime.MINYEAR, month = 1, day = 1, hour = 0, minute = 0, second = 0)
test1date = datetime.datetime(year= datetime.MINYEAR, month = 1, day = 1, hour = 0, minute = 0, second = 15)
test2date = datetime.datetime(year= datetime.MINYEAR, month = 1, day = 1, hour = 3, minute = 0, second = 59)
test3date = datetime.datetime(year= datetime.MINYEAR, month = 1, day = 1, hour = 3, minute = 0, second = 56)
#for testing purposes to form testlist

def get_information():
    #returns a list of lists of the JSON messages in the format [actor, target, time]
    master_list = []
    filename = 'venmo-trans.txt'
    with open(filename, 'r') as input_file:
        for line in input_file:
            current_line = ast.literal_eval(line)
            current_time = current_line["created_time"]
            time = datetime.datetime.strptime(current_time, "%Y-%m-%dT%H:%M:%SZ")
            current_actor = current_line["actor"]
            current_target = current_line["target"]
            current_time = current_time.split(':')
            all_info = [current_actor, current_target, time]
            master_list.append(all_info)
        return master_list

def find_max_time(timeA, timeB):
    #returns the time which is greater out of two times
    if timeA > timeB:
        return timeA
    else:
        return timeB
    
def within_sixty(timeA, timeB):
    #returns true if there is only a 60 second difference between two times and false otherwise
    if timeB >= timeA:
        difference = timeB - timeA
    else:
        difference = timeA - timeB
    if difference <= datetime.timedelta(seconds = 60):
        return True
    else:
        return False

def find_median(list1):
    #returns the median of the list
    length = len(list1)
    #even list
    if length%2 == 0:
        left = length/2 - 1
        right = length/2
        median = round((list1[left] + list1[right])/2.0, 2)
    #odd list
    else:
        median = round(list1[length/2],2)
    return median

#used for testing purposes; tested manually, checking median output against pencil and paper work; tested for cases of payments within each other,
#payments out of order but within window, and out of order but not in 60 second window
testlist = [["wayne", "libby", test1date], ["wayne", "hammersmith", test1date], ["gretsky", "brick", test1date],
            ["libby", "scott", test2date], ["gretchen", "lionel", test1date], ["olivia", "nieman", mindate],
            ["brett", "johnny", test3date], ["brett", "gretchen", test3date], ["brett", "louisa", test3date], ["gretchen", "samuel", test2date]]
testlist2 = [["brett", "johnny", test3date], ["brett", "gretchen", test3date], ["brett", "louisa", test3date],
             ["johnny", "gretchen", test3date], ["johnny", "samuel", test3date], ["louisa", "samuel", test3date], ["samuel", "gretchen", test3date]]

outputFile = file('output.txt', 'w')

def main():
    #finds the median after each payment and writes it to output.txt
    all_medians = []
    #list1 = testlist2
    list1 = get_information()
    max_time = mindate
    created_times_dict = {}
    nodes_dict ={}
    g = Graph(nodes_dict, max_time)
    for i in list1:
        #if time of new payment within window, add the actor and the time to dictionary of times; also add the target and time
        #replaces maximum processed time if the new payment has a bigger time stamp
        max_time = find_max_time(max_time, i[2])
        #checks if payment is within maximum processed time
        if within_sixty(max_time, i[2]):
            if i[0] not in created_times_dict:
                created_times_dict[i[0]] = i[2]
            if i[1] not in created_times_dict:
                created_times_dict[i[1]] = i[2]
            if i[0] in created_times_dict:
                if i[2]>created_times_dict[i[0]]:
                    created_times_dict[i[0]] = i[2]
            if i[1] in created_times_dict:
                if i[2]>created_times_dict[i[1]]:
                    created_times_dict[i[1]] = i[2]
            #adds nodes to graphs if not already present
            firstNode = Node(i[0])
            secondNode = Node(i[1])
            if firstNode not in g.get_nodes():
                g.add_node(firstNode)
            if secondNode not in g.get_nodes():
                g.add_node(secondNode)
            #connects actor and target
            g.add_edge(firstNode, secondNode)
        #adds nodes that should be removed (no longer within window or not connected to anything) to a list
        remove_nodes = []
        for a in g.get_nodes():
            if not within_sixty(created_times_dict[a.get_actor()], max_time) or not g.get_nodes()[a]:
                remove_nodes.append(a)
            if not g.get_nodes()[a]:
                remove_nodes.append(a)
        #removes nodes that were added to the remove list
        for c in remove_nodes:
            g.remove_node(c)
        #gets the degree of each node in the graph and sorts the list of degrees
        degree_list = []
        for d in g.get_nodes():
            degree_list.append(g.get_degree_node(d))
        degree_list.sort()
        #finds median of the list of degrees and adds it to a master list
        all_medians.append(find_median(degree_list))
    #writes medians to an output file
    for f in all_medians:
        stringed = str(f) +'0' + '\n'
        outputFile.write(stringed)
print main()
outputFile.close()

        
                
            
                
                




