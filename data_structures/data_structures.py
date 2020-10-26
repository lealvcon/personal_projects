class Node:
    '''Implementation of a node to work with data structures'''
    
    def __init__(self, data, next_node=None):
        """assigns the data to the node while initializing its link as None"""
        self.data=data
        self.next_node=next_node
        
    def __repr__(self):
        return "Node({0}, {1})".format(repr(self.data),repr(self.next_node))
        
    def set_data(self, data):
        '''assigns the specified data to the node'''
        self.data=data
        
    def get_data(self):
        '''retrieve the data contained in this node'''
        return self.data
    
    def set_next_node(self, node):
        '''sets the link this node points to'''
        self.next_node=node
        
    def get_next_node(self):
        '''retrieve the node this node points to'''
        return self.next_node
    
#%%
    
class LinkedList:
    '''Linked list class with iterables implemented. each element is a Node
    class object. see reference for Node'''
    def __init__(self):
        '''Initializes an empty linked list'''
        self.head_node=None
        self.size=0
        
    def __iter__(self):
        self.i=0
        self.current_node=self.head_node
        return self
    
    def __next__(self):
        if self.i < self.size:
            n=self.current_node
            self.current_node=self.current_node.get_next_node()
            self.i+=1
            return n
        else:
            raise StopIteration
          
    def get_size(self):
        '''returns the size of the linked list'''
        return self.size
    
    def add_node(self, new_node):
        '''appends a node to the linked list as the new head node and creates 
         a link to the previous head node. if the linked list is empty it assigns
         the new node as the head and tail'''
        if self.size == 0:
            self.head_node=new_node
            self.size+=1
        else:
            new_node.set_next_node(self.head_node)
            self.head_node=new_node
            self.size+=1
            
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
        if self.size == 0:
            raise IndexError('attempting to remove a node from an empty linked list')
        elif self.head_node.get_data() == data:
            self.head_node=self.head_node.get_next_node()
            self.size-=1
        else:
            prev_node=self.head_node
            current_node=self.head_node.get_next_node()
            while current_node:
                if current_node.get_data() == data:
                    prev_node.set_next_node(current_node.get_next_node())
                    self.size-=1
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
        self.max_size=max_size
        self.size=0
        self.top=None
        
    def push(self, value):
        '''adds the specified value to the top of the stack'''
        if self.size == self.max_size:
            class StackOverflow(Exception):
                def __init__(self,message):
                    self.message=message
            raise StackOverflow('reached maximum capacity of the stack')
        else:
            t=Node(value)    
            t.set_next_node(self.top)
            self.top=t
            self.size+=1
        
    def pop(self):
        '''returns and removes data from the top of the stack'''
        if self.size == 0:
            class StackUnderflow(Exception):
                def __init__(self, message):
                    self.message=message
            raise StackUnderflow('attempted to remove an element from an empty stack')
        else:    
            t=self.top
            self.top=self.top.get_next_node()
            self.size-=1
            return t.get_data()
        
    def get_size(self):
        return self.size
    
    def peek(self):
        '''returns data from the top of the stack without removing it'''
        if self.top:
            return self.top.get_data()
        else:
            return None
    
#%%

class Queue:
    '''implements a queue data structure using a linked list as an underlying 
    data structure'''
    
    def __init__(self, max_length):
        '''initializes an empty queue with the set maximum length'''
        self.max_length=max_length
        self.length=0
        self.front_node=None
        self.back_node=None
        
    def get_length(self):
        return self.length
    
    def peek(self):
        '''reveals data from the front of the queue without removing it'''
        if self.front_node:
            return self.front_node.get_data()
        else:
            return None
        
    def enqueue(self, value):
        '''adds data to the end of the queue'''
        if self.length == self.max_length:
            class QueueOverflow(Exception):
                def __init__(self, message):
                    self.message=message
            raise QueueOverflow('reached maximum length of the queue')
        elif self.length == 0:
            t=Node(value)
            self.front_node=t
            self.back_node=t
            self.front_node.set_next_node(self.back_node)
            self.length+=1
        else:
            t=Node(value)
            self.back_node.set_next_node(t)
            self.back_node=t
            self.length+=1
            
    def dequeue(self):
        '''provides and removes data from the front of the queue'''
        if self.length==0:
            class QueueUnderflow(Exception):
                def __init__(self, message):
                    self.message=message
            raise QueueUnderflow('attempted to dequeue an element of an empty queue')
        else:
            t=self.front_node
            self.front_node=self.front_node.get_next_node()
            self.length-=1
            return t
    
        
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
        self.heap=[]
        
    def get_size(self):
        return len(self.heap)
    
    def get_heap(self):
        '''returns the list used to create the heap'''
        return self.heap
    
    def heapify_up(self):
        idx=len(self.heap)-1
        parent_idx=(idx-1)//2
        while parent_idx>=0:
            if self.heap[idx] < self.heap[parent_idx]:
                t=self.heap[parent_idx]
                self.heap[parent_idx]=self.heap[idx]
                self.heap[idx]=t
            idx=parent_idx
            parent_idx=(idx-1)//2
            
    def heapify_down(self):
        idx=0
        left_idx=idx*2+1
        right_idx=idx*2+2
        while left_idx < self.get_size()-1:
            if self.heap[left_idx] < self.heap[right_idx]:
                lesser_child=self.heap[left_idx]
                self.heap[left_idx]=self.heap[idx]
                self.heap[idx]=lesser_child
                idx=left_idx
                left_idx=idx*2+1
                right_idx=idx*2+2
            else:
                lesser_child=self.heap[right_idx]
                self.heap[right_idx]=self.heap[idx]
                self.heap[idx]=lesser_child
                idx=right_idx
                left_idx=idx*2+1
                right_idx=idx*2+2
            
            
    def add(self, value):
        '''adds a value to the heap and updates the values to mantain the min rule'''
        self.heap.append(value)
        self.heapify_up()
        
    def pop(self):
        '''returns and removes the minimum value of the heap, updates the values 
        to mantain the min rule'''
        if self.get_size() == 0:
            class EmptyHeap(Exception):
                def __init__(self, message):
                    self.message=message
            raise EmptyHeap('attempted to pop an element from an empty heap')
        else:
            rightmost_child=self.heap.pop(self.get_size()-1)
            min_val=self.heap[0]
            self.heap[0]=rightmost_child
            self.heapify_down()
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
        self.heap=[]
        
    def get_size(self):
        return len(self.heap)
    
    def get_heap(self):
        '''returns the list used to create the heap'''
        return self.heap
    
    def heapify_up(self):
        idx=len(self.heap)-1
        parent_idx=(idx-1)//2
        while parent_idx>=0:
            if self.heap[idx]>self.heap[parent_idx]:
                t=self.heap[parent_idx]
                self.heap[parent_idx]=self.heap[idx]
                self.heap[idx]=t
            idx=parent_idx
            parent_idx=(idx-1)//2
            
    def heapify_down(self):
        idx=0
        left_idx=idx*2+1
        right_idx=idx*2+2
        while left_idx < self.get_size()-1:
            if self.heap[left_idx] > self.heap[right_idx]:
                lesser_child=self.heap[left_idx]
                self.heap[left_idx]=self.heap[idx]
                self.heap[idx]=lesser_child
                idx=left_idx
                left_idx=idx*2+1
                right_idx=idx*2+2
            else:
                lesser_child=self.heap[right_idx]
                self.heap[right_idx]=self.heap[idx]
                self.heap[idx]=lesser_child
                idx=right_idx
                left_idx=idx*2+1
                right_idx=idx*2+2
            
            
    def add(self, value):
        '''adds a value to the heap and updates the values to mantain the max rule'''
        self.heap.append(value)
        self.heapify_up()
        
    def pop(self):
        '''returns and removes the minimum value of the heap, updates the values 
        to mantain the max rule'''
        if self.get_size() == 0:
            class EmptyHeap(Exception):
                def __init__(self, message):
                    self.message=message
            raise EmptyHeap('attempted to pop an element from an empty heap')
        else:
            rightmost_child=self.heap.pop(self.get_size()-1)
            max_val=self.heap[0]
            self.heap[0]=rightmost_child
            self.heapify_down()
            return max_val
    


            