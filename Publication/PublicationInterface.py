import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout,QMessageBox,
    QPushButton, QWidget, QTableWidget, QTableWidgetItem
)
import psycopg2
from PyQt5.QtCore import pyqtSignal
from Publication.AjouterPublicationDialog import AjouterPublicationDialog
from Publication.BibliographieDialog import BibliographieDialog
from Config import connect_to_database

class PublicationInterface(QMainWindow):

    publication_selected = pyqtSignal(dict)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Publication Interface")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.table_publication = QTableWidget(self)
        self.layout.addWidget(self.table_publication)

        self.btn_ajouter = QPushButton("Ajouter", self)
        self.btn_ajouter.clicked.connect(self.show_ajouter_publication_dialog)
        self.layout.addWidget(self.btn_ajouter)

        self.btn_extraire_bibliographie = QPushButton("Extraire Bibliographie", self)
        self.btn_extraire_bibliographie.clicked.connect(self.extraire_bibliographie)
        self.layout.addWidget(self.btn_extraire_bibliographie)

        self.central_widget.setLayout(self.layout)

        self.populate_publication()

        self.table_publication.cellClicked.connect(self.handle_publication_selection)


    def populate_publication(self):
        connection = connect_to_database()

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    pubno, titre, theme, type_p, volume_p, date_p, apparition,
                    editeur
                FROM Publication
            """)
            publication_data = cursor.fetchall()

            self.table_publication.setColumnCount(len(publication_data[0]))
            self.table_publication.setHorizontalHeaderLabels([
                "Pubno", "Titre", "Theme", "Type", "Volume", "Date",
                "Apparition", "Editeur"
            ])

            self.table_publication.setRowCount(len(publication_data))
            for row, publication in enumerate(publication_data):
                for col, value in enumerate(publication):
                    item = QTableWidgetItem(str(value))
                    self.table_publication.setItem(row, col, item)

        connection.close()

    def show_ajouter_publication_dialog(self):
        dialog = AjouterPublicationDialog(self)
        dialog.exec_()
        self.populate_publication()
        
    
    def extraire_bibliographie(self):        
        selected_row = self.table_publication.currentRow()
        if selected_row == -1:
            self.show_error_message("Veuillez sélectionner une Publication à Consulter.")
            return 0
            
        pubno_item = self.table_publication.item(selected_row, 0)
        
        if pubno_item is None:
            self.show_error_message("Erreur lors de la récupération du numéro de publication.")
            return 0
        
        pubno = pubno_item.text()
        
        bib_interface = BibliographieDialog(pubno)
        bib_interface.exec_()   


    def handle_publication_selection(self, row, col):
        publication_info = {}
        for col in range(self.table_publication.columnCount()):
            header = self.table_publication.horizontalHeaderItem(col).text()
            item = self.table_publication.item(row, col)
            if item:
                publication_info[header] = item.text()
        self.publication_selected.emit(publication_info)


    def show_error_message(self, message):
            QMessageBox.critical(self, "Error", message, QMessageBox.Ok)