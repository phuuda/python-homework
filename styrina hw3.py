#Sofia Styrina

class Stack:
    def __init__(self, arr = []):
        self.arr = []
    
    def push(self, item): # кладет эл-т в конец очереди
        self.arr.append(item) # no return needed
    
    def pop(self): # убрать из очереди новейший эл-т
        n = self.arr[-1]
        self.arr.pop()
        return(n) # вернуть удаленный объект
    
    def peek(self): # возвращает новейший эл-т очереди, не удаляет
        return(self.arr[-1])

    def isEmpty(self): # returns True/False
        if len(self.arr) == 0:
            return(True)
        else:
            return(False)

class Queue:
    def __init__(self, stack1 = [], stack2 = []):
        self.stack1 = Stack()
        self.stack2 = Stack()

    def enqueue(self, item): # add to stack1
        self.stack1.arr.append(item)
        return(self.stack1.arr) # no return needed
            
    def dequeue(self):
        x = self.stack1.arr[0]
        
        for i in range(len(self.stack1.arr)): # move all items from stack1 to stack2
            n = self.stack1.arr[-1]
            self.stack1.pop()
            self.stack2.push(n)

        self.stack2.pop() # pop from stack2
        for i in range(len(self.stack2.arr)): # move all items from stack2 to stack1
            n = self.stack2.arr[-1]
            self.stack2.pop()
            self.stack1.push(n)
            
        return(x)
                        
    def peek(self): # return oldest [0] item from stack1
        return(self.stack1.arr[0])
                        
    def isEmpty(self): # check if stack1 is empty
        if len(self.stack1.arr) == 0:
            return(True)
        else:
            return(False)
        
q = Queue()
q.enqueue(1)
q.enqueue(2)
q.enqueue(3)
q.enqueue(4)
print(q.enqueue(5))

print(q.dequeue())
print(q.stack1.arr)

q.enqueue(6)
q.enqueue(7)
q.dequeue()
print(q.stack1.arr)

print(q.peek())
print(q.isEmpty())
