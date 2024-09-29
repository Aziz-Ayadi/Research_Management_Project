from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QComboBox, QPushButton, QMessageBox, QDateEdit
from PyQt5.QtCore import Qt, QDate
import psycopg2
from Config import connect_to_database

class AjouterFaculteDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Ajouter Faculte")
        self.setGeometry(200, 200, 400, 300)

        self.layout = QFormLayout()

        self.facno_edit = QLineEdit(self)
        self.layout.addRow("Facno:", self.facno_edit)

        self.facnom_edit = QLineEdit(self)
        self.layout.addRow("Facnom:", self.facnom_edit)

        self.adresse_edit = QLineEdit(self)
        self.layout.addRow("Adresse:", self.adresse_edit)

        self.libelle_edit = QLineEdit(self)
        self.layout.addRow("Libellé:", self.libelle_edit)

        self.btn_ajouter = QPushButton("Ajouter", self)
        self.btn_ajouter.clicked.connect(self.ajouter_faculte)
        self.layout.addRow(self.btn_ajouter)

        self.setLayout(self.layout)

    def ajouter_faculte(self):
        try:
            facno = int(self.facno_edit.text())  if self.facno_edit.text().isnumeric else None,
            facnom = self.facnom_edit.text(),
            adresse = self.adresse_edit.text(),
            libelle = self.libelle_edit.text() 
        
            connection = connect_to_database()
            
            with connection.cursor() as cursor:
                cursor.execute("Insert Into Faculte Values (%s, %s,%s, %s)",(facno,facnom,adresse,libelle)
                            )
            connection.commit()
            
            self.close()

        except Exception as e:
            self.show_error_message(str(e))
        finally:
            connection.close()

    def show_error_message(self, message):
        QMessageBox.critical(self, "Error", message, QMessageBox.Ok)