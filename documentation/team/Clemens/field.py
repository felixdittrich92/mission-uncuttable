class Field:

    def __init__(self, size):
        self.size = size
        self.buttons = []

    def get_neighbours(self, x, y):
        res = []
        for i in range(self.size):
            for j in range(self.size):
                if j == y and ((i-1) == x or (i+1) == x):
                    res.append((i*self.size) + j)
                elif x == i and ((j-1) == y or (j+1) == y):
                    res.append((i*self.size) + j)

        return res

    def is_won(self):
        for b in self.buttons:
            if b.cget("bg") == "white":
                return False

        return True
