from PyQt5.QtWidgets import QLCDNumber
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import QTime
from PyQt5 import Qt


class DigitalClock(QLCDNumber):
    def __init__(self, parent):
        super().__init__(parent)
        self.setDigitCount(9)
        self.setSegmentStyle(QLCDNumber.Filled);
        self.i = 0
        self.timer = QTimer(self)
        #self.time = QTime()
        #self.time.start()
        self.timer.timeout.connect(self.showTime)
        self.timer.start(1000)
        self.showTime()

    def showTime(self):
        #time = self.time.elapsed()
        #self.text = self.time.toString("hh:mm:ss")
        self.display(str(self.i))
        self.i += 1


    def reset(self):
        self.i = 0
        #self.time.restart()
        self.showTime()

    def stop(self):
        self.timer.stop()

    def start(self):
        self.timer.start(1000)

if __name__ == '__main__':
    app = Qt.QApplication([])
    w = DigitalClock(None)
    w.show()
    app.exec()