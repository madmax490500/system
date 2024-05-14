import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

class CWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.year = QLCDNumber(self)        
        self.month = QLCDNumber(self)
        self.day = QLCDNumber(self)
        self.hour = QLCDNumber(self)
        self.min = QLCDNumber(self)
        self.sec = QLCDNumber(self)

        self.initUI()

    def initUI(self):        
        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.year)
        hbox1.addWidget(self.month)
        hbox1.addWidget(self.day)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.hour)
        hbox2.addWidget(self.min)
        hbox2.addWidget(self.sec)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)

        self.setLayout(vbox)

        self.setWindowTitle('시계')
        self.setGeometry(200,200, 400, 200)  

        self.showtime()

    def showtime(self):
        # 현재 시간 얻기
        current_time = QDateTime.currentDateTime()
        # LCD 표시
        self.year.display(current_time.date().year())
        self.month.display(current_time.date().month())
        self.day.display(current_time.date().day())
        self.hour.display(current_time.time().hour())
        self.min.display(current_time.time().minute())
        self.sec.display(current_time.time().second())

        # 타이머 설정 (1초마다, 콜백함수)
        # 업데이트를 위한 테스트 주석
        QTimer.singleShot(1000, self.showtime)

    def showEvent(self, event):
        super().showEvent(event)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = CWidget()
    w.show()    
    sys.exit(app.exec_())
