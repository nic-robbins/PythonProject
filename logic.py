import csv
from PyQt6.QtCore import *
from gui import *
from PyQt6.QtWidgets import *

class Logic(QMainWindow, Ui_MainWindow):
    """
    Class which includes all logic related to the functionality of the Brew Tracker app.
    This app tracks different coffee recipes/brew strategies and saves each entry to a provided and formatted csv file.
    """
    def __init__(self) -> None:
        """
        Constructor method. Sets the default values of the brew object.
        """
        super().__init__()
        self.setupUi(self)
        self.__csv_file_name: str = "data.csv"
        self.dateTimeEdit.setDate(QDate.currentDate())
        self.dateTimeEdit.setMaximumDate(QDate.currentDate())
        self.brewNotesInput.setTabChangesFocus(True)
        self.saveButton.clicked.connect(self.submit)
        self.clearButton.clicked.connect(self.reset_form)

    def submit(self) -> None:
        """
        Submits the filled form so that an entry gets written to the csv file.
        Also includes data validation.
        """
        bean_str: str = self.beanOriginInput.text()
        method_str: str = self.dripperSelectionInput.currentText().strip()

        try:
            if not bean_str:
                raise ValueError("The 'Bean/Origin' field cannot be left blank")
            if not method_str:
                raise ValueError("Please select or type a valid 'Dripper/Brew Method'")

            dose: int = self.coffeeDoseInput.value()
            water: int = self.totalWaterInput.value()

            if dose <= 0 or water <= 0:
                raise ValueError("Dose and water must be greater than 0")

            grind: str = self.grindSettingInput.currentText()
            temp: int = self.waterTempInput.value()
            brew_time: str = self.brewTimeInput.text()
            notes: str = self.brewNotesInput.toPlainText().strip()
            rating: str = self.rateInput.currentText()
            select_date: str = self.dateTimeEdit.date().toString("MM-dd-yyyy")

            row_data: list = [select_date, bean_str, method_str, grind, dose, water, temp, brew_time, notes, rating]

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


    def reset_form(self) -> None:
        """
        Clears out all text and restores the default values.
        Asks the user if they're sure they want to reset the form.
        """
        reply = QMessageBox.question(
            self,
            "Confirm Clear",
            "Are you sure you want to clear the form?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.beanOriginInput.clear()
            self.dripperSelectionInput.setCurrentIndex(0)
            self.grindSettingInput.setCurrentIndex(0)
            self.coffeeDoseInput.setValue(self.coffeeDoseInput.minimum())
            self.totalWaterInput.setValue(self.totalWaterInput.minimum())
            self.waterTempInput.setValue(self.waterTempInput.minimum())
            self.brewTimeInput.setTime(self.brewTimeInput.minimumTime())
            self.brewNotesInput.clear()
            self.rateInput.setCurrentIndex(0)
            self.dateTimeEdit.setDate(QDate.currentDate())

