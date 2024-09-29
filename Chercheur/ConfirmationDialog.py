from PyQt5.QtWidgets import (
    QPushButton,
    QDialog, QFormLayout, QLineEdit, QComboBox, QPushButton, QMessageBox, QDateEdit,QHBoxLayout,QLabel,QVBoxLayout
)
from PyQt5.QtCore import Qt, QDate
import psycopg2

class ConfirmationDialog(QDialog):
    
    def __init__(self, chno):
        super().__init__()

        self.setWindowTitle("Confirmation de suppression")
        self.setMinimumWidth(300)

        label = QLabel(f"Êtes-vous sûr de vouloir supprimer le chercheur avec le numéro {chno} ?")

        yes_button = QPushButton("Oui")
        yes_button.clicked.connect(self.accept)

        no_button = QPushButton("Non")
        no_button.clicked.connect(self.reject)

        button_layout = QHBoxLayout()
        button_layout.addWidget(yes_button)
        button_layout.addWidget(no_button)

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addLayout(button_layout)

        self.setLayout(layout)
