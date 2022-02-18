class Memory:

    def __init__(self, name):  # memory name
        self.name = name
        self.memory = {} #dict

    def has_key(self, name):  # variable name
        return name in self.memory

    def get(self, name):  # gets from memory current value of variable <name>
        return self.memory[name]

    def put(self, name, value):  # puts into memory current value of variable <name>
        self.memory[name] = value


class MemoryStack:
    def __init__(self, memory=None):
        self.memoryStack = []
        self.size = 0
        if memory:
            self.memoryStack.append(memory)
            self.size += 1

    def get(self, name):
        i = self.size - 1
        while i >= 0:
            if self.memoryStack[i].has_key(name):
                return self.memoryStack[i].get(name)
            i -= 1
        return None

    def insert(self, name, value):
        self.memoryStack[-1].put(name, value)

    def set(self, name, value):
        i = self.size - 1
        while i >= 0:
            if self.memoryStack[i].has_key(name):
                self.memoryStack[i].put(name, value)
                return
            i -= 1
        self.insert(name, value)

    def push(self, memory):
        self.memoryStack.append(memory)
        self.size += 1

    def pop(self):
        if self.size <= 0:
            raise Exception("Cannot pop from empty memory stack!")
        self.size -= 1
        return self.memoryStack.pop()
