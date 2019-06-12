import sys
from PyQt5 import QtWidgets, Qt
from PyQt5.QtWidgets import QMessageBox
from map_model import MapModel
from button2 import MyButton2
from digitalClock import DigitalClock

class MinerMap(QtWidgets.QWidget):

    def __init__(self, h, w, b, cheat, parent):
        super().__init__(parent)
        self.w = w
        self.h = h
        self.b = b

        self.initUI()

        self.cheat = cheat

        self.MAP = MapModel(h, w , b)

        self.cart = self.MAP.generate()

        self.win = False
        self.end = False
        self.bomb = "💣"

        if self.cheat == 1:
            self.cheats()

    def initUI(self):

        grid = QtWidgets.QGridLayout()
        vbox = QtWidgets.QVBoxLayout()
        hbox = QtWidgets.QHBoxLayout()

        self.clock = DigitalClock(self)
        self.clock.stop()

        buts = []

        for i in range(self.h):
            buts.append([])
            for j in range(self.w):
                #buts[-1].append(QtWidgets.QPushButton("{} {}".format(i,j), self))
                buts[-1].append(MyButton2("*+", self))
                buts[-1][-1].setMinimumSize(25, 25)
                buts[-1][-1].setMaximumSize(25, 25)
                buts[-1][-1].clicked.connect(self.btnclick)
                grid.addWidget(buts[i][j],i, j)
        self.buts = buts
        hbox.addStretch()
        hbox.addWidget(self.clock)
        hbox.addStretch()
        vbox.addLayout(hbox)
        vbox.addLayout(grid)

        self.setLayout(vbox)
        self.show()

    """def onMiddleClick(self, button):
        for i in range(self.h):
            if button in self.buts[i]:
                j = self.buts[i].index(button)
            else:
                continue
        print(i,j)


    def getbuts(self):
        return self.buts"""

    def btnclick(self):


        if self.MAP.open == 0:
            self.clock.reset()
            self.clock.start()


        for i in range(self.h):
            if self.sender() in self.buts[i]:
                j = self.buts[i].index(self.sender())
            else:
                continue

            result = self.MAP.btnclick(i, j, Qt.Qt.LeftButton)
            if result["type"] == "cell":
                self.buts[i][j].setText(result["value"])
            elif result["type"] == "cell_ZERO":
                x = result["value"]
                for i in x:
                    self.buts[i[0]][i[1]].setText(i[2])
            elif result["type"] == "mine":
                x = result["bombs"]
                for i in x:
                    self.buts[i[0]][i[1]].setText(self.bomb)
                self.disabled(True)
                self.clock.stop()
            elif result["type"] == "win_cell":
                x = result["value"]
                self.buts[i][j].setText(x)
                self.disabled(True)
                self.clock.stop()





    """def set_text(self,i,j):
        if self.cart[i][j] != "*" and self.buts[i][j].isEnabled():
            self.buts[i][j].setText(str(self.cart[i][j]))
            self.buts[i][j][1] == "-"
            self.open += 1
            print(i, "", j, "", self.open,"/",self.h * self.w - self.b, "no_mins")
            if self.cart[i][j] == 0:
                self.no_mins(i,j)



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
                print(x,y)"""


    def disabled(self, TF):
        for i in range(self.h):
            self.buts.append([])
            for j in range(self.w):
                self.buts[i][j].setDisabled(TF)




if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    ex = MinerMap(8, 5, 5, 1, None)
    sys.exit(app.exec_())