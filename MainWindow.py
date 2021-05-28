import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from VideoWindow import VideoWindow
from VideoThread import VideoLoading
from LoadingWindow import LoadingWindow
from pytube import YouTube


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.video_window: VideoWindow = VideoWindow(self)
        self.loading_window: LoadingWindow = LoadingWindow(self, self.video_window)

    def initUI(self) -> None:
        self.setWindowModality(QtCore.Qt.NonModal)
        self.setFixedSize(700, 100)
        self.setWindowIcon(QtGui.QIcon("files/youtube_icon.png"))
        self.setIconSize(QtCore.QSize(24, 24))
        self.setTabShape(QtWidgets.QTabWidget.Triangular)

        self.centralwidget: QtWidgets.QWidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2: QtWidgets.QHBoxLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.horizontalLayout: QtWidgets.QHBoxLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.linkLabel: QtWidgets.QLabel = QtWidgets.QLabel(self.centralwidget)
        self.linkLabel.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.linkLabel.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.linkLabel.setFrameShadow(QtWidgets.QFrame.Plain)
        self.linkLabel.setLineWidth(1)
        self.linkLabel.setMidLineWidth(0)
        self.linkLabel.setTextFormat(QtCore.Qt.AutoText)
        self.linkLabel.setObjectName("linkLabel")
        self.horizontalLayout.addWidget(self.linkLabel)

        self.gridLayout: QtWidgets.QGridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.gridLayout.setHorizontalSpacing(0)
        self.gridLayout.setObjectName("gridLayout")

        self.lineEdit: QtWidgets.QLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy: QtWidgets.QSizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                                                  QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setBaseSize(QtCore.QSize(0, 0))

        font: QtGui.QFont = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)

        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 0, 1, 1)

        self.findVideoButton: QtWidgets.QPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.findVideoButton.clicked.connect(self.button_clicked)
        self.findVideoButton.setMinimumSize(QtCore.QSize(0, 0))

        font: QtGui.QFont = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(-1)
        font.setUnderline(False)
        font.setStrikeOut(False)

        self.findVideoButton.setFont(font)
        self.findVideoButton.setStyleSheet("""
                        QPushButton {
                            background-color: #FF0000;
                            border: none;
                            color: white;
                            padding: 6px 20px;
                            text-align: center;
                            font-size: 16px;
                            margin: 0px 2px;
                            opacity: 0.6;
                            transition: 0.3s;
                            display: inline-block;
                            text-decoration: none;
                            cursor: pointer;
                        }

                        QPushButton::hover {background-color: #282828}

                        """)
        self.findVideoButton.setObjectName("findVideoButton")
        self.gridLayout.addWidget(self.findVideoButton, 0, 1, 1, 1)

        self.horizontalLayout.addLayout(self.gridLayout)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.setCentralWidget(self.centralwidget)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)
        self.show()

    def button_clicked(self) -> None:
        try:
            YouTube(self.lineEdit.text())
        except:
            return
        self.thread: VideoLoading = VideoLoading(self.video_window)
        self.thread.finished.connect(self.on_finished)
        self.thread.start()
        self.hide()
        self.loading_window.show()

    @QtCore.pyqtSlot()
    def on_finished(self) -> None:
        if not self.loading_window.isHidden():
            self.loading_window.hide()
            self.video_window.show()

    def retranslateUi(self) -> None:
        _translate: QtCore.QCoreApplication.translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Download Video"))
        self.linkLabel.setText(_translate("MainWindow", """
                                                        <html><head/><body><p><span style=
                                                        "font-size:12pt;
                                                        font-weight:600;">
                                                        Video Link:
                                                        </span></p></body></html>
                                                        """))
        self.findVideoButton.setText(_translate("MainWindow", "Find Video"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
