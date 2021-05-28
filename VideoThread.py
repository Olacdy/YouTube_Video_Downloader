from PyQt5.QtCore import QThread
from PyQt5.QtGui import QImage, QPixmap
from pytube import YouTube, Stream, StreamQuery
import urllib
from utils import get_name_from_stream
from PyQt5.QtWidgets import QMainWindow


class VideoLoading(QThread):
    def __init__(self, video_window=None):
        QThread.__init__(self)
        self.video_window: QMainWindow = video_window

    def run(self) -> None:
        video: YouTube = YouTube(self.video_window.get_link())

        self.video_window.titleLabel.setText(video.title)

        data = urllib.request.urlopen(video.thumbnail_url).read()

        image: QImage = QImage()
        image.loadFromData(data)

        self.video_window.graphicsView.setPixmap(QPixmap(image))

        audio_streams: StreamQuery = video.streams.filter(only_audio=True)
        streams: list = [stream for stream in video.streams if stream not in audio_streams]

        video_items: dict = {get_name_from_stream(stream): stream for stream in streams}
        audio_items: dict = {get_name_from_stream(stream): stream for stream in audio_streams}

        self.video_window.audio_items = audio_items
        self.video_window.video_items = video_items

        print(self.video_window.titleLabel.fontMetrics().boundingRect(self.video_window.titleLabel.text()).width())
        self.video_window.fill_combobox()


class VideoDownload(QThread):
    def __init__(self, parent: QMainWindow, stream: Stream):
        QThread.__init__(self)
        self.parent: QMainWindow = parent
        self.stream: Stream = stream

    def run(self) -> None:
        self.stream.download()
        self.parent.formatComboBox.setEnabled(True)
        self.parent.loaing_label.hide()
