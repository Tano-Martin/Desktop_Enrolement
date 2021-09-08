import sqlite3
import os

class DataConfig:
    def __init__(self):
        self.db = sqlite3.connect(os.path.join(os.path.dirname("__file__"), "baseDeDonnee.db"))
        self.cursor = self.db.cursor()
    
    def recupereID(self, id):
        commande = """ SELECT * FROM enrolement WHERE ID=? """
        resultat = self.cursor.execute(commande, (id,))
        valeur = resultat.fetchone()
        return valeur

    def recupereData(self):
        commande = """ SELECT * from enrolement """
        resultat = self.cursor.execute(commande)
        return resultat

    def modifieData(self, valeur):
        commande = """ UPDATE enrolement SET Nom=?, Prenom=?, Date_de_naissance=?, Lieu_de_naissance=?, Genre=?, Nom_pere=?, Nom_mere=?, Domicile=?, Nationalite=?, Photo=? WHERE ID=? """
        self.cursor.execute(commande, valeur)
        self.db.commit()

    def ajoutData(self, valeur):
        commande = """ INSERT INTO enrolement (Nom, Prenom, Date_de_naissance, Lieu_de_naissance, Genre, Nom_pere, Nom_mere, Domicile, Nationalite, Photo) VALUES (?,?,?,?,?,?,?,?,?,?) """
        self.cursor.execute(commande, valeur)
        self.db.commit()

    def supprimeData(self, id):
        commande = """ SELECT * from enrolement WHERE ID=? """
        resultat = self.cursor.execute(commande, (id,))
        valeur = resultat.fetchone()
        photo = valeur[10]
        
        command = """ DELETE FROM enrolement WHERE ID=? """
        self.cursor.execute(command, (id,))
        self.db.commit()

        return photo

    def rechercheData(self, recherche):
        commande = """ SELECT * FROM enrolement WHERE Nom LIKE ? OR Prenom LIKE ? OR Domicile LIKE ?"""
        resultat = self.cursor.execute(commande, (f"%{recherche}%", f"%{recherche}%", f"%{recherche}%"))
        return resultat

    def filtreData(self, filtre):
        commande = """  SELECT * FROM enrolement WHERE Genre=? """
        resultat = self.cursor.execute(commande, (filtre,))
        return resultat
    
    def verifieData(self, nom, prenom):
        commande = """ SELECT * from enrolement WHERE Nom=? AND Prenom=? """
        resultat = self.cursor.execute(commande, (nom, prenom))
        valeur = resultat.fetchone()
        return valeur
