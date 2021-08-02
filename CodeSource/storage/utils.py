import sqlite3
import os

class DataConfig:
    def __init__(self):
        self.db = sqlite3.connect(os.path.join(os.path.dirname("__file__"), "database.db"))
        self.cursor = self.db.cursor()
    
    def recupereID(self, id):
        commande = """ SELECT * FROM register WHERE ID=? """
        resultat = self.cursor.execute(commande, (id,))
        valeur = resultat.fetchone()
        return valeur

    def recupereData(self):
        commande = """ SELECT * from register """
        resultat = self.cursor.execute(commande)
        return resultat

    def ajoutData(self, valeur):
        commande = """ UPDATE register SET Nom=?, Prenom=?, Date_de_naissance=?, Lieu_de_naissance=?, Genre=?, Nom_pere=?, Nom_mere=?, Domicile=?, Nationalite=?, Photo=? WHERE ID=? """
        self.cursor.execute(commande, valeur)
        self.db.commit()

    def modifieData(self, valeur):
        commande = """ INSERT INTO register (Nom, Prenom, Date_de_naissance, Lieu_de_naissance, Genre, Nom_pere, Nom_mere, Domicile, Nationalite, Photo) VALUES (?,?,?,?,?,?,?,?,?,?) """
        self.cursor.execute(commande, valeur)
        self.db.commit()

    def supprimeData(self, id):
        commande = """ DELETE FROM register WHERE ID=? """
        self.cursor.execute(commande, (id,))
        self.db.commit()

    def rechercheData(self, recherche):
        commande = """ SELECT * FROM register WHERE Nom LIKE ? OR Prenom LIKE ? OR Domicile LIKE ?"""
        resultat = self.cursor.execute(commande, (f"%{recherche}%", f"%{recherche}%", f"%{recherche}%"))
        return resultat

    def filtreData(self, filtre):
        commande = """  SELECT * FROM register WHERE Genre=? """
        resultat = self.cursor.execute(commande, (filtre,))
        return resultat
    
    def verifieData(self, nom, prenom):
        commande = """ SELECT * from register WHERE Nom=? AND Prenom=? """
        resultat = self.cursor.execute(commande, (nom, prenom))
        valeur = resultat.fetchone()
        return valeur
