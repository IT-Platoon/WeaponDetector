import os

from PyQt5 import QtCore, QtWidgets

from weapon_detector.constants import (
    FAILED_SELECT,
    REFERENCE,
    RESULT_MESSAGE,
    MethodsLoad,
)
from weapon_detector.forms import Ui_DetectionWindow
from weapon_detector.ml import load_model, run_detection_webcam, run_detection_images, run_detection_videos
from weapon_detector.palettes import main_window_styles

from .result_dialog import ResultDialog


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_DetectionWindow()
        self.ui.setupUi(self)
        self.directory_to_save = ""
        self.files = []
        self.ui.reference.setPlainText(REFERENCE)
        self.ui.reference.setReadOnly(True)
        self.setStyleSheet(main_window_styles)
        self.result_model = None
        self.result_func = None
        self.model_path = ""
        self.progress_bar = None
        self.view_result = None

    @QtCore.pyqtSlot()
    def on_load_button_clicked(self) -> None:
        right_extensions_images = (".jpeg", ".jpg", ".png")
        right_extensions_videos = (".mp4",)
        method_load = self.ui.select_files.currentText()
        if method_load in (MethodsLoad.GET_FILES_IMAGES, MethodsLoad.GET_FILES_VIDEOS):
            media_type, media, extensions, self.result_func = (
                ("изображения", "Images", "*.jpeg *.jpg *.png", run_detection_images)
                if method_load == MethodsLoad.GET_FILES_IMAGES else
                ("видео файлы", "Videos", "*.mp4", run_detection_videos)
            )
            self.files, _ = QtWidgets.QFileDialog.getOpenFileNames(
                self,
                f"Выберите {media_type}",
                "/",
                f"{media} ({extensions})",
            )
        elif method_load in (MethodsLoad.GET_DIRECTORY_IMAGES, MethodsLoad.GET_DIRECTORY_VIDEOS):
            try:
                media_type, extensions, self.result_func = (
                    ("изображений", right_extensions_images, run_detection_images)
                    if method_load == MethodsLoad.GET_DIRECTORY_IMAGES else
                    ("видео файлов", right_extensions_videos, run_detection_videos)
                )
                directory_to_load = QtWidgets.QFileDialog.getExistingDirectory(
                    self,
                    f"Выберите директорию для загрузки {media_type}",
                    "/",
                )
                files = os.listdir(directory_to_load)
                self.files = [
                    os.path.join(directory_to_load, file)
                    for file in files
                    if file.endswith(extensions)
                ]
            except FileNotFoundError:
                pass
        elif method_load == MethodsLoad.WEBCAM:
            self.files = "0"
            self.result_func = run_detection_webcam
        self.directory_to_save = QtWidgets.QFileDialog.getExistingDirectory(
            self,
            "Выберите директорию для загрузки конечного csv",
            "/",
        )
        if self.files:
            self.model_path, _ = QtWidgets.QFileDialog.getOpenFileName(
                self,
                f"Выберите модель машинного обучения",
                "/",
                f"PyTorch (*.pt)",
            )
            self.result_model = load_model(self.model_path)
            result = self.compute_result()
            self.result_model = None
            self.result_func = None
            self.model_path = ""
            if result:
                self.finish_detecting(result)
        else:
            QtWidgets.QMessageBox.warning(
                self,
                "Ошибка!",
                FAILED_SELECT,
            )

    def compute_result(self):
        self.progress_bar = QtWidgets.QProgressDialog(
            minimum=0,
            maximum=100,
        )
        self.progress_bar.setAccessibleName("Прогресс детекции")
        self.progress_bar.setWindowTitle("Прогресс детекции")
        self.progress_bar.setCancelButtonText("Прервать")
        self.progress_bar.setMinimumDuration(0)
        self.progress_bar.setMinimumSize(550, 100)
        self.progress_bar.setWindowModality(QtCore.Qt.ApplicationModal)
        progress = 0
        detection = self.result_func(
            self.result_model,
            self.files,
            self.directory_to_save,
        )
        try:
            while True:
                progress = next(detection)
                if self.progress_bar.wasCanceled():
                    QtWidgets.QMessageBox.warning(
                        self,
                        "Детекция прервана!",
                        "Вы прервали детекцию!",
                    )
                    break
                self.progress_bar.setLabelText(f"Прогресс: {int(progress)}")
                self.progress_bar.setValue(int(progress))
        except StopIteration as exception:
            progress = 100
            self.progress_bar.setLabelText(f"Прогресс: {int(progress)}")
            self.progress_bar.setValue(int(progress))
            self.progress_bar.cancel()
            return exception.value
        except Exception as exception:
            self.progress_bar.cancel()
            QtWidgets.QMessageBox.warning(
                self,
                "Детекция прервана!",
                str(exception),
            )
            return None

    def finish_detecting(self, info: list) -> None:
        QtWidgets.QMessageBox.warning(
            self,
            "Детекция завершена!",
            RESULT_MESSAGE,
        )
        self.view_result = ResultDialog(info)
        self.view_result.show()
        self.view_result.exec_()
