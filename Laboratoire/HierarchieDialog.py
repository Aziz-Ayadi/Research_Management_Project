from PyQt5.QtWidgets import QTableWidgetItem, QDialog, QTableWidget, QWidget, QLabel,QVBoxLayout,QMessageBox
from PyQt5.QtCore import Qt, QDate
import psycopg2
from Config import connect_to_database

class HierarchieDialog(QDialog):

    def __init__(self, labno):
        super().__init__()

        self.setWindowTitle("Hierarchie")
        self.setGeometry(200, 200, 400, 300)

        self.central_widget = QWidget(self)

        self.layout = QVBoxLayout()
        
        self.label = QLabel(f"Chercheurs for Laboratoire with Labno: {labno}")
        self.layout.addWidget(self.label)

        self.table_chercheurs = QTableWidget(self)
        self.layout.addWidget(self.table_chercheurs)

        self.populate_chercheurs(labno)

        self.central_widget.setLayout(self.layout)

    def populate_chercheurs(self,labno):
        connection = connect_to_database()

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    c.chno, c.chnom, c.grade, c.statut, c.daterecrut,
                    c.email, s.chnom AS supnom,
                    l.labnom, f.facnom
                FROM Chercheur c
                LEFT JOIN Chercheur s ON c.supno = s.chno
                LEFT JOIN Laboratoire l ON c.labno = l.labno
                LEFT JOIN Faculte f ON c.facno = f.facno
                WHERE c.labno = %s
            """, (labno,))
            chercheurs_data = cursor.fetchall()
            
            if not chercheurs_data:
                self.show_error_message(f"Le laboratoire avec le numéro {labno} n'admet pas des chercheurs.")
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