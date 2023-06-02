# third party modules
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
import pandas as pd

# graph modules
import matplotlib.pyplot as plt
import seaborn as sns

# in-house
import load
import driver
import time
import solve

# setup
pd.set_option('display.max_columns', None)

# driver to be used throughout entire application
driver = driver.driver()

# loader used for loading and resetting data
loader = load.Load(driver.driver)

# runs the queries for questions
task = solve.Solution(driver.driver)

# populate list of valid countries
countries = loader.get_countries().to_numpy().flatten()

# populate list of valid cities
cities = loader.get_cities().to_numpy().flatten()


class TableModel(QtCore.QAbstractTableModel):

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        if self._data.empty is True:
            return ""

        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                return str(self._data.index[section])


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        # set window basic size
        self.setGeometry(100, 60, 1000, 800)
        # set window main title
        self.setWindowTitle("Datakeeper")

        # create table to display query results
        self.table = QtWidgets.QTableView()
        model = TableModel(pd.DataFrame())
        self.table.setModel(model)

        # create widgets for controlling program flow

        # create buttons
        button1 = QtWidgets.QPushButton('Question 1')
        button2 = QtWidgets.QPushButton('Question 2')
        button3 = QtWidgets.QPushButton('Question 3')
        button4 = QtWidgets.QPushButton('Question 4')
        button5 = QtWidgets.QPushButton('Question 5')
        button6 = QtWidgets.QPushButton('Question 6')
        button7 = QtWidgets.QPushButton('Question 7')
        button8 = QtWidgets.QPushButton('Question 8')
        button9 = QtWidgets.QPushButton('Question 9')
        button10 = QtWidgets.QPushButton('Question 10')

        # create and set layout of buttons
        buttonGroup = QtWidgets.QWidget()
        buttonGroupLeft = QtWidgets.QWidget()
        buttonGroupRight = QtWidgets.QWidget()

        buttonGroupLayout = QtWidgets.QHBoxLayout()
        buttonGroupLeftLayout = QtWidgets.QVBoxLayout()
        buttonGroupRightLayout = QtWidgets.QVBoxLayout()

        buttonGroupLeftLayout.setAlignment(Qt.AlignTop)
        buttonGroupRightLayout.setAlignment(Qt.AlignTop)

        buttonGroup.setLayout(buttonGroupLayout)
        buttonGroupLeft.setLayout(buttonGroupLeftLayout)
        buttonGroupRight.setLayout(buttonGroupRightLayout)

        # add buttons to layout
        buttonGroupLayout.addWidget(buttonGroupLeft)
        buttonGroupLayout.addWidget(buttonGroupRight)

        buttonGroupLeftLayout.addWidget(button1)
        buttonGroupLeftLayout.addWidget(button2)
        buttonGroupLeftLayout.addWidget(button3)
        buttonGroupLeftLayout.addWidget(button4)
        buttonGroupLeftLayout.addWidget(button5)

        buttonGroupRightLayout.addWidget(button6)
        buttonGroupRightLayout.addWidget(button7)
        buttonGroupRightLayout.addWidget(button8)
        buttonGroupRightLayout.addWidget(button9)
        buttonGroupRightLayout.addWidget(button10)

        # add input elements below buttons
        inputGroup = QtWidgets.QWidget()
        self.inputGroupLayout = QtWidgets.QVBoxLayout()  # make available in class
        self.inputGroupLayout.setAlignment(Qt.AlignBottom)
        self.inputGroupLayoutList = []  # when adding a widget to layout, also add to the list so can remove them later
        inputGroup.setLayout(self.inputGroupLayout)

        # create layout container for both buttons and input items (left panel)
        leftPanel = QtWidgets.QWidget()
        leftPanelLayout = QtWidgets.QVBoxLayout()
        leftPanel.setLayout(leftPanelLayout)
        leftPanelLayout.addWidget(buttonGroup)
        leftPanelLayout.addWidget(inputGroup)

        # set slots (event handler) for signals (events)
        button1.clicked.connect(self.button1_clicked_slot)
        button2.clicked.connect(self.button2_clicked_slot)
        button3.clicked.connect(self.button3_clicked_slot)
        button4.clicked.connect(self.button4_clicked_slot)
        button5.clicked.connect(self.button5_clicked_slot)
        button6.clicked.connect(self.button6_clicked_slot)
        button7.clicked.connect(self.button7_clicked_slot)
        button8.clicked.connect(self.button8_clicked_slot)
        button9.clicked.connect(self.button9_clicked_slot)
        button10.clicked.connect(self.button10_clicked_slot)

        # create the top layout for MainWindow
        self.layout = QtWidgets.QHBoxLayout()

        # add widgets to the layout
        self.layout.addWidget(self.table)
        self.layout.addWidget(leftPanel)

        container = QtWidgets.QWidget()
        container.setLayout(self.layout)

        self.setCentralWidget(container)

    def reset_table(self):
        # reset data
        model = TableModel(pd.DataFrame())
        self.table.setModel(model)

    def clear_input_widgets(self):
        # remove prior widgets (if any) from the input layout
        for widget in self.inputGroupLayoutList:
            widget.deleteLater()
        self.inputGroupLayoutList.clear()

    def button1_clicked_slot(self):
        # remove prior widgets (if any) from the input layout
        self.clear_input_widgets()

        # reset data
        self.reset_table()

        # populate screen with appropriate options
        combobox = QtWidgets.QComboBox()
        combobox.addItems(countries)
        combobox.currentTextChanged.connect(self.question1_combobox_textchanged_slot)
        label = QtWidgets.QLabel("Time: 0 seconds")
        self.inputGroupLayout.addWidget(label)
        self.inputGroupLayoutList.append(label)

        self.inputGroupLayout.addWidget(combobox)
        self.inputGroupLayoutList.append(combobox)

    def question1_combobox_textchanged_slot(self, text):
        start_time = time.time()
        data = task.problem1(text)
        end_time = time.time()
        total_time = end_time - start_time
        self.inputGroupLayout.itemAt(0).widget().setText("Time: " + str(total_time) + " seconds")

        model = TableModel(data)
        self.table.setModel(model)

    def button2_clicked_slot(self):
        # remove prior widgets (if any) from the input layout
        self.clear_input_widgets()

        # reset data
        self.reset_table()

        spinbox = QtWidgets.QSpinBox()
        spinbox.valueChanged.connect(lambda: self.question2_spinbox_changed_slot(spinbox.value()))

        label = QtWidgets.QLabel("Time: 0 seconds")
        self.inputGroupLayout.addWidget(label)
        self.inputGroupLayoutList.append(label)

        self.inputGroupLayout.addWidget(spinbox)
        self.inputGroupLayoutList.append(spinbox)

    def question2_spinbox_changed_slot(self, value):
        start_time = time.time()
        data = task.problem2(value)
        end_time = time.time()
        total_time = end_time - start_time
        self.inputGroupLayout.itemAt(0).widget().setText("Time: " + str(total_time) + " seconds")
        model = TableModel(data)
        self.table.setModel(model)

    def button3_clicked_slot(self):
        # remove prior widgets (if any) from the input layout
        self.clear_input_widgets()

        # reset data
        self.reset_table()

        checkbox = QtWidgets.QCheckBox('Codeshare?')

        checkbox.stateChanged.connect(lambda: self.question3_checkbox_slot(checkbox))

        label = QtWidgets.QLabel("Time: 0 seconds")
        self.inputGroupLayout.addWidget(label)
        self.inputGroupLayoutList.append(label)

        self.inputGroupLayout.addWidget(checkbox)
        self.inputGroupLayoutList.append(checkbox)

    def question3_checkbox_slot(self, checkbox):
        data = None
        start_time = time.time()
        if checkbox.isChecked():
            data = task.problem3('Y')
        else:
            data = task.problem3('N')
        end_time = time.time()
        total_time = end_time - start_time
        self.inputGroupLayout.itemAt(0).widget().setText("Time: " + str(total_time) + " seconds")

        model = TableModel(data)
        self.table.setModel(model)

    def button4_clicked_slot(self):
        # remove prior widgets (if any) from the input layout
        self.clear_input_widgets()

        # reset data
        self.reset_table()

        checkbox = QtWidgets.QCheckBox('Active?')

        checkbox.stateChanged.connect(lambda: self.question4_checkbox_slot(checkbox))

        label = QtWidgets.QLabel("Time: 0 seconds")
        self.inputGroupLayout.addWidget(label)
        self.inputGroupLayoutList.append(label)

        self.inputGroupLayout.addWidget(checkbox)
        self.inputGroupLayoutList.append(checkbox)

    def question4_checkbox_slot(self, checkbox):
        data = None
        start_time = time.time()
        if checkbox.isChecked():
            data = task.problem4('Y')
        else:
            data = task.problem4('N')
        end_time = time.time()
        total_time = end_time - start_time
        self.inputGroupLayout.itemAt(0).widget().setText("Time: " + str(total_time) + " seconds")

        model = TableModel(data)
        self.table.setModel(model)


    def button5_clicked_slot(self):
        # remove prior widgets (if any) from the input layout
        self.clear_input_widgets()

        # reset data
        self.reset_table()

        label = QtWidgets.QLabel("Time: 0 seconds")
        self.inputGroupLayout.addWidget(label)
        self.inputGroupLayoutList.append(label)

        start_time = time.time()
        data = task.problem5()
        model = TableModel(data)
        self.table.setModel(model)
        end_time = time.time()
        total_time = end_time - start_time
        self.inputGroupLayout.itemAt(0).widget().setText("Time: " + str(total_time) + " seconds")

        # visualization (graph)
        CountryLabel = list(data["p.Country"])
        plt.pie(data.Count, labels=CountryLabel,
                startangle=90, counterclock=False)
        plt.title("Top 10 Countries\nWith the most Airports",
                  fontdict={'fontweight': 'bold'})
        plt.show()


    def button6_clicked_slot(self):
        # remove prior widgets (if any) from the input layout
        self.clear_input_widgets()

        # reset data
        self.reset_table()

        spinbox = QtWidgets.QSpinBox()
        spinbox.valueChanged.connect( lambda : self.question6_spinbox_changed_slot(spinbox.value()))

        label = QtWidgets.QLabel("Time: 0 seconds")
        self.inputGroupLayout.addWidget(label)
        self.inputGroupLayoutList.append(label)

        self.inputGroupLayout.addWidget(spinbox)
        self.inputGroupLayoutList.append(spinbox)

    def question6_spinbox_changed_slot(self, limit: int):
        start_time = time.time()
        data = task.problem6(limit)
        end_time = time.time()
        total_time = end_time - start_time
        self.inputGroupLayout.itemAt(0).widget().setText("Time: " + str(total_time) + " seconds")

        model = TableModel(data)
        self.table.setModel(model)

        # visualization (graph)
        plt.figure(figsize=(12, 5))
        sns.barplot(data=data, x="n.City", y="Total")
        plt.title(f"Top {limit} Cities\nWith the most incoming & outgoing",
                  fontdict={'fontweight': 'bold'})
        plt.show()


    def button7_clicked_slot(self):
        # remove prior widgets (if any) from the input layout
        self.clear_input_widgets()

        # reset data
        self.reset_table()

        combobox1 = QtWidgets.QComboBox()
        combobox1.addItems(cities)
        combobox1.currentTextChanged.connect(
            lambda text: self.question7_combobox_textchanged_slot(text, combobox2.currentText()))

        combobox2 = QtWidgets.QComboBox()
        combobox2.addItems(cities)
        combobox2.currentTextChanged.connect(
            lambda text: self.question7_combobox_textchanged_slot(combobox1.currentText(), text))

        label = QtWidgets.QLabel("Time: 0 seconds")
        self.inputGroupLayout.addWidget(label)
        self.inputGroupLayoutList.append(label)

        self.inputGroupLayout.addWidget(combobox1)
        self.inputGroupLayout.addWidget(combobox2)
        self.inputGroupLayoutList.append(combobox1)
        self.inputGroupLayoutList.append(combobox2)

    def question7_combobox_textchanged_slot(self, city1: str, city2: str):
        start_time = time.time()
        data = task.problem7(city1, city2)
        end_time = time.time()
        total_time = end_time - start_time
        self.inputGroupLayout.itemAt(0).widget().setText("Time: " + str(total_time) + " seconds")
        model = TableModel(data)
        self.table.setModel(model)

    def button8_clicked_slot(self):
        # remove prior widgets (if any) from the input layout
        self.clear_input_widgets()

        # reset data
        self.reset_table()

        combobox1 = QtWidgets.QComboBox()
        combobox1.addItems(cities)
        combobox2 = QtWidgets.QComboBox()
        combobox2.addItems(cities)
        spinbox = QtWidgets.QSpinBox()

        combobox1.currentTextChanged.connect(
            lambda text: self.question8_slot(text, combobox2.currentText(), spinbox.value()))
        combobox2.currentTextChanged.connect(
            lambda text: self.question8_slot(combobox1.currentText(), text, spinbox.value()))
        spinbox.valueChanged.connect(
            lambda: self.question8_slot(combobox1.currentText(), combobox2.currentText(), spinbox.value()))

        label = QtWidgets.QLabel("Time: 0 seconds")
        self.inputGroupLayout.addWidget(label)
        self.inputGroupLayoutList.append(label)

        self.inputGroupLayout.addWidget(combobox1)
        self.inputGroupLayout.addWidget(combobox2)
        self.inputGroupLayout.addWidget(spinbox)
        self.inputGroupLayoutList.append(combobox1)
        self.inputGroupLayoutList.append(combobox2)
        self.inputGroupLayoutList.append(spinbox)

    def question8_slot(self, city1, city2, stops):
        start_time = time.time()
        data = task.problem8(city1, city2, stops)
        end_time = time.time()
        total_time = end_time - start_time
        self.inputGroupLayout.itemAt(0).widget().setText("Time: " + str(total_time) + " seconds")
        model = TableModel(data)
        self.table.setModel(model)

    def button9_clicked_slot(self):
        # remove prior widgets (if any) from the input layout
        self.clear_input_widgets()

        # reset data
        self.reset_table()

        combobox = QtWidgets.QComboBox()
        combobox.addItems(cities)
        spinbox = QtWidgets.QSpinBox()

        combobox.currentTextChanged.connect(lambda text: self.question9_slot(text, spinbox.value()))
        spinbox.valueChanged.connect(lambda: self.question9_slot(combobox.currentText(), spinbox.value()))

        label = QtWidgets.QLabel("Time: 0 seconds")
        self.inputGroupLayout.addWidget(label)
        self.inputGroupLayoutList.append(label)

        self.inputGroupLayout.addWidget(combobox)
        self.inputGroupLayout.addWidget(spinbox)
        self.inputGroupLayoutList.append(combobox)
        self.inputGroupLayoutList.append(spinbox)

    def question9_slot(self, city, stops):
        start_time = time.time()
        data = task.problem9(city, stops)
        end_time = time.time()
        total_time = end_time - start_time
        self.inputGroupLayout.itemAt(0).widget().setText("Time: " + str(total_time) + " seconds")
        model = TableModel(data)
        self.table.setModel(model)

    def button10_clicked_slot(self):
        # remove prior widgets (if any) from the input layout
        self.clear_input_widgets()

        # reset data
        self.reset_table()

        combobox = QtWidgets.QComboBox()
        combobox.addItems(cities)
        combobox.currentTextChanged.connect(self.question10_combobox_textchanged_slot)

        label = QtWidgets.QLabel("Time: 0 seconds")
        self.inputGroupLayout.addWidget(label)
        self.inputGroupLayoutList.append(label)

        self.inputGroupLayout.addWidget(combobox)
        self.inputGroupLayoutList.append(combobox)

    def question10_combobox_textchanged_slot(self, text):
        start_time = time.time()
        data = task.problem10(text)
        end_time = time.time()
        total_time = end_time - start_time
        self.inputGroupLayout.itemAt(0).widget().setText("Time: " + str(total_time) + " seconds")
        model = TableModel(data)
        self.table.setModel(model)

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
