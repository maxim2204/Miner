from PyQt5 import Qt

class MyButton(Qt.QPushButton):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def mousePressEvent(self, event):
        button = event.button()
        if button == Qt.Qt.RightButton:
            self.setStyleSheet("""QPushButton{
                    background-color: #aaaaff;
                    border: 2px solid black;
                    border-radius: 5px;
                }
                """)
            self.setText("cheats were activated")
        return Qt.QPushButton.mousePressEvent(self, event)

class Widget(Qt.QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__()
        layout = Qt.QGridLayout(self)
        for i in range(8):
            for j in range(8):
                layout.addWidget(MyButton("Button[{}, {}]".format(i, j)), i, j)


if __name__ == '__main__':
    app = Qt.QApplication([])
    w = Widget()
    w.show()
    app.exec()