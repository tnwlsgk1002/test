import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        formbox = QHBoxLayout()
        self.setLayout(formbox)

        left = QVBoxLayout()
        right = QVBoxLayout()

        gb = QGroupBox('그리기 종류')
        left.addWidget(gb)

        box = QVBoxLayout()
        gb.setLayout(box)

        text = ['펜', '선', '세모', '사각형', '원']
        self.radiobtns = []

        for i in range(len(text)):
            self.radiobtns.append(QRadioButton(text[i], self))
            self.radiobtns[i].clicked.connect(self.radioClicked)
            box.addWidget(self.radiobtns[i])

        self.radiobtns[0].setChecked(True)
        self.drawType = 0

        gb = QGroupBox('펜 설정')
        left.addWidget(gb)

        grid = QGridLayout()
        gb.setLayout(grid)

        label = QLabel('선 두께')
        grid.addWidget(label, 0, 0)

        self.spinbox = QSpinBox()
        self.spinbox.setRange(1, 30)
        self.spinbox.valueChanged.connect(self.value_changed)
        grid.addWidget(self.spinbox, 0, 1)

        label = QLabel('선 색상')
        grid.addWidget(label, 1, 0)

        self.pencolor = QColor(0, 0, 0)
        self.penbtn = QPushButton()
        self.penbtn.setStyleSheet('backgroud-color : rgb(0,0,0)')
        self.penbtn.clicked.connect(self.showColorDlg)
        grid.addWidget(self.penbtn, 1, 1)

        gb = QGroupBox('채우기 설정')
        left.addWidget(gb)

        hbox = QHBoxLayout()
        gb.setLayout(hbox)

        label = QLabel('채우기 색상')
        hbox.addWidget(label)

        self.brushcolor = QColor(255, 255, 255)
        self.brushbtn = QPushButton()
        self.brushbtn.setStyleSheet('backgroud-color : rgb(255, 255, 255)')
        self.brushbtn.clicked.connect(self.showColorDlg)
        hbox.addWidget(self.brushbtn)

        gb = QGroupBox('배경 설정')
        left.addWidget(gb)

        hbox = QHBoxLayout()
        gb.setLayout(hbox)

        label = QLabel('배경 색상')
        hbox.addWidget(label)

        self.backcolor = QColor(255, 255, 255)
        self.backbtn = QPushButton()
        self.backbtn.setStyleSheet('backgroud-color : rgb(255, 255, 255)')
        self.backbtn.clicked.connect(self.showColorDlg)
        hbox.addWidget(self.backbtn)

        gb = QGroupBox('지우개')
        left.addWidget(gb)

        hbox = QHBoxLayout()
        gb.setLayout(hbox)

        self.checkbox = QCheckBox('지우개 동작')
        self.checkbox.stateChanged.connect(self.checkClicked)
        hbox.addWidget(self.checkbox)

        left.addStretch(1)

        self.canvas = Canvas(self)
        self.canvas.setGeometry(300, 0, self.width() - 300, self.height())
        self.canvas.createPixmap()
        # self.canvas.show()

        self.canvas.mousePressEvent = self.canvas_mousePressEvent
        right.addWidget(self.canvas)

        formbox.addLayout(left)
        formbox.addLayout(right)

        formbox.setStretchFactor(left, 0)
        formbox.setStretchFactor(right, 1)
        # self.resize(1280, 720)
        self.show()

    def radioClicked(self):
        for i in range(len(self.radiobtns)):
            if self.radiobtns[i].isChecked():
                self.drawType = i
                break

    def checkClicked(self):
        pass

    def showColorDlg(self):

        color = QColorDialog.getColor()
        sender = self.sender()

        if sender == self.penbtn and color.isValid():
            self.pencolor = color
            self.penbtn.setStyleSheet('backgroud-color: {}'.format(color.name()))
        elif sender == self.brushbtn and color.isValid():
            self.brushcolor = color
            self.brushbtn.setStyleSheet('backgroud-color: {}'.format(color.name()))
        else:
            self.backcolor = color
            self.backbtn.setStyleSheet('backgroud-color: {}'.format(color.name()))

    def value_changed(self):
        pass

    # self.spinbox.value()

    def canvas_mousePressEvent(self, e):
        pass

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Paint')
        self.setFixedSize(1280, 720)

        openAction = QAction('Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('그림을 불러옵니다.')
        # openAction.triggered.connect(self.file_open)

        saveAction = QAction('Save', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.setStatusTip('그림을 저장합니다.')
        # saveAction.triggered.connect(self.file_save)

        self.statusBar()

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        filemenu = menubar.addMenu('&File')
        filemenu.addAction(openAction)
        filemenu.addAction(saveAction)

        wg = MyWidget()
        self.setCentralWidget(wg)


class Canvas(QLabel):
    def __init__(self, parent):
        super().__init__()
        self.setParent(parent)
        self.setupUi()

    def setupUi(self):
        self.setStyleSheet('background-color: white;')

    def createPixmap(self):
        pixmap = QPixmap(self.width(), self.height())
        pixmap.fill(Qt.white)
        self.setPixmap(pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())
