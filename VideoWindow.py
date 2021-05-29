from PyQt5.QtWidgets import QAction
from VideoThread import VideoDownload
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class VideoWindow(QtWidgets.QMainWindow):
    def __init__(self, parent: QtWidgets.QMainWindow):
        super().__init__()
        self.parent: QtWidgets.QMainWindow = parent
        self.initUI()
        self.link: str = ""
        self.video_items: dict = {}
        self.audio_items: dict = {}

    def initUI(self) -> None:
        self.setObjectName("MainWindow")
        self.setFixedSize(570, 230)
        self.setWindowIcon(QtGui.QIcon("files/youtube_icon.png"))
        self.setIconSize(QtCore.QSize(24, 24))

        self.centralwidget: QtWidgets.QWidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.graphicsView: QtWidgets.QLabel = QtWidgets.QLabel(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(10, 10, 260, 147))
        self.graphicsView.setScaledContents(True)
        self.graphicsView.setObjectName("graphicsView")

        self.titleLabel: ScaledLabel = ScaledLabel(self.centralwidget)
        self.titleLabel.setGeometry(QtCore.QRect(12, 160, 260, 60))
        self.titleLabel.setFont(QtGui.QFont('MS Shell Dlg 2', 12))
        self.titleLabel.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.titleLabel.setWordWrap(True)
        self.titleLabel.setObjectName("titleLabel")
        size_policy = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.titleLabel.setSizePolicy(size_policy)
        self.titleLabel.setScaledContents(True)
        self.titleLabel.setMinimumSize(260, 60)

        self.formatComboBox: QtWidgets.QComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.formatComboBox.setGeometry(QtCore.QRect(290, 10, 155, 35))
        self.formatComboBox.setObjectName("formatComboBox")
        self.formatComboBox.activated.connect(self.handle_item_pressed)

        self.audioCheckBox: QtWidgets.QCheckBox = QtWidgets.QCheckBox(self.centralwidget)
        self.audioCheckBox.setGeometry(QtCore.QRect(470, 12, 80, 30))
        self.audioCheckBox.stateChanged.connect(self.fill_combobox)

        font: QtGui.QFont = QtGui.QFont()
        font.setPointSize(10)
        font.setUnderline(True)

        self.audioCheckBox.setFont(font)
        self.audioCheckBox.setObjectName("audioCheckBox")
        self.setCentralWidget(self.centralwidget)

        self.loaing_label: QtWidgets.QLabel = QtWidgets.QLabel(self)
        self.loaing_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.loaing_label.setGeometry(QtCore.QRect(330, 35, 200, 200))
        self.loaing_label.hide()

        self.movie: QMovie = QMovie("files/loader_spinner.gif")
        self.loaing_label.setMovie(self.movie)
        self.movie.start()

        quit: QAction = QAction("Quit", self)
        quit.triggered.connect(self.closeEvent)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def closeEvent(self, event) -> None:
        self.hide()
        self.parent.show()

    def fill_combobox(self) -> None:
        self.formatComboBox.clear()
        if self.audioCheckBox.isChecked():
            self.formatComboBox.addItems(self.audio_items)
        else:
            self.formatComboBox.addItems(self.video_items)

    def handle_item_pressed(self, event) -> None:
        if self.audioCheckBox.isChecked():
            self.download_thread = VideoDownload(self, self.audio_items[self.formatComboBox.currentText()])
        else:
            self.download_thread = VideoDownload(self, self.video_items[self.formatComboBox.currentText()])
        self.formatComboBox.setEnabled(False)
        self.loaing_label.show()
        self.download_thread.start()

    def get_link(self) -> None:
        return self.parent.lineEdit.text()

    def retranslateUi(self) -> None:
        _translate: QtCore.QCoreApplication.translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Download Video"))
        self.titleLabel.setText(_translate("MainWindow", "TextLabel"))
        self.audioCheckBox.setText(_translate("MainWindow", "Audio only"))


class ScaledLabel(QLabel):

    def resize_font(self):
        if not self.hasScaledContents():
            return

        i = 0
        self.setFont(QtGui.QFont('MS Shell Dlg 2', 12))
        text = self.fontMetrics().boundingRect(self.text())
        while True:
            print(text.width() * text.height(), self.width() * self.height() - 1500)
            if text.width() * text.height() < self.width() * self.height() - 1500:
                return
            else:
                text = self.fontMetrics().boundingRect(self.text())
                self.setFont(QtGui.QFont('MS Shell Dlg 2', 12-i))
                i += 1