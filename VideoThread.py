from PyQt5.QtCore import QThread
from PyQt5.QtGui import QImage
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
        self.video_window.titleLabel.resize_font()

        data = urllib.request.urlopen(video.thumbnail_url).read()

        image: QImage = QImage()
        image.loadFromData(data)

        self.video_window.set_rounded_image(image)

        audio_streams: StreamQuery = video.streams.filter(only_audio=True)
        streams: list = [stream for stream in video.streams if stream not in audio_streams]

        video_items: dict = {get_name_from_stream(stream): stream for stream in streams}
        audio_items: dict = {get_name_from_stream(stream): stream for stream in audio_streams}

        self.video_window.audio_items = audio_items
        self.video_window.video_items = video_items

        self.video_window.fill_combobox()


class VideoDownload(QThread):
    def __init__(self, parent: QMainWindow, stream: Stream, title: str):
        QThread.__init__(self)
        self.parent: QMainWindow = parent
        self.stream: Stream = stream
        self.title = title

    def run(self) -> None:
        self.stream.download()
        try:
            self.parent.toaster.show_toast("Download finished!", self.title, icon_path='files/youtube_icon.ico',
                                    duration=5, threaded=True)
        except:
            pass
        self.parent.formatComboBox.setEnabled(True)
        self.parent.loaing_label.hide()