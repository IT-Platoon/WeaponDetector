# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/run/media/zzarryadd/E602B7E902B7BD3D/Users/Admin/YandexDisk/coding/Hakatons/weapon_detector/weapon_detector/qt/main_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DetectionWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(811, 608)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setToolTip("")
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout = QtWidgets.QGridLayout(self.tab)
        self.gridLayout.setObjectName("gridLayout")
        self.widget = QtWidgets.QWidget(self.tab)
        self.widget.setObjectName("widget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.load_button = QtWidgets.QToolButton(self.widget)
        self.load_button.setMinimumSize(QtCore.QSize(300, 300))
        self.load_button.setStyleSheet("")
        self.load_button.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/download.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.load_button.setIcon(icon)
        self.load_button.setIconSize(QtCore.QSize(64, 64))
        self.load_button.setObjectName("load_button")
        self.gridLayout_2.addWidget(self.load_button, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.widget, 2, 0, 1, 1)
        self.select_files = QtWidgets.QComboBox(self.tab)
        self.select_files.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.select_files.setObjectName("select_files")
        self.select_files.addItem("")
        self.select_files.addItem("")
        self.select_files.addItem("")
        self.select_files.addItem("")
        self.gridLayout.addWidget(self.select_files, 0, 0, 1, 1)
        self.select_model = QtWidgets.QComboBox(self.tab)
        self.select_model.setObjectName("select_model")
        self.select_model.addItem("")
        self.select_model.addItem("")
        self.gridLayout.addWidget(self.select_model, 1, 0, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.tab_5)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.reference = QtWidgets.QPlainTextEdit(self.tab_5)
        self.reference.setObjectName("reference")
        self.gridLayout_5.addWidget(self.reference, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_5, "")
        self.gridLayout_3.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.load_button.setToolTip(_translate("MainWindow", "Загрузить данные для детекции"))
        self.select_files.setItemText(0, _translate("MainWindow", "Указать файл(ы) для детекции по изображениям"))
        self.select_files.setItemText(1, _translate("MainWindow", "Указать файл(ы) для детекции по видео"))
        self.select_files.setItemText(2, _translate("MainWindow", "Указать путь до директории с изображениями"))
        self.select_files.setItemText(3, _translate("MainWindow", "Указать путь до директории с видео"))
        self.select_model.setItemText(0, _translate("MainWindow", "Модель бинарной классификации"))
        self.select_model.setItemText(1, _translate("MainWindow", "Модель категориальной классификации"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Детекция"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), _translate("MainWindow", "Справка"))
from . import resources
