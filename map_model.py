import random

class MapModel(object):
    NOT_CLICKED_EMPTY = "0+"
    NOT_CLICKED_BOMB = "*+"
    def __init__(self, h, w, b):
        self.h = h
        self.w = w
        self.b = b
        assert self.b <= self.h * self.w
        self.generate()


    def generate(self):
        self.map = []
        for i in range(self.h):
            self.map.append([])
            for j in range(self.w):
                self.map[-1].append(self.NOT_CLICKED_EMPTY)

        w = random.randint(0, self.w - 1)
        h = random.randint(0, self.h - 1)

        for b in range(self.b):
            while self.map[h][w] != self.NOT_CLICKED_EMPTY:
                w = random.randint(0,self.w-1)
                h = random.randint(0,self.h-1)
            self.map[h][w] = self.NOT_CLICKED_BOMB
        self.map = self.count_mins()
        return self.map


    def cell_value(self, i , j):
        return self.map[i][j]

    def is_bomb(self, i, j):
        return self.map[i][j] == self.NOT_CLICKED_BOMB

    def is_not_click_bomb(self, i, j):
        return self.map[i][j] == self.NOT_CLICKED_BOMB

    def get_all_bombs(self):
        all_map = []
        for i in range(self.h):
            for j in range(self.w):
                if self.map[i][j] == self.NOT_CLICKED_BOMB:
                    all_map.append([i,j])
        self.all_map = all_map
        return self.all_map

    def count_mins(self):
        for i in range(self.h):
            for j in range(self.w):
                if  self.map[i][j] != "*+":
                    count = 0
                    if i != self.h -1 and j != self.w - 1:
                        if self.map[i+1][j+1] == "*+":
                            count += 1
                    if i != 0 and j != 0:
                        if self.map[i-1][j-1] == "*+":
                            count += 1
                    if i != 0 and j != self.w - 1:
                        if self.map[i-1][j+1] == "*+":
                            count += 1
                    if i != self.h - 1 and j != 0:
                        if self.map[i+1][j-1] == "*+":
                            count += 1
                    if j != self.w - 1:
                        if self.map[i][j+1] == "*+":
                            count += 1
                    if i != self.h - 1:
                        if self.map[i+1][j] == "*+":
                            count += 1
                    if j != 0:
                        if self.map[i][j-1] == "*+":
                            count += 1
                    if i != 0:
                        if self.map[i-1][j] == "*+":
                            count += 1
                    self.map[i][j] = str(count)+"+"
        print(self.map)
        return self.map

    def btnclick(self):
        pass

x = MapModel(8,10,2)
#print(x.generate())
