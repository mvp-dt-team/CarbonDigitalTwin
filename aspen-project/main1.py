from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QToolBar,
    QWidget,
    QVBoxLayout,
    QStackedWidget,
)
from PySide6.QtGui import QAction
import sys
import design
import design2
from functions import calculation_column_params, calculation_flow_composition
from CodeLibraryCustom import Simulation
import os
import random

from design import Ui_MainWindow
from design2 import Ui_SecondWindow


class FirstWindow(QMainWindow):
    def __init__(self, sim):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.calc.clicked.connect(self.func_calculation_column_params)
        self.sim = sim

    def func_calculation_column_params(self):
        amountEB = float(self.ui.dataMol.toPlainText())
        (
            Condenser_RefluxRatio_Col11,
            Reboiler_BottomsToFeedRatio_Col11,
            Reboiler_BottomsToFeedRatio_Col12,
        ) = calculation_column_params(amountEB, self.sim)
        self.ui.dataMol_2.setText(f"{Condenser_RefluxRatio_Col11: .4f}")
        self.ui.dataMol_3.setText(f"{Reboiler_BottomsToFeedRatio_Col11: .4f}")
        self.ui.dataMol_4.setText(f"{Reboiler_BottomsToFeedRatio_Col12: .4f}")


class SecondWindow(QMainWindow):
    def __init__(self, sim):
        super().__init__()
        self.ui = Ui_SecondWindow()
        self.ui.setupUi(self)
        self.ui.calc.clicked.connect(self.func_calculation_flow_composition)
        self.sim = sim
        self.results = {}
        self.ui.pushButton.clicked.connect(self.change_flow)
        self.ui.pushButton_3.clicked.connect(self.change_flow)
        self.ui.pushButton_4.clicked.connect(self.change_flow)
        self.ui.pushButton_5.clicked.connect(self.change_flow)
        self.cases = {
            "60-VAPOR": [
                "Общее",
                "ETHYLBEN",
                "TOLUENE",
                "BENZENE",
                "STYRENE",
                "ETHYLENE",
                "HYDROGEN",
                "METHANE",
                "WATER",
            ],
            "56-ORGAN": [
                "Общее",
                "ETHYLBEN",
                "TOLUENE",
                "BENZENE",
                "STYRENE",
                "ETHYLENE",
                "HYDROGEN",
                "METHANE",
                "WATER",
            ],
            "64-STYRE": [
                "Общее",
                "ETHYLBEN",
                "TOLUENE",
                "BENZENE",
                "STYRENE",
                "ETHYLENE",
                "HYDROGEN",
                "METHANE",
                "WATER",
            ],
            "62-ORGAN": [
                "Общее",
                "ETHYLBEN",
                "TOLUENE",
                "BENZENE",
                "STYRENE",
                "ETHYLENE",
                "HYDROGEN",
                "METHANE",
                "WATER",
            ],
        }

    def func_calculation_flow_composition(self):
        reflux_ratio = float(self.ui.dataMol.toPlainText())
        bottoms_to_feed_ratio = float(self.ui.dataMol_5.toPlainText())
        self.results = calculation_flow_composition(
            reflux_ratio, bottoms_to_feed_ratio, self.sim
        )
        # print(self.results)
        self.change_flow()

    def change_flow(self):
        sender = self.sender()
        if sender not in [
            self.ui.pushButton,
            self.ui.pushButton_3,
            self.ui.pushButton_4,
            self.ui.pushButton_5,
        ]:  # если sender is None, значит change_flow вызывается вручную, а не в ответ на событие
            sender = self.ui.pushButton_5  # по умолчанию выбираем первую кнопку
        self.ui.dataMol_16.setText(
            f"{self.results[sender.text().upper()]['Общее']:.4f}"
        )
        self.ui.dataMol_17.setText(
            f"{self.results[sender.text().upper()]['ETHYLBEN']:.4f}"
        )
        self.ui.dataMol_18.setText(
            f"{self.results[sender.text().upper()]['TOLUENE']:.4f}"
        )
        self.ui.dataMol_19.setText(
            f"{self.results[sender.text().upper()]['BENZENE']:.4f}"
        )
        self.ui.dataMol_20.setText(
            f"{self.results[sender.text().upper()]['STYRENE']:.4f}"
        )
        self.ui.dataMol_21.setText(
            f"{self.results[sender.text().upper()]['ETHYLENE']:.4f}"
        )
        self.ui.dataMol_22.setText(
            f"{self.results[sender.text().upper()]['HYDROGEN']:.4f}"
        )
        self.ui.dataMol_23.setText(
            f"{self.results[sender.text().upper()]['METHANE']:.4f}"
        )
        self.ui.dataMol_24.setText(
            f"{self.results[sender.text().upper()]['WATER']:.4f}"
        )

        for i in [
            self.ui.pushButton,
            self.ui.pushButton_3,
            self.ui.pushButton_4,
            self.ui.pushButton_5,
        ]:
            i.setStyleSheet(
                "color: white; font-family: Montserrat, sans-serif; font-size: 12px ;font-weight: bold; text-align: center; background-color: #4B594E; border-radius: 20%;"
            )
        sender.setStyleSheet(
            "color: black; font-family: Montserrat, sans-serif; font-size: 12px ;font-weight: bold; text-align: center; background-color: #ffffff; border-radius: 20%;"
        )


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ASPEN UI FACTORY")
        self.setGeometry(0, 0, 790, 600)
        self.setFixedSize(790, 650)

        self.toolbar = QToolBar("Toolbar")
        self.toolbar.setFixedHeight(30)
        self.addToolBar(self.toolbar)
        self.toolbar.setStyleSheet(
            "QToolBar { background-color: #577550; } QToolBar QToolButton { min-width: 20px;background-color: black; color: white; font-family: Montserrat, sans-serif; font-size: 15px ;font-weight: bold; text-align: center; margin-right: 10px; border-radius: 5%}"
        )

        switch_first_action = QAction("Расчет параметров ректификационных колонн", self)
        switch_first_action.triggered.connect(self.show_first_window)
        self.toolbar.addAction(switch_first_action)

        switch_second_action = QAction("Расчет выходных потоков", self)
        switch_second_action.triggered.connect(self.show_second_window)
        # self.toolbar.addAction(switch_second_action)

        # Создаем окна, но не отображаем их сраз

        self.working_path = os.getcwd()
        self.sim = Simulation(
            AspenFileName="Styrene.bkp",
            WorkingDirectoryPath=self.working_path + "\\schemes",
            VISIBILITY=False,
        )
        self.setCentralWidget(FirstWindow(self.sim))

    def show_first_window(self):
        self.setCentralWidget(FirstWindow(self.sim))

    def show_second_window(self):
        self.setCentralWidget(SecondWindow(self.sim))

    def closeEvent(self, event):
        self.sim.CloseAspen()
        # self.sim2.CloseAspen()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
