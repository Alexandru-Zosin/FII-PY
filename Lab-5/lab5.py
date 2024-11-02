# 1. Write a Python class that simulates a Stack. 
# The class should implement methods like push, pop, peek 
# (the last two methods should return None if no element is present in the stack).
class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        if len(self.items) == 0:
            return True
        else:
            return False

    def size(self):
        return len(self.items)

    def push(self, *new_items):
        for item in new_items:
            self.items.append(item)

    def pop(self):
        if self.is_empty():
            return None
        else:
            return self.items.pop()

    def peek(self):
        if self.items.count != 0:
            return self.items[-1]
        else:
            return None

# 2. Write a Python class that simulates a Queue. 
# The class should implement methods like push, pop, peek 
# (the last two methods should return None if no element is present in the queue).

class Queue:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def push(self, *new_items):
        for item in new_items:
            self.items.append(item)

    def pop(self):
        if self.is_empty():
            return None
        else:
            return self.items.pop(0)

    def peek(self):
        if not self.is_empty():
            return self.items[0]
        else:
            return None

# 3. Write a Python class that simulates a matrix of size NxM, with N and M provided at initialization.
# The class should provide methods to access elements (get and set methods) and some mathematical 
# functions such as transpose, matrix multiplication and a method that allows iterating through all 
# elements from a matrix and apply a transformation over them (via a lambda function).

class Matrix:
    def __init__(self, n, m):
        self.rows = n
        self.columns = m
        self.matrix = [[0 for j in range(m)] for i in range (n)]

    def get(self, i, j):
        if 0 <= i < self.rows and 0 <= j < self.columns:
            return self.matrix[i][j]
        else:
            return None

    def set(self, i, j, value):
        if 0 <= i < self.rows and 0 <= j < self.columns:
            self.matrix[i][j] = value
        else:
            print("Invalid position.")

    def transpose(self):
        result = Matrix(self.columns, self.rows)
        for i in range(self.rows):
            for j in range(self.columns):
                result.matrix[j][i] = self.matrix[i][j]
        return result

    def multiply(self, other):
        if self.columns != other.rows:
            print("Invalid dimensions for multiplication")
            return None 

        result = Matrix(self.rows, other.columns)
        
        for i in range(self.rows):
            for j in range(other.columns):
                sum = 0
                for k in range(self.columns):
                    sum += self.matrix[i][k] * other.matrix[k][j]
                result.matrix[i][j] = sum
        return result

    def items_transformation(self, lambda_func):
        for i in range(self.rows):
            for j in range(self.columns):
                self.matrix[i][j] = lambda_func(self.matrix[i][j])

    def display(self):
        for i in range(self.rows):
            for j in range(self.columns):
                print(self.matrix[i][j], end=" ")
            print()

if __name__ == "__main__":
    ###
    stack = Stack()
    stack.push(1)
    stack.push(2, 3)
    print("size:", stack.size())  # should be 3

    print("peek:", stack.peek())  # should be 3
    stack.pop()
    print(stack.pop()) # should be 2
    stack.pop()
    print(stack.pop()) # should be None

    ###
    queue = Queue()
    queue.push(1)
    queue.push(2, 3)
    print("size:", queue.size())  # should be 3

    print("peek:", queue.peek())  # should be 1
    print("pop:", queue.pop())    # should be 1
    queue.pop()
    print("pop:", queue.pop())    # should be 3
    print("pop:", queue.pop())    # should be None
    print("pop:", queue.pop())    # should be None

    ###
    matrix = Matrix(2, 3)
    print("initial matrix (with 0s):")
    matrix.display()

    print()
    matrix.set(0, 1, 5) # 050  007
    matrix.set(1, 2, 7)
    matrix.display()

    print()
    print(matrix.get(0, 1))  # should be 5
    print(matrix.get(1, 2))    # should be 7
    print(matrix.get(2, 2))    # should be None

    print()
    transposed = matrix.transpose()
    transposed.display() # 00 50 07

    other = Matrix(3, 2)
    other.set(0, 0, 1)
    other.set(1, 1, 1)
    other.set(2, 0, 1)

    print
    product = matrix.multiply(other)
    product.display() # 05 70

    print()
    matrix.items_transformation(lambda item: (item + 1) * 2)
    matrix.display() # 2-12-2 2-2-16 