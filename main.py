import sys
from gui.edge_based_dices_detection_screen import EdgeBasedDicesDetectionScreen
from PyQt5.QtWidgets import QApplication


def main():
    app = QApplication(sys.argv)
    video_screen = EdgeBasedDicesDetectionScreen("Video")
    video_screen.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()