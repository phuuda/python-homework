class Node:
    def __init__(self, data, next = None):
        self.data = data                    # node info
        self.next = next                    # connected node

class LinkedList:
    def __init__(self, head = None):
        self.head = head

    def empty(self):
        if self.head:
            return False
        return True

    def printList(self):
        node = self.head
        while node:
            print(node.data, end = "->")
            node = node.next
        print()

    def size(self):
        node = self.head
        i = 0
        while node:
            node = node.next
            i += 1
        return(i)
            
    def push(self, data):               # adds element as head O(1)
        node = Node(data, next = self.head)
        self.head = node

    def append(self, data):             # adds element to end O(n)
        new_node = Node(data)
        if not self.head:               # if head is missing
            self.head = new_node
        else:
            node = self.head
            while node.next:            # run through all nodes
                node = node.next
            node.next = new_node        # add to last node

    def delete(self, value):            # delete first occurance of value
        if self.head is not None:
            node = self.head

            if node.data == value:          # delete head
                if node.next is not None:
                    self.head = node.next
                else:
                    self.head = None

            else:                           # delete not head
                while node is not None:
                    node2 = node.next
                    if node2.data == value:
                        node.next = node2.next
                        return True
                    else:
                        node = node.next

    def insert(self, index, value):
        if index == 0:
            self.push(value)
            
        elif index > self.size():
            print("index out of range")

        elif index == self.size():
            self.append(value)

        else:
            temp = Node(value, index)
            curr = self.head
            prev = None
            curr_index = 0

            while curr_index != index:
                prev = curr
                curr = curr.next
                curr_index += 1

            prev.next = temp
            temp.next = curr


    def reverse(self):
        prev = None
        curr = self.head
        while curr is not None:
            next = curr.next
            curr.next = prev
            prev = curr
            curr = next
        self.head = prev


n3 = Node(3)
n2 = Node(2, next = n3)
n1 = Node(1, next = n2)

l = LinkedList(head = n1)
for i in [1,2,3,4,5,4,5,6,6,6,6,1,1,54]:
    l.append(i)
    
l.printList()
print(l.size())
print('\n')

l.delete(5)

l.printList()
print(l.size())
print('\n')

l.insert(3, 13)
l.printList()
print(l.size())
print('\n')

l.reverse()
l.printList()
print(l.size())

