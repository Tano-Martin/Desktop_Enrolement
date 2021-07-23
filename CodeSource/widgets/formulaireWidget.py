import sqlite3
import os
import re
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.uic import loadUiType
from widgets.carteWidget import MainCarte
from widgets.formulaireInterface import Ui_MainWindow

# FORM_CLASS, _ = loadUiType(os.path.join(os.path.dirname("__file__"), "ui/formulaire.ui"))
FORM_CLASS = Ui_MainWindow

photo = {1 : ""}
ligne = ""
class MainWindow(QtWidgets.QMainWindow, FORM_CLASS):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        self.setFixedSize(1299, 684)
        self.data_()
        self.bouton()
        
    def lancer_piece(self, id_element):
        self.windowData = MainCarte(id_element)
        self.windowData.show()

    def bouton(self):
        self.photo_btn.clicked.connect(self.choisir_photo)
        self.envoyer_btn.clicked.connect(self.enregistrer_data)
        self.nettoyer_btn.clicked.connect(self.nettoyer_data)
        self.recherche_edit.textEdited.connect(self.recherche_data)
        self.recherche_edit.returnPressed.connect(self.recherche_data)
        self.filtrer_btn.clicked.connect(self.filtrer_data)
        self.modifier_btn.clicked.connect(self.modifier_data)
        self.supprimer_btn.clicked.connect(self.supprimer_data)
        self.apercu_btn.clicked.connect(self.apercu_data)
    
    def apercu_data(self):
        ligne = self.tableWidget.currentRow()
        if ligne == "":
            QtWidgets.QMessageBox.warning(self, "Erreur", "Veuillez selectionner une personne s'il vous plaît !")
        else :
            id_ligne = self.tableWidget.item(ligne, 0).text()
            self.lancer_piece(id_ligne)

    def data_(self):
        db = sqlite3.connect(os.path.join(os.path.dirname("__file__"), "storage/database.db"))
        cursor = db.cursor()
        commande = """ SELECT * from register """
        resultat = cursor.execute(commande)
        self.tableWidget.setRowCount(0)

        for row_number, row_data in enumerate(resultat):
            self.tableWidget.insertRow(row_number)
            for colum_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, colum_number, QtWidgets.QTableWidgetItem(str(data)))

    def choisir_photo(self):
        nom_photo = QtWidgets.QFileDialog.getOpenFileName(self, "Choisir photo", "c://", "images (*.png *.jpg *.jpeg *.gif)")
        photo[1] = nom_photo[0]
        self.photo.setPixmap(QtGui.QPixmap(photo[1]))
        self.photo.setScaledContents(True)

    def enregistrer_data(self):
        nom = self.nom_field.text().upper()
        prenom = self.prenom_field.text().upper()
        date = self.date_field.text()
        lieu = self.lieu_field.text().upper()
        genre_homme = self.genre_h.isChecked()
        nationalite = self.nationalite_field.text().upper()
        domicile = self.domicile_field.text().upper()
        pere_field = self.pere_field.text().upper()
        mere_field = self.mere_field.text().upper()
        if genre_homme:
            genre = "M"
        else:
            genre = "F"

        if not nom or not prenom or not lieu or not nationalite or not domicile or not pere_field or not mere_field or date == "01/01/1921":
            QtWidgets.QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs avant de les soumettre !")
        elif not photo[1]:
            QtWidgets.QMessageBox.warning(self, "Erreur", "Veuillez ajouter un photo d'identité s'il vous plaît !")
        else:
            db = sqlite3.connect(os.path.join(os.path.dirname("__file__"), "storage/database.db"))
            cursor = db.cursor()
            commande = """ SELECT * from register WHERE Nom=? AND Prenom=? """
            resultat = cursor.execute(commande, (nom, prenom))
            valeurs = resultat.fetchone()
            if valeurs != None:
                image = open(photo[1], "rb")
                db = sqlite3.connect(os.path.join(os.path.dirname("__file__"), "storage/database.db"))
                cursor = db.cursor()
                valeur = (nom, prenom, date, lieu, genre, pere_field, mere_field, domicile, nationalite, sqlite3.Binary(image.read()), int(valeurs[0]))
                commande = """ UPDATE register SET Nom=?, Prenom=?, Date_de_naissance=?, Lieu_de_naissance=?, Genre=?, Nom_pere=?, Nom_mere=?, Domicile=?, Nationalite=?, Photo=? WHERE ID=? """
                cursor.execute(commande, valeur)
                db.commit()
                QtWidgets.QMessageBox.information(self, "Succès", "Modification effectué avec succès")
                self.nettoyer_data()
                self.data_()
            else:
                image = open(photo[1], "rb")
                db = sqlite3.connect(os.path.join(os.path.dirname("__file__"), "storage/database.db"))
                cursor = db.cursor()
                valeur = (nom, prenom, date, lieu, genre, pere_field, mere_field, domicile, nationalite, sqlite3.Binary(image.read()))
                commande = """ INSERT INTO register (Nom, Prenom, Date_de_naissance, Lieu_de_naissance, Genre, Nom_pere, Nom_mere, Domicile, Nationalite, Photo) VALUES (?,?,?,?,?,?,?,?,?,?) """
                cursor.execute(commande, valeur)
                db.commit()
                QtWidgets.QMessageBox.information(self, "Succès", "Enregristrement effectué avec succès")
                self.nettoyer_data()
                self.data_()

    def modifier_data(self):
        ligne = self.tableWidget.currentRow()
        id_ligne = self.tableWidget.item(ligne, 0).text()
        db = sqlite3.connect(os.path.join(os.path.dirname("__file__"), "storage/database.db"))
        cursor = db.cursor()
        commande = """ SELECT * FROM register WHERE ID=? """
        resultat = cursor.execute(commande, (id_ligne,))
        valeur = resultat.fetchone()
        if valeur != None:
            date_string = valeur[3]
            date_list = [int(i) for i in re.findall(r"-?\d+\.?\d*", date_string)]
            self.nom_field.setText(str(valeur[1]).title())
            self.prenom_field.setText(str(valeur[2]).title())
            self.date_field.setDate(QtCore.QDate(date_list[2], date_list[1], date_list[0]))
            self.lieu_field.setText(str(valeur[4]).title())
            genre = str(valeur[5])
            self.domicile_field.setText(str(valeur[6]).title())
            self.nationalite_field.setText(str(valeur[7]).title())
            self.pere_field.setText(str(valeur[8]).title())
            self.mere_field.setText(str(valeur[9]).title())
            image = valeur[10]
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(image)

            self.photo.setPixmap(pixmap)
            if genre == "M":
                self.genre_h.setChecked(True)
                self.genre_f.setChecked(False)
            elif genre == "F":
                self.genre_h.setChecked(False)
                self.genre_f.setChecked(True)

    def supprimer_data(self):
        ligne = self.tableWidget.currentRow()
        id_ligne = self.tableWidget.item(ligne, 0).text()
        reponse = QtWidgets.QMessageBox.question(self, "Danger", "Voulez-vous vraiment supprimer ?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if reponse == 16384:
            db = sqlite3.connect(os.path.join(os.path.dirname("__file__"), "storage/database.db"))
            cursor = db.cursor()
            commande = """ DELETE FROM register WHERE ID=? """
            cursor.execute(commande, (id_ligne,))
            db.commit()
            self.data_()

    def recherche_data(self):
        recherche = self.recherche_edit.text()
        if recherche == "":
            self.data_()
        else:
            db = sqlite3.connect(os.path.join(os.path.dirname("__file__"), "storage/database.db"))
            cursor = db.cursor()
            recherche = recherche.upper()
            commande = """ SELECT * FROM register WHERE Nom LIKE ? OR Prenom LIKE ? OR Domicile LIKE ?"""
            resultat = cursor.execute(commande, (f"%{recherche}%", f"%{recherche}%", f"%{recherche}%"))
            self.tableWidget.setRowCount(0)

            for row_number, row_data in enumerate(resultat):
                self.tableWidget.insertRow(row_number)
                for colum_number, data in enumerate(row_data):
                    self.tableWidget.setItem(
                        row_number, colum_number, QtWidgets.QTableWidgetItem(str(data)))

    def filtrer_data(self):
        filtre = self.filtre_field.currentText()
        db = sqlite3.connect(os.path.join(os.path.dirname("__file__"), "storage/database.db"))
        cursor = db.cursor()
        if filtre == "Tout":
            self.data_()
        elif filtre == "Masculin (M)":
            filtre_ = "M"
            commande = """  SELECT * FROM register WHERE Genre=? """
            resultat = cursor.execute(commande, (filtre_,))
            self.tableWidget.setRowCount(0)
            for row_number, row_data in enumerate(resultat):
                self.tableWidget.insertRow(row_number)
                for colum_number, data in enumerate(row_data):
                    self.tableWidget.setItem(
                        row_number, colum_number, QtWidgets.QTableWidgetItem(str(data)))
        elif filtre == "Feminin (F)":
            filtre_ = "F"
            commande = """ SELECT * FROM register WHERE Genre=? """
            resultat = cursor.execute(commande, (filtre_,))
            self.tableWidget.setRowCount(0)
            for row_number, row_data in enumerate(resultat):
                self.tableWidget.insertRow(row_number)
                for colum_number, data in enumerate(row_data):
                    self.tableWidget.setItem(
                        row_number, colum_number, QtWidgets.QTableWidgetItem(str(data)))

    def nettoyer_data(self):
        self.nom_field.clear()
        self.prenom_field.clear()
        self.date_field.setDate(QtCore.QDate(1921, 1, 1))
        self.lieu_field.clear()
        self.genre_h.setChecked(True)
        self.genre_f.setChecked(False)
        self.nationalite_field.clear()
        self.domicile_field.clear()
        self.pere_field.clear()
        self.mere_field.clear()
        self.photo.setPixmap(QtGui.QPixmap(":/img/assets/photo.png"))
