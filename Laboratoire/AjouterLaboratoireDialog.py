from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QComboBox, QPushButton, QDateEdit, QMessageBox
from PyQt5.QtCore import Qt, QDate
import psycopg2
from Config import connect_to_database

class AjouterLaboratoireDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Ajouter Laboratoire")
        self.setGeometry(200, 200, 400, 300)

        self.layout = QFormLayout()

        self.labno_edit = QLineEdit(self)
        self.layout.addRow("Labno:", self.labno_edit)

        self.labnom_edit = QLineEdit(self)
        self.layout.addRow("Labnom:", self.labnom_edit)

        self.faculty_combo = QComboBox(self)
        self.populate_faculty_combo()
        self.layout.addRow("Faculté:", self.faculty_combo)

        self.btn_ajouter = QPushButton("Ajouter", self)
        self.btn_ajouter.clicked.connect(self.ajouter_laboratoire)
        self.layout.addRow(self.btn_ajouter)

        self.setLayout(self.layout)

    def populate_faculty_combo(self):
        connection = connect_to_database()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT facno, facnom FROM Faculte")
                faculties = cursor.fetchall()
                self.faculty_combo.addItems([f"{fac[1]} (FacNo: {fac[0]})" for fac in faculties])

        finally:
            connection.close()

    def ajouter_laboratoire(self):
        connection = connect_to_database()
        try:     
            facno = int(self.faculty_combo.currentText().split("(FacNo: ")[1].split(")")[0]) if self.faculty_combo.currentText().isnumeric else None
            labno = int(self.labno_edit.text()) if self.labno_edit.text().isnumeric else None 
            labnom = self.labnom_edit.text(),
                
            with connection.cursor() as cursor:
                cursor.execute("Insert Into laboratoire Values (%s, %s,%s)",
                                    ( labno, labnom, facno))
            connection.commit()
            self.close()

        except Exception as e:
            self.show_error_message(str(e))
        finally:
            connection.close()


    def show_error_message(self, message):
        QMessageBox.critical(self, "Error", message, QMessageBox.Ok)