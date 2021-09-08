import sqlite3
import re
import os
import shutil
from pathlib import Path
from storage import utils
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.uic import loadUiType
from widgets.carteWidget import MainCarte
from ui.formulaire import Ui_MainWindow

# FORM_CLASS, _ = loadUiType(os.path.join(os.path.dirname("__file__"), "ui/formulaire.ui"))
FORM_CLASS = Ui_MainWindow

photo = {1 : ""}
class MainWindow(QtWidgets.QMainWindow, FORM_CLASS):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        QtWidgets.QMainWindow.__init__(self)
        self.donnee = utils.DataConfig()
        self.setupUi(self)
        self.setFixedSize(1299, 684)
        self.gestion_de_repertoire()
        self.data_()
        self.bouton()

    def gestion_de_repertoire(self):
        chemin = os.path.join(Path(__file__).resolve().parent.parent, "resource")
        if os.path.exists(chemin) == False:
            os.mkdir(chemin)

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

    def choisir_photo(self):
        nom_photo = QtWidgets.QFileDialog.getOpenFileName(self, "Choisir une photo", "c://", "images (*.png *.jpg *.jpeg *.gif)")
        photo[1] = nom_photo[0]
        self.photo.setPixmap(QtGui.QPixmap(photo[1]))
        self.photo.setScaledContents(True)

    def apercu_data(self):
        ligne = self.tableWidget.currentRow()
        if ligne == -1:
            QtWidgets.QMessageBox.warning(self, "Erreur", "Veuillez selectionner une personne s'il vous plaît !")
        else :
            id_ligne = self.tableWidget.item(ligne, 0).text()
            self.lancer_piece(id_ligne)

    def data_(self):
        resultat = self.donnee.recupereData()
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(resultat):
            self.tableWidget.insertRow(row_number)
            for colum_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, colum_number, QtWidgets.QTableWidgetItem(str(data)))

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
            valeurs = self.donnee.verifieData(nom, prenom)
            chemin = os.path.join(Path(__file__).resolve().parent.parent, "resource")
            if valeurs != None:
                valeur = (nom, prenom, date, lieu, genre, pere_field, mere_field, domicile, nationalite, photo[1], int(valeurs[0]))
                self.donnee.modifieData(valeur)
                QtWidgets.QMessageBox.information(self, "Succès", "Modification effectué avec succès")
                self.nettoyer_data()
                self.data_()
            else:
                chemin_photo = shutil.copy(photo[1], chemin)
                valeur = (nom, prenom, date, lieu, genre, pere_field, mere_field, domicile, nationalite, chemin_photo)
                self.donnee.ajoutData(valeur)
                QtWidgets.QMessageBox.information(self, "Succès", "Enregristrement effectué avec succès")
                self.nettoyer_data()
                self.data_()

    def modifier_data(self):
        ligne = self.tableWidget.currentRow()
        if ligne == -1:
            QtWidgets.QMessageBox.warning(self, "Erreur", "Veuillez selectionner une personne s'il vous plaît !")
        else:
            id_ligne = self.tableWidget.item(ligne, 0).text()
            valeur = self.donnee.recupereID(id_ligne)
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
                photo[1] = valeur[10]
                self.photo.setPixmap(QtGui.QPixmap(photo[1]))
                if genre == "M":
                    self.genre_h.setChecked(True)
                    self.genre_f.setChecked(False)
                elif genre == "F":
                    self.genre_h.setChecked(False)
                    self.genre_f.setChecked(True)

    def supprimer_data(self):
        ligne = self.tableWidget.currentRow()
        if ligne == -1:
            QtWidgets.QMessageBox.warning(self, "Erreur", "Veuillez selectionner une personne s'il vous plaît !")
        else:
            id_ligne = self.tableWidget.item(ligne, 0).text()
            reponse = QtWidgets.QMessageBox.question(self, "Danger", "Voulez-vous vraiment supprimer ?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if reponse == 16384:
                chemin_photo = self.donnee.supprimeData(id_ligne)
                os.remove(chemin_photo)
                self.data_()
                self.nettoyer_data()

    def recherche_data(self):
        recherche = self.recherche_edit.text()
        if recherche == "":
            self.data_()
        else:
            recherche = recherche.upper()
            resultat = self.donnee.rechercheData(recherche)
            self.tableWidget.setRowCount(0)

            for row_number, row_data in enumerate(resultat):
                self.tableWidget.insertRow(row_number)
                for colum_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, colum_number, QtWidgets.QTableWidgetItem(str(data)))

    def filtrer_data(self):
        filtre = self.filtre_field.currentText()
        if filtre == "Tout":
            self.data_()
        elif filtre == "Masculin (M)":
            filtre_ = "M"
            resultat = self.donnee.filtreData(filtre_)
            self.tableWidget.setRowCount(0)
            for row_number, row_data in enumerate(resultat):
                self.tableWidget.insertRow(row_number)
                for colum_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, colum_number, QtWidgets.QTableWidgetItem(str(data)))
        elif filtre == "Feminin (F)":
            filtre_ = "F"
            resultat = self.donnee.filtreData(filtre_)
            self.tableWidget.setRowCount(0)
            for row_number, row_data in enumerate(resultat):
                self.tableWidget.insertRow(row_number)
                for colum_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, colum_number, QtWidgets.QTableWidgetItem(str(data)))

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

