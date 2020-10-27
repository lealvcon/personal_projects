class Node:
    '''Implementation of a node to work with data structures'''
    
    def __init__(self, data):
        """assigns the data to the node while initializing its link as None"""
        self.__data=data
        self.__next_node=None
        
    def __repr__(self):
        return "Node({0}, {1})".format(repr(self.__data),repr(self.__next_node))
        
    def set_data(self, data):
        '''assigns the specified data to the node'''
        self.__data=data
        
    def get_data(self):
        '''retrieve the data contained in this node'''
        return self.__data
    
    def set_next_node(self, node):
        '''sets the link this node points to'''
        self.__next_node=node
        
    def get_next_node(self):
        '''retrieve the node this node points to'''
        return self.__next_node
    
#%%
    
class LinkedList:
    '''Linked list class with iterables implemented. each element is a Node
    class object. see reference for Node'''
    def __init__(self):
        '''Initializes an empty linked list'''
        self.__head_node=None
        self.__size=0
        
    def __iter__(self):
        self.__i=0
        self.current_node=self.__head_node
        return self
    
    def __next__(self):
        if self.__i < self.__size:
            n=self.current_node
            self.current_node=self.current_node.get_next_node()
            self.__i+=1
            return n
        else:
            raise StopIteration
          
    def get_size(self):
        '''returns the size of the linked list'''
        return self.__size
    
    def add_node(self, new_node):
        '''appends a node to the linked list as the new head node and creates 
         a link to the previous head node. if the linked list is empty it assigns
         the new node as the head and tail'''
        if self.__size == 0:
            self.__head_node=new_node
            self.__size+=1
        else:
            new_node.set_next_node(self.__head_node)
            self.__head_node=new_node
            self.__size+=1
            
    def find_node(self, data):
        """Searches through the linked list for a node's data that matches the
        data provided as argument in the function. If it exists within the
        linked list it returns a list with the node and the index it was found 
        in (head at 0); if it is not within the list returns -1"""
        index=0
        for node in self:
            if node.get_data() == data:
                return [node, index]
            else:
                index+=1
        return -1
            
    def remove_node(self, data):
        '''Removes the first node containing the specified data, returns True
        if succesful and False if the specified data was not found'''
        if self.__size == 0:
            raise IndexError('attempting to remove a node from an empty linked list')
        elif self.__head_node.get_data() == data:
            self.__head_node=self.__head_node.get_next_node()
            self.__size-=1
        else:
            prev_node=self.__head_node
            current_node=self.__head_node.get_next_node()
            while current_node:
                if current_node.get_data() == data:
                    prev_node.set_next_node(current_node.get_next_node())
                    self.__size-=1
                    return True
                else:
                    prev_node=current_node
                    current_node=current_node.get_next_node()
            return False
#%%

class Stack:
    '''Implements a stack data structure using a linked list as an underlying
    data structure'''
    def __init__(self, max_size):
        '''initializes an empty stack with the set maximum size'''
        self.__max_size=max_size
        self.__size=0
        self.__top=None
        
    def push(self, value):
        '''adds the specified value to the top of the stack'''
        if self.__size == self.__max_size:
            class StackOverflow(Exception):
                def __init__(self,message):
                    self.message=message
            raise StackOverflow('reached maximum capacity of the stack')
        else:
            t=Node(value)    
            t.set_next_node(self.__top)
            self.__top=t
            self.__size+=1
        
    def pop(self):
        '''returns and removes data from the top of the stack'''
        if self.__size == 0:
            class StackUnderflow(Exception):
                def __init__(self, message):
                    self.message=message
            raise StackUnderflow('attempted to remove an element from an empty stack')
        else:    
            t=self.__top
            self.__top=self.__top.get_next_node()
            self.__size-=1
            return t.get_data()
        
    def get_size(self):
        return self.__size
    
    def peek(self):
        '''returns data from the top of the stack without removing it'''
        if self.__top:
            return self.__top.get_data()
        else:
            return None
    
#%%

class Queue:
    '''implements a queue data structure using a linked list as an underlying 
    data structure'''
    
    def __init__(self, max_length):
        '''initializes an empty queue with the set maximum length'''
        self.__max_length=max_length
        self.__length=0
        self.__front_node=None
        self.__back_node=None
        
    def get_length(self):
        return self.__length
    
    def peek(self):
        '''reveals data from the front of the queue without removing it'''
        if self.__front_node:
            return self.__front_node.get_data()
        else:
            return None
        
    def enqueue(self, value):
        '''adds data to the end of the queue'''
        if self.__length == self.__max_length:
            class QueueOverflow(Exception):
                def __init__(self, message):
                    self.message=message
            raise QueueOverflow('reached maximum length of the queue')
        elif self.__length == 0:
            t=Node(value)
            self.__front_node=t
            self.__back_node=t
            self.__front_node.set_next_node(self.__back_node)
            self.__length+=1
        else:
            t=Node(value)
            self.__back_node.set_next_node(t)
            self.__back_node=t
            self.__length+=1
            
    def dequeue(self):
        '''provides and removes data from the front of the queue'''
        if self.__length==0:
            class QueueUnderflow(Exception):
                def __init__(self, message):
                    self.message=message
            raise QueueUnderflow('attempted to dequeue an element of an empty queue')
        else:
            t=self.__front_node
            self.__front_node=self.__front_node.get_next_node()
            self.__length-=1
            return t.get_data()
    
        
#%%

class MinHeap:
    '''min heap implemented using a list \n
    root is index 0
    parent = (index-1)//2 #except at root
    left child = (index*2)+1
    right child = (index*2)+2
    '''
    def __init__(self):
        '''initializes an empty min heap'''
        self.__heap=[]
        
    def get_size(self):
        return len(self.__heap)
    
    def get_heap(self):
        '''returns the list used to create the heap'''
        return self.__heap
    
    def __heapify_up(self):
        idx=len(self.__heap)-1
        parent_idx=(idx-1)//2
        while parent_idx>=0:
            if self.__heap[idx] < self.__heap[parent_idx]:
                t=self.__heap[parent_idx]
                self.__heap[parent_idx]=self.__heap[idx]
                self.__heap[idx]=t
            idx=parent_idx
            parent_idx=(idx-1)//2
            
    def __heapify_down(self):
        idx=0
        left_idx=idx*2+1
        right_idx=idx*2+2
        while left_idx < self.get_size()-1:
            if self.__heap[left_idx] < self.__heap[right_idx]:
                lesser_child=self.__heap[left_idx]
                self.__heap[left_idx]=self.__heap[idx]
                self.__heap[idx]=lesser_child
                idx=left_idx
                left_idx=idx*2+1
                right_idx=idx*2+2
            else:
                lesser_child=self.__heap[right_idx]
                self.__heap[right_idx]=self.__heap[idx]
                self.__heap[idx]=lesser_child
                idx=right_idx
                left_idx=idx*2+1
                right_idx=idx*2+2
            
            
    def add(self, value):
        '''adds a value to the heap and updates the values to mantain the min rule'''
        self.__heap.append(value)
        self.__heapify_up()
        
    def pop(self):
        '''returns and removes the minimum value of the heap, updates the values 
        to mantain the min rule'''
        if self.get_size() == 0:
            class EmptyHeap(Exception):
                def __init__(self, message):
                    self.message=message
            raise EmptyHeap('attempted to pop an element from an empty heap')
        else:
            rightmost_child=self.__heap.pop(self.get_size()-1)
            min_val=self.__heap[0]
            self.__heap[0]=rightmost_child
            self.__heapify_down()
            return min_val
        
#%%

class MaxHeap:
    '''max heap implemented using a list \n
    root is index 0
    parent = (index-1)//2 #except at root
    left child = (index*2)+1
    right child = (index*2)+2
    '''
    
    def __init__(self):
        self.__heap=[]
        
    def get_size(self):
        return len(self.__heap)
    
    def get_heap(self):
        '''returns the list used to create the heap'''
        return self.__heap
    
    def __heapify_up(self):
        idx=len(self.__heap)-1
        parent_idx=(idx-1)//2
        while parent_idx>=0:
            if self.__heap[idx]>self.__heap[parent_idx]:
                t=self.__heap[parent_idx]
                self.__heap[parent_idx]=self.__heap[idx]
                self.__heap[idx]=t
            idx=parent_idx
            parent_idx=(idx-1)//2
            
    def __heapify_down(self):
        idx=0
        left_idx=idx*2+1
        right_idx=idx*2+2
        while left_idx < self.get_size()-1:
            if self.__heap[left_idx] > self.__heap[right_idx]:
                lesser_child=self.__heap[left_idx]
                self.__heap[left_idx]=self.__heap[idx]
                self.__heap[idx]=lesser_child
                idx=left_idx
                left_idx=idx*2+1
                right_idx=idx*2+2
            else:
                lesser_child=self.__heap[right_idx]
                self.__heap[right_idx]=self.__heap[idx]
                self.__heap[idx]=lesser_child
                idx=right_idx
                left_idx=idx*2+1
                right_idx=idx*2+2
            
            
    def add(self, value):
        '''adds a value to the heap and updates the values to mantain the max rule'''
        self.__heap.append(value)
        self.__heapify_up()
        
    def pop(self):
        '''returns and removes the minimum value of the heap, updates the values 
        to mantain the max rule'''
        if self.get_size() == 0:
            class EmptyHeap(Exception):
                def __init__(self, message):
                    self.message=message
            raise EmptyHeap('attempted to pop an element from an empty heap')
        else:
            rightmost_child=self.__heap.pop(self.get_size()-1)
            max_val=self.__heap[0]
            self.__heap[0]=rightmost_child
            self.__heapify_down()
            return max_val
        
#%%

class Vertex:
    
    def __init__(self, value):
        self.__value=value
        self.__edges={}
        
    def __repr__(self):
        return 'Vertex({})'.format(repr(self.__value))
        
    def add_edge(self, vertex, weight=0):
        self.__edges[vertex]=weight
    
    def get_value(self):
        return self.__value
    
    def get_edges(self):
        return list(zip(self.__edges.keys(), self.__edges.values()))
    
#%%

class Graph:
    
    def __init__(self, directed=False):
        self.__directed=directed
        self.__graph_dict={}
        
    def get_graph(self):
        '''dictionary with all vertices found in the graph'''
        return self.__graph_dict
    
    def add_vertex(self, vertex_value):
        '''adds a vertex to the graph using the specified value'''
        self.__graph_dict[vertex_value]=Vertex(vertex_value)
        
    def add_edge(self, from_vertex, to_vertex, weight=0):
        '''adds an edge between two vertices within the graph, both specified by value'''
        self.__graph_dict[from_vertex].add_edge(self.__graph_dict[to_vertex], weight)
        if not self.__directed:
            self.__graph_dict[to_vertex].add_edge(self.__graph_dict[from_vertex], weight)
            
    def find_path(self, start_vertex, end_vertex):
        path=[self.__graph_dict[start_vertex]]
        visited=[]
        while path:
            current_vertex=path.pop(0)
            if (current_vertex.get_value() == self.__graph_dict[end_vertex].get_value()) :
                return True
            else:
                visited.append(current_vertex.get_value())
                path+=[v for v,w in current_vertex.get_edges() if v.get_value() not in visited]
        return False
            
    def dfs(self, start_vertex, end_vertex, traverse=False):
        '''DFS algorithm, outputs a topological sort if traverse is set to True'''
        s=Stack(len(self.__graph_dict.keys()))
        visited=[]
        out=[]
        s.push(self.__graph_dict[start_vertex])
        while s.get_size()>0:
            current_vertex=s.peek()
            if not traverse and current_vertex.get_value() == end_vertex:
                visited.append(current_vertex.get_value())
                return visited
            if current_vertex.get_value() not in visited:
                visited.append(current_vertex.get_value())
            next_vertices=[v for v,w in current_vertex.get_edges() if v.get_value() not in visited]
            if not next_vertices:
                out.append(s.pop().get_value())
            else:
                s.push(next_vertices.pop(0))
        return out[::-1]
                
    def bfs(self, start_vertex, end_vertex):
        queue=[self.__graph_dict[start_vertex]]
        path=[]
        visited=[]
        prev=[None]
        while queue:
            current_vertex=queue[0]
            if current_vertex.get_value() not in visited:
                visited.append(current_vertex.get_value())
            neighbors=[v for v,w in current_vertex.get_edges() if v.get_value() not in visited]
            if not neighbors:
                queue.pop(0)
                continue
            for vertex in neighbors:
                queue.append(vertex)
                visited.append(vertex.get_value())
                prev.append(current_vertex.get_value())
        now=end_vertex
        if self.find_path(start_vertex, end_vertex):
            while now != start_vertex:
                path.append(now)
                i=visited.index(now)
                p=prev[i]
                now=p
            path.append(start_vertex)
            return path[::-1]
        else:
            return None
                
                
                
