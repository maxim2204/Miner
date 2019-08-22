import sys
from PyQt5.QtWidgets import QMainWindow, QAction, QApplication, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer
from miner_map import MinerMap
from map_settings import Map_settings
import socket
import select
from threading import Thread, Event
conn=None
tcpClientA=None
import time


class MainWindow(QMainWindow):

    def __init__(self, mode, ip="0.0.0.0:8080"):
        super().__init__()
        print(ip)
        self.MODE = mode
        print(self.MODE)
        # self.signal = Event()
        ip, port = ip.split(":")
        self.timer = QTimer()
        if self.MODE == "master":
            self.start_server(ip, port)
            print("connect timer for master")
            self.timer.timeout.connect(self.listen_master)
            print("connected timer for master")
        elif self.MODE == "slave":
            self.start_client_slave(ip, port)
            print("connect timer for slave")
            self.timer.timeout.connect(self.listen_slave)
            print("connected timer for slave")
        elif self.MODE != "single_player":
            raise ValueError("Invalid MODE")
        self.timer.start(3000)
        self.initUI(5,5,3)


    def initUI(self, x, y, z):

        self.x = x
        self.y = y
        self.z = z

        self.setWindowTitle('minesweeper by taurl and Alexey')
        self.setWindowIcon(QIcon('minesweeper-ico.png'))
        self.map_ = MinerMap(x,y,z,0,self)

        #self.setCentralWidget(self.map_)
        #self.map_.disabled(True)

        self.setCentralWidget(self.map_)

        exitAction = QAction(QIcon('exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(self.close)


        mapSettingsAction = QAction(QIcon('settings.png'), 'MapSettings', self)
        mapSettingsAction.setShortcut('Ctrl+J')
        mapSettingsAction.triggered.connect(self.mapSettings)

        menubar = self.menuBar()

        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        settings = menubar.addMenu('&Settings')
        settings.addAction(mapSettingsAction)

        if self.MODE == "slave":
            settings.setEnabled(False)

        if self.MODE != "single_player":
            self.map_.disabled(True)

        self.show()

    def closeEvent(self, event):
        if self.MODE != "single_player":
            self.timer.stop()
            print(42)

    def end(self, message):
        if message == "win":
            self.map_.game_end("lose", True)
        if message == "lose":
            self.map_.game_end("win", True)

    def start(self, message):
        x,y,z = message.split(",")
        x,y,z = int(x),int(y),int(z)
        self.create_game(x,y,z)

    def create_game(self,x,y,z,cheats=0):
        self.map_ = MinerMap(x,y,z,cheats,self)
        print(1111111111)
        self.map_.disabled(True)
        self.setCentralWidget(self.map_)
        self.resize(150, 220)
        self.map_.disabled(False)


    def send(self, message):
        print("Send: {}".format(message))
        if self.MODE == "master":
            conn.send(message.encode("utf-8"))
        elif self.MODE == "slave":
            tcpClientA.send(message.encode("utf-8"))
        else:
            pass
            #raise ValueError("wrong mode {}".format(self.MODE))
        print("Sent successfully")

    def mapSettings(self):
        self.map_.disabled(True)
        self.s = Map_settings(self)
        self.s.btn_ok.clicked.connect(self.close_map_settings)


    def close_map_settings(self):
        if self.MODE == "master":
            self.send("{},{},{}".format(self.s.slider_x.value(), self.s.slider_y.value(), self.s.slider_b.value()))
        x,y,z = self.s.slider_x.value(), self.s.slider_y.value(), self.s.slider_b.value()
        self.create_game(x,y,z,1 if self.s.is_cheats() else 0)
        #self.setMaximumSize(self.s.slider_x.value()*10, self.s.slider_y.value()*4)
        #self.maximumSize()

    def start_server(self, ip, port):
        BUFFER_SIZE = 20
        tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcpServer.bind((ip, int(port)))
        threads = []

        tcpServer.listen(4)
        # while not self.window.signal.isSet():
        print("Multithreaded Python server : Waiting for connections from TCP clients...")
        global conn
        (conn, (ip, port)) = tcpServer.accept()

    def start_client_slave(self, ip, port):
        print("start_client start")
        BUFFER_SIZE = 2000
        global tcpClientA
        tcpClientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcpClientA.connect((ip, int(port)))
        print("start_client end")

    def listen_master(self):
        print("listen_master start")
        global conn
        if conn is None:
            print("no connection at master")
            return
        if select.select([conn], [], [], 1.0)[0]:
            data = conn.recv(2048)
            data = data.decode("utf-8")
            if data == "win" or data == "lose":
                self.end(data)
            else:
                self.start(data)
        print("listen_master end")

    def listen_slave(self):
        print("listen_slave start")
        if tcpClientA is None:
            print("no connection at slave")
            return
        if select.select([tcpClientA], [], [], 1.0)[0]:
            data = tcpClientA.recv(2048)
            data = data.decode("utf-8")
            if data == "win" or data == "lose":
                self.end(data)
            else:
                self.start(data)
        print("listen_slave end")
