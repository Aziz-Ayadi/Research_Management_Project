import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QWidget, QStackedWidget
import psycopg2
from Chercheur.ChercheurInterface import ChercheurInterface
from Publication.PublicationInterface import PublicationInterface
from Laboratoire.LaboratoireInterface import LaboratoireInterface
from Faculte.FaculteInterface import FaculteInterface
from Config import connect_to_database

class MainDashboard(QMainWindow):
    
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Main Dashboard")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.label_overview = QLabel("Database Overview:")
        self.layout.addWidget(self.label_overview)

        self.stacked_widget = QStackedWidget()
        self.layout.addWidget(self.stacked_widget)

        self.display_overview()

        self.btn_chercheurs = QPushButton("Chercheurs Section")
        self.chercheur_interface = ChercheurInterface()
        self.btn_chercheurs.clicked.connect(self.show_chercheurs_section)
        self.layout.addWidget(self.btn_chercheurs)
        
        self.btn_laboratoires = QPushButton("Laboratoires Section")
        self.laboratoire_interface = LaboratoireInterface()
        self.btn_laboratoires.clicked.connect(self.show_laboratoires_section)
        self.layout.addWidget(self.btn_laboratoires)

        self.btn_facultes = QPushButton("Facultes Section")
        self.faculte_interface = FaculteInterface()
        self.btn_facultes.clicked.connect(self.show_facultes_section)
        self.layout.addWidget(self.btn_facultes)

        self.btn_publications = QPushButton("Publications Section")
        self.publication_interface = PublicationInterface()
        self.btn_publications.clicked.connect(self.show_publications_section)
        self.layout.addWidget(self.btn_publications)

        self.central_widget.setLayout(self.layout)


    def display_overview(self):
        connection = connect_to_database()

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    f.facno,
                    f.facnom,
                    l.labno,
                    l.labnom,
                    COUNT(c.chno) AS num_chercheurs
                FROM
                    Faculte f
                    LEFT JOIN Laboratoire l ON f.facno = l.facno
                    LEFT JOIN Chercheur c ON l.labno = c.labno
                GROUP BY
                    f.facno, f.facnom, l.labno, l.labnom
                ORDER BY
                    f.facno, l.labno
            """)

            faculties_and_labs = cursor.fetchall()

            overview_text = ""
            current_faculty = None

            for row in faculties_and_labs:
                facno, facnom, labno, labnom, num_chercheurs = row

                if facno != current_faculty:
                    overview_text += f"\nFaculty {facno}: {facnom}\n"
                    current_faculty = facno

                overview_text += f"  - Laboratory {labno}: {labnom} : Number of Chercheurs: {num_chercheurs}\n"

            self.label_overview.setText(overview_text)

        connection.close()


    def show_chercheurs_section(self):
        self.stacked_widget.addWidget(self.chercheur_interface)
        self.stacked_widget.setCurrentWidget(self.chercheur_interface)


    def show_laboratoires_section(self):
        self.stacked_widget.addWidget(self.laboratoire_interface)
        self.stacked_widget.setCurrentWidget(self.laboratoire_interface)



    def show_facultes_section(self):
        self.stacked_widget.addWidget(self.faculte_interface)
        self.stacked_widget.setCurrentWidget(self.faculte_interface)


    def show_publications_section(self):
        self.stacked_widget.addWidget(self.publication_interface)
        self.stacked_widget.setCurrentWidget(self.publication_interface)



