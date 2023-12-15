#######################################################
# Graphy v2.0                                         #
# (C) 2023 Abdon Morales                              #
# https://git.moralesresearch.org/abdonmorales/graphy #
# December 8, 2023                                    #
#######################################################

import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
import json

from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QGridLayout, QMessageBox, QTreeView, QComboBox)
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QDoubleValidator, QAction
from PyQt6.QtWidgets import QFileDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT


class GraphingCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Graphy Release II")
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        # Create Menu Bar
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')

        # Add 'Load Graph' and 'Save Graph' actions
        loadAction = QAction('&Load Graph', self)
        loadAction.triggered.connect(self.loadGraph)
        fileMenu.addAction(loadAction)

        saveAction = QAction('&Save Graph', self)
        saveAction.triggered.connect(self.saveGraph)
        fileMenu.addAction(saveAction)

        # Create widgets
        func_label = QLabel("Enter function:")
        self.func_input = QLineEdit()
        self.func_input.setToolTip("Enter your function using x as the variable. Example: x**2 + 5*x + 6")

        # Graph title input
        self.graph_title_input = QLineEdit()
        title_label = QLabel("Graph Title:")

        # Buttons for operations
        add_btn = QPushButton("+", clicked=lambda: self.appendSymbol('+'))
        subtract_btn = QPushButton("-", clicked=lambda: self.appendSymbol('-'))
        multiply_btn = QPushButton("*", clicked=lambda: self.appendSymbol('*'))
        divide_btn = QPushButton("/", clicked=lambda: self.appendSymbol('/'))
        power_btn = QPushButton("^", clicked=lambda: self.appendSymbol('**'))
        left_parenthesis_btn = QPushButton("(", clicked=lambda: self.appendSymbol('('))
        right_parenthesis_btn = QPushButton(")", clicked=lambda: self.appendSymbol(')'))

        plot_btn = QPushButton("Plot", clicked=self.plotFunc)
        table_btn = QPushButton("Table", clicked=self.showTable)

        # Sidebar controls
        self.step_size_input = QLineEdit("1")
        self.step_size_input.setValidator(QDoubleValidator(0.1, 10.0, 2))
        step_size_label = QLabel("Step size:")

        self.grid_style_combo = QComboBox()
        self.grid_style_combo.addItems(["regular", "dotted", "dashed"])
        grid_style_label = QLabel("Grid style:")

        apply_settings_btn = QPushButton("Apply Settings", clicked=self.applySettings)

        # Canvas
        fig = plt.figure()
        canvas = FigureCanvasQTAgg(fig)
        toolbar = NavigationToolbar2QT(canvas, centralWidget)

        # Layout
        layout = QGridLayout(centralWidget)
        layout.addWidget(func_label, 0, 0)
        layout.addWidget(self.func_input, 0, 1, 1, 3)
        layout.addWidget(title_label, 1, 0)
        layout.addWidget(self.graph_title_input, 1, 1, 1, 3)
        layout.addWidget(add_btn, 2, 0)
        layout.addWidget(subtract_btn, 2, 1)
        layout.addWidget(multiply_btn, 2, 2)
        layout.addWidget(divide_btn, 2, 3)
        layout.addWidget(power_btn, 2, 4)
        layout.addWidget(left_parenthesis_btn, 2, 5)
        layout.addWidget(right_parenthesis_btn, 2, 6)
        layout.addWidget(plot_btn, 3, 0, 1, 7)
        layout.addWidget(toolbar, 4, 0, 1, 7)
        layout.addWidget(canvas, 5, 0, 5, 7)
        layout.addWidget(table_btn, 10, 0, 1, 7)
        layout.addWidget(step_size_label, 11, 0)
        layout.addWidget(self.step_size_input, 11, 1)
        layout.addWidget(grid_style_label, 11, 2)
        layout.addWidget(self.grid_style_combo, 11, 3)
        layout.addWidget(apply_settings_btn, 11, 4, 1, 3)

    def appendSymbol(self, symbol):
        text = self.func_input.text()
        self.func_input.setText(text + symbol)

    def plotFunc(self):
        try:
            x = sp.symbols('x')
            y = sp.lambdify(x, sp.sympify(self.func_input.text()), 'numpy')(np.linspace(-10, 10, 100))
            self.plot(np.linspace(-10, 10, 100), y)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Invalid Function: {e}")

    def plot(self, x, y):
        fig = self.centralWidget().findChild(FigureCanvasQTAgg).figure
        fig.clear()
        ax = fig.add_subplot(111)
        ax.plot(x, y)

        # Set title of the graph from the user input
        ax.set_title(self.graph_title_input.text())

        # Set the step size for the x and y axis ticks
        step_size = float(self.step_size_input.text())
        ax.set_xticks(np.arange(min(x), max(x) + step_size, step_size))
        ax.set_yticks(np.arange(min(y), max(y) + step_size, step_size))

        # Customize the gridlines based on the user's choice
        grid_style = self.grid_style_combo.currentText()
        if grid_style == "dotted":
            linestyle = ":"
        elif grid_style == "dashed":
            linestyle = "--"
        else:
            linestyle = "-"

        # Enable gridlines with the selected style
        ax.grid(True, linestyle=linestyle)

        # Emphasize the x=0 and y=0 axes with bold lines
        ax.axhline(0, color='black', linewidth=1.5)
        ax.axvline(0, color='black', linewidth=1.5)

        self.centralWidget().findChild(FigureCanvasQTAgg).draw()

    def showTable(self):
        try:
            x = np.linspace(-10, 10, 100)
            x_sym = sp.symbols('x')
            y = sp.lambdify(x_sym, sp.sympify(self.func_input.text()), 'numpy')(x)
            self.table = TableWindow(x, y)
            self.table.show()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Unable to generate table: {e}")

    def applySettings(self):
        self.plotFunc()

    def saveGraph(self):
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getSaveFileName(self, "Save Graph", "", "Graph Files (*.gph)", options=options)
        if filename:
            with open(filename, 'w') as file:
                data = {
                    "function": self.func_input.text(),
                    "title": self.graph_title_input.text(),
                    "step_size": self.step_size_input.text(),
                    "grid_style": self.grid_style_combo.currentText()
                }
                file.write(json.dumps(data))

    def loadGraph(self):
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(self, "Load Graph", "", "Graph Files (*.gph)", options=options)
        if filename:
            with open(filename, 'r') as file:
                data = json.loads(file.read())
                self.func_input.setText(data.get("function", ""))
                self.graph_title_input.setText(data.get("title", ""))
                self.step_size_input.setText(data.get("step_size", "1"))
                self.grid_style_combo.setCurrentText(data.get("grid_style", "regular"))
                self.plotFunc()


class TableWindow(QMainWindow):
    def __init__(self, x_values, y_values):
        super().__init__()

        self.setWindowTitle("Function Table")
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(['X', 'Y'])

        for x, y in zip(x_values, y_values):
            model.appendRow([QStandardItem(str(x)), QStandardItem(str(y))])

        self.table = QTreeView()
        self.table.setModel(model)
        self.setCentralWidget(self.table)


app = QApplication([])
window = GraphingCalculator()
window.show()
app.exec()

