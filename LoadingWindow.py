from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class LoadingWindow(QtWidgets.QMainWindow):
    def __init__(self, parent: QMainWindow, imitation_window: QMainWindow):
        super().__init__()
        self.parent: QMainWindow = parent
        self.imitation_window: QMainWindow = imitation_window
        self.initUI()

    def initUI(self) -> None:
        self.setFixedSize(self.imitation_window.frameGeometry().width(), self.imitation_window.frameGeometry().height())
        self.setWindowIcon(QtGui.QIcon("files/youtube_icon.png"))
        self.setIconSize(QtCore.QSize(24, 24))
        self.setWindowTitle("Download Video")

        self.label: QtWidgets.QLabel = QtWidgets.QLabel(self)
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setMinimumSize(QtCore.QSize(200, 200))
        self.label.move((self.imitation_window.frameGeometry().width() - self.label.width()) / 2,
                        (self.imitation_window.frameGeometry().height() - self.label.height()) / 2)

        self.movie: QMovie = QMovie("F:\\Python\\Python Projects\\YouTubeDownload\\files\\loader_spinner.gif")
        self.label.setMovie(self.movie)
        self.movie.start()

        quit: QAction = QAction("Quit", self)
        quit.triggered.connect(self.closeEvent)

    def closeEvent(self, event) -> None:
        self.hide()
        self.parent.show()
