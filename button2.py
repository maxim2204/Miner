from PyQt5 import Qt, QtCore

class MyButton2(Qt.QPushButton):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setText("")

    def mousePressEvent(self, event):
        button = event.button()
        if button == Qt.Qt.RightButton:
            if self.text() == "":
                self.setText("⚑")
            elif self.text() == "⚑":
                self.setText("")
        elif button == QtCore.Qt.MiddleButton:
            #if "1" <= self.text() <= "8":
            self.parent().onMiddleClick(self)
        return Qt.QPushButton.mousePressEvent(self, event)


class Widget(Qt.QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__()
        layout = Qt.QGridLayout(self)
        for i in range(8):
            for j in range(8):
                layout.addWidget(MyButton2("Button[{}, {}]".format(i, j)), i, j)


if __name__ == '__main__':
    app = Qt.QApplication([])
    w = Widget()
    w.show()
    app.exec()