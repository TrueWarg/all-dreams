import sys
from gui.video_screen import VideoScreen
from PyQt5.QtWidgets import QApplication


def main():
    app = QApplication(sys.argv)
    video_screen = VideoScreen("Video")
    video_screen.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()