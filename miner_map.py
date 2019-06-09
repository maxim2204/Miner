import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from map_model import MapModel
from button2 import MyButton2
from digitalClock import DigitalClock

class MinerMap(QtWidgets.QWidget):

    def __init__(self, H, W, N, cheat, parent):
        super().__init__(parent)
        self.W = W
        self.H = H
        self.N = N

        self.initUI()

        self.cheat = cheat

        self.MAP = MapModel(H, W , N)

        self.cart = self.MAP.generate()
        print(self.cart)

        self.open = 0
        self.win = False

        self.end = False

        if self.cheat == 1:
            self.cheats()

    def initUI(self):

        grid = QtWidgets.QGridLayout()
        vbox = QtWidgets.QVBoxLayout()

        self.clock = DigitalClock(self)
        self.clock.stop()

        buts = []

        for i in range(self.H):
            buts.append([])
            for j in range(self.W):
                #buts[-1].append(QtWidgets.QPushButton("{} {}".format(i,j), self))
                buts[-1].append(MyButton2("*+", self))
                buts[-1][-1].setMinimumSize(25, 25)
                buts[-1][-1].setMaximumSize(25, 25)
                buts[-1][-1].clicked.connect(self.btnclick)
                grid.addWidget(buts[i][j],i, j)
        self.buts = buts
        vbox.addWidget(self.clock)
        vbox.addLayout(grid)

        self.setLayout(vbox)
        self.show()

    def onMiddleClick(self, button):
        for i in range(self.H):
            if button in self.buts[i]:
                j = self.buts[i].index(button)
            else:
                continue
        print(i,j)


    def getbuts(self):
        return self.buts

    def btnclick(self):

        if self.open == 0:
            self.clock.reset()
            self.clock.start()

        sender = self.sender()

        for i in range(self.H):
            if sender in self.buts[i]:
                j = self.buts[i].index(sender)
            else:
                continue
            if self.MAP.is_bomb(i, j) == True:
                self.game_end("click", "lose")
            else:
                self.buts[i][j].setText(str(self.cart[i][j][0]))
                self.buts[i][j][1] == "-"
                self.open += 1
                print(i, "", j, "", self.open, "/", self.H * self.W - self.N, "click")
                if self.open == self.H * self.W - self.N:
                    self.game_end("click", "win")
            if self.cart[i][j] == 0:
                self.no_mins(i,j)

    def set_text(self,i,j):
        if self.cart[i][j] != "*+" and self.buts[i][j][1] == "+":
            self.buts[i][j].setText(str(self.cart[i][j])[0])
            self.buts[i][j][1] == "-"
            self.open += 1
            print(i, "", j, "", self.open,"/",self.H * self.W - self.N, "no_mins")
            if self.cart[i][j] == 0:
                self.no_mins(i,j)

    def no_mins(self,i,j):
        if self.open != self.H * self.W - self.N:

            if i != self.H - 1 and j != self.W - 1:
                    self.set_text(i+1,j+1)

            if i != 0 and j != 0:
                    self.set_text(i - 1, j - 1)

            if i != 0 and j != self.W - 1:
                    self.set_text(i - 1, j + 1)

            if i != self.H - 1 and j != 0:
                    self.set_text(i + 1, j - 1)

            if j != self.W - 1:
                    self.set_text(i, j + 1)

            if i != self.H - 1:
                    self.set_text(i + 1, j)

            if j != 0:
                    self.set_text(i, j - 1)

            if i != 0:
                    self.set_text(i - 1, j)

        else:
            self.game_end("no_mins", "win")

    def game_end(self, ttype, winorlose):
        self.cheats()
        self.setDisabled(True)
        if self.end == False:
            # self.clock.stop()
            # todo: create method parameter if you need report result to the friend (two different win ttype's)
            self.parent().send(winorlose)  # if self.MODE == 'master' else "dfdfdf"
            massage = QMessageBox.question(self,  "ВИН" if winorlose == "win" else "Мина", "Красавчик" if winorlose == "win" else "ЛОХ", QMessageBox.Close)
            if winorlose == "win":
                self.win = True
            else:
                self.win = False
            self.end = True
            print(ttype)

    def win(self):
        return self.win

    def cheats(self):
        s = self.MAP.get_all_bombs()
        for j in s:
            try:
                x = j[1]
                y = j[0]
                self.buts[y][x].setText("💣")
            except IndexError:
                print(x,y)


    def disabled(self, TF):
        for i in range(self.H):
            self.buts.append([])
            for j in range(self.W):
                self.buts[i][j].setDisabled(TF)




if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    ex = MinerMap(8, 5, 5, 1, None)
    sys.exit(app.exec_())