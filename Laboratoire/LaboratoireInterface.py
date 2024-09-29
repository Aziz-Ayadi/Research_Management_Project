import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout,QMessageBox,
    QPushButton, QWidget, QTableWidget, QTableWidgetItem
)
from PyQt5.QtCore import pyqtSignal
import psycopg2
from Laboratoire.AjouterLaboratoireDialog import AjouterLaboratoireDialog
from Laboratoire.HierarchieDialog import HierarchieDialog
from Config import connect_to_database

class LaboratoireInterface(QMainWindow):

    laboratoire_selected = pyqtSignal(dict)


    def __init__(self):
        super().__init__()

        self.setWindowTitle("Laboratoire Interface")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.table_laboratoire = QTableWidget(self)
        self.layout.addWidget(self.table_laboratoire)

        self.btn_ajouter = QPushButton("Ajouter", self)
        self.btn_ajouter.clicked.connect(self.show_ajouter_laboratoire_dialog)
        self.layout.addWidget(self.btn_ajouter)

        self.btn_afficher_hierarchie = QPushButton("Afficher Hierarchie", self)
        self.btn_afficher_hierarchie.clicked.connect(self.afficher_hierarchie)
        self.layout.addWidget(self.btn_afficher_hierarchie)

        self.central_widget.setLayout(self.layout)

        self.populate_laboratoire()
        
        self.table_laboratoire.cellClicked.connect(self.handle_chercheur_selection)


    def populate_laboratoire(self):
        connection = connect_to_database()

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    l.labno, l.labnom, f.facno , f.facnom
                FROM Laboratoire l 
                LEFT JOIN Faculte f ON l.facno = f.facno
            """)
            laboratoire_data = cursor.fetchall()

            self.table_laboratoire.setColumnCount(len(laboratoire_data[0]))
            self.table_laboratoire.setHorizontalHeaderLabels([
                "Labno", "Labnom", "Facno" , "Facnom"
            ])

            self.table_laboratoire.setRowCount(len(laboratoire_data))
            for row, laboratoire in enumerate(laboratoire_data):
                for col, value in enumerate(laboratoire):
                    item = QTableWidgetItem(str(value))
                    self.table_laboratoire.setItem(row, col, item)

        connection.close()


    def show_ajouter_laboratoire_dialog(self):
        dialog = AjouterLaboratoireDialog(self)
        dialog.exec_()
        self.populate_laboratoire()
            

    def afficher_hierarchie(self):        
        selected_row = self.table_laboratoire.currentRow()
        if selected_row == -1:
            self.show_error_message("Veuillez sélectionner un Laboratoire à Consulter.")
            return 0
            
        labno_item = self.table_laboratoire.item(selected_row, 0)
        
        if labno_item is None:
            self.show_error_message("Erreur lors de la récupération du numéro de laboratoire.")
            return 0
        
        labno = int(labno_item.text())
        
        laboratoire_interface = HierarchieDialog(labno)
        laboratoire_interface.exec_()


    def handle_chercheur_selection(self, row, col):
        laboratoire_info = {}
        for col in range(self.table_laboratoire.columnCount()):
            header = self.table_laboratoire.horizontalHeaderItem(col).text()
            item = self.table_laboratoire.item(row, col)
            if item:
                laboratoire_info[header] = item.text()
        self.laboratoire_selected.emit(laboratoire_info)
        
        
    def show_error_message(self, message):
            QMessageBox.critical(self, "Error", message, QMessageBox.Ok)
