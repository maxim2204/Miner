import sys
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout, QRadioButton, QSlider, QLabel
from PyQt5.QtGui import QIcon
from button_ import MyButton




class Map_settings(QDialog):

    def __init__(self, parent):
        super().__init__(parent, Qt.Dialog | Qt.Popup)
        self.setWindowTitle('map_settings')
        self.setWindowIcon(QIcon('settings.png'))

        self.setMinimumSize(300, 260)

        self.check_LOW = QRadioButton("LOW")
        self.check_MID = QRadioButton("MID")
        self.check_PRO = QRadioButton("PRO")

        self.hbox_ch = QHBoxLayout()
        self.vbox = QVBoxLayout()

        self.hbox_ch.addWidget(self.check_LOW)
        self.hbox_ch.addWidget(self.check_MID)
        self.hbox_ch.addWidget(self.check_PRO)

        self.lbl_x = QLabel("x")
        self.lbl_x_value = QLabel("0")
        self.slider_x = QSlider(Qt.Horizontal)
        self.lbl_y = QLabel("y")
        self.lbl_y_value = QLabel("0")
        self.slider_y = QSlider(Qt.Horizontal)
        self.lbl_b = QLabel("b")
        self.lbl_b_value = QLabel("0")
        self.slider_b = QSlider(Qt.Horizontal)

        self.slider_x.setMinimum(3)
        self.slider_y.setMinimum(3)
        self.slider_b.setMinimum(2)

        self.slider_x.setMaximum(20)
        self.slider_y.setMaximum(20)
        self.slider_b.setMaximum(100)

        self.slider_x.setValue(2)
        self.slider_y.setValue(2)
        self.slider_b.setValue(2)

        self.btn_ok = MyButton()

        self.vbox.addLayout(self.hbox_ch)
        self.vbox.addWidget(self.btn_ok)
        self.vbox.addWidget(self.lbl_x)
        self.vbox.addWidget(self.lbl_x_value)
        self.vbox.addWidget(self.slider_x)
        self.vbox.addWidget(self.lbl_y)
        self.vbox.addWidget(self.lbl_y_value)
        self.vbox.addWidget(self.slider_y)
        self.vbox.addWidget(self.lbl_b)
        self.vbox.addWidget(self.lbl_b_value)
        self.vbox.addWidget(self.slider_b)

        self.vbox.addStretch()

        self.setLayout(self.vbox)

        self.slider_b.valueChanged.connect(self.lbl_change)
        self.slider_x.valueChanged.connect(self.lbl_change)
        self.slider_y.valueChanged.connect(self.lbl_change)

        self.check_MID.toggled.connect(self.rud_change)
        self.check_PRO.toggled.connect(self.rud_change)
        self.check_LOW.toggled.connect(self.rud_change)


        self.btn_ok.clicked.connect(self.close)

        self.show()

    def is_cheats(self):
        return self.btn_ok.text() == "cheats were activated"



    def lbl_change(self):
        self.lbl_x_value.setText(str(self.slider_x.value()))
        self.lbl_y_value.setText(str(self.slider_y.value()))
        self.lbl_b_value.setText(str(self.slider_b.value()))

        if self.slider_x.value() == 4 and self.slider_y.value() == 4 and self.slider_b.value() == 2:
            self.check_LOW.click()
        elif self.slider_x.value() == 5 and self.slider_y.value() == 5 and self.slider_b.value() == 6:
            self.check_MID.click()
        elif self.slider_x.value() == 6 and self.slider_y.value() == 6 and self.slider_b.value() == 9:
            self.check_PRO.click()



    def rud_change(self):
        if self.check_LOW.isChecked():
            self.slider_x.setValue(4)
            self.slider_y.setValue(4)
            self.slider_b.setValue(2)
        if self.check_MID.isChecked():
            self.slider_x.setValue(5)
            self.slider_y.setValue(5)
            self.slider_b.setValue(6)
        if self.check_PRO.isChecked():
            self.slider_x.setValue(6)
            self.slider_y.setValue(6)
            self.slider_b.setValue(9)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Map_settings(None)
    sys.exit(app.exec_())