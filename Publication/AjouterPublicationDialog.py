from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QComboBox, QPushButton, QDateEdit,QMessageBox
from PyQt5.QtCore import Qt, QDate
import psycopg2
from Config import connect_to_database

class AjouterPublicationDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Ajouter Publication")
        self.setGeometry(200, 200, 400, 300)

        self.layout = QFormLayout()

        self.pubno_edit = QLineEdit(self)
        self.layout.addRow("Pubno:", self.pubno_edit)

        self.titre_edit = QLineEdit(self)
        self.layout.addRow("Titre:", self.titre_edit)

        self.theme_edit = QLineEdit(self)
        self.layout.addRow("Theme:", self.theme_edit)

        self.type_combo = QComboBox(self)
        self.type_combo.addItems(['AS', 'PC', 'P', 'L', 'T', 'M'])
        self.layout.addRow("Type:", self.type_combo)

        self.volume_edit = QLineEdit(self)
        self.layout.addRow("Volume:", self.volume_edit)

        self.date_edit = QDateEdit(self)
        self.date_edit.setDate(QDate.currentDate())
        self.layout.addRow("Date:", self.date_edit)

        self.apparition_edit = QLineEdit(self)
        self.layout.addRow("Apparition:", self.apparition_edit)

        self.editeur_edit = QLineEdit(self)
        self.layout.addRow("Editeur:", self.editeur_edit)

        self.rang_edit = QLineEdit(self)
        self.layout.addRow("Rang:", self.rang_edit)

        self.chercheur_combo = QComboBox(self)
        self.populate_chercheur_combo()
        self.layout.addRow("Chercheur:", self.chercheur_combo)

        self.btn_ajouter = QPushButton("Ajouter", self)
        self.btn_ajouter.clicked.connect(self.ajouter_publication)
        self.layout.addRow(self.btn_ajouter)

        self.setLayout(self.layout)

    def populate_chercheur_combo(self):
        connection = connect_to_database()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT chno,chnom FROM Chercheur")
                chercheurs = cursor.fetchall()
                self.chercheur_combo.addItems([f"{chercheur[1]} (Chno: {chercheur[0]})" for chercheur in chercheurs])

        finally:
            connection.close()

    def ajouter_publication(self):
        connection = connect_to_database()
        
        try:
            pubno = self.pubno_edit.text(),
            titre = self.titre_edit.text(),
            theme = self.theme_edit.text(),
            type = self.type_combo.currentText(),
            volume = int(self.volume_edit.text())  if self.volume_edit.text().isnumeric else None ,
            date = self.date_edit.date().toString(Qt.ISODate),
            apparition = self.apparition_edit.text(),
            editeur = self.editeur_edit.text(),
            rang = int(self.rang_edit.text()) if self.rang_edit.text().isnumeric else None ,
            chno = int(self.chercheur_combo.currentText().split("(Chno: ")[1].split(")")[0]) if self.chercheur_combo.currentText().isnumeric else None
            

            with connection.cursor() as cursor:
                cursor.execute("Insert Into Publication Values (%s, %s, %s, %s, %s, %s, %s, %s)",
                            (pubno, titre,theme, type,volume, date, apparition, editeur))
                
                cursor.execute("Insert Into Publier Values (%s, %s, %s)",
                            (chno, pubno,rang))
            connection.commit()
            self.close()

        except Exception as e:
            self.show_error_message(str(e))
        finally:
            connection.close()


    def show_error_message(self, message):
        QMessageBox.critical(self, "Error", message, QMessageBox.Ok)