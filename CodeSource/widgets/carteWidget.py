import os
import sys
from storage import utils
from PyQt5 import QtWidgets, QtGui
from PyQt5.uic import loadUiType
from ui.carte import Ui_Dialog


# FORM_CLASS,_ = loadUiType(os.path.join(os.path.dirname("__file__"), "ui/carte.ui"))
FORM_CLASS = Ui_Dialog

class MainCarte(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, id_element):
        super().__init__()
        self.id_element = id_element
        self.setupUi(self)
        self.donnee = utils.DataConfig()
        self.datas_()
        self.capture_btn.clicked.connect(self.capture)

    def capture(self):
        dimension = self.frame.frameGeometry()
        print(dimension)
        img,_ = QtWidgets.QFileDialog.getSaveFileName(self, "Enregistrer sous", filter="PNG(*.png);; JPEG(*.jpg)")
        if sys.platform == "darwin":
            screen = QtWidgets.QApplication.primaryScreen()
            screenshot = screen.grabWindow(dimension)
            if img[-3:] == "png":
                screenshot.save(img, 'png')
            elif img[-3:] == "jpg":
                screenshot.save(img, 'jpg')
        else:
            screen = QtWidgets.QApplication.primaryScreen()
            screenshot = screen.grabWindow(self.frame.winId())
            if img[-3:] == "png":
                screenshot.save(img, 'png')
            elif img[-3:] == "jpg":
                screenshot.save(img, 'jpg')
        QtWidgets.QMessageBox.information(self, "Succès", "Capture enregistrer avec succès.")
        self.close()

    def datas_(self):
        valeur = self.donnee.recupereID(self.id_element)
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


