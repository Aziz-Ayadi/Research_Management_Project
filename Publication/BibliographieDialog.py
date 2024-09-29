from PyQt5.QtWidgets import QTableWidgetItem, QDialog, QTableWidget, QWidget, QVBoxLayout, QLabel, QMessageBox
from PyQt5.QtCore import Qt, QDate
import psycopg2
from Config import connect_to_database


class BibliographieDialog(QDialog):
    
    def __init__(self, pubno):
        super().__init__()

        self.setWindowTitle("Bibliographie")
        self.setGeometry(200, 200, 400, 300)

        self.central_widget = QWidget(self)

        self.layout = QVBoxLayout()

        self.label = QLabel(f"Chercheurs for Publication with Pabno: {pubno}")
        self.layout.addWidget(self.label)

        self.table_chercheurs = QTableWidget(self)
        self.layout.addWidget(self.table_chercheurs)

        self.populate_chercheurs(pubno)

        self.central_widget.setLayout(self.layout)

    def populate_chercheurs(self,pubno):
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
                WHERE c.chno IN (
                    SELECT pr.chno
                    FROM Publier pr
                    WHERE pr.pubno = %s
                )
            """, (pubno,))

            chercheurs_data = cursor.fetchall()

            if not chercheurs_data:
                self.show_error_message(f"La publication avec le numéro {pubno} n'admet pas des chercheurs.")
                return 0

            self.table_chercheurs.setColumnCount(len(chercheurs_data[0]))
            self.table_chercheurs.setHorizontalHeaderLabels([
                "Chno", "Chnom", "Grade", "Statut", "DateRecrut","Email", "Supnom", "Labnom", "Facnom"
            ])

            self.table_chercheurs.setRowCount(len(chercheurs_data))
            for row, chercheur in enumerate(chercheurs_data):
                for col, value in enumerate(chercheur):
                    item = QTableWidgetItem(str(value))
                    self.table_chercheurs.setItem(row, col, item)

        connection.close()
        
    def show_error_message(self, message):
        QMessageBox.critical(self, "Error", message, QMessageBox.Ok)