from PyQt5.QtWidgets import QVBoxLayout,QPushButton,QWidget,QApplication, QLineEdit
import sys
from miner import MainWindow


class Home(QWidget):
    def __init__(self):
        super().__init__()
        vbox = QVBoxLayout()
        self.ip = QLineEdit()
        but_server = QPushButton("SERVER")
        but_server.clicked.connect(self.open_SERVER)
        but_client = QPushButton("CLIENT")
        but_client.clicked.connect(self.open_CLIENT)
        but_single = QPushButton("SINGLE")
        but_single.clicked.connect(self.open_SINGLE_PLAYER)
        vbox.addWidget(self.ip)
        vbox.addWidget(but_server)
        vbox.addWidget(but_client)
        vbox.addWidget(but_single)
        self.setLayout(vbox)
        self.setGeometry(700, 450, 250, 50)
        self.show()

    def open_SERVER(self):
        self.server = MainWindow("master", self.ip.text() if self.ip.text() != "" else "127.0.0.1:8080")
        self.close()

    def open_CLIENT(self):
        self.client = MainWindow("slave", self.ip.text() if self.ip.text() != "" else "127.0.0.1:8080")
        self.close()

    def open_SINGLE_PLAYER(self):
        self.client = MainWindow("single_player")
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Home()
    sys.exit(app.exec_())
