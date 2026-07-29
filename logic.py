import csv
from PyQt6.QtCore import *
from gui import *
from PyQt6.QtWidgets import *


class Logic(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.__csv_file_name: str = "data.csv"

        self.dateTimeEdit.setDate(QDate.currentDate())
        self.dateTimeEdit.setMaximumDate(QDate.currentDate())

        self.brewNotesInput.setTabChangesFocus(True)

        self.saveButton.clicked.connect(self.submit)
        self.clearButton.clicked.connect(self.reset_form)


    def submit(self):
        bean_str = self.beanOriginInput.text()
        method_str = self.dripperSelectionInput.currentText().strip()

        try:
            if not bean_str:
                raise ValueError("The 'Bean/Origin' field cannot be left blank")
            if not method_str:
                raise ValueError("Please select or type a valid 'Dripper/Brew Method'")

            dose = self.coffeeDoseInput.value()
            water = self.totalWaterInput.value()

            if dose <= 0 or water <= 0:
                raise ValueError("Dose and water must be greater than 0")


            select_date = self.dateTimeEdit.date().toString("MM-dd-yyyy")
            grind = self.grindSettingInput.currentText()
            temp = self.waterTempInput.value()
            brew_time = self.brewTimeInput.text()
            notes = self.brewNotesInput.toPlainText().strip()
            rating = self.rateInput.currentText()

            row_data = [select_date, bean_str, method_str, grind, dose, water, temp, brew_time, notes, rating]

            with open(self.__csv_file_name, "a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(row_data)

            QMessageBox.information(self, "Success", "Brew submitted")
            self.reset_form()

            if self.dripperSelectionInput.findText(method_str) == -1:
                self.dripperSelectionInput.addItem(method_str)

        except ValueError as val_error:
            QMessageBox.warning(self, "Input Error", str(val_error))

        except IOError as io_error:
            QMessageBox.critical(self, "Failure", "Entry could not be saved", io_error)


    def reset_form(self):
        self.beanOriginInput.clear()
        self.brewNotesInput.clear()


        self.coffeeDoseInput.setValue(self.coffeeDoseInput.minimum())
        self.totalWaterInput.setValue(self.totalWaterInput.minimum())
        self.waterTempInput.setValue(self.waterTempInput.minimum())

        self.brewTimeInput.setTime(self.brewTimeInput.minimumTime())
        self.dateTimeEdit.setDate(QDate.currentDate())

        self.dripperSelectionInput.setCurrentIndex(0)
        self.grindSettingInput.setCurrentIndex(0)
        self.rateInput.setCurrentIndex(0)

