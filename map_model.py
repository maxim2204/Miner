import random
from PyQt5 import Qt

from PyQt5 import QtCore

class MapModel(object):
    NOT_CLICKED_EMPTY = "0+"
    NOT_CLICKED_BOMB = "*+"
    # NOT_CLICKED_CELL and CLICKED_CELL chars are appended to the matrix value as 2nd chars
    NOT_CLICKED_CELL = "+"
    CLICKED_CELL = "-"
    def __init__(self, h, w, b):
        self.h = h
        self.w = w
        self.b = b
        assert self.b <= self.h * self.w
        self.generate()


    def generate(self):
        self.map = []
        self.open = 0
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
                if  self.map[i][j] != self.NOT_CLICKED_BOMB:
                    count = 0
                    if i != self.h -1 and j != self.w - 1:
                        if self.map[i+1][j+1] == self.NOT_CLICKED_BOMB:
                            count += 1
                    if i != 0 and j != 0:
                        if self.map[i-1][j-1] == self.NOT_CLICKED_BOMB:
                            count += 1
                    if i != 0 and j != self.w - 1:
                        if self.map[i-1][j+1] == self.NOT_CLICKED_BOMB:
                            count += 1
                    if i != self.h - 1 and j != 0:
                        if self.map[i+1][j-1] == self.NOT_CLICKED_BOMB:
                            count += 1
                    if j != self.w - 1:
                        if self.map[i][j+1] == self.NOT_CLICKED_BOMB:
                            count += 1
                    if i != self.h - 1:
                        if self.map[i+1][j] == self.NOT_CLICKED_BOMB:
                            count += 1
                    if j != 0:
                        if self.map[i][j-1] == self.NOT_CLICKED_BOMB:
                            count += 1
                    if i != 0:
                        if self.map[i-1][j] == self.NOT_CLICKED_BOMB:
                            count += 1
                    self.map[i][j] = str(count) + self.NOT_CLICKED_CELL
        print(self.map)
        return self.map

    def all_open(self):
        return self.open == self.h * self.w - self.b

    def no_mins(self,i,j, clicked_cells = None):
        if clicked_cells is None:
            clicked_cells = []
        # collect list of clicked_cells
        if not self.all_open():
            if i != self.H - 1 and j != self.W - 1:
                    self.click_cell(i+1,j+1)
                    clicked_cells.append((i+1, j+1, self.map[i+1][j+1][0]))
            if i != 0 and j != 0:
                    self.click_cell(i - 1, j - 1)

            if i != 0 and j != self.W - 1:
                    self.click_cell(i - 1, j + 1)

            if i != self.H - 1 and j != 0:
                    self.click_cell(i + 1, j - 1)

            if j != self.W - 1:
                    self.click_cell(i, j + 1)

            if i != self.H - 1:
                    self.click_cell(i + 1, j)

            if j != 0:
                    self.click_cell(i, j - 1)

            if i != 0:
                    self.click_cell(i - 1, j)

        else:
            self.game_end("no_mins", "win")

    def click_cell(self,i,j):
        if self.cart[i][j][0] != self.NOT_CLICKED_BOMB[0]:
            self.open += 1
            self.map[i][j] = self.map[i][j][0] + self.CLICKED_CELL
            if self.cart[i][j] == self.NOT_CLICKED_EMPTY:
                self.no_mins(i,j)
        return self.all_open()


    def btnclick(self, i, j, mouseBut=Qt.Qt.LeftButton):
        if mouseBut == Qt.Qt.LeftButton:
            if self.map[i][j][1] == self.CLICKED_CELL:
                return {"type":"already_clicked"}
            elif self.map[i][j] == self.NOT_CLICKED_BOMB:
                return {"type" : "mine",
                        "bombs": self.get_all_bombs()}
            elif self.map[i][j][0] in '12345678':
                if self.click_cell(i, j): # last
                    return {"type" : "win_cell",
                            "value" : self.map[i][j][0]}
                else:
                    return {"type": "cell",
                            "value": self.map[i][j][0]}
            elif self.map[i][j] == self.NOT_CLICKED_EMPTY:
                self.no_mins(i, j)
                if self.click_cell(i, j): # last
                    return {"type" : "win_cell",
                            "value" : self.map[i][j][0]}
                else:
                    return {"type": "cell",
                            "value": self.map[i][j][0]}



x = MapModel(8,10,2)
#print(x.generate())
