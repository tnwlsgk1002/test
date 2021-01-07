import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import cv2
import os  # 확장자 파일 가져오기
import copy
import natsort


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('labeling program')
        self.setGeometry(300, 300, 500, 400)

        # 라벨
        self.label_list = []
        self.label = Label(self)

        # SetCursor 설정
        Cursor = QCursor(QPixmap('cross.png'))
        self.label.setCursor(Cursor)

        # 라디오버튼
        self.dog = QRadioButton('Dog', self)
        icon = QIcon('red.png')
        self.dog.setIcon(icon)
        self.dog.clicked.connect(self.radioclicked)

        self.cat = QRadioButton('Cat', self)
        icon = QIcon('blue.png')
        self.cat.setIcon(icon)
        self.cat.clicked.connect(self.radioclicked)

        self.dog.setChecked(True)

        self.animalType = 0

        # 디렉터리 선택 및 표시
        dirbtn = QPushButton('디렉터리 선택', self)
        dirbtn.clicked.connect(self.Directory)

        self.dir = QLineEdit(self)
        self.dir.setReadOnly(True)

        # 이미지 이동 버튼
        self.leftbtn = QPushButton("<", self)
        self.rightbtn = QPushButton(">", self)
        self.leftbtn.setShortcut("Left")
        self.rightbtn.setShortcut("Right")
        self.leftbtn.clicked.connect(self.movebtnClicked)
        self.rightbtn.clicked.connect(self.movebtnClicked)

        # 레이아웃 설정
        vbox = QVBoxLayout()

        hbox = QHBoxLayout()
        hbox.addWidget(self.leftbtn)
        hbox.addWidget(self.rightbtn)
        hbox.addStretch(3)
        hbox.addWidget(self.dog)
        hbox.addWidget(self.cat)
        vbox.addLayout(hbox)

        vbox.addWidget(self.label)

        hbox = QHBoxLayout()
        hbox.addWidget(dirbtn)
        hbox.addWidget(self.dir)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.show()

    def Directory(self):
        self.folder = QFileDialog.getExistingDirectory(self, 'Open Folder', 'c:/')
        try:
            self.dir.setText(self.folder)
            file_list = os.listdir(self.folder)
            self.label_list = [file for file in file_list if file.endswith(".png") or file.endswith(".jpg")]
            self.label_list = natsort.natsorted(self.label_list)
            if not self.label_list:
                return
            self.total = len(self.label_list)
            self.file = self.folder + "/" + self.label_list[0]
            self.n1 = 0
            self.label.initPixmap()

        except FileNotFoundError:
            return

    def radioclicked(self):
        sender = self.sender()
        if sender == self.dog:
            self.animalType = 0
        else:
            self.animalType = 1

    def movebtnClicked(self):
        if not self.label_list:
            return
        sender = self.sender()
        self.label.text_save()
        if sender == self.leftbtn:
            self.n1 = self.n1 - 1
            if self.n1 == -1:
                self.n1 = len(self.label_list) - 1
        elif sender == self.rightbtn:
            self.n1 = self.n1 + 1
            if self.n1 == len(self.label_list):
                self.n1 = 0
        self.file = self.folder + "/" + self.label_list[self.n1]
        self.label.createPixmap()


class Label(QLabel):
    def __init__(self, parent):
        super().__init__()
        self.setParent(parent)
        self.drawing = False
        self.removing = False
        self.exist = False
        self.ix = None
        self.iy = None
        self.ori_image = []
        self.text = []

    def initPixmap(self):
        self.image = cv2.imread(self.parent().file, cv2.IMREAD_COLOR)
        image = copy.deepcopy(self.image)
        self.ori_image.append(image)
        self.h, self.w = self.image.shape[:2]
        qimage = QImage(self.image.data, self.w, self.h, self.image.strides[0], QImage.Format_BGR888)
        self.setPixmap(QPixmap.fromImage(qimage))
        self.exist = True
        self.text.append([0])
        self.resize(self.w, self.h)
        self.parent().resize(self.w + 200, self.h + 200)

    # 텍스트를 기반으로 setPixmap (이동, 삭제 시)
    def createPixmap(self):
        print("\n=====createPixmap=====")
        print("self.parent().n1:", self.parent().n1)

        # 처음 이미지를 열었을 경우
        if len(self.text) < self.parent().n1 + 1:
            print("이미지를 부른 적이 없음")
            self.initPixmap()
            return

        print("text[n1]: ", self.text[self.parent().n1])

        # 이미지에 바운딩박스가 없는 경우
        if self.text[self.parent().n1] == [0]:
            print('이미지를 불러봤으나 바운딩박스가 없음')
            self.image = copy.deepcopy(self.ori_image[self.parent().n1])
            print('d')
            self.h, self.w = self.image.shape[:2]
            qimage = QImage(self.image.data, self.w, self.h, self.image.strides[0], QImage.Format_BGR888)
            print('s')
            self.setPixmap(QPixmap.fromImage(qimage))
            print('e')
            self.update()
            self.resize(self.w, self.h)
            print('aa')
            return

        print("self.text[n1]: ", self.text[self.parent().n1])
        self.image = copy.deepcopy(self.ori_image[self.parent().n1])
        for i in self.text[self.parent().n1]:
            if i[4] == 'Dog':
                self.image = cv2.rectangle(self.image, (i[0], i[1]), (i[2], i[3]), (0, 0, 255))
                self.image = cv2.putText(self.image, 'Dog', ((i[0] + i[2]) // 2, i[1] - 10),
                                         cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            elif i[4] == 'Cat':
                self.image = cv2.rectangle(self.image, (i[0], i[1]), (i[2], i[3]), (255, 0, 0))
                self.image = cv2.putText(self.image, 'Cat', ((i[0] + i[2]) // 2, i[1] - 10),
                                         cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        self.h, self.w = self.image.shape[:2]
        qimage = QImage(self.image.data, self.w, self.h, self.image.strides[0], QImage.Format_BGR888)
        self.setPixmap(QPixmap.fromImage(qimage))
        self.update()
        self.resize(self.w, self.h)

    def mousePressEvent(self, e):
        if not self.exist:
            return

        if e.button() == Qt.LeftButton:
            self.ix = e.x()
            self.iy = e.y()
            self.drawing = True
            return

        # 삭제
        if e.button() == Qt.RightButton:
            remove_index = self.box_exist(e.x(), e.y())
            print('\nremove_index: ', remove_index)
            if remove_index == -1:
                return
            # text에서 바운딩 박스 삭제
            # text를 바탕으로 qimage draw, self.image에 적용
            if len(self.text[self.parent().n1]) == 1:
                self.text[self.parent().n1].pop(remove_index)
                self.createPixmap()
                self.text[self.parent().n1].append(0)
                return

            self.text[self.parent().n1].pop(remove_index)
            self.createPixmap()

            return

    # text 안에 바운딩 박스가 있는가 확인
    def box_exist(self, x, y):
        for i in self.text[self.parent().n1]:
            if i == -1:
                break
            if (i[0] <= x and i[1] <= y and i[2] >= x and i[3] >= y) or (
                    i[0] >= x and i[1] >= y and i[2] <= x and i[3] <= y):
                return self.text[self.parent().n1].index(i)
        return -1

    def mouseMoveEvent(self, e):
        if not self.exist:
            return

        if self.drawing:
            qimage = QImage(self.image.data, self.w, self.h, self.image.strides[0], QImage.Format_BGR888)
            self.setPixmap(QPixmap.fromImage(qimage))

            img = copy.deepcopy(self.image)
            if self.parent().animalType == 0:
                img = cv2.rectangle(img, (self.ix, self.iy), (e.x(), e.y()), (0, 0, 255))
            else:
                img = cv2.rectangle(img, (self.ix, self.iy), (e.x(), e.y()), (255, 0, 0))
            qimage = QImage(img.data, self.w, self.h, img.strides[0], QImage.Format_BGR888)
            self.setPixmap(QPixmap.fromImage(qimage))
            self.repaint()

    def mouseReleaseEvent(self, e):

        # 삭제 시 그리기 방지
        if e.button() == Qt.RightButton:
            return

        if not self.exist:
            return

        self.drawing = False
        if self.parent().animalType == 0:
            self.image = cv2.rectangle(self.image, (self.ix, self.iy), (e.x(), e.y()), (0, 0, 255))
            self.image = cv2.putText(self.image, 'Dog', ((self.ix + e.x()) // 2, self.iy - 10),
                                     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            list = [self.ix, self.iy, e.x(), e.y(), 'Dog']
        else:
            self.image = cv2.rectangle(self.image, (self.ix, self.iy), (e.x(), e.y()), (255, 0, 0))
            self.image = cv2.putText(self.image, 'Cat', ((self.ix + e.x()) // 2, self.iy - 10),
                                     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            list = [self.ix, self.iy, e.x(), e.y(), 'Cat']

        self.text[self.parent().n1].append(list)
        if self.text[self.parent().n1][0] == 0:  # 첫 바운딩 박스인 경우
            del self.text[self.parent().n1][0]
        print("========그리기 =======")
        print("self.text : ", self.text)
        qimage = QImage(self.image.data, self.w, self.h, self.image.strides[0], QImage.Format_BGR888)
        self.setPixmap(QPixmap.fromImage(qimage))

    # 텍스트파일을 저장하여 업로드
    def text_save(self):
        fname = self.parent().file.split('.')
        print(self.text)
        with open(fname[0] + ".txt", 'w') as file:
            for i in self.text:
                for j in i:
                    if j == 0:
                        return
                    for k in j:
                        file.write(str(k) + ' ')
                    file.write('\n')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())