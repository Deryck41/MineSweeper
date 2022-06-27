import sys
import random
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui



icons = {'normal':'resources/normal.png',
	'excited':'resources/excited.png',
	'dead':'resources/dead.png',
	'flag':'resources/flag.png'}

levels = {'easy':{'width':9, 'height':9, 'mines':10},
	'normal':{'width':16, 'height':16, 'mines':40},
	'hard':{'width':30, 'height':30, 'mines':99}}

class MainWindow(QtWidgets.QMainWindow):
	def __init__(self, *argc, **argv):
		super().__init__(*argc, **argv)
		self.virtualCells = []
		self.flagCells = []
		self.width = 9
		self.height = 9
		self.mines = 10
		self.endOfGame = False
		self.gameStart = False
		self.seconds = 0
		self.timer = QtCore.QTimer(self)
		self.timer.setInterval(1000)
		self.timer.timeout.connect(self.displayTime)
		self.initUI()
		self.level = levels['easy']
		self.initGame()

	def gameEnd(self, win):
		self.endOfGame = True
		self.timer.stop()
		if win:
			self.setWindowTitle('Win!')
		else:
			self.buttonStart.setIcon(QtGui.QIcon(icons['dead']))
			self.setWindowTitle('Lose!')
			for i in range(self.height):
				for j in range(self.width):
					if self.virtualCells[i][j] == -1:
						self.cells[i][j].hide()
						self.fieldGrid.removeWidget(self.cells[i][j])
						lab = QtWidgets.QLabel("")
						lab.setStyleSheet("border-image: url(resources/mine.png) 0 0 0 0 stretch stretch;")
						lab.setAlignment(QtCore.Qt.AlignCenter)
						self.resize(lab, 20, 20)
						self.fieldGrid.addWidget(lab, i, j)

	def checkWin(self):
		for i in range(self.height):
			for j in range(self.width):
				if self.virtualCells[i][j] != -1:
					if not self.cells[i][j].isHidden():
						return False
		self.gameEnd(True)

	def displayTime(self):
		self.seconds+=1
		self.timeDisplay.display(str(self.seconds).zfill(3))

	def restartGame(self):
		self.virtualCells = []
		self.flagCells = []
		self.gameStart = False
		self.seconds = 0
		self.timeDisplay.display('000')
		self.endOfGame = False
		self.buttonStart.setIcon(QtGui.QIcon(icons['normal']))
		for i in reversed(range(self.fieldGrid.count())): 
			self.fieldGrid.itemAt(i).widget().hide()
			self.fieldGrid.removeWidget(self.fieldGrid.itemAt(i).widget())
		self.initGame()
	def generateGameField(self, y, x):
		def checkAndAdd(y, x):
			if self.virtualCells[y][x] != -1:
				self.virtualCells[y][x] += 1
		self.virtualCells = []
		freeCells = []
		for i in range(self.height):
			self.virtualCells.append([])
			for j in range(self.width):
				if (i == y and j == x) or (i == y + 1 and j == x) or (i == y + 1 and j == x + 1) or (i == y and j == x + 1) or (i == y - 1 and j == x + 1) or (i == y - 1 and j == x) or (i == y - 1 and j == x - 1) or (i == y and j == x) or (i == y and j == x - 1) or (i == y + 1 and j == x - 1):
					self.virtualCells[i].append(0)
				else:
					self.virtualCells[i].append(0)
					freeCells.append({i:j})

		for i in range(self.mines):
			coords = freeCells.pop(random.randrange(len(freeCells)))
			y = next(iter(coords))
			x = next(iter(coords.values()))
			self.virtualCells[y][x] = -1

		for i in range(self.height):
			for j in range(self.width):
				if self.virtualCells[i][j] == -1:
					if j + 1 < self.width:
						checkAndAdd(i, j + 1)
						if i - 1 >= 0:
							checkAndAdd(i - 1, j + 1)
						if i + 1 < self.height:
							checkAndAdd(i + 1, j + 1)
					if j - 1 >= 0:
						checkAndAdd(i, j - 1)
						if i - 1 >= 0:
							checkAndAdd(i - 1, j - 1)
						if i + 1 < self.height:
							checkAndAdd(i + 1, j -1)
					if i + 1 < self.height:
						checkAndAdd(i + 1, j)
					if i - 1 >= 0:
						checkAndAdd(i - 1, j)

		self.gameStart = True
		self.timer.start()

	def cellLClicked(self, y, x):
		if not self.endOfGame:
			for i in range(self.height):
				for j in range(self.width):
					if i == y and j == x:
						if not self.flagCells[i][j]:
							if self.gameStart:
								
								if self.virtualCells[i][j] == 0:
									self.cells[i][j].hide()
									self.fieldGrid.removeWidget(self.cells[i][j])
									lab = QtWidgets.QLabel("")
									lab.setAlignment(QtCore.Qt.AlignCenter)
									self.resize(lab, 20, 20)
									self.fieldGrid.addWidget(lab, i, j)
								elif self.virtualCells[i][j] != -1:
									self.cells[i][j].hide()
									self.fieldGrid.removeWidget(self.cells[i][j])
									lab = QtWidgets.QLabel(str(self.virtualCells[i][j]))
									lab.setAlignment(QtCore.Qt.AlignCenter)
									self.resize(lab, 20, 20)
									self.fieldGrid.addWidget(lab, i, j)
								else:
									self.gameEnd(False)
								
							else:
								self.generateGameField(i, j)
								self.cells[i][j].hide()
			self.checkWin()

	def cellRClicked(self, y, x):
		if not self.endOfGame:
			for i in range(self.height):
				for j in range(self.width):
					if i == y and j == x:

						if self.flagCells[i][j]:
							self.mines+=1
							self.cells[i][j].setIcon(QtGui.QIcon())
							self.flagCells[i][j] = not self.flagCells[i][j]
						else:
							if self.mines != 0:
								self.mines-=1
								self.cells[i][j].setIconSize(QtCore.QSize(17, 17))
								self.cells[i][j].setIcon(QtGui.QIcon(icons['flag']))
								self.flagCells[i][j] = not self.flagCells[i][j]
						self.updateMinesDisplay()

			self.checkWin()

	def initGame(self):
		self.setWindowTitle('Minesweeper')
		self.initField(self.level['width'], self.level['height'])
		self.minesDisplay.display(str(self.level['mines']).zfill(3))
		self.width, self.height = self.level['width'], self.level['height']
		self.mines = self.level['mines']

		for i in range(self.height):
			self.flagCells.append([])
			for j in range(self.width):
				self.flagCells[i].append(False)

	def updateMinesDisplay(self):
		self.minesDisplay.display(str(self.mines).zfill(3))

	def initField(self, width, height):
		self.cells = []
		for i in range(height):
			self.cells.append([])
			for j in range(width):
				self.cells[i].append(QtWidgets.QPushButton(""))
				self.cells[i][j].setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
				self.cells[i][j].customContextMenuRequested.connect(lambda checked, y = i, x = j: self.cellRClicked(y, x))
				self.cells[i][j].clicked.connect(lambda checked, y = i, x = j: self.cellLClicked(y, x))
				self.resize(self.cells[i][j], 20, 20)
				self.fieldGrid.addWidget(self.cells[i][j], i, j)

	def resize(self, widget, width, height):
		widget.setMinimumWidth(width)
		widget.setMaximumWidth(width)
		widget.setMinimumHeight(height)
		widget.setMaximumHeight(height)

	def initUI(self):
		mainWidget = QtWidgets.QWidget()
		mainLayout = QtWidgets.QVBoxLayout()
		mainLayout.setContentsMargins(0,0,0,0)
		mainLayout.setSpacing(0)
		mainWidget.setLayout(mainLayout)
		self.setCentralWidget(mainWidget)

		topWidget = QtWidgets.QWidget()
		topWidget.setFixedHeight(40)
		#topWidget.setStyleSheet("background-color: red")
		mainLayout.addWidget(topWidget, alignment=QtCore.Qt.AlignTop)
		controlLayout = QtWidgets.QHBoxLayout()
		controlLayout.setContentsMargins(5,0,5,0)
		topWidget.setLayout(controlLayout)

		self.minesDisplay = QtWidgets.QLCDNumber()
		self.minesDisplay.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
		self.minesDisplay.display('000')
		self.minesDisplay.setMinimumHeight(38)
		self.minesDisplay.setDigitCount(3)
		self.timeDisplay = QtWidgets.QLCDNumber()
		self.timeDisplay.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
		self.timeDisplay.setDigitCount(3)
		self.timeDisplay.display('000')
		self.timeDisplay.setMinimumHeight(38)
		self.buttonStart = QtWidgets.QPushButton("")
		self.buttonStart.clicked.connect(self.restartGame)
		self.buttonStart.setMinimumHeight(34)
		self.buttonStart.setMinimumWidth(38)
		self.buttonStart.setIconSize(QtCore.QSize(24, 24))
		self.buttonStart.setIcon(QtGui.QIcon(icons['normal']))
		controlLayout.addWidget(self.minesDisplay, alignment=QtCore.Qt.AlignLeft)
		controlLayout.addWidget(self.buttonStart, alignment=QtCore.Qt.AlignCenter)
		controlLayout.addWidget(self.timeDisplay, alignment=QtCore.Qt.AlignRight)

		fieldWidget = QtWidgets.QWidget()
		#fieldWidget.setStyleSheet("background-color: blue")
		self.fieldGrid = QtWidgets.QGridLayout()
		self.fieldGrid.setSpacing(0)
		self.cells = []
		fieldWidget.setLayout(self.fieldGrid)
		mainLayout.addStretch(1)
		mainLayout.addWidget(fieldWidget, 999)
		mainLayout.addStretch(1)



if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	file = open("resources/style.css", "r")
	app.setStyleSheet(file.read())

	file.close()
	window = MainWindow()
	window.show()

	sys.exit(app.exec_())