# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'design2.ui'
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
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QStatusBar,
    QTextBrowser,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class Ui_SecondWindow(object):
    def setupUi(self, SecondWindow):
        if not SecondWindow.objectName():
            SecondWindow.setObjectName("SecondWindow")
        SecondWindow.resize(790, 600)
        SecondWindow.setStyleSheet("background-color: #82CF83;")
        self.action = QAction(SecondWindow)
        self.action.setObjectName("action")
        self.action_2 = QAction(SecondWindow)
        self.action_2.setObjectName("action_2")
        self.centralwidget = QWidget(SecondWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.groupBox_2.setGeometry(QRect(360, 20, 411, 531))
        self.groupBox_2.setStyleSheet("background-color: black; border-radius: 20%;")
        self.molFlow_2 = QLabel(self.groupBox_2)
        self.molFlow_2.setObjectName("molFlow_2")
        self.molFlow_2.setGeometry(QRect(20, 20, 361, 31))
        self.molFlow_2.setStyleSheet(
            "color: white; font-family: Montserrat, sans-serif; font-size: 20px ;font-weight: bold; text-align: center;"
        )
        self.molFlow_2.setTextFormat(Qt.AutoText)
        self.molFlow_2.setScaledContents(False)
        self.molFlow_2.setAlignment(Qt.AlignCenter)
        self.molFlow_2.setWordWrap(True)
        self.pushButton_5 = QPushButton(self.groupBox_2)
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.setGeometry(QRect(20, 80, 91, 41))
        self.pushButton_5.setStyleSheet(
            "color: white; font-family: Montserrat, sans-serif; font-size: 12px ;font-weight: bold; text-align: center; background-color: #4B594E; border-radius: 20%;"
        )
        self.pushButton_4 = QPushButton(self.groupBox_2)
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.setGeometry(QRect(123, 80, 91, 41))
        self.pushButton_4.setStyleSheet(
            "color: white; font-family: Montserrat, sans-serif; font-size: 12px ;font-weight: bold; text-align: center; background-color: #4B594E; border-radius: 20%;"
        )
        self.pushButton_3 = QPushButton(self.groupBox_2)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setGeometry(QRect(223, 80, 81, 41))
        self.pushButton_3.setStyleSheet(
            "color: white; font-family: Montserrat, sans-serif; font-size: 12px ;font-weight: bold; text-align: center; background-color: #4B594E;"
        )
        self.pushButton = QPushButton(self.groupBox_2)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setGeometry(QRect(313, 80, 81, 41))
        self.pushButton.setStyleSheet(
            "color: white; font-family: Montserrat, sans-serif; font-size: 12px ;font-weight: bold; text-align: center; background-color: #4B594E; border-radius: 20%;"
        )
        self.dataMol_16 = QTextBrowser(self.groupBox_2)
        self.dataMol_16.setObjectName("dataMol_16")
        self.dataMol_16.setGeometry(QRect(250, 160, 121, 31))
        self.dataMol_16.setStyleSheet(
            "background-color: #303932; color: white; font-family: Montserrat, sans-serif; font-size: 15px ;font-weight: bold; text-align: center;"
        )
        self.molFlow_9 = QLabel(self.groupBox_2)
        self.molFlow_9.setObjectName("molFlow_9")
        self.molFlow_9.setGeometry(QRect(20, 160, 221, 31))
        self.molFlow_9.setStyleSheet(
            "color: white; font-family: Montserrat, sans-serif; font-size: 15px ;font-weight: bold; text-align: left;"
        )
        self.molFlow_9.setTextFormat(Qt.AutoText)
        self.molFlow_9.setScaledContents(False)
        self.molFlow_9.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)
        self.molFlow_9.setWordWrap(True)
        self.dataMol_17 = QTextBrowser(self.groupBox_2)
        self.dataMol_17.setObjectName("dataMol_17")
        self.dataMol_17.setGeometry(QRect(250, 200, 121, 31))
        self.dataMol_17.setStyleSheet(
            "background-color: #303932; color: white; font-family: Montserrat, sans-serif; font-size: 15px ;font-weight: bold; text-align: center;"
        )
        self.dataMol_18 = QTextBrowser(self.groupBox_2)
        self.dataMol_18.setObjectName("dataMol_18")
        self.dataMol_18.setGeometry(QRect(250, 240, 121, 31))
        self.dataMol_18.setStyleSheet(
            "background-color: #303932; color: white; font-family: Montserrat, sans-serif; font-size: 15px ;font-weight: bold; text-align: center;"
        )
        self.dataMol_19 = QTextBrowser(self.groupBox_2)
        self.dataMol_19.setObjectName("dataMol_19")
        self.dataMol_19.setGeometry(QRect(250, 280, 121, 31))
        self.dataMol_19.setStyleSheet(
            "background-color: #303932; color: white; font-family: Montserrat, sans-serif; font-size: 15px ;font-weight: bold; text-align: center;"
        )
        self.dataMol_20 = QTextBrowser(self.groupBox_2)
        self.dataMol_20.setObjectName("dataMol_20")
        self.dataMol_20.setGeometry(QRect(250, 320, 121, 31))
        self.dataMol_20.setStyleSheet(
            "background-color: #303932; color: white; font-family: Montserrat, sans-serif; font-size: 15px ;font-weight: bold; text-align: center;"
        )
        self.dataMol_21 = QTextBrowser(self.groupBox_2)
        self.dataMol_21.setObjectName("dataMol_21")
        self.dataMol_21.setGeometry(QRect(250, 360, 121, 31))
        self.dataMol_21.setStyleSheet(
            "background-color: #303932; color: white; font-family: Montserrat, sans-serif; font-size: 15px ;font-weight: bold; text-align: center;"
        )
        self.dataMol_22 = QTextBrowser(self.groupBox_2)
        self.dataMol_22.setObjectName("dataMol_22")
        self.dataMol_22.setGeometry(QRect(250, 400, 121, 31))
        self.dataMol_22.setStyleSheet(
            "background-color: #303932; color: white; font-family: Montserrat, sans-serif; font-size: 15px ;font-weight: bold; text-align: center;"
        )
        self.dataMol_23 = QTextBrowser(self.groupBox_2)
        self.dataMol_23.setObjectName("dataMol_23")
        self.dataMol_23.setGeometry(QRect(250, 440, 121, 31))
        self.dataMol_23.setStyleSheet(
            "background-color: #303932; color: white; font-family: Montserrat, sans-serif; font-size: 15px ;font-weight: bold; text-align: center;"
        )
        self.dataMol_24 = QTextBrowser(self.groupBox_2)
        self.dataMol_24.setObjectName("dataMol_24")
        self.dataMol_24.setGeometry(QRect(250, 480, 121, 31))
        self.dataMol_24.setStyleSheet(
            "background-color: #303932; color: white; font-family: Montserrat, sans-serif; font-size: 15px ;font-weight: bold; text-align: center;"
        )
        self.molFlow_10 = QLabel(self.groupBox_2)
        self.molFlow_10.setObjectName("molFlow_10")
        self.molFlow_10.setGeometry(QRect(20, 200, 221, 31))
        self.molFlow_10.setStyleSheet(
            "color: white; font-family: Montserrat, sans-serif; font-size: 15px ;font-weight: bold; text-align: center;"
        )
        self.molFlow_10.setTextFormat(Qt.AutoText)
        self.molFlow_10.setScaledContents(False)
        self.molFlow_10.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)
        self.molFlow_10.setWordWrap(True)
        self.molFlow_11 = QLabel(self.groupBox_2)
        self.molFlow_11.setObjectName("molFlow_11")
        self.molFlow_11.setGeometry(QRect(20, 240, 221, 31))
        self.molFlow_11.setStyleSheet(
            "color: white; font-family: Montserrat, sans-serif; font-size: 15px ;font-weight: bold; text-align: center;"
        )
        self.molFlow_11.setTextFormat(Qt.AutoText)
        self.molFlow_11.setScaledContents(False)
        self.molFlow_11.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)
        self.molFlow_11.setWordWrap(True)
        self.molFlow_12 = QLabel(self.groupBox_2)
        self.molFlow_12.setObjectName("molFlow_12")
        self.molFlow_12.setGeometry(QRect(20, 280, 221, 31))
        self.molFlow_12.setStyleSheet(
            "color: white; font-family: Montserrat, sans-serif; font-size: 15px ;font-weight: bold; text-align: center;"
        )
        self.molFlow_12.setTextFormat(Qt.AutoText)
        self.molFlow_12.setScaledContents(False)
        self.molFlow_12.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)
        self.molFlow_12.setWordWrap(True)
        self.molFlow_13 = QLabel(self.groupBox_2)
        self.molFlow_13.setObjectName("molFlow_13")
        self.molFlow_13.setGeometry(QRect(20, 320, 221, 31))
        self.molFlow_13.setStyleSheet(
            "color: white; font-family: Montserrat, sans-serif; font-size: 15px ;font-weight: bold; text-align: center;"
        )
        self.molFlow_13.setTextFormat(Qt.AutoText)
        self.molFlow_13.setScaledContents(False)
        self.molFlow_13.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)
        self.molFlow_13.setWordWrap(True)
        self.molFlow_14 = QLabel(self.groupBox_2)
        self.molFlow_14.setObjectName("molFlow_14")
        self.molFlow_14.setGeometry(QRect(20, 360, 221, 31))
        self.molFlow_14.setStyleSheet(
            "color: white; font-family: Montserrat, sans-serif; font-size: 15px ;font-weight: bold; text-align: center;"
        )
        self.molFlow_14.setTextFormat(Qt.AutoText)
        self.molFlow_14.setScaledContents(False)
        self.molFlow_14.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)
        self.molFlow_14.setWordWrap(True)
        self.molFlow_15 = QLabel(self.groupBox_2)
        self.molFlow_15.setObjectName("molFlow_15")
        self.molFlow_15.setGeometry(QRect(20, 400, 221, 31))
        self.molFlow_15.setStyleSheet(
            "color: white; font-family: Montserrat, sans-serif; font-size: 15px ;font-weight: bold; text-align: center;"
        )
        self.molFlow_15.setTextFormat(Qt.AutoText)
        self.molFlow_15.setScaledContents(False)
        self.molFlow_15.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)
        self.molFlow_15.setWordWrap(True)
        self.molFlow_16 = QLabel(self.groupBox_2)
        self.molFlow_16.setObjectName("molFlow_16")
        self.molFlow_16.setGeometry(QRect(20, 440, 221, 31))
        self.molFlow_16.setStyleSheet(
            "color: white; font-family: Montserrat, sans-serif; font-size: 15px ;font-weight: bold; text-align: center;"
        )
        self.molFlow_16.setTextFormat(Qt.AutoText)
        self.molFlow_16.setScaledContents(False)
        self.molFlow_16.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)
        self.molFlow_16.setWordWrap(True)
        self.molFlow_17 = QLabel(self.groupBox_2)
        self.molFlow_17.setObjectName("molFlow_17")
        self.molFlow_17.setGeometry(QRect(20, 480, 221, 31))
        self.molFlow_17.setStyleSheet(
            "color: white; font-family: Montserrat, sans-serif; font-size: 15px ;font-weight: bold; text-align: center;"
        )
        self.molFlow_17.setTextFormat(Qt.AutoText)
        self.molFlow_17.setScaledContents(False)
        self.molFlow_17.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)
        self.molFlow_17.setWordWrap(True)
        self.groupBox_3 = QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName("groupBox_3")
        self.groupBox_3.setGeometry(QRect(20, 380, 281, 171))
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
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.groupBox.setGeometry(QRect(20, 20, 281, 341))
        self.groupBox.setStyleSheet("background-color: black; border-radius: 20%;")
        self.calc = QPushButton(self.groupBox)
        self.calc.setObjectName("calc")
        self.calc.setGeometry(QRect(70, 290, 141, 41))
        self.calc.setStyleSheet(
            "color: black; font-family: Montserrat, sans-serif; font-size: 17px ;font-weight: bold; text-align: center;\n"
            "border-radius: 5%; background-color: #FFF200;"
        )
        self.verticalLayoutWidget_2 = QWidget(self.groupBox)
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(30, 70, 221, 216))
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setSpacing(10)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 5, 5, 5)
        self.molFlow_7 = QLabel(self.verticalLayoutWidget_2)
        self.molFlow_7.setObjectName("molFlow_7")
        self.molFlow_7.setStyleSheet(
            "color: white; font-family: Montserrat, sans-serif; font-size: 15px ;font-weight: bold; text-align: center;"
        )
        self.molFlow_7.setTextFormat(Qt.AutoText)
        self.molFlow_7.setScaledContents(False)
        self.molFlow_7.setAlignment(Qt.AlignCenter)
        self.molFlow_7.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.molFlow_7)

        self.dataMol = QTextEdit(self.verticalLayoutWidget_2)
        self.dataMol.setObjectName("dataMol")
        self.dataMol.setStyleSheet(
            "color: white; border-radius: 10%; background-color: #303932;  font-family: Montserrat, sans-serif; font-size: 20px ;font-weight: bold;"
        )

        self.verticalLayout_2.addWidget(self.dataMol)

        self.molFlow = QLabel(self.verticalLayoutWidget_2)
        self.molFlow.setObjectName("molFlow")
        self.molFlow.setStyleSheet(
            "color: white; font-family: Montserrat, sans-serif; font-size: 15px ;font-weight: bold; text-align: center;"
        )
        self.molFlow.setTextFormat(Qt.AutoText)
        self.molFlow.setScaledContents(False)
        self.molFlow.setAlignment(Qt.AlignCenter)
        self.molFlow.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.molFlow)

        self.dataMol_5 = QTextEdit(self.verticalLayoutWidget_2)
        self.dataMol_5.setObjectName("dataMol_5")
        self.dataMol_5.setStyleSheet(
            "color: white; border-radius: 10%; background-color: #303932;  font-family: Montserrat, sans-serif; font-size: 20px ;font-weight: bold;"
        )

        self.verticalLayout_2.addWidget(self.dataMol_5)

        self.molFlow_8 = QLabel(self.groupBox)
        self.molFlow_8.setObjectName("molFlow_8")
        self.molFlow_8.setGeometry(QRect(30, 20, 221, 41))
        self.molFlow_8.setStyleSheet(
            "color: white; font-family: Montserrat, sans-serif; font-size: 17px ;font-weight: bold; text-align: center;"
        )
        self.molFlow_8.setTextFormat(Qt.AutoText)
        self.molFlow_8.setScaledContents(False)
        self.molFlow_8.setAlignment(Qt.AlignCenter)
        self.molFlow_8.setWordWrap(True)
        SecondWindow.setCentralWidget(self.centralwidget)
        self.statusBar = QStatusBar(SecondWindow)
        self.statusBar.setObjectName("statusBar")
        SecondWindow.setStatusBar(self.statusBar)

        self.retranslateUi(SecondWindow)

        QMetaObject.connectSlotsByName(SecondWindow)

    # setupUi

    def retranslateUi(self, SecondWindow):
        SecondWindow.setWindowTitle(
            QCoreApplication.translate("SecondWindow", "MainWindow", None)
        )
        self.action.setText(
            QCoreApplication.translate(
                "SecondWindow",
                "\u0420\u0430\u0441\u0447\u0435\u0442 \u043f\u0430\u0440\u0430\u043c\u0435\u0442\u0440\u043e\u0432 \u043a\u043e\u043b\u043e\u043d",
                None,
            )
        )
        self.action_2.setText(
            QCoreApplication.translate(
                "SecondWindow",
                "\u0420\u0430\u0441\u0447\u0435\u0442 \u043f\u043e\u0442\u043e\u043a\u043e\u0432 \u043f\u043e\u0441\u043b\u0435 \u043a\u043e\u043b\u043e\u043d",
                None,
            )
        )
        self.groupBox_2.setTitle("")
        self.molFlow_2.setText(
            QCoreApplication.translate(
                "SecondWindow",
                "\u0414\u0430\u043d\u043d\u044b\u0435 \u043f\u043e\u0442\u043e\u043a\u043e\u0432",
                None,
            )
        )
        self.pushButton_5.setText(
            QCoreApplication.translate("SecondWindow", "56-Organ", None)
        )
        self.pushButton_4.setText(
            QCoreApplication.translate("SecondWindow", "60-Vapor", None)
        )
        self.pushButton_3.setText(
            QCoreApplication.translate("SecondWindow", "64-Styre", None)
        )
        self.pushButton.setText(
            QCoreApplication.translate("SecondWindow", "62-Organ", None)
        )
        self.molFlow_9.setText(
            QCoreApplication.translate(
                "SecondWindow",
                "\u041c\u0430\u0441\u0441\u043e\u0432\u044b\u0439 \u043f\u043e\u0442\u043e\u043a (\u0432 \u043a\u0433/\u0447)",
                None,
            )
        )
        self.molFlow_10.setText(
            QCoreApplication.translate(
                "SecondWindow",
                "\u041c\u0430\u0441\u0441\u043e\u0432\u0430\u044f \u0434\u043e\u043b\u044f \u044d\u0442\u0438\u043b\u0431\u0435\u043d\u0437\u043e\u043b\u0430",
                None,
            )
        )
        self.molFlow_11.setText(
            QCoreApplication.translate(
                "SecondWindow",
                "\u041c\u0430\u0441\u0441\u043e\u0432\u0430\u044f \u0434\u043e\u043b\u044f \u0442\u043e\u043b\u0443\u043e\u043b\u0430",
                None,
            )
        )
        self.molFlow_12.setText(
            QCoreApplication.translate(
                "SecondWindow",
                "\u041c\u0430\u0441\u0441\u043e\u0432\u0430\u044f \u0434\u043e\u043b\u044f \u0431\u0435\u043d\u0437\u043e\u043b\u0430",
                None,
            )
        )
        self.molFlow_13.setText(
            QCoreApplication.translate(
                "SecondWindow",
                "\u041c\u0430\u0441\u0441\u043e\u0432\u0430\u044f \u0434\u043e\u043b\u044f \u0441\u0442\u0438\u0440\u043e\u043b\u0430",
                None,
            )
        )
        self.molFlow_14.setText(
            QCoreApplication.translate(
                "SecondWindow",
                "\u041c\u0430\u0441\u0441\u043e\u0432\u0430\u044f \u0434\u043e\u043b\u044f \u044d\u0442\u0438\u043b\u0435\u043d\u0430",
                None,
            )
        )
        self.molFlow_15.setText(
            QCoreApplication.translate(
                "SecondWindow",
                "\u041c\u0430\u0441\u0441\u043e\u0432\u0430\u044f \u0434\u043e\u043b\u044f \u0432\u043e\u0434\u043e\u0440\u043e\u0434\u0430",
                None,
            )
        )
        self.molFlow_16.setText(
            QCoreApplication.translate(
                "SecondWindow",
                "\u041c\u0430\u0441\u0441\u043e\u0432\u0430\u044f \u0434\u043e\u043b\u044f \u043c\u0435\u0442\u0430\u043d\u0430",
                None,
            )
        )
        self.molFlow_17.setText(
            QCoreApplication.translate(
                "SecondWindow",
                "\u041c\u0430\u0441\u0441\u043e\u0432\u0430\u044f \u0434\u043e\u043b\u044f \u0432\u043e\u0434\u044b",
                None,
            )
        )
        self.groupBox_3.setTitle("")
        self.molFlow_6.setText(
            QCoreApplication.translate(
                "SecondWindow",
                "\u0420\u0430\u0441\u0447\u0435\u0442 \u0432\u044b\u0445\u043e\u0434\u043d\u044b\u0445 \u043f\u043e\u0442\u043e\u043a\u043e\u0432 \u0432 \u0437\u0430\u0432\u0438\u0441\u0438\u043c\u043e\u0441\u0442\u0438 \u043e\u0442 \u043f\u0430\u0440\u0430\u043c\u0435\u0442\u0440\u043e\u0432 \u043a\u043e\u043b\u043e\u043d\u043d\u044b COL11",
                None,
            )
        )
        self.groupBox.setTitle("")
        self.calc.setText(
            QCoreApplication.translate(
                "SecondWindow", "\u0420\u0430\u0441\u0447\u0435\u0442", None
            )
        )
        self.molFlow_7.setText(
            QCoreApplication.translate(
                "SecondWindow",
                "Reflux ratio \u0432 \u043c\u043e\u043b\u044c\u043d\u043e\u043c \u0441\u043e\u043e\u0442\u043d\u043e\u0448\u0435\u043d\u0438\u0438",
                None,
            )
        )
        self.molFlow.setText(
            QCoreApplication.translate(
                "SecondWindow",
                "Bottoms to feed ratio \u0432 \u043c\u043e\u043b\u044c\u043d\u043e\u043c \u0441\u043e\u043e\u0442\u043d\u043e\u0448\u0435\u043d\u0438\u0438",
                None,
            )
        )
        self.molFlow_8.setText(
            QCoreApplication.translate(
                "SecondWindow",
                "\u041f\u0430\u0440\u0430\u043c\u0435\u0442\u0440\u044b \u043a\u043e\u043b\u043e\u043d\u043d\u044b COL11",
                None,
            )
        )

    # retranslateUi
