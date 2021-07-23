import os
import sys
import sqlite3
from PyQt5 import QtWidgets, QtGui
from PyQt5.uic import loadUiType
from widgets.carteInterface import Ui_Dialog


# FORM_CLASS,_ = loadUiType(os.path.join(os.path.dirname("__file__"), "ui/carte.ui"))
FORM_CLASS = Ui_Dialog

class MainCarte(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, id_element):
        super().__init__()
        self.id_element = id_element
        self.setupUi(self)
        self.datas_()
        self.capture_btn.clicked.connect(self.capture)

    def capture(self):
        img,_ = QtWidgets.QFileDialog.getSaveFileName(self, "Enregistrer sous", filter="PNG(*.png);; JPEG(*.jpg)")
        if sys.platform == "darwin":
            if img[-3:] == "png":
                screen = QtWidgets.QApplication.primaryScreen()
                screenshot = screen.grabWindow(40, 30, 501, 301)
                screenshot.save(img, 'png')
            elif img[-3:] == "jpg":
                screen = QtWidgets.QApplication.primaryScreen()
                screenshot = screen.grabWindow(40, 30, 501, 301)
                screenshot.save(img, 'jpg')
        else:
            if img[-3:] == "png":
                screen = QtWidgets.QApplication.primaryScreen()
                screenshot = screen.grabWindow(self.frame.winId())
                screenshot.save(img, 'png')
            elif img[-3:] == "jpg":
                screen = QtWidgets.QApplication.primaryScreen()
                screenshot = screen.grabWindow(self.frame.winId())
                screenshot.save(img, 'jpg')
        QtWidgets.QMessageBox.information(self, "Succès", "Capture enregistrer avec succès.")
        self.close()

    def datas_(self):
        db = sqlite3.connect(os.path.join(os.path.dirname("__file__"), "storage/database.db"))
        cursor = db.cursor()
        commande = """ SELECT * FROM register WHERE ID=? """
        resultat = cursor.execute(commande, (self.id_element,))
        valeur = resultat.fetchone()
        if valeur != None:
            self.id_field.setText(str(valeur[0]))
            self.nom_field.setText(str(valeur[1]))
            self.prenom_field.setText(str(valeur[2]))
            self.date_field.setText(str(valeur[3]))
            self.lieu_field.setText(str(valeur[4]))
            self.sexe_field.setText(str(valeur[5]))
            self.domicile_field.setText(str(valeur[6]))
            self.nationalite_field.setText(str(valeur[7]))
            self.pere_field.setText(str(valeur[8]))
            self.mere_field.setText(str(valeur[9]))
            image = valeur[10]
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(image)
            self.photo.setPixmap(pixmap)


