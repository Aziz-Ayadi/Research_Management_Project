import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout,
    QPushButton, QWidget, QTableWidget, QTableWidgetItem,QDialog,QMessageBox ,QStackedWidget
)
from PyQt5.QtCore import pyqtSignal
import psycopg2
from Chercheur.AjouterChercheurDialog import AjouterChercheurDialog
from Chercheur.ChercheurModificationDialog import ChercheurModificationDialog
from Chercheur.ConfirmationDialog import ConfirmationDialog
from Chercheur.PublicationInterface import PublicationInterface
from Config import connect_to_database

class ChercheurInterface(QMainWindow):
    chercheur_selected = pyqtSignal(dict)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Chercheur Interface")
        self.setGeometry(250, 250, 1400, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.table_chercheurs = QTableWidget(self)
        self.layout.addWidget(self.table_chercheurs)

        self.btn_ajouter = QPushButton("Ajouter", self)
        self.btn_ajouter.clicked.connect(self.show_ajouter_chercheur_dialog)
        self.layout.addWidget(self.btn_ajouter)

        self.btn_modifier = QPushButton("Modifier", self)
        self.btn_modifier.clicked.connect(self.modifier_chercheur)
        self.layout.addWidget(self.btn_modifier)

        self.btn_supprimer = QPushButton("Supprimer", self)
        self.btn_supprimer.clicked.connect(self.supprimer_chercheur)
        self.layout.addWidget(self.btn_supprimer)

        self.btn_consulter_articles = QPushButton("Consulter Articles", self)
        self.layout.addWidget(self.btn_consulter_articles)
        self.btn_consulter_articles.clicked.connect(self.consulter_articles)
        
        self.central_widget.setLayout(self.layout)

        self.populate_chercheurs()

        self.table_chercheurs.cellClicked.connect(self.handle_chercheur_selection)
        
        
        
    def populate_chercheurs(self):
        connection = connect_to_database()

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    c.chno, c.chnom, c.grade, c.statut, c.daterecrut,
                    c.salaire, c.prime, c.email, s.chnom AS supnom,
                    l.labnom, f.facnom
                FROM Chercheur c
                LEFT JOIN Chercheur s ON c.supno = s.chno
                LEFT JOIN Laboratoire l ON c.labno = l.labno
                LEFT JOIN Faculte f ON c.facno = f.facno
                ORDER BY c.chno ASC 
            """)
            chercheurs_data = cursor.fetchall()

            self.table_chercheurs.setColumnCount(len(chercheurs_data[0]))
            self.table_chercheurs.setHorizontalHeaderLabels([
                "Chno", "Chnom", "Grade", "Statut", "DateRecrut", "Salaire",
                "Prime", "Email", "Supnom", "Labnom", "Facnom"
            ])

            self.table_chercheurs.setRowCount(len(chercheurs_data))
            for row, chercheur in enumerate(chercheurs_data):
                for col, value in enumerate(chercheur):
                    item = QTableWidgetItem(str(value))
                    self.table_chercheurs.setItem(row, col, item)

        connection.close()



    def show_ajouter_chercheur_dialog(self):
        dialog = AjouterChercheurDialog(self)
        dialog.exec_()
        self.populate_chercheurs()



    def modifier_chercheur(self):
        selected_row = self.table_chercheurs.currentRow()
        if selected_row == -1:
            self.show_error_message("Veuillez sélectionner un chercheur à modifier.")
            return 0
        
        chercheur_info = {}
        for col in range(self.table_chercheurs.columnCount()):
            header = self.table_chercheurs.horizontalHeaderItem(col).text()
            item = self.table_chercheurs.item(selected_row, col)
            if item:
                chercheur_info[header] = item.text()

        modification_dialog = ChercheurModificationDialog(chercheur_info, self)
        modification_dialog.exec_()
        self.populate_chercheurs()



    def supprimer_chercheur(self):
        selected_row = self.table_chercheurs.currentRow()
        if selected_row == -1:
            self.show_error_message("Veuillez sélectionner un chercheur à supprimer.")
            return 0
        
        chno_item = self.table_chercheurs.item(selected_row, 0)
        if chno_item is None:
            self.show_error_message("Erreur lors de la récupération du numéro de chercheur.")
            return 0

        chno = int(chno_item.text())

        confirmation_dialog = ConfirmationDialog(chno)
        result = confirmation_dialog.exec_()

        if result == QDialog.Accepted:
            self.delete_chercheur(chno)
            self.populate_chercheurs() 
    
    def delete_chercheur(self, chno):
        try:
            connection = connect_to_database()

            with connection.cursor() as cursor:
                cursor.execute('Call supprimer_chercheur(%s)', (chno,))

            connection.commit()

        except psycopg2.Error as e:
            self.show_error_message(str(e))

        finally:
            connection.close()


        
    def consulter_articles(self):
        selected_row = self.table_chercheurs.currentRow()
        if selected_row == -1:
            self.show_error_message("Veuillez sélectionner un chercheur à Consulter.")
            return 0
            
        chno_item = self.table_chercheurs.item(selected_row, 0)
        
        if chno_item is None:
            self.show_error_message("Erreur lors de la récupération du numéro de chercheur.")
            return 0
        
        chno = int(chno_item.text())
        
        publication_interface = PublicationInterface(chno)
        publication_interface.exec_()



    def handle_chercheur_selection(self, row, col):
        chercheur_info = {}
        for col in range(self.table_chercheurs.columnCount()):
            header = self.table_chercheurs.horizontalHeaderItem(col).text()
            item = self.table_chercheurs.item(row, col)
            if item:
                chercheur_info[header] = item.text()
        self.chercheur_selected.emit(chercheur_info)

    def show_error_message(self, message):
            QMessageBox.critical(self, "Error", message, QMessageBox.Ok)

