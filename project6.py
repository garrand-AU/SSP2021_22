import tkinter as tk
from tkinter import filedialog as fd
from queue import PriorityQueue
import itertools
import re
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from PIL import ImageTk, Image
import random
from datetime import datetime



class Graph():
    def __init__(self):
        self.nodes =[]  # store vertices objects
        self.edges = [] # store edges objects
        # self.number_of_nodes = 0
        self.number_of_edges = 0

    def add_vertex(self,name, addr, type):
        v = self.Vertex(name, addr, type)
        self.nodes.append(v)

    # add u, v adges
    def add_edge(self, u, v, w, b):
        # get u, v nodes

        u_node = self.get_node(u)
        v_node = self.get_node(v)

        # u or v not exist, create u or v nodes
        if u_node == None:
            u_node = self.Vertex(u, 1, 1)
            self.nodes.append(u_node)
        if v_node == None:
            v_node = self.Vertex(v, 1, 1)
            self.nodes.append(v_node)

        # initialize Edge class with u, v nodes
        e = self.Edge(u_node, v_node, w, b)

        self.edges.append(e)
        # add edge to u, v nodes
        u_node.add_edge(e)
        v_node.add_edge(e)

        return True

    def create_message(self, type, src, dest, addr, pri, m):
        return self.Message(type, src, dest, addr, pri, m)
    # get the given name node
    def get_node(self, name):
        for n in self.nodes:
            if name == n.name:
                return n
        return None

    def get_edge(self, v):
        for n in self.nodes:
            if v == n.name:
                return n.edges
        return []

    def get_number_of_nodes(self):
        return len(self.nodes)

    # store the number of edges
    def set_number_of_edges(self, n):
        self.number_of_edges = n

    def get_number_of_edges(self):
        return self.number_of_edges

    def get_edge_weight(self, u, v):
        for e in self.edges:
            if (e.start_vertex.name == u and e.end_vertex.name == v) or \
                (e.start_vertex.name == v and e.end_vertex.name == u):
                return e.weight
        return None

    # get the wight of edge uv
    def set_edge_weight(self, u, v, w):
        for e in self.edges:
            if (e.start_vertex.name == u and e.end_vertex.name == v) or \
                (e.start_vertex.name == v and e.end_vertex.name == u):
                e.weight = w
                e.prev_weight = w
                return True
        return False

    # get the bandwidtth of edge uv
    def get_edge_bandwidth(self, u, v):
        for e in self.edges:
            if (e.start_vertex.name == u and e.end_vertex.name == v) or \
                (e.start_vertex.name == v and e.end_vertex.name == u):
                return e.bandwidth
        return 0

    # set the bandwidth of edge uv
    def set_edge_bandwidth(self, u, v, b):
        for e in self.edges:
            if (e.start_vertex.name == u and e.end_vertex.name == v) or \
               (e.start_vertex.name == v and e.end_vertex.name == u):
                e.bandwidth = b
                e.prev_bandwidth = b
                return True
        return False

    # the delete vertex function may not be in use
    def delete_vertex(self, v):
        # remove edges
        index = 0
        for n in self.nodes:
            # find v vertex
            if v == n.name:
                for e in n.edges:
                    # delete edges in corresponding vertices
                    for ns in self.nodes:
                        if e == ns.get_name():
                            ns.del_edge(v)
                # remove vertex
                del self.nodes[index]
                return
            index += 1

    def delete_edge(self, v1, v2):
        v1_exist = False
        v2_exist = False
        n_v1 = self.vertex('','',0)
        n_v2 = self.vertex('','',0)

        for n in self.nodes:
            if v1 == n.get_name():
                v1_exist = True
                n_v1 = n
            if v2 == n.get_name():
                v2_exist = True
                n_v2 = n

        # if the edge exists, delete it
        if v1_exist and v2_exist:
            n_v1.del_edge(v2)
            n_v2.del_edge(v1)

    # update the whole graph status
    # 1. update all vertices status
    #    a. update the weight of edges with random funtion
    #    b. update the bandwidth of edges with random funtion
    def update_network(self):
        for e in self.edges:
            w = int(random.random()*100)
            if w < 3:
                e.weight = float('inf')
            elif w < 30:
                e.weight = 5
            elif w < 70:
                e.weight += 1
            else:
                e.weight -= 1

            if e.weight < 0:
                e.weight = 1

            b = int(random.random()*100)
            if b < 50:
                e.bandwidth += 1
            else:
                e.bandwidth -= 1

            if e.bandwidth < 0:
                e.bandwidth = 1


    def print_graph_nodes(self):
        print("Total nodes:" + str(len(self.nodes)))
        for v in self.nodes:
            v.print_vertex()
            print("-----------------With Messages: --------------")
            v.print_message()
            print('\n\n\n')

    def print_graph_edges(self):
        print("Total edges:" + str(len(self.edges)))
        for e in self.edges:
            e.print_edge()

    def print_graph_message(self):
        for n in self.nodes:
            n.print_message()

    class Vertex():
        addr_iter = itertools.count()
        def __init__(self, name, addr, type):
            self.name = name    # string name
            self.addr = next(self.addr_iter)
            self.type = type
            self.edges = []      # string, store the vertex name connecting with each other
            self.rec_buffer = []       # Message object list, store the temporaly received messages
            self.send_buffer = []       # Message object list, store the temporaly messages to send
            self.votes = []      # store the voting results
            self.msg_id = []    # store messages id

        # add an edge to the edges list
        def add_edge(self, v):
            self.edges.append(v)

        # delete the given name in the edges list
        def del_edge(self,name):
            self.edges.remove(name)

        # after receive a message, reply the message to the sender if needed
        # prepare for reply message, return new message object
        def prepare_reply_msg(self, m):
            if m == None:
                return m
            v = True
            t = 0
            if random.random() > 0.9:
                v = False
            # if len(self.edges) <= 4: # for testing decision making affected by message's priority
            #     v = False
            if random.random() > 0.5:
                t = 1
            m.type = 1              # this is a private message

            m.vote = v           # Boolean: True or False
            m.path.append(self.name)          # record the address (name) that messages go through
            m.delay = t          # int, store the message delay time
            m.reply = False      # Boolean, False: no need to replay, True: Need to reply
            # if len(self.edges) >
            m.priority = int(random.random()*10)
            #m.priority = 5
            return m


        # handle the messages in receive buffer
        # prepare data to send, put it in the send buffer
        # no data to handle, return 0, data is prepared, return 1, if  error, return -1
        def receive_msg(self):
            # receive information
            if not self.rec_buffer:
                return -1
            for m in self.rec_buffer:

                # receive the reply votes and store in the self.votes list
                if not m.reply and m.destination == self.name:
                    print(self.name + " receives vote from " + m.source)
                    self.votes.append([m.vote, m.priority, m.source])
                else:
                    self.send_buffer.append(m)
                self.rec_buffer.remove(m)

            return 1

        # return the message with the highest priority
        def get_msg(self):
            # buffer is not empty
            # find the highest priority messages
            highest = 0
            if not self.send_buffer:
                return None
            for i in range(len(self.send_buffer)):
                if self.send_buffer[i].priority > self.send_buffer[highest].priority:
                    highest = i
            # print(highest)
            new_msg = self.send_buffer[highest]

            return new_msg

        # broadcast the message to its neighbor's vertices
        #    -- store the message to recieve buffer
        def broadcast_msg(self, m):
            # print('Message Delay: ' + str(m.delay))
            if int(m.delay) == 0:
                # print('test point -------')
                for e in self.edges:
                    if e.start_vertex.name != self.name:
                        # m.receiver = e.start_vertex.name
                        # if msg is not in rec_buffer, store it to the rec_buffer
                        if m.mid not in e.start_vertex.msg_id:
                            e.start_vertex.msg_id.append(m.mid)
                            e.start_vertex.rec_buffer.append(m)
                            # m.path.append(e.start_vertex.name)
                    else:
                        # m.receiver = e.end_vertex.name
                        if m.mid not in e.end_vertex.msg_id:
                            e.end_vertex.msg_id.append(m.mid)
                            e.end_vertex.rec_buffer.append(m)
                            # m.path.append(e.end_vertex.name)
                # remove m from send buffer
                if m in self.send_buffer:
                    self.send_buffer.remove(m)
            else:
                m.delay = int(m.delay) - 1

        def print_vertex(self):
            print(self.name + " "+ str(self.addr) + " "+ str(self.type) +" with edges:")
            for e in self.edges:
                if e.start_vertex.name != self.name:
                    print(e.start_vertex.name)
                else:
                    print(e.end_vertex.name)
            print('\n')

        def print_message(self):
            print(self.name + ' Receive buffer:')
            for m in self.rec_buffer:
                m.print_message()
            print(self.name + ' Send buffer:')
            for m in self.send_buffer:
                m.print_message()
            print(self.name + ' message id buffer:')
            print(self.msg_id)

    class Edge():
        def __init__(self, u, v, w = 0, b = 0):
            self.start_vertex = u   # Vertex object
            self.end_vertex = v     # Vertex object
            self.weight = float(w)         # float (0 to inf)
            self.bandwidth = int(b)      # int, e.g value from 0 to 9, 0 no bandwidth, 9 maximium bandwidth
            self.prev_weight= float(w)
            self.prev_bandwidth = int(b)
        def set_weight(self, w):
            self.weight = w

        def set_bandwidth(self,b):
            self.bandwidth = b

        def print_edge(self):
            print("u, v, weight, bandwidth:")
            print(self.start_vertex.name, self.end_vertex.name, self.weight, self.bandwidth)
            print('\n')

    class Message():
        global msg_iter
        msg_iter = itertools.count()
        def __init__(self, type, src, dest, addr =0, pri=0, m=False):
            self.mid = next(msg_iter)
            self.type = type           # int, 0, public info, 1, private info
            self.source = src          # string start address
            self.receiver = addr       # string, receiver address, it is temporary address before the message reaches its destination
            self.destination = dest    # string destination address
            #self.priority = int(random.random()*10)        # priority
            self.priority = pri
            self.vote = m           # Boolean: True or False
            self.path = []          # record the address (name) that messages go through
            self.delay = 0          # int, store the message delay time
            self.reply = True      # Boolean, False: no need to replay, True: Need to reply

        def print_message(self):
            print('message id: ' + str(self.mid) + \
            '; ' + 'type: ' + str(self.type) + \
            '; source: '+ str(self.source) + \
            '; transfer address: '+str(self.receiver) + \
            '; final destination: '+ str(self.destination)+ \
            '; priority: ' + str(self.priority) + \
            '; vote: ' + str(self.vote) + \
            '; delay: ' + str(self.delay) + \
            '; reply: ' + str(self.reply)
            )

###################################################
# Dijkstra's algorithm to find the shortest path to server from a given node
# from the given agent, the distance is 0
# put in the given agent to the queue and label it as visited
# search its neighbours, and get distances (weights)
# if the neighbour not in visited list, compare, and update its distances from the given agent
# if the neighbour is server, return
# The path from given agent to server is found
# input: class: graph, string: start_vertex
##################################################
def dijkstra(graph, start_vertex):
    # pass
    # initialize the distance to inf for each node
    D = {}

    #Path dictionary to store shortest path tree
    #Path = {}
    Parent = {}

    for vertex in graph.nodes:
        v = vertex.name
        D[v] = float('inf')
        #Path[v] = []

    # the first node distance is 0
    D[start_vertex] = 0

    visited = []

    pq = PriorityQueue()
    # put the start vertex to queue
    pq.put((0, start_vertex))

    while not pq.empty():
        # get the current vertex
        (dist, current_vertex) = pq.get()
        # label the current vertex visited
        visited.append(current_vertex)
        # for neighbor in range(graph.v): visit current_vertex neighbor
        curr_node = graph.get_node(current_vertex)

        for e in curr_node.edges:
            distance = float(e.weight)
            neighbor = e.start_vertex.name

            if e.end_vertex.name != current_vertex:
                neighbor = e.end_vertex.name

            if neighbor not in visited:
                old_cost = D[neighbor]
                new_cost = D[current_vertex] + distance
                # Path[neighbor].append(current_vertex)

                if new_cost < old_cost:
                    pq.put((new_cost, neighbor))
                    D[neighbor] = new_cost
                    Parent[neighbor] = current_vertex

    return D, Parent


##################################################
# get next node to transfer the message
# input: Graph, current node name, message
# return: next node object
#
#################################################
def send_info2next_node(graph, start_vertex, m):
    D, Parent = dijkstra(graph, start_vertex)
    # send the reply message to the nearest node on the path

    # print(D)
    # print(start_vertex)
    # m.print_message()

    v = m.destination
    path = v
    if v in Parent.keys():
        while(Parent[v] != start_vertex):
            path = Parent[v] + '->' + path
            v = Parent[v]
        path = start_vertex + '->' + path

        # print(path)

    v = m.destination
    path = v
    if Parent:
        if v not in Parent.keys():
            v = list(Parent)[-1]
        else:
            v = Parent[v]
        if v == start_vertex:
            v = m.destination
        print('Next path: ' + v)
        if v != m.source:
            transfer_node = G.get_node(v)
            start_node = G.get_node(start_vertex)
            if int(m.delay) == 0:
                transfer_node.rec_buffer.append(m)
                if m in start_node.send_buffer:
                    start_node.send_buffer.remove(m)
                return True
            else:
                m.delay = int(m.delay) - 1
                return False


# read file and return Graph object
def read_file():
    G = Graph()
    with open("graph.txt", "r") as fin:
        for line in fin:
            line = line.rstrip()
            if "#name" in line:
                line_is_node = True
                continue

            if "#edges" in line:
                line_is_node = False
                continue

            if ',' not in line:
            # if not line:
                # only one column in this line, skip
                continue

            if line_is_node:
                # print(line)
                name, address, type = line.split(",")
                G.add_vertex(name, address, type)
            # G.print_graph()
            else:
                v1, v2,w,b = line.split(",")
                G.add_edge(v1,v2,w,b)
                G.number_of_edges += 1

    return G

def main():

    global G
    G = Graph()

    random.seed(str(datetime.now()))

    root = tk.Tk()
    root.title("Unstable Network Simulation")
    root.geometry("800x800")

    BACKGROUND = 'white'
    root.configure(background=BACKGROUND)
    Font_size = ('Times', 15)
    # positions
    start_row = 1
    start_col = 0
    display_row = 16
    frame_row = display_row + 1
    # current_row = 11

    # display information frame
    info_frame = tk.Frame(root)
    info_frame.grid(row = frame_row, column = 0, columnspan = 4)

    # open a file
    def open_file():
        filetypes = (('text files', '*.txt'),('all files','*.*'))
        global filename
        filename = fd.askopenfilename(title='Open a file',initialdir='/', filetypes=filetypes)

        # clear G nodes and edges
        del G.nodes[:]
        del G.edges[:]

        # read file to contruct a graph
        line_is_node = False
        with open(filename, "r") as fin:
            for line in fin:
                line = line.rstrip()
                if "#name" in line:
                    line_is_node = True
                    continue
                if "#edges" in line:
                    line_is_node = False
                    continue
                if ',' not in line:
                    continue

                if line_is_node:
                    name, address, type = line.split(",")
                    G.add_vertex(name, address, type)
                else:
                    v1, v2,w,b = line.split(",")
                    G.add_edge(v1,v2,w,b)
                    G.number_of_edges += 1

        file = tk.Label(root, text=filename, anchor = 'w',font=Font_size, padx=5, pady=5,bg=BACKGROUND)
        file.grid(row=0, column = 1, columnspan=4)
        # showinfo(title='Selected File',message=filename)

    # draw a graph
    def draw_graph():
        g_net_work = nx.Graph()
        for e in G.edges:
            u = e.start_vertex.name
            v = e.end_vertex.name
            if not e.weight == float('inf'):
                g_net_work.add_edge(u,v)
        nx.draw(g_net_work, with_labels=1)
        plt.show()

    # button click functions
    def add_a_node():
        name = u_input.get()
        address = ua_input.get()
        type = 0
        G.add_vertex(name, address, type)
        u_input.delete(0, 'end')
        ua_input.delete(0, 'end')
        for widgets in info_frame.winfo_children():
            widgets.destroy()
        global current_row
        add_label = tk.Label(info_frame, text='Add Vertex: ' + name + ' with address: ' + str(address), anchor = 'e',font=Font_size, padx=5, pady=5,bg=BACKGROUND)
        add_label.grid(row = frame_row, column = 0, columnspan = 4)

    def add_edge():
        u = eu_input.get()
        v = ev_input.get()
        print(u,v)
        w = 1
        b = 9
        res = G.add_edge(u,v,w,b)
        for widgets in info_frame.winfo_children():
            widgets.destroy()
        if res:
            mw_label = tk.Label(info_frame, text='Edge between ' + u + ' and '+ v+' added successfully, weight = '+str(w)+', bandwidth = '+str(b), anchor = 'e',font=Font_size, padx=5, pady=5,bg=BACKGROUND)
            mw_label.grid(row = frame_row, column = 0, columnspan = 4)
        else:
            mw_label = tk.Label(info_frame, text='Edge between ' + u + ' and '+ v+' added failed', anchor = 'e',font=Font_size, padx=5, pady=5,bg=BACKGROUND)
            mw_label.grid(row = frame_row, column = 0, columnspan = 4)
        eu_input.delete(0, 'end')
        ev_input.delete(0, 'end')

    #modify edge's weight
    def modify_weight():
        u = wu_input.get()
        v = wv_input.get()
        w = int(w_input.get())
        res = G.set_edge_weight(u,v,w)
        wu_input.delete(0, 'end')
        wv_input.delete(0, 'end')
        w_input.delete(0, 'end')
        for widgets in info_frame.winfo_children():
            widgets.destroy()
        if res:
            mw_label = tk.Label(info_frame, text='Weight of Edge between' + u + 'and '+ v+' modified successful', anchor = 'e',font=Font_size, padx=5, pady=5,bg=BACKGROUND)
            mw_label.grid(row = frame_row, column = 0, columnspan = 4)
        else:
            mw_label = tk.Label(info_frame, text='Weight of Edge between' + u + 'and '+ v+' modified failed', anchor = 'e',font=Font_size, padx=5, pady=5,bg=BACKGROUND)
            mw_label.grid(row = frame_row, column = 0, columnspan = 4)

    def modify_bandwidth():
        u = bu_input.get()
        v = bv_input.get()
        b = int(b_input.get())
        res = G.set_edge_bandwidth(u,v,b)
        bu_input.delete(0, 'end')
        bv_input.delete(0, 'end')
        b_input.delete(0, 'end')
        for widgets in info_frame.winfo_children():
            widgets.destroy()
        if res:
            mw_label = tk.Label(info_frame, text='Bandwidth of Edge between ' + u + 'and '+ v+' modified successfully', anchor = 'e',font=Font_size, padx=5, pady=5,bg=BACKGROUND)
            mw_label.grid(row = frame_row, column = 0, columnspan = 4)
        else:
            mw_label = tk.Label(info_frame, text='Bandwidth of Edge between ' + u + 'and '+ v+' modified failed', anchor = 'e',font=Font_size, padx=5, pady=5,bg=BACKGROUND)
            mw_label.grid(row = frame_row, column = 0, columnspan = 4)

    def delete_edge():
        u = du_input.get()
        v = dv_input.get()
        res = G.set_edge_weight(u,v,float('inf'))
        du_input.delete(0, 'end')
        dv_input.delete(0, 'end')
        for widgets in info_frame.winfo_children():
            widgets.destroy()
        if res:
            mw_label = tk.Label(info_frame, text='Edge between' + u + 'and '+ v+' deleted successfully', anchor = 'e',font=Font_size, padx=5, pady=5,bg=BACKGROUND)
            mw_label.grid(row = frame_row, column = 0, columnspan = 4)
        else:
            mw_label = tk.Label(info_frame, text='Edge between' + u + 'and '+ v+' deleted failed', anchor = 'e',font=Font_size, padx=5, pady=5,bg=BACKGROUND)
            mw_label.grid(row = frame_row, column = 0, columnspan = 4)

    def save():
        with open('network.txt', 'w') as f:
            f.write('#name, address, type \n')
            for n in G.nodes:
                line = n.name + ','+ str(n.addr) +','+str(n.type)
                f.write(line)
                f.write('\n')
            f.write('\n')

            f.write('#edges，u, v, weight, bandwidth\n')
            for e in G.edges:
                # print(e.start_vertex, e.end_vertex, e.weight, e.bandwidth)
                line = e.start_vertex.name + ','+ e.end_vertex.name +','+ str(e.weight) + ',' + str(e.bandwidth)
                f.write(line)
                f.write('\n')
            for widgets in info_frame.winfo_children():
                widgets.destroy()

            sav_label = tk.Label(info_frame, text='Save to file: network.txt successfully', anchor = 'e',font=Font_size, padx=5, pady=5,bg=BACKGROUND)
            sav_label.grid(row = frame_row, column = 0, columnspan = 4)

    def find_path():
        start_vertex = start_u.get()
        end_vertex = end_v.get()

        # find the shortest path with dijkstra algorithm
        D, P = dijkstra(G, start_vertex)

        # print out the shortest path
        v = end_vertex
        path = v
        while(P[v] != start_vertex):
            path = P[v] + '->' + path
            v = P[v]
        path = start_vertex + '->' + path

        start_u.delete(0, 'end')
        end_v.delete(0, 'end')
        # display info
        for widgets in info_frame.winfo_children():
            widgets.destroy()
        path_label = tk.Label(info_frame, text=path, anchor = 'e',width = label_width, font=Font_size, padx=5, pady=5,bg=BACKGROUND)
        path_label.grid(row = frame_row, column = 0, columnspan = 3)

    def find_bw_path():
        start_vertex = bw_start_u.get()
        end_vertex = bw_end_v.get()
        # clear the entry
        bw_start_u.delete(0, 'end')
        bw_end_v.delete(0, 'end')
        # find one of the shortet path
        D, Parent = dijkstra(G, start_vertex)
        shortest_path = D[end_vertex]

        v = end_vertex
        path = end_vertex
        if v in Parent.keys():
            while (Parent[v] != start_vertex):
                path = Parent[v] + '->' + path
                v = Parent[v]
            path = start_vertex + '->' + path
        # print out one of the shortest path
        for widgets in info_frame.winfo_children():
            widgets.destroy()
        if path == end_vertex:
            path == 'No path found for maximium bandwidth between ' + start_vertex + ' and ' + end_vertex
        else:
            path_label = tk.Label(info_frame, text="A shortest path: " + path, anchor = 'e', font=Font_size, padx=5, pady=5,bg=BACKGROUND)
            path_label.grid(row = frame_row, column = 0, columnspan = 4)

        # find the shortest path with maximium bandwidth
        run_once = True
        while shortest_path < D[end_vertex] or run_once:
            run_once = False
            # print the bandwidth of the edges on the shortest path
            v = end_vertex
            u = ''
            smallest_bandwidth = 9
            smallest_bandwidth_edge = []

            # find the minimum bandwidth edge
            if v in Parent.keys():
                while not Parent[v] and (Parent[v] != start_vertex):
                    u = Parent[v]
                    b = G.get_edge_bandwidth(u, v)
                    if int(b) < smallest_bandwidth and int(b) != 0:
                        smallest_bandwidth = int(b)
                        smallest_bandwidth_edge = [u,v]
                    v = u
            # get the bandwidth of the last edge on the shortest path
            b = G.get_edge_bandwidth(start_vertex, v)
            if int(b) < smallest_bandwidth and int(b) != 0:
                smallest_bandwidth = int(b)
                smallest_bandwidth_edge = [start_vertex, v]

            # set the weight of the edges, whose bandwidth is smaller than the smallest bandwidth, to inf
            for e in G.edges:
                if e.bandwidth <= smallest_bandwidth:
                    e.weight = float('inf')

            D, P = dijkstra(G, start_vertex)

            v = end_vertex
            if v not in P:
                # print('Not find a path to the end_vertex')
                break
            if v in P.keys():
                while (P[v] != start_vertex):
                    path = P[v] + '->' + path
                    v = P[v]

                path = start_vertex + '->' + path

        # restore the edges
        # print('\n\n\n\n')
        # G.print_graph_edges()
        for e in G.edges:
            e.weight = e.prev_weight
            e.bandwidth = e.prev_bandwidth
        # print('\n\n\n\n')
        # G.print_graph_edges()
        # G.print_graph_edges()
        # for widgets in info_frame.winfo_children():
        #     widgets.destroy()
        edge = 'between ' + start_vertex + ' and ' + end_vertex
        if path == end_vertex:
            path == 'No path found for maximium bandwidth ' + edge
        else:
            path_label = tk.Label(info_frame, text='Shortest path with maximium bandwidth ' + edge + ': ' + path, anchor = 'e', font=Font_size, padx=5, pady=5,bg=BACKGROUND)
            next_row = frame_row + 1
            path_label.grid(row = next_row, column = 0, columnspan = 4)

    # create a message object
    def init_message():
        # clear nodes' messages IDs, receive/send buffers in graph nodes :
        for n in G.nodes:
            del n.rec_buffer[:]
            del n.send_buffer[:]
            del n.msg_id[:]

        global M_type
        M_type = msg_type.get()
        global M_src
        M_src = msg_src.get()
        global M_dest
        M_dest = msg_dst.get()
        global Run_time
        Run_time = int(run_time.get())

        global Message
        Message = G.create_message(M_type, M_src, M_dest, 0, 0, 0)


        start_vertex = G.get_node(M_src)
        if start_vertex:
            start_vertex.send_buffer.append(Message)
            start_vertex.msg_id.append(Message.mid)
        else:
            print("Failed to initialize a message")

        # send a public messages
        if int(M_type) == 0 and Message != None:
            start_src = G.get_node(M_src)
            for e in start_src.edges:
                if e.start_vertex.name != M_src:
                    if Message.mid not in e.start_vertex.msg_id:
                        e.start_vertex.msg_id.append(Message.mid)
                        e.start_vertex.rec_buffer.append(Message)
                        # Message.path.append(e.start_vertex.name)
                else:
                    if Message.mid not in e.end_vertex.msg_id:
                        e.end_vertex.msg_id.append(Message.mid)
                        e.end_vertex.rec_buffer.append(Message)
                        # Message.path.append(e.end_vertex.name)
            if Message in start_src.send_buffer:
                start_src.send_buffer.remove(Message)

        if int(M_type) != 0 and Message != None:

            D, Parent = dijkstra(G, M_src)
            # send the message to the nearest node on the shortest path

            v = M_dest
            path = v
            if v in Parent.keys():
                while(Parent[v] != M_src):
                    path = Parent[v] + '->' + path
                    v = Parent[v]
                path = M_src + '->' + path

                print(path)

            transfer_node = G.get_node(M_dest)
            transfer_node.rec_buffer.append(Message)

            # display info
            for widgets in info_frame.winfo_children():
                widgets.destroy()
            content = "Message is dilivered through " + path
            msg_path = tk.Label(info_frame, text=content, anchor = 'e', font=Font_size, padx=5, pady=5,bg=BACKGROUND)
            msg_path.grid(row = frame_row, column = start_col + 1, columnspan = 3)


    # create a dynamic network
    # a message flows through dynamic_network
    # within time t
    def dynamic_network(t):

        # within limited time decision
        while t > 0:
            # print('\n\n')
            # print('=======================     '+str(t)+'    after sending message ==================')
            # G.print_graph_message()
            # print('\n\n')

            # update network status
            G.update_network()
            # G.print_graph_edges()

            # all nodes process messages
            for n in G.nodes:
                if n.receive_msg():
                    # print('Receiving message succeeded!')
                    continue

            # print('\n\n')
            # print('------------  after receiving message --------------')
            # G.print_graph_message()
            # src_node = G.get_node(M_src)
            # print(M_src + " votes: ")
            # print(src_node.votes)
            # print('\n\n')
            # all nodes send message
            for n in G.nodes:
                # get the message from recieve buffer
                reply_msg = n.get_msg()

                if reply_msg == None:
                    # print(n.name + ': new_msg is None')
                    continue

                reply_msg.transfer = n.name

                if int(reply_msg.type) == 0:
                    # if the message is public, broadcast message to its neighbors

                    n.broadcast_msg(reply_msg)

                    # add delay, vote info, path to the message object
                    # reply_msg = n.prepare_reply_msg(reply_msg)
                    # if the message is public and ask for reply, create a new reply message
                    if reply_msg.reply == True:
                        tmp_msg = G.create_message(1, n.name, reply_msg.destination, 0,0,0)
                        reply_msg = n.prepare_reply_msg(tmp_msg)

                    # reply_msg.print_message()
                    # find the shortest path to deliver the reply message
                    if send_info2next_node(G, n.name, reply_msg):
                        print("send message successfully")
                    else:
                        print("Delay to send message")
                        # remove message from the send buffer
                        # if reply_msg in n.send_buffer:
                        #     n.send_buffer.remove(reply_msg)

                # transfer the reply to the destination
                else:
                    if send_info2next_node(G, n.name, reply_msg):
                        print("Send message successfully")
                    else:
                        print("Delay to send message")
                        # remove message from the send buffer
                        # if reply_msg in n.send_buffer:
                        #     n.send_buffer.remove(reply_msg)

            t -= 1

    def make_decision_with_avg_weight():

        dynamic_network(Run_time)
        src_node = G.get_node(M_src)

        count_true = 0
        count_false = 0

        for v, p, n in src_node.votes:
            if v == True:
                count_true +=1
            else:
                count_false += 1

        total = len(G.nodes) - 1
        content = "Nodes Voting for True: " + str(count_true) + '; False: ' + str(count_false) + '; missing nodes: ' +str(abs(total - count_true-count_false))
        avg_weight_label = tk.Label(root, text=content, anchor = 'e', font=Font_size, padx=5, pady=5,bg=BACKGROUND)
        avg_weight_label.grid(row = start_row+12, column = start_col + 1, columnspan = 3)

        del src_node.votes[:]

    def make_decision_with_weighted_weight():

        dynamic_network(Run_time)
        src_node = G.get_node(M_src)

        count_true = 0
        count_false = 0

        for v, p, n in src_node.votes:
            # calculate the weight based on the number of edges
            node = G.get_node(n)
            w = len(node.edges)

            if v == True:
                count_true += w
            else:
                count_false += w

        percentage = 0.00
        if count_true + count_false != 0:
            percentage = 100*count_true/(count_true + count_false)

        missing = abs(len(G.nodes) - 1 - len(src_node.votes))

        # for test decision making affected by message's priority
        # content = ''
        # if count_true > count_false:
        #
        #     content = content + 'Make a decision, voting for true/false: ' + str(count_true) + '/' + str(count_false)
        # else:
        #     content = content+ 'Do not make decision, voting for true/false:' + str(count_true) + '/' + str(count_false)

        content = "Nodes Voting for True: " + str(percentage) + '%; missing nodes: ' + str(missing)
        avg_weight_label = tk.Label(root, text=content, anchor = 'e', font=Font_size, padx=5, pady=5,bg=BACKGROUND)
        avg_weight_label.grid(row = start_row+13, column = start_col + 1, columnspan = 3)

        del src_node.votes[:]


    #----------------------------------------------------------
    #                        GUI part
    #----------------------------------------------------------
    # create labels
    label_width = 20
    info_label = tk.Label(root, text='Information Display', anchor = 'center',width = label_width, font=('Times', 18), padx=5, pady=5,bg=BACKGROUND)

    # create entries
    box_length = 27
    box_font = ('Times', 15)
    font_color = '#666666'
    # add a vertex input
    u_input = tk.Entry(root, width = box_length, font= box_font, fg= font_color)
    u_input.insert(tk.END, 'Input a Vertex Name')
    ua_input = tk.Entry(root, width = box_length, font= box_font, fg= font_color)
    ua_input.insert(tk.END, 'Input Address Number')
    # add an edge input
    eu_input = tk.Entry(root, width = box_length, font= box_font, fg= font_color)
    eu_input.insert(tk.END, 'Edge: U Side')
    ev_input = tk.Entry(root, width = box_length, font= box_font, fg= font_color)
    ev_input.insert(tk.END, 'Edge: V Side')
    # modify weight input
    wu_input = tk.Entry(root, width = box_length, font= box_font, fg= font_color)
    wu_input.insert(tk.END, 'Edge: U Side')
    wv_input = tk.Entry(root, width = box_length, font= box_font, fg= font_color)
    wv_input.insert(tk.END, 'Edge: V Side')
    w_input = tk.Entry(root, width = box_length, font= box_font, fg= font_color)
    w_input.insert(tk.END, 'Weight Number (0 to inf)')
    # Mofidy bandwidth input
    bu_input = tk.Entry(root, width = box_length, font= box_font, fg= font_color)
    bu_input.insert(tk.END, 'Edge: U Side')
    bv_input = tk.Entry(root, width = box_length, font= box_font, fg= font_color)
    bv_input.insert(tk.END, 'Edge: V Side')
    b_input = tk.Entry(root, width = box_length, font= box_font, fg= font_color)
    b_input.insert(tk.END, 'Bandwidth Number (0 to 9)')
    # delete edge input
    du_input = tk.Entry(root, width = box_length, font= box_font, fg= font_color)
    du_input.insert(tk.END, 'Edge: U Side')
    dv_input = tk.Entry(root, width = box_length, font= box_font, fg= font_color)
    dv_input.insert(tk.END, 'Edge: V Side')
    # find the shortest path input
    start_u = tk.Entry(root, width = box_length, font= box_font, fg= font_color)
    start_u.insert(tk.END, 'Input a Start Vertex')
    end_v   = tk.Entry(root, width = box_length, font= box_font, fg= font_color)
    end_v.insert(tk.END, 'Input an End Vertex')
    # find the shortest path with maximium bandwidth input
    bw_start_u = tk.Entry(root, width = box_length, font= box_font, fg= font_color)
    bw_start_u.insert(tk.END, 'Input a Start Vertex')
    bw_end_v   = tk.Entry(root, width = box_length, font= box_font, fg= font_color)
    bw_end_v.insert(tk.END, 'Input an End Vertex')

    msg_type = tk.Entry(root, width = box_length, font= box_font, fg= font_color)
    msg_type.insert(tk.END, '0')
    msg_src   = tk.Entry(root, width = box_length, font= box_font, fg= font_color)
    msg_src.insert(tk.END, 'LS3')
    msg_dst   = tk.Entry(root, width = box_length, font= box_font, fg= font_color)
    msg_dst.insert(tk.END, 'LS3')
    run_time = tk.Entry(root, width = box_length, font= box_font, fg= font_color)
    run_time.insert(tk.END, '20')


    button_width = 18
    # function buttions
    add_button = tk.Button(root, text = 'Add a Vertex', width=button_width, font=Font_size, padx=5, pady=5, command=add_a_node)
    edg_button = tk.Button(root, text = 'Add an Edge', width=button_width, font=Font_size, padx=5, pady=5, command=add_edge)
    wgt_button = tk.Button(root, text = 'Modofy Edge\'s Weight', width=button_width, font=Font_size,padx=5, pady=5, command=modify_weight)
    bwh_button = tk.Button(root, text = 'Modofy Edge\'s Bandwidth', width=button_width, font=Font_size,padx=5, pady=5, command=modify_bandwidth)
    del_button = tk.Button(root, text = 'Delete an Edge', width=button_width, font=Font_size,padx=5, pady=5, command=delete_edge)
    sav_button = tk.Button(root, text = 'Save', width=button_width, font=Font_size,padx=5, pady=5, command=save)
    pat_button = tk.Button(root, text = 'Find the Shortest Path', width=button_width, font=Font_size,padx=5, pady=5, command=find_path)
    shw_button = tk.Button(root, text = 'Show the Graph', width=button_width, font=Font_size,padx=5, pady=5, command=draw_graph)
    mbwh_button = tk.Button(root, text = 'Find the Max BW Path', width=button_width, font=Font_size,padx=5, pady=5, command=find_bw_path)
    msg_button = tk.Button(root, text = 'Send Messages', width=button_width, font=Font_size,padx=5, pady=5, command=init_message)
    average_decision_button = tk.Button(root, text = 'Decision w Average Weights', width=button_width, font=Font_size,padx=5, pady=5, command=make_decision_with_avg_weight)
    weighted_decision_button = tk.Button(root, text = 'Decision w Weighted Weights', width=button_width, font=Font_size,padx=5, pady=5, command=make_decision_with_weighted_weight)
    # clr_button = tk.Button(root, text = 'Clear', width=button_width, font=Font_size,padx=5, pady=5, command=clear_info)

    # open button
    open_button = tk.Button(root,text='Open a Graph',width=button_width, font=Font_size, padx=5, pady=5, command=open_file)


    open_button.grid(row=0, column=0, padx = 30, pady = 3)
    shw_button.grid(row=start_row,  column=start_col,   pady = 3)
    # add node button
    add_button.grid(row=start_row+1, column=start_col,   pady = 3)
    u_input.grid(row=start_row+1,    column=start_col+1)
    ua_input.grid(row=start_row+1,   column=start_col+2)
    # add edge button
    edg_button.grid(row=start_row+2, column=start_col)
    eu_input.grid(row=start_row+2,   column=start_col+1)
    ev_input.grid(row=start_row+2,   column=start_col+2)
    # weight button
    wgt_button.grid(row=start_row+3,column=start_col,   pady = 3)
    wu_input.grid(row=start_row+3,  column=start_col+1)
    wv_input.grid(row=start_row+3,  column=start_col+2, padx = 3)
    w_input.grid(row=start_row+4,   column=start_col+1)
    # bandwidth button
    bwh_button.grid(row=start_row+5, column=start_col, )
    bu_input.grid(row=start_row+5,   column=start_col+1)
    bv_input.grid(row=start_row+5,   column=start_col+2)
    b_input.grid(row=start_row+6,   column=start_col+1)
    #delete button
    del_button.grid(row=start_row+7,column=start_col,   pady = 3)
    du_input.grid(row=start_row+7,  column=start_col+1, pady = 3)
    dv_input.grid(row=start_row+7,  column=start_col+2, padx = 3, pady = 3)
    #find shortest path button
    pat_button.grid(row=start_row+8,column=start_col,   pady = 3)
    start_u.grid(row=start_row+8,   column=start_col+1, padx = 3, pady = 3)
    end_v.grid(row=start_row+8,     column=start_col+2, padx = 3, pady = 3)
    # fint the shortest path with maximium bandwidth button
    mbwh_button.grid(row=start_row+9,column=start_col,   pady = 3)
    bw_start_u.grid(row=start_row+9,   column=start_col+1, padx = 3, pady = 3)
    bw_end_v.grid(row=start_row+9,     column=start_col+2, padx = 3, pady = 3)
    # initialize message button
    msg_button.grid(row=start_row+10,column=start_col,   pady = 3)
    msg_src.grid(row=start_row+10,column=start_col+1,   pady = 3)
    msg_dst.grid(row=start_row+10,column=start_col+2,   pady = 3)
    msg_type.grid(row=start_row+11,column=start_col+1,   pady = 3)
    run_time.grid(row=start_row+11,column=start_col+2,   pady = 3)
    # making decision button
    average_decision_button.grid(row=start_row+12,column=start_col,   pady = 3)
    weighted_decision_button.grid(row=start_row+13,column=start_col,   pady = 3)

    sav_button.grid(row=start_row+14,column=start_col,   pady = 3)
    info_label.grid(row=start_row+15,column=start_col,   columnspan = 3)
    # clr_button.grid(row=display_row,   column=start_col)


    root.mainloop()



if __name__ == "__main__":
    main()
