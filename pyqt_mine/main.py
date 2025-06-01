import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton, 
                             QHBoxLayout, QVBoxLayout, QAction, QLCDNumber)
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPainter, QColor
from PyQt5.Qt import *
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QTranslator
from enum import Enum
import random

class LANGUAGE(Enum):
    English = 0
    Chinese = 1
class GridType(Enum):
    GRID_NORMAL = 0
    GRID_FLAG = 1
    GRID_INTERROGATION = 2
    GRID_CLICKOPEN = 3
    GRID_DEFEAT = 4

class CHESS_DIFFICULTY(Enum):
    Difficult_Easy = 0
    Difficult_Middle = 1
    Difficult_Hard = 2
    
class GAME_RESULT(Enum):
    SUCCESS = 0
    FAIL = 1
    PROGRESSING = 2

class Chessmantype:
    Chessmantype = False
    iMineNum = 0
    x = 0
    y = 0
    eGridType = GridType.GRID_NORMAL
    def __init__(self):
        self.Chessmantype = False
        self.iMineNum = 0
        self.x = 0
        self.y = 0
        self.eGridType = GridType.GRID_NORMAL
        
EASY_SCREEN_SIZE_W=360
EASY_SCREEN_SIZE_H=440
MID_SCREEN_SIZE_W=400
MID_SCREEN_SIZE_H=470
HARD_SCREEN_SIZE_W=480
HARD_SCREEN_SIZE_H=560
CHESSNUM_EASY=8
MINESNUM_EASY=10

CHESSNUM_MID=12
MINESNUM_MID=15

CHESSNUM_HARD=15
MINESNUM_HARD=20

RowCount = CHESSNUM_EASY;
ColCount = CHESSNUM_EASY;
chessnum = CHESSNUM_EASY;
minenum = MINESNUM_EASY;
hx1 = 10;
hy1 = 3;
bh = 40;
bw = bh;
sChessmine = None
level = CHESS_DIFFICULTY.Difficult_Easy
mainwidth = EASY_SCREEN_SIZE_W
mainheight = EASY_SCREEN_SIZE_H
bMineDefeat = False
#true:mine defeat,display game over,false:game doesn't over,
iFindMineNumber = 0
#Find the mine number
game_result = GAME_RESULT.PROGRESSING
bStartMine = False

def SetMines(iRow,iCol):
    global sChessmine
    if sChessmine[iRow][iCol].bCheck:
        return
    if sChessmine[iRow][iCol].iMineNum != 0:
        sChessmine[iRow][iCol].eGridType = GridType.GRID_CLICKOPEN
        sChessmine[iRow][iCol].bCheck = True
        return

    sChessmine[iRow][iCol].eGridType = GridType.GRID_CLICKOPEN
    sChessmine[iRow][iCol].bCheck = True
    if ((iRow == 0) and (iCol == 0)):
        SetMines(iRow,iCol + 1)#2
        SetMines(iRow + 1,iCol + 1)#5
        SetMines(iRow + 1,iCol)#4

    elif ((iRow == 0) and (0 < iCol) and (iCol < chessnum - 1)):
        SetMines(iRow,iCol - 1)#1
        SetMines(iRow,iCol + 1)#3
        SetMines(iRow + 1,iCol - 1)#4
        SetMines(iRow + 1,iCol)#5
        SetMines(iRow + 1,iCol + 1)#6

    elif ((iRow == 0) and (iCol == chessnum - 1)):
        SetMines(iRow,iCol - 1)#2
        SetMines(iRow + 1,iCol - 1)#5
        SetMines(iRow + 1,iCol)#6

    elif ((0 < iRow) and (iRow < chessnum - 1) and (iCol == 0)):
        SetMines(iRow - 1,iCol)#1
        SetMines(iRow - 1,iCol + 1)#2
        SetMines(iRow,iCol + 1)#5
        SetMines(iRow + 1,iCol + 1)#8
        SetMines(iRow + 1,iCol)#7

    elif ((0 < iRow) and (iRow < chessnum - 1) and (iCol == chessnum - 1)):
        SetMines(iRow - 1,iCol - 1)#2
        SetMines(iRow - 1,iCol)#3
        SetMines(iRow,iCol - 1)#5
        SetMines(iRow + 1,iCol - 1)#8
        SetMines(iRow + 1,iCol)#9

    elif ((iRow == chessnum - 1) and (iCol == 0)):
        SetMines(iRow - 1,iCol)#4
        SetMines(iRow - 1,iCol + 1)#5
        SetMines(iRow,iCol + 1)#8

    elif ((iRow == chessnum - 1) and (0 < iCol) and (iCol < chessnum - 1)):
        SetMines(iRow - 1,iCol - 1)#4
        SetMines(iRow - 1,iCol)#5
        SetMines(iRow - 1,iCol + 1)#6
        SetMines(iRow,iCol - 1)#7
        SetMines(iRow,iCol + 1)#9

    elif ((iRow == chessnum - 1) and (iCol == chessnum - 1)):
        SetMines(iRow - 1,iCol)#6
        SetMines(iRow - 1,iCol - 1)#5
        SetMines(iRow,iCol - 1)#8

    else:
        SetMines(iRow - 1,iCol - 1)#1
        SetMines(iRow - 1,iCol)#2
        SetMines(iRow - 1,iCol + 1)#3
        SetMines(iRow,iCol - 1)#4
        SetMines(iRow,iCol + 1)#6
        SetMines(iRow + 1,iCol - 1)#7
        SetMines(iRow + 1,iCol)#8
        SetMines(iRow + 1,iCol + 1)#9
        
def IfExistMineInCurrentCol(icol):
    global chessnum
    global sChessmine
    for i in range(chessnum):
        if sChessmine[i][icol].bMineType == True:
            return True
    return False
        
class MainWindow(QMainWindow):
    app = None
    Chinese = None
    English = 0
    #0:english
    #1:chinese
    Language = LANGUAGE.English
    def __init__(self,a,en,ch):
        super().__init__()
        self.app = a
        self.Chinese = ch
        self.English = en
        self.initUI()
        
    def setText(self):
        if self.Language == LANGUAGE.English:
            self.app.installTranslator(self.English)
            self.En.setChecked(True)
            self.Ch.setChecked(False)
        else:
            self.app.installTranslator(self.Chinese)
            self.En.setChecked(False)
            self.Ch.setChecked(True)
        
        self.setWindowTitle(self.tr('mine'))
        self.file_menu.setTitle(self.tr("File"))
        self.Easy.setText(self.tr("Easy"))
        self.Middle.setText(self.tr("Middle"))
        self.Hard.setText(self.tr("Hard"))
        self.About.setText(self.tr("About"))
        self.Quit.setText(self.tr("Exit"))
        
    def initUI(self):
        # 设置主窗口
        self.setWindowTitle(self.tr('mine'))
        self.setGeometry(100, 100, EASY_SCREEN_SIZE_W, EASY_SCREEN_SIZE_H)
        self.setWindowIcon(QIcon('logo.ico'))
        self.setWindowFlags(Qt.WindowMinimizeButtonHint|Qt.WindowCloseButtonHint)
        #self.setFixedSize(self.width(), self.height());
        
        self.img_path_s1 = "s1.png"
        self.img_path_s2 = "s2.png"
        # 创建菜单栏
        self.menubar = self.menuBar()
        self.file_menu = self.menubar.addMenu(self.tr("File"))
        
        self.Easy = QAction(self.tr("Easy"),self,checkable=True)
        self.Easy.triggered.connect(self.easyFunc)
        self.Easy.setChecked(True)
        self.file_menu.addAction(self.Easy)
    
        self.Middle = QAction(self.tr("Middle"),self,checkable=True)
        self.Middle.triggered.connect(self.middleFunc)
        self.file_menu.addAction(self.Middle)
        
        self.Hard = QAction(self.tr("Hard"),self,checkable=True)
        self.Hard.triggered.connect(self.hardFunc)
        self.file_menu.addAction(self.Hard)
        
        self.Ch = QAction("中文",self,checkable=True)
        self.Ch.triggered.connect(self.ChineseFunc)
        self.file_menu.addAction(self.Ch)
        
        self.En = QAction("English",self,checkable=True)
        self.En.triggered.connect(self.EnglishFunc)
        self.En.setChecked(True)
        self.file_menu.addAction(self.En)
        
        self.About = QAction(self.tr("About"),self)
        self.About.triggered.connect(self.aboutFunc)
        self.file_menu.addAction(self.About)
        
        self.Quit = QAction(self.tr("Exit"),self) 
        self.file_menu.addAction(self.Quit)
        self.Quit.triggered.connect(self.quitFunc)
        # self.file_menu.triggered[QAction].connect(self.processtrigger)
        
        # 添加退出动作
#        exit_action = QAction('退出', self)
#        exit_action.setShortcut('Ctrl+Q')
#        exit_action.setStatusTip('退出应用程序')
#        exit_action.triggered.connect(self.close)
#        file_menu.addAction(exit_action)
        
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建垂直布局
        main_layout = QVBoxLayout(central_widget)
        
        # 创建水平布局和三个控件
        horizontal_layout = QHBoxLayout()
        
        # 使用QLCDNumber替换原来的QLabel
        self.lcd1 = QLCDNumber()
        self.lcd1.display(0)
        
        self.button = QPushButton('')
        self.button.setFixedSize(50, 50);
        self.button.clicked.connect(self.ButtonNewGame)
        self.button.setStyleSheet("QPushButton{\n"
            "background-image: url(\"%s\");\n"
            "background-position:center;\n"
            "background-repeat:no-repeat;\n"
            "}" % self.img_path_s1)
        
        self.lcd2 = QLCDNumber()
        self.lcd2.display(minenum)
        
        # 将控件添加到水平布局
        horizontal_layout.addWidget(self.lcd1)
        horizontal_layout.addWidget(self.button)
        horizontal_layout.addWidget(self.lcd2)
        
        # 将水平布局添加到主布局
        main_layout.addLayout(horizontal_layout)
        
        # 创建绘图区域
        self.canvas = CanvasWidget(self)
        main_layout.addWidget(self.canvas, 1)  # 占据剩余空间
        
        self.InitChessman(CHESS_DIFFICULTY.Difficult_Easy)
        self.mineTimer = QTimer(self)
        self.mineTimer.timeout.connect(self.onTimer)
        self.counter = 0
        
        self.canvas.GameStart.connect(self.slot_StartMine)
        self.canvas.GameStop.connect(self.slot_StopMine)
        self.canvas.GameSetMineNumber.connect(self.slot_SetMineNumber)
        self.canvas.GameFail.connect(self.slot_GameFail)
        
    def ChineseFunc(self):
        self.Language = LANGUAGE.Chinese
        self.setText()
    
    def EnglishFunc(self):
        self.Language = LANGUAGE.English
        self.setText()
    
    def quitFunc(self):
        quit()
        
    def easyFunc(self):
        self.Easy.setChecked(True)
        self.Middle.setChecked(False)
        self.Hard.setChecked(False)
        mainwidth = EASY_SCREEN_SIZE_W
        mainheight = EASY_SCREEN_SIZE_H
        self.setGeometry(100, 100, EASY_SCREEN_SIZE_W, EASY_SCREEN_SIZE_H)
        self.InitChessman(CHESS_DIFFICULTY.Difficult_Easy)
        self.canvas.updateCanvas()
        self.slot_StopAndClearTimer()
        self.button.setStyleSheet("QPushButton{\n"
            "background-image: url(\"%s\");\n"
            "background-position:center;\n"
            "background-repeat:no-repeat;\n"
            "}" % self.img_path_s1)

    def middleFunc(self):
        self.Easy.setChecked(False)
        self.Middle.setChecked(True)
        self.Hard.setChecked(False)
        mainwidth = MID_SCREEN_SIZE_W
        mainheight = MID_SCREEN_SIZE_H
        self.setGeometry(100, 100, MID_SCREEN_SIZE_W, MID_SCREEN_SIZE_H)
        self.InitChessman(CHESS_DIFFICULTY.Difficult_Middle)
        self.canvas.updateCanvas()
        self.slot_StopAndClearTimer()
        self.button.setStyleSheet("QPushButton{\n"
            "background-image: url(\"%s\");\n"
            "background-position:center;\n"
            "background-repeat:no-repeat;\n"
            "}" % self.img_path_s1)
            
    def hardFunc(self):
        self.Easy.setChecked(False)
        self.Middle.setChecked(False)
        self.Hard.setChecked(True)
        mainwidth = HARD_SCREEN_SIZE_W
        mainheight = HARD_SCREEN_SIZE_H
        self.setGeometry(100, 100, HARD_SCREEN_SIZE_W, HARD_SCREEN_SIZE_H)
        self.InitChessman(CHESS_DIFFICULTY.Difficult_Hard)
        self.canvas.updateCanvas()
        self.slot_StopAndClearTimer()
        self.button.setStyleSheet("QPushButton{\n"
            "background-image: url(\"%s\");\n"
            "background-position:center;\n"
            "background-repeat:no-repeat;\n"
            "}" % self.img_path_s1)

    def aboutFunc(self):
        trans = QTranslator()
        if self.Language == LANGUAGE.English:
            self.app.installTranslator(self.English)
        else:
            self.app.installTranslator(self.Chinese)
        
        self.app.installTranslator(trans)
        QMessageBox.about(self,self.tr("About"),self.tr("1.0 version Copyright 03-28-2025 zhaoyong"))
        
    def onTimer(self):
        self.counter = self.counter + 1
        self.lcd1.display(self.counter)
    
    def slot_GameFail(self,msg):
        print("slot_GameFail")
        self.button.setStyleSheet("QPushButton{\n"
            "background-image: url(\"%s\");\n"
            "background-position:center;\n"
            "background-repeat:no-repeat;\n"
            "}" % self.img_path_s2)
            
    def slot_StopAndClearTimer(self):
        self.mineTimer.stop()
        self.counter = 0
        self.lcd1.display(0)
        self.lcd2.display(minenum)
        
    def slot_StopMine(self,msg):
        self.mineTimer.stop()
        
    def slot_StartMine(self,msg):
        print("slot_StartMine!!!" + msg)
        self.mineTimer.start(1000)

    def slot_SetMineNumber(self,c):
        self.lcd2.display(c)

    def ButtonNewGame(self):
        global level
        if level == CHESS_DIFFICULTY.Difficult_Easy:
            self.easyFunc()
        elif level == CHESS_DIFFICULTY.Difficult_Middle:
            self.middleFunc()
        else:
            self.hardFunc()

    def InitChessman(self,chess_level):
        global RowCount
        global ColCount
        global chessnum
        global minenum
        global level
        global sChessmine
        global hx1
        global hy1
        global bh
        global bw
        global bMineDefeat
        global iFindMineNumber
        global game_result
        global bStartMine
        i = 0
        j = 0
        iMinenum = 0
        iMineCol = 0
        iMineCount = 0
        bMineDefeat = False;
        iFindMineNumber = 0;
        bStartMine = False;
        level = chess_level;
        game_result = GAME_RESULT.PROGRESSING;
        print("level:" + str(level))
        if level == CHESS_DIFFICULTY.Difficult_Easy:
            RowCount = CHESSNUM_EASY;
            ColCount = CHESSNUM_EASY;
            chessnum = CHESSNUM_EASY;
            minenum = MINESNUM_EASY;
            hx1 = 10;
            hy1 = 3;
            bh = 40;
            bw = bh;
        elif level == CHESS_DIFFICULTY.Difficult_Middle:
            RowCount = CHESSNUM_MID;
            ColCount = CHESSNUM_MID;
            chessnum = CHESSNUM_MID;
            minenum = MINESNUM_MID;
            hx1 = 10;
            hy1 = 3;
            bh = 30;
            bw = bh;
        else:
            RowCount = CHESSNUM_HARD;
            ColCount = CHESSNUM_HARD;
            chessnum = CHESSNUM_HARD;
            minenum = MINESNUM_HARD;
            hx1 = 10;
            hy1 = 3;
            bh = 30;
            bw = bh;
        
        sChessmine = [[Chessmantype() for j in range(ColCount)] for i in range(RowCount)]
        for i in range(RowCount):
            for j in range(ColCount):
                sChessmine[i][j].bMineType = False
                sChessmine[i][j].eGridType = GridType.GRID_NORMAL
                sChessmine[i][j].bCheck = False
                sChessmine[i][j].iMineNum = 0
                sChessmine[i][j].x = hx1 + bw * i + 1
                sChessmine[i][j].y = hy1 + bh * j + 1
                
        i = 0
        while i < chessnum:
            iMineCol = random.randint(0, chessnum - 1)
            if sChessmine[i][iMineCol].bMineType == False and IfExistMineInCurrentCol(iMineCol) == False:
                sChessmine[i][iMineCol].bMineType = True;
                sChessmine[i][iMineCol].iMineNum  = -1;
                i = i + 1
                iMinenum = iMinenum + 1
                
        while iMinenum < minenum:
            i = random.randint(0, chessnum - 1)
            j = random.randint(0, chessnum - 1)
            if sChessmine[i][j].bMineType == False:
                sChessmine[i][j].bMineType = True
                sChessmine[i][j].iMineNum  = -1
                iMinenum = iMinenum + 1
        
        i = 0
        j = 0
        for i in range(chessnum):
            for j in range(chessnum):
                if sChessmine[i][j].bMineType == False:
                    iMineCount = 0
                    if ((i == 0) and (j == 0)):
                        if sChessmine[i][j + 1].bMineType == True:
                            iMineCount = iMineCount + 1
                        if sChessmine[i + 1][j].bMineType == True:
                            iMineCount = iMineCount + 1
                        if sChessmine[i + 1][j + 1].bMineType == True:
                            iMineCount = iMineCount + 1
                    elif ((i == 0) and (0 < j) and (j < chessnum - 1)):
                        if sChessmine[i][j - 1].bMineType == True:
                            iMineCount = iMineCount + 1
                        if sChessmine[i][j + 1].bMineType == True:
                            iMineCount = iMineCount + 1
                        if sChessmine[i + 1][j - 1].bMineType == True:
                            iMineCount = iMineCount + 1
                        if sChessmine[i + 1][j].bMineType == True:
                            iMineCount = iMineCount + 1
                        if sChessmine[i + 1][j + 1].bMineType == True:
                            iMineCount = iMineCount + 1
                    elif ((i == 0) and (j == chessnum - 1)):
                        if sChessmine[i][j - 1].bMineType == True:
                            iMineCount = iMineCount + 1
                        if sChessmine[i + 1][j - 1].bMineType == True:
                            iMineCount = iMineCount + 1
                        if sChessmine[i + 1][j].bMineType == True:
                            iMineCount = iMineCount + 1
                    elif ((0 < i) and (i < chessnum - 1) and (j == 0)):
                        if sChessmine[i - 1][j].bMineType == True:
                            iMineCount = iMineCount + 1
                        if sChessmine[i - 1][j + 1].bMineType == True:
                            iMineCount = iMineCount + 1
                        if sChessmine[i][j + 1].bMineType == True:
                            iMineCount = iMineCount + 1
                        if sChessmine[i + 1][j + 1].bMineType == True:
                            iMineCount = iMineCount + 1
                        if sChessmine[i + 1][j].bMineType == True:
                            iMineCount = iMineCount + 1
                    elif ((0 < i) and (i < chessnum - 1) and (j == chessnum - 1)):
                        if sChessmine[i - 1][j - 1].bMineType == True:
                            iMineCount = iMineCount + 1
                        if sChessmine[i - 1][j].bMineType == True:
                            iMineCount = iMineCount + 1
                        if sChessmine[i][j - 1].bMineType == True:
                            iMineCount = iMineCount + 1
                        if sChessmine[i + 1][j - 1].bMineType == True:
                            iMineCount = iMineCount + 1
                        if sChessmine[i + 1][j].bMineType == True:
                            iMineCount = iMineCount + 1
                    elif ((i == chessnum - 1) and (j == 0)):
                        if sChessmine[i - 1][j].bMineType == True:
                            iMineCount = iMineCount + 1
                        if sChessmine[i - 1][j + 1].bMineType == True:
                            iMineCount = iMineCount + 1
                        if sChessmine[i][j + 1].bMineType == True:
                            iMineCount = iMineCount + 1
                    elif ((i == chessnum - 1) and (0 < j) and (j < chessnum - 1)):
                        if sChessmine[i - 1][j - 1].bMineType == True:
                            iMineCount = iMineCount + 1
                        if sChessmine[i - 1][j].bMineType == True:
                            iMineCount = iMineCount + 1
                        if sChessmine[i - 1][j + 1].bMineType == True:
                            iMineCount = iMineCount + 1
                        if sChessmine[i][j - 1].bMineType == True:
                            iMineCount = iMineCount + 1
                        if sChessmine[i][j + 1].bMineType == True:
                            iMineCount = iMineCount + 1
                    elif ((i == chessnum - 1) and (j == chessnum - 1)):
                        if sChessmine[i - 1][j].bMineType == True:
                            iMineCount = iMineCount + 1
                        if sChessmine[i - 1][j - 1].bMineType == True:
                            iMineCount = iMineCount + 1
                        if sChessmine[i][j - 1].bMineType == True:
                            iMineCount = iMineCount + 1
                    else:
                        if sChessmine[i - 1][j - 1].bMineType == True:
                            iMineCount = iMineCount + 1
                        if sChessmine[i - 1][j].bMineType == True:
                            iMineCount = iMineCount + 1
                        if sChessmine[i - 1][j + 1].bMineType == True:
                            iMineCount = iMineCount + 1
                        if sChessmine[i][j - 1].bMineType == True:
                            iMineCount = iMineCount + 1
                        if sChessmine[i][j + 1].bMineType == True:
                            iMineCount = iMineCount + 1
                        if sChessmine[i + 1][j - 1].bMineType == True:
                            iMineCount = iMineCount + 1
                        if sChessmine[i + 1][j].bMineType == True:
                            iMineCount = iMineCount + 1
                        if sChessmine[i + 1][j + 1].bMineType == True:
                            iMineCount = iMineCount + 1
                    
                    sChessmine[i][j].iMineNum = iMineCount;
            
        minucount = 0
#        for i in range(chessnum):
#            ss = ""
#            for j in range(chessnum):
#                ss = ss + "(" + str(sChessmine[i][j].iMineNum) + ")" + "\t"
#                if sChessmine[i][j].iMineNum == -1:
#                    minucount = minucount + 1
#            print(ss)
#        print("minucount:" + str(minucount))
            
    def processtrigger(self,q):
        print(q.text()+" is triggered")

class CanvasWidget(QWidget):
    GameStart = pyqtSignal(str)
    GameStop = pyqtSignal(str)
    GameSetMineNumber = pyqtSignal(int)
    GameFail = pyqtSignal(str)
    def __init__(self,parent=None):
        super().__init__(parent)
        self.initUI()
        
    def initUI(self):
        self.blackmine = QPixmap("blackmine.png")
        self.redmine = QPixmap("redmine.png")
        self.interrogation = QPixmap("interrogation.png");
        self.flag = QPixmap("flag.png");
        self.setMinimumSize(100, 100)
        
    def updateCanvas(self):
        self.update()
        
    def GetChessNumber(self,x,y):
        global chessnum
        global sChessmine
        global bw
        global bh 
        for i in range(chessnum):
            for j in range(chessnum):
                if sChessmine[i][j].x < x and x < sChessmine[i][j].x + bw and \
                    sChessmine[i][j].y < y and y < sChessmine[i][j].y + bh:
                    return [i,j]
        return None

    def MineOver(self):
        global bStartMine
        if bStartMine == False:
            #print("The mine hasn't start")
            return
        bStartMine = False
        self.GameStop.emit("MineOver from CanvasWidget")
    
    def BeginMine(self):
        global bStartMine
        if bStartMine:
            #print("The mine has started!")
            return
        bStartMine = True
        self.GameStart.emit("BeginMine from CanvasWidget")

    def mousePressEvent(self, event):
        global sChessmine
        global bMineDefeat
        global game_result
        irow = 0
        icol = 0
        lst = self.GetChessNumber(event.x(),event.y())
        if lst is None:
            return
        irow = lst[0]
        icol = lst[1]
        print("mousePressEvent,irow:" + str(irow) + " icol:" + str(icol))
        
        if self.IfGameOver():
            self.MineOver()
            return
            
        self.BeginMine()
        
        if event.buttons() == Qt.LeftButton:
            if sChessmine[irow][icol].bMineType:
                sChessmine[irow][icol].eGridType = GridType.GRID_DEFEAT;
                bMineDefeat = True
                game_result = GAME_RESULT.FAIL
                self.MineOver()
            else:
                if sChessmine[irow][icol].eGridType != GridType.GRID_NORMAL:
                    return
                if sChessmine[irow][icol].iMineNum == 0:
                    SetMines(irow,icol)
                else:
                    sChessmine[irow][icol].eGridType = GridType.GRID_CLICKOPEN;
                    
                if self.IfGameOver():
                    game_result = GAME_RESULT.SUCCESS;
                    self.MineOver()
                    
            self.update()
        elif event.buttons() == Qt.RightButton:
            if sChessmine[irow][icol].eGridType == GridType.GRID_NORMAL:
                sChessmine[irow][icol].eGridType = GridType.GRID_FLAG;
                self.SetMineNumber(1)
                if self.IfGameOver():
                    game_result = GAME_RESULT.SUCCESS;
                    self.MineOver()
            elif sChessmine[irow][icol].eGridType == GridType.GRID_FLAG:
                sChessmine[irow][icol].eGridType = GridType.GRID_INTERROGATION;
                self.SetMineNumber(-1)
            elif sChessmine[irow][icol].eGridType == GridType.GRID_INTERROGATION:
                sChessmine[irow][icol].eGridType = GridType.GRID_NORMAL;
            else:
                print("irow:" + str(irow) + ",icol:" + str(icol) + " default")
            
            self.update()

    def SetMineNumber(self,iValue):
        global iFindMineNumber
        global minenum
        if iValue > 0:
            if iFindMineNumber >= minenum:
                return
            iFindMineNumber = iFindMineNumber + 1
        elif iValue < 0:
            if iFindMineNumber <= 0:
                return
            iFindMineNumber = iFindMineNumber - 1
        self.GameSetMineNumber.emit(minenum - iFindMineNumber)
            
    def IfGameOver(self):
        global chessnum
        global sChessmine
        global minenum
        iMineNumber = 0
        for i in range(chessnum):
            for j in range(chessnum):
                if sChessmine[i][j].eGridType == GridType.GRID_FLAG and sChessmine[i][j].bMineType:
                    iMineNumber = iMineNumber + 1

        for i in range(chessnum):
            for j in range(chessnum):
                if sChessmine[i][j].bMineType == False and sChessmine[i][j].eGridType != GridType.GRID_CLICKOPEN:
                    return False

        if minenum == iMineNumber:
            return True
        else:
            return False
    
    def paintEvent(self, event):
        global bMineDefeat
        global sChessmine
        global game_result
        global bw
        global bh
        iPicWidth = 30
        iPicHeight = 30;
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        painter.setPen(QColor(192,192,192))
        painter.setBrush(QColor(192,192,192))
        
        iLinenum = (chessnum + 1) * 2;
        for i in range(iLinenum):
            if i < iLinenum / 2:
                painter.drawLine(hx1,int(hy1 + bh * i),int(hx1 + bw * chessnum),int(hy1 + bh * i))
            else:
                painter.drawLine(int(hx1 + bw * (i - iLinenum / 2)),int(hy1),int(hx1 + bw * (i - iLinenum / 2)),int(hy1 + bh * chessnum))
        
        for i in range(chessnum):
            for j in range(chessnum):
                if bMineDefeat:
                    if sChessmine[i][j].eGridType == GridType.GRID_DEFEAT:
                        painter.drawPixmap(sChessmine[i][j].x + 1,sChessmine[i][j].y + 1, self.redmine)
                    else:
                        if sChessmine[i][j].bMineType:
                            painter.drawPixmap(sChessmine[i][j].x + 1,sChessmine[i][j].y + 1, self.blackmine)
                        elif sChessmine[i][j].iMineNum != 0:
                            painter.drawText(sChessmine[i][j].x + 15,sChessmine[i][j].y + 10,sChessmine[i][j].x + bw,sChessmine[i][j].y + bh,0,str(sChessmine[i][j].iMineNum))
                else:
                    if sChessmine[i][j].eGridType == GridType.GRID_NORMAL:
                        painter.drawRect(sChessmine[i][j].x + 1, sChessmine[i][j].y + 1,bw - 2,bh - 2)
                    elif sChessmine[i][j].eGridType == GridType.GRID_FLAG:
                        painter.drawPixmap(sChessmine[i][j].x,sChessmine[i][j].y , self.flag)
                    elif sChessmine[i][j].eGridType == GridType.GRID_INTERROGATION:
                        painter.drawPixmap(sChessmine[i][j].x,sChessmine[i][j].y , self.interrogation)
                    elif sChessmine[i][j].eGridType == GridType.GRID_CLICKOPEN:
                        if sChessmine[i][j].iMineNum == -1:
                            painter.drawRect(sChessmine[i][j].x + 1, sChessmine[i][j].y + 1,bw - 2,bh - 2)
                        elif sChessmine[i][j].iMineNum != 0:
                            painter.drawText(sChessmine[i][j].x + 15,sChessmine[i][j].y + 10,sChessmine[i][j].x + bw,sChessmine[i][j].y + bh,0,str(sChessmine[i][j].iMineNum))
                            
        if bMineDefeat or self.IfGameOver():
            if game_result == GAME_RESULT.FAIL:
                print("emit gamefail();")
                self.GameFail.emit("Game fail!")
                self.MineOver()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    trans = QTranslator()
    trans.load('./en_us.qm')
    
    transCh = QTranslator()
    transCh.load('./zh_CN.qm')
    app.installTranslator(trans)
    
    window = MainWindow(app,trans,transCh)
    window.show()
    sys.exit(app.exec_())
