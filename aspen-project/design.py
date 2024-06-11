# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'design.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QAction,
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QApplication,
    QGroupBox,
    QLabel,
    QLayout,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QStatusBar,
    QTextBrowser,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(790, 600)
        MainWindow.setStyleSheet("background-color: #82CF83;")
        self.action = QAction(MainWindow)
        self.action.setObjectName("action")
        self.action_2 = QAction(MainWindow)
        self.action_2.setObjectName("action_2")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.groupBox.setGeometry(QRect(50, 50, 281, 271))
        self.groupBox.setStyleSheet("background-color: black; border-radius: 20%;")
        self.molFlow = QLabel(self.groupBox)
        self.molFlow.setObjectName("molFlow")
        self.molFlow.setGeometry(QRect(20, 20, 241, 81))
        self.molFlow.setStyleSheet(
            "color: white; font-family: Montserrat, sans-serif; font-size: 20px ;font-weight: bold; text-align: center;"
        )
        self.molFlow.setTextFormat(Qt.AutoText)
        self.molFlow.setScaledContents(False)
        self.molFlow.setAlignment(Qt.AlignCenter)
        self.molFlow.setWordWrap(True)
        self.dataMol = QTextEdit(self.groupBox)
        self.dataMol.setObjectName("dataMol")
        self.dataMol.setGeometry(QRect(20, 110, 241, 71))
        self.dataMol.setStyleSheet(
            "color: white; border-radius: 10%; background-color: #303932;  font-family: Montserrat, sans-serif; font-size: 20px ;font-weight: bold;"
        )
        self.calc = QPushButton(self.groupBox)
        self.calc.setObjectName("calc")
        self.calc.setGeometry(QRect(80, 210, 111, 41))
        self.calc.setStyleSheet(
            "color: black; font-family: Montserrat, sans-serif; font-size: 20px ;font-weight: bold; text-align: center;\n"
            "border-radius: 5%; background-color: #FFF200;"
        )
        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.groupBox_2.setGeometry(QRect(360, 50, 401, 481))
        self.groupBox_2.setStyleSheet("background-color: black; border-radius: 20%;")
        self.molFlow_2 = QLabel(self.groupBox_2)
        self.molFlow_2.setObjectName("molFlow_2")
        self.molFlow_2.setGeometry(QRect(20, 20, 361, 81))
        self.molFlow_2.setStyleSheet(
            "color: white; font-family: Montserrat, sans-serif; font-size: 20px ;font-weight: bold; text-align: center;"
        )
        self.molFlow_2.setTextFormat(Qt.AutoText)
        self.molFlow_2.setScaledContents(False)
        self.molFlow_2.setAlignment(Qt.AlignCenter)
        self.molFlow_2.setWordWrap(True)
        self.verticalLayoutWidget = QWidget(self.groupBox_2)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(29, 109, 351, 351))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.molFlow_4 = QLabel(self.verticalLayoutWidget)
        self.molFlow_4.setObjectName("molFlow_4")
        self.molFlow_4.setStyleSheet(
            "color: white; font-family: Montserrat, sans-serif; font-size: 15px ;font-weight: bold; text-align: center;"
        )
        self.molFlow_4.setTextFormat(Qt.AutoText)
        self.molFlow_4.setScaledContents(False)
        self.molFlow_4.setAlignment(Qt.AlignCenter)
        self.molFlow_4.setWordWrap(True)

        self.verticalLayout.addWidget(self.molFlow_4)

        self.dataMol_2 = QTextBrowser(self.verticalLayoutWidget)
        self.dataMol_2.setObjectName("dataMol_2")
        self.dataMol_2.setStyleSheet(
            "background-color: #303932; color: white; font-family: Montserrat, sans-serif; font-size: 15px ;font-weight: bold; text-align: center;"
        )

        self.verticalLayout.addWidget(self.dataMol_2)

        self.molFlow_3 = QLabel(self.verticalLayoutWidget)
        self.molFlow_3.setObjectName("molFlow_3")
        self.molFlow_3.setStyleSheet(
            "color: white; font-family: Montserrat, sans-serif; font-size: 15px ;font-weight: bold; text-align: center;"
        )
        self.molFlow_3.setTextFormat(Qt.AutoText)
        self.molFlow_3.setScaledContents(False)
        self.molFlow_3.setAlignment(Qt.AlignCenter)
        self.molFlow_3.setWordWrap(True)

        self.verticalLayout.addWidget(self.molFlow_3)

        self.dataMol_3 = QTextBrowser(self.verticalLayoutWidget)
        self.dataMol_3.setObjectName("dataMol_3")
        self.dataMol_3.setStyleSheet(
            "background-color: #303932; color: white; font-family: Montserrat, sans-serif; font-size: 15px ;font-weight: bold; text-align: center;"
        )

        self.verticalLayout.addWidget(self.dataMol_3)

        self.molFlow_5 = QLabel(self.verticalLayoutWidget)
        self.molFlow_5.setObjectName("molFlow_5")
        self.molFlow_5.setStyleSheet(
            "color: white; font-family: Montserrat, sans-serif; font-size: 15px ;font-weight: bold; text-align: center;"
        )
        self.molFlow_5.setTextFormat(Qt.AutoText)
        self.molFlow_5.setScaledContents(False)
        self.molFlow_5.setAlignment(Qt.AlignCenter)
        self.molFlow_5.setWordWrap(True)

        self.verticalLayout.addWidget(self.molFlow_5)

        self.dataMol_4 = QTextBrowser(self.verticalLayoutWidget)
        self.dataMol_4.setObjectName("dataMol_4")
        self.dataMol_4.setStyleSheet(
            "background-color: #303932; color: white; font-family: Montserrat, sans-serif; font-size: 15px ;font-weight: bold; text-align: center;"
        )

        self.verticalLayout.addWidget(self.dataMol_4)

        self.groupBox_3 = QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName("groupBox_3")
        self.groupBox_3.setGeometry(QRect(50, 340, 271, 191))
        self.groupBox_3.setStyleSheet("background-color: #303932; border-radius: 20%;")
        self.molFlow_6 = QLabel(self.groupBox_3)
        self.molFlow_6.setObjectName("molFlow_6")
        self.molFlow_6.setGeometry(QRect(10, 20, 251, 151))
        self.molFlow_6.setStyleSheet(
            "color: white; font-family: Montserrat, sans-serif; font-size: 20px ;font-weight: bold; text-align: center;"
        )
        self.molFlow_6.setTextFormat(Qt.AutoText)
        self.molFlow_6.setScaledContents(False)
        self.molFlow_6.setAlignment(Qt.AlignCenter)
        self.molFlow_6.setWordWrap(True)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QCoreApplication.translate("MainWindow", "MainWindow", None)
        )
        self.action.setText(
            QCoreApplication.translate(
                "MainWindow",
                "\u0420\u0430\u0441\u0447\u0435\u0442 \u043f\u0430\u0440\u0430\u043c\u0435\u0442\u0440\u043e\u0432 \u043a\u043e\u043b\u043e\u043d",
                None,
            )
        )
        self.action_2.setText(
            QCoreApplication.translate(
                "MainWindow",
                "\u0420\u0430\u0441\u0447\u0435\u0442 \u043f\u043e\u0442\u043e\u043a\u043e\u0432 \u043f\u043e\u0441\u043b\u0435 \u043a\u043e\u043b\u043e\u043d",
                None,
            )
        )
        self.groupBox.setTitle("")
        self.molFlow.setText(
            QCoreApplication.translate(
                "MainWindow",
                "\u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u043c\u043e\u043b\u044c\u043d\u044b\u0439 \u043f\u043e\u0442\u043e\u043a",
                None,
            )
        )
        self.calc.setText(
            QCoreApplication.translate(
                "MainWindow", "\u0420\u0430\u0441\u0447\u0435\u0442", None
            )
        )
        self.groupBox_2.setTitle("")
        self.molFlow_2.setText(
            QCoreApplication.translate(
                "MainWindow",
                "\u0414\u0430\u043d\u043d\u044b\u0435 \u0440\u0435\u043a\u0442\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u043e\u043d\u043d\u044b\u0445 \u043a\u043e\u043b\u043e\u043d",
                None,
            )
        )
        self.molFlow_4.setText(
            QCoreApplication.translate(
                "MainWindow",
                "\u0424\u043b\u0435\u0433\u043c\u043e\u0432\u043e\u0435 \u0447\u0438\u0441\u043b\u043e (COL11)",
                None,
            )
        )
        self.molFlow_3.setText(
            QCoreApplication.translate(
                "MainWindow",
                "\u041e\u0442\u043d\u043e\u0448\u0435\u043d\u0438\u0435 \u043a\u0443\u0431\u043e\u0432\u043e\u0433\u043e \u043f\u043e\u0442\u043e\u043a\u0430 \u043a \u0441\u044b\u0440\u044c\u0435\u0432\u043e\u043c\u0443 \u043f\u043e\u0442\u043e\u043a\u0443 (COL11)",
                None,
            )
        )
        self.molFlow_5.setText(
            QCoreApplication.translate(
                "MainWindow",
                "\u041e\u0442\u043d\u043e\u0448\u0435\u043d\u0438\u0435 \u043a\u0443\u0431\u043e\u0432\u043e\u0433\u043e \u043f\u043e\u0442\u043e\u043a\u0430 \u043a \u0441\u044b\u0440\u044c\u0435\u0432\u043e\u043c\u0443 \u043f\u043e\u0442\u043e\u043a\u0443 (COL12)",
                None,
            )
        )
        self.groupBox_3.setTitle("")
        self.molFlow_6.setText(
            QCoreApplication.translate(
                "MainWindow",
                "\u0420\u0430\u0441\u0447\u0435\u0442 \u043f\u0430\u0440\u0430\u043c\u0435\u0442\u0440\u043e\u0432 \u043a\u043e\u043b\u043e\u043d \u0432 \u0437\u0430\u0432\u0438\u0441\u0438\u043c\u043e\u0441\u0442\u0438 \u043e\u0442 \u043c\u043e\u043b\u044c\u043d\u043e\u0433\u043e \u0440\u0430\u0441\u0445\u043e\u0434\u0430 \u044d\u0442\u0438\u043b\u0431\u0435\u043d\u0437\u043e\u043b\u0430 \u0432 \u043f\u043e\u0442\u043e\u043a\u0435 FEED",
                None,
            )
        )

    # retranslateUi
