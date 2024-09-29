from PyQt5.QtWidgets import (
    QPushButton,QVBoxLayout,QLabel,
    QDialog, QFormLayout, QLineEdit, QComboBox, QPushButton, QMessageBox, QDateEdit
)
from PyQt5.QtCore import Qt, QDate
import psycopg2
from Config import connect_to_database

class ChercheurModificationDialog(QDialog):
    
    def __init__(self, chercheur_info, parent=None):
        super().__init__(parent)

        self.chno = chercheur_info.get("Chno")
        
        self.chnom_edit = QLineEdit(chercheur_info.get("Chnom"))
        self.grade_combo = QComboBox(self)
        self.statut_combo = QComboBox(self)
        self.daterecrut_edit = QDateEdit(self)
        self.salaire_edit = QLineEdit(chercheur_info.get("Salaire"))
        self.prime_edit = QLineEdit(chercheur_info.get("Prime"))
        self.email_edit = QLineEdit(chercheur_info.get("Email"))
        self.faculty_combo = QComboBox(self)
        self.lab_combo = QComboBox(self)
        self.supervisor_combo = QComboBox(self)

        self.setup_ui(chercheur_info)
    
    def setup_ui(self, chercheur_info):
        layout = QVBoxLayout(self)

        self.add_label_and_widget(layout, "Chercheur Nom:", self.chnom_edit)
        self.add_label_and_widget(layout, "Grade:", self.grade_combo)
        self.add_label_and_widget(layout, "Statut:", self.statut_combo)

        label_daterecrut = QLabel("Date de Recrutement:")
        layout.addWidget(label_daterecrut)
        self.daterecrut_edit.setDate(QDate.fromString(chercheur_info.get("DateRecrut"), Qt.ISODate))
        layout.addWidget(self.daterecrut_edit)

        self.add_label_and_widget(layout, "Salaire:", self.salaire_edit)
        self.add_label_and_widget(layout, "Prime:", self.prime_edit)
        self.add_label_and_widget(layout, "Email:", self.email_edit)
        self.add_label_and_widget(layout, "Faculté:", self.faculty_combo)
        self.add_label_and_widget(layout, "Laboratoire:", self.lab_combo)
        self.add_label_and_widget(layout, "Superviseur:", self.supervisor_combo)

        self.populate_combo_boxes(chercheur_info)
        self.faculty_combo.currentTextChanged.connect(self.on_faculty_combo_change)
        self.lab_combo.currentTextChanged.connect(self.on_labo_combo_change)

        self.btn_modifier = QPushButton("Modifier", self)
        self.btn_modifier.clicked.connect(self.handle_modifier)
        layout.addWidget(self.btn_modifier)
    
    def add_label_and_widget(self, layout, label_text, widget):
        label = QLabel(label_text)
        layout.addWidget(label)
        layout.addWidget(widget)



    def populate_combo_boxes(self, chercheur_info):
        self.grade_combo.addItems(['E', 'D', 'A', 'MA', 'MC', 'PR'])
        self.grade_combo.setCurrentText(chercheur_info.get("Grade"))
        
        self.statut_combo.addItems(['P', 'C'])
        self.statut_combo.setCurrentText(chercheur_info.get("Statut"))
        
        self.populate_faculty_combo()
        self.faculty_combo.setCurrentText(chercheur_info.get("Facnom"))

        self.populate_lab_combo()
        self.lab_combo.setCurrentText(chercheur_info.get("Labnom"))
        
        self.populate_supervisor_combo()
        self.supervisor_combo.setCurrentText(chercheur_info.get("Supnom"))
    
    
    
    def populate_faculty_combo(self):
        connection = connect_to_database()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT facno, facnom FROM Faculte")
                faculties = cursor.fetchall()
                self.faculty_combo.addItems([f"{fac[1]} (FacNo: {fac[0]})" for fac in faculties])

        finally:
            connection.close()
    
    def populate_lab_combo(self):
        selected_faculty = self.faculty_combo.currentText()

        if not selected_faculty:
            return
        connection = connect_to_database()

        try:
            with connection.cursor() as cursor:
                facno = selected_faculty.split("(FacNo: ")[1].split(")")[0]
                cursor.execute("SELECT labno, labnom FROM Laboratoire WHERE facno = %s", (facno,))
                labs = cursor.fetchall()
                self.lab_combo.clear()
                self.lab_combo.addItems([f"{lab[1]} (LabNo: {lab[0]})" for lab in labs])

        finally:
            connection.close()
    
    def populate_supervisor_combo(self):
        selected_faculty = self.faculty_combo.currentText()
        selected_lab = self.lab_combo.currentText()

        if not selected_faculty or not selected_lab:
            return

        connection = connect_to_database()

        try:
            with connection.cursor() as cursor:
                facno = selected_faculty.split("(FacNo: ")[1].split(")")[0]
                labno = selected_lab.split("(LabNo: ")[1].split(")")[0]
                cursor.execute("SELECT chno, chnom FROM Chercheur WHERE grade IN ('A', 'MA', 'PR', 'MC') AND labno = %s AND facno = %s",
                            (labno, facno))
                supervisors = cursor.fetchall()
                self.supervisor_combo.clear()
                self.supervisor_combo.addItems([f"{sup[1]} (ChNo: {sup[0]})" for sup in supervisors])

        finally:
            connection.close()
    
    def on_faculty_combo_change(self):
        self.populate_lab_combo()
        self.populate_supervisor_combo()
    
    def on_labo_combo_change(self):
        self.populate_supervisor_combo()
    
    def show_error_message(self, message):
        QMessageBox.critical(self, "Error", message, QMessageBox.Ok)



    def handle_modifier(self):
        chno = int(self.chno)
        modified_chnom = self.chnom_edit.text()
        modified_grade = self.grade_combo.currentText()
        modified_statut = self.statut_combo.currentText()
        modified_daterecrut = self.daterecrut_edit.date().toString(Qt.ISODate)
        modified_salaire =  float(self.salaire_edit.text()) if self.salaire_edit.text() else None
        modified_prime = float(self.prime_edit.text()) if self.prime_edit.text() else None
        modified_email = self.email_edit.text() if self.email_edit.text() else None
        modified_faculty = int(self.faculty_combo.currentText().split("(FacNo: ")[1].split(")")[0]) if self.faculty_combo.currentText() else None
        modified_lab = int(self.lab_combo.currentText().split("(LabNo: ")[1].split(")")[0]) if self.lab_combo.currentText() else None
        modified_supervisor = int(self.supervisor_combo.currentText().split("(ChNo: ")[1].split(")")[0]) if self.supervisor_combo.currentText() else None

        connection = connect_to_database()
        
        try:
            with connection.cursor() as cursor:
                cursor.execute('''
                    Call modifier_profil_chercheur(
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    )
                ''', (
                    chno, modified_chnom, modified_grade, modified_statut, modified_daterecrut,
                    modified_salaire, modified_prime, modified_email ,modified_supervisor,modified_lab,modified_faculty
                ))
            connection.commit()
            self.close()
            
        except psycopg2.Error as e:
            self.show_error_message(str(e))
        finally:
            connection.close()


