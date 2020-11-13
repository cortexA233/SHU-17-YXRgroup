from apscheduler.schedulers.background import BackgroundScheduler
from PyQt5.QtGui import QPalette, QPixmap, QBrush, QIcon, QPainter
from PyQt5.QtWidgets import QMainWindow,QApplication,QTextEdit,QAction,QFileDialog
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Client import Client
import datetime
import winsound
import time
import sys
import ast

global_cli = Client()


class Runthread(QtCore.QThread):
    _signal = pyqtSignal(str)  # 通过类成员对象定义信号对象
    def __init__(self):
        super(Runthread, self).__init__()
    def __del__(self):
        pass
        # self.wait()
    def run(self):
        winsound.PlaySound("报警", winsound.SND_NOSTOP)
class Drowpic(QtCore.QThread):
    _signal = pyqtSignal(str)  # 通过类成员对象定义信号对象
    def __init__(self):
        super(Drowpic, self).__init__()
    def __del__(self):
        pass
        # self.wait()
    def run(self):
        time = datetime.datetime.now().strftime("%Y-%m-%dps%H-%M-%S")
        path = 'history/' + time+'.txt'
        print(path)
        with open(file="123.txt", mode='r+') as f1:
            data = f1.read()
        with open(file=path, mode='a+', encoding="utf-8") as f2:
            f2.write(data)
        self._signal.emit(str(path))

class Runthread_1(QtCore.QThread):
    _signal = pyqtSignal(str)
    def sleeptime(hour, min, sec):
        return hour * 3600 + min * 60 + sec  # 设置自动执行间隔时间，我这里设置的5s
    def __init__(self):
        super(Runthread_1, self).__init__()
    def __del__(self):
        pass
        # self.wait()
    def run(self):
        second = Runthread_1.sleeptime(0, 0, 1)
        time.sleep(second)  # 延时
        with open(file="123.txt", mode='r+') as f1:
            data = f1.read()
        data = data.replace(" ", ',').replace("0", '')
        data = ast.literal_eval(data)
        print(data)
        a = data[len(data) - 1]
        self._signal.emit(str(a))

class hello_mainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(hello_mainWindow, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(550, 380)#550, 480

        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap('ui_picture.png')))
        MainWindow.setPalette(palette)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(90, 55, 91, 21))
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(400, 50, 75, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(130, 210, 100, 41))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(130, 130, 75, 41))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(340, 130, 75, 41))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(340, 210, 100, 41))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(90, 90, 75, 23))
        self.pushButton_6.setObjectName("pushButton_6")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(200, 50, 177, 31))
        self.label_2.setObjectName("label_2")
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 550, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.pushButton_6.clicked.connect(self.setText_qlabel)
        self.pushButton.clicked.connect(self.cancel)
        self.pushButton_2.clicked.connect(self.alarm)
        self.pushButton_3.clicked.connect(self.pol)
        self.pushButton_4.clicked.connect(self.history)
        self.pushButton_5.clicked.connect(self.limit)
        #textEdit设置
        openfile = QAction(QIcon(r'history'), 'open', self)
        openfile.setShortcut("Ctrl + 0")
        openfile.setStatusTip('open new file')
        openfile.triggered.connect(self.showDialog)
        filemune = self.menubar.addMenu('选择历史记录')
        filemune.addAction(openfile)


        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def showDialog(self):
        fname = QFileDialog.getOpenFileName(self,'open file', 'history')
        try:
            dr = global_cli.draw_pic(fname[0])
            print(dr)
        except FileNotFoundError as err:
            pass


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "电器盘柜云平台"))
        self.label.setText(_translate("MainWindow", "电器盘柜状态"))
        self.pushButton.setText(_translate("MainWindow", "上传"))
        self.pushButton_2.setText(_translate("MainWindow", "数据库下载"))
        self.pushButton_3.setText(_translate("MainWindow", "报警记录"))
        self.pushButton_4.setText(_translate("MainWindow", "历史记录"))
        self.pushButton_5.setText(_translate("MainWindow", "数据库记录"))
        self.pushButton_6.setText(_translate("MainWindow", "开始"))
        self.label_2.setText(_translate("MainWindow", "状态显示"))

    def history(self):
        self.thread_2 = Drowpic()
        self.thread_2.start()
        self.thread_2._signal.connect(self.Path)
        print('历史记录')
    def Path(self,path):
        dr = global_cli.draw_pic(path)
        print(dr)

    def alarm(self):
        st, msg = global_cli.download()
        print(st, msg)
        print('数据库下载')

    def cancel(self):
        up, msg = global_cli.upload()
        print(up, msg)
        print('上传记录')

    def pol(self):
        with open(file="test.txt", mode='r+', encoding="utf-8") as f3:
            time = f3.read()
        QMessageBox.warning(self,
                            "警报记录",
                            time,
                            QMessageBox.Yes)
        print('报警记录')

    def limit(self):
        dr = global_cli.draw_pic('download/123.txt')
        print(dr)
        print('数据库记录')

    def setText_qlabel(self):
        font = QtGui.QFont()
        font.setFamily('微软雅黑')
        font.setBold(True)
        font.setPointSize(13)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.thread_1 = Runthread_1()
        self.thread_1._signal.connect(self.call_backlog)
        self.thread_1.start()  # 执行

    def call_backlog(self, a):
        print(a)
        if a == '2':  # 定时循环
            self.thread_1 = Runthread_1()
            self.thread_1.start()  # 执行
            self.thread_1._signal.connect(self.call_backlog)
            self.label_2.setStyleSheet('background-color: rgb(0,255,0)')
            self.label_2.setText("<font color=%s>%s</font>" % ('#000000', "绿灯"))
        elif a == '1':  # 没有调用定时代码
            self.thread = Runthread()
            self.thread.start()
            self.label_2.setStyleSheet('background-color: rgb(255, 0, 0)')
            self.label_2.setText("<font color=%s>%s</font>" % ('#000000', "红灯"))
            time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with open(file="test.txt", mode='a+', encoding="utf-8") as f2:
                f2.write("warn:" + time + "\n")
        else:
            self.thread_1 = Runthread_1()
            self.thread_1.start()  # 执行
            self.thread_1._signal.connect(self.call_backlog)
            self.label_2.setStyleSheet('background-color: rgb(255, 255, 255)')
            self.label_2.setText("<font color=%s>%s</font>" % ('#000000', "无灯亮"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    ui = hello_mainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())
