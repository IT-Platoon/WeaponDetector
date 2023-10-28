from PyQt5 import QtCore, QtGui, QtWidgets

from weapon_detector.forms import Ui_ResultItem


class ResultItem(QtWidgets.QWidget):
    def __init__(self, image_paths: list) -> None:
        super().__init__()
        self.ui = Ui_ResultItem()
        self.ui.setupUi(self)
        image_places = [self.ui.start_image, self.ui.result_image]
        self.start_image = image_paths[0]
        self.result_image = image_paths[1]
        for index, image_path in enumerate(image_paths):
            image = QtGui.QImage(image_path)
            pixmap = QtGui.QPixmap.fromImage(image)
            pixmap_resized = pixmap.scaled(
                512,
                512,
                QtCore.Qt.KeepAspectRatio,
            )
            image_places[index].setPixmap(pixmap_resized)
            image_places[index].setScaledContents(True)
