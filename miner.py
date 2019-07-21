import sys
from PyQt5.QtWidgets import QMainWindow, QAction, QApplication, QMessageBox
from PyQt5.QtGui import QIcon
from miner_map import MinerMap
from map_settings import Map_settings
import socket
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
        if self.MODE == "master":
            self.serverThread = ServerThread(self,ip, port)
            self.serverThread.start()
        elif self.MODE == "slave":
            self.clientThread = ClientThreadSlave(self,ip, port)
            self.clientThread.start()
        elif self.MODE != "single_player":
            raise ValueError("Invalid MODE")
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

        self.show()

    def closeEvent(self, event):
        if self.MODE != "single_player":
            self.signal.set()
            print(42)

    def end(self):
        # check if self is won already
        self.map_.game_end("Your friend was faster","lose")





    def send(self, message):
        if self.MODE != "single_player":
            global conn
            conn.send(message.encode("utf-8")) if self.MODE == 'master' else tcpClientA.send(message.encode())



    def mapSettings(self):
        self.map_.disabled(True)
        self.s = Map_settings(self)
        self.s.btn_ok.clicked.connect(self.close_map_settings)


    def close_map_settings(self):
        self.map_ = MinerMap(self.s.slider_x.value(), self.s.slider_y.value(), self.s.slider_b.value(),
                             1 if self.s.is_cheats() else 0, self)
        self.map_.disabled(True)
        self.setCentralWidget(self.map_)
        self.resize(150, 220)
        self.map_.disabled(False)

        #self.setMaximumSize(self.s.slider_x.value()*10, self.s.slider_y.value()*4)
        #self.maximumSize()

class ServerThread(Thread):
    def __init__(self, window,ip, port):
        Thread.__init__(self)
        self.window = window
        self.ip = ip
        self.port = port

    def run(self):
        TCP_IP = self.ip
        TCP_PORT = int(self.port)
        BUFFER_SIZE = 20
        tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcpServer.bind((TCP_IP, TCP_PORT))
        threads = []

        tcpServer.listen(4)
        # while not self.window.signal.isSet():
        while True:
            print("Multithreaded Python server : Waiting for connections from TCP clients...")
            global conn
            (conn, (ip, port)) = tcpServer.accept()
            newthread = ClientThreadMaster(ip, port, self.window)
            newthread.start()
            threads.append(newthread)


class ClientThreadMaster(Thread):
    def __init__(self, ip, port, window):
        Thread.__init__(self)
        self.window = window
        self.ip = ip
        self.port = port
        print("[+] New server socket thread started for " + ip + ":" + str(port))

    def run(self):
        # while not self.window.signal.isSet():
        while True:
            # (conn, (self.ip,self.port)) = serverThread.tcpServer.accept()
            global conn
            data = conn.recv(2048)
            if data.decode("utf-8") == "win":
                print("&&&&&&&&&&&&&&&&&&")
                self.window.end()


class ClientThreadSlave(Thread):
    def __init__(self, window, ip, port):
        Thread.__init__(self)
        self.window = window
        self.ip = ip
        self.port = port

    def run(self):
        host = self.ip
        port = int(self.port)
        BUFFER_SIZE = 2000
        global tcpClientA
        tcpClientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcpClientA.connect((host, port))
        # while not self.window.signal.isSet():
        while True:
            data = tcpClientA.recv(BUFFER_SIZE)
            print("&&&&&&&&&&&&&&&&&&")
            if data.decode("utf-8") == "win":
                self.window.end()
        tcpClientA.close()



