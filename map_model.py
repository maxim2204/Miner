import random
from PyQt5 import Qt

class MapModel(object):

    NOT_CLICKED_EMPTY = "0+"
    NOT_CLICKED_BOMB = "*+"

    NOT_CLICKED_CELL = "+"
    CLICKED_CELL = "-"


    def __init__(self, h, w, b, parent):
        self.h = h
        self.w = w
        self.b = b
        self.parent = parent
        assert self.b <= self.h * self.w # проверяем что бомб меньше или равно кол-ву клеток
        self.generate() # создаем карту


    def generate(self):
        self.map = []
        self.open = 0
        seed = random.randint(0, 10000000)
        random.seed(seed)
        print("seed = {}".format(seed))
        "Все нули"
        for i in range(self.h):
            self.map.append([])
            for j in range(self.w):
                self.map[-1].append(self.NOT_CLICKED_EMPTY)

        w = random.randint(0, self.w - 1)
        h = random.randint(0, self.h - 1)

        "Добавляем бомбы"
        for b in range(self.b):
            while self.map[h][w] != self.NOT_CLICKED_EMPTY:
                w = random.randint(0,self.w-1)
                h = random.randint(0,self.h-1)
            self.map[h][w] = self.NOT_CLICKED_BOMB

        "Количкство бомб вокруг"
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
        self.pprint(self.map)
        return self.map


    def get_all_bombs(self):
        all_map = []
        for i in range(self.h):
            for j in range(self.w):
                if self.map[i][j] == self.NOT_CLICKED_BOMB:
                    all_map.append([i,j])
        self.all_map = all_map
        return self.all_map


    def all_open(self):
        return self.open == self.h * self.w - self.b

    def no_mins(self,i,j):
        if not self.all_open():
            if i != self.h - 1 and j != self.w - 1:
                    self.click_cell(i+1,j+1)
            if i != 0 and j != 0:
                    self.click_cell(i - 1, j - 1)
            if i != 0 and j != self.w - 1:
                    self.click_cell(i - 1, j + 1)
            if i != self.h - 1 and j != 0:
                    self.click_cell(i + 1, j - 1)
            if j != self.h - 1:
                    self.click_cell(i, j + 1)
            if i != self.h - 1:
                    self.click_cell(i + 1, j)
            if j != 0:
                    self.click_cell(i, j - 1)
            if i != 0:
                    self.click_cell(i - 1, j)
        else:
            self.parent.game_end("win")
        return

    def click_cell(self,i,j):
        try:
            if self.clicked_cells is None:
                pass
        except AttributeError:
            self.clicked_cells = []
        except:
            raise
        # collect list of clicked_cells
        if self.map[i][j][0] in "123456780" and self.map[i][j][1] == self.NOT_CLICKED_CELL:
            self.open += 1
            self.clicked_cells.append((i, j, self.map[i][j][0]))
            if self.map[i][j] == self.NOT_CLICKED_EMPTY:
                self.map[i][j] = self.map[i][j][0] + self.CLICKED_CELL
                self.no_mins(i,j)
            else:
                self.map[i][j] = self.map[i][j][0] + self.CLICKED_CELL
        return self.clicked_cells


    def btnclick(self, i, j, mouseBut=Qt.Qt.LeftButton):
        """нажатие на кнопку"""
        print(self.open)
        if mouseBut == Qt.Qt.LeftButton:
            if self.map[i][j][1] == self.CLICKED_CELL:
                print("already_clicked")
                return {"type":"already_clicked"}

            elif self.map[i][j] == self.NOT_CLICKED_BOMB:
                return {"type" : "mine",
                        "bombs": self.get_all_bombs()}

            elif self.map[i][j][0] in '12345678':
                self.click_cell(i,j)
                if self.all_open():
                    return {"type" : "win_cell",
                            "value" : self.map[i][j][0]}
                else:
                    return {"type": "cell",
                            "value": self.map[i][j][0]}

            elif self.map[i][j] == self.NOT_CLICKED_EMPTY:
                if self.all_open():
                    return {"type" : "win_cell",
                            "value" : self.map[i][j][0]}
                else:
                    print("cell")
                    return {"type": "cell_ZERO",
                        "value": self.click_cell(i,j)}
            elif self.map[i][j][-1] == "F":
                return {"type": "cell_Flag"}



        if mouseBut == Qt.Qt.RightButton:
            if self.map[i][j][-1] == "F":
                self.map[i][j] = self.map[i][j][:-1]
                return {"type": "removeFlag"}
            elif self.map[i][j][-1] == self.NOT_CLICKED_CELL:
                self.map[i][j] = self.map[i][j] + "F"
                return {"type": "addFlag"}
            elif self.map[i][j][-1] == self.CLICKED_CELL:
                return {"type": "clicked"}



    def pprint(self, text):
        """Добавляем красоту"""
        for i in text:
            for j in i:
                print(j[0],end=" ")
            print("")
        print("")

#x = MapModel(4,3,2)
