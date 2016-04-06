"""Gestion de la base de données du jeu >BacMan the baccalaureates Adventure!<"""

import sqlite3
import constantes
import time

class Database:
    "Classe gérant les entrées et sorties de la base de données du jeu"

    def __init__(self):
        """
        __init__() --> None.
        Instanciation de la base de données du jeu <PacMan>.
        """
        self.conn = sqlite3.connect(constantes.DATABASE) #Création/connexion à la base de données <constantes.DATABASE>
        self.cur = self.conn.cursor()

        try:    #Test de création des tables Players et Scores, pour éviter l'erreur si le programme a déjà été lancé une fois.
            self.cur.execute("""CREATE TABLE Players (      
                playerID INTEGER PRIMARY KEY AUTOINCREMENT,
                pseudo VARCHAR(16) NOT NULL,
                password VARCHAR(16) NOT NULL,
                nom VARCHAR(16) NOT NULL,
                prenom VARCHAR(16) NOT NULL)
                """)
            self.cur.execute("""CREATE TABLE Scores (
                scoreID INTEGER PRIMARY KEY AUTOINCREMENT,
                pseudo VARCHAR(16) NOT NULL,
                score INTEGER,
                level INTEGER,
                datetime DATETIME)
                """)
        except:
            pass # Rien n'est fait, vu que les tables ont déjà été créées.
        else:
            self.conn.commit()  #Les nouvelles tables sont enregistrées


    def newPlayer(self, pseudo, mdp, nom, prenom):
        """
        newPlayer(str pseudo, str mdp) --> None.
        Permet d'enregistrer un nouveau joueur dans la base de données.
        """
        self.cur.execute("INSERT INTO Players(pseudo, password, nom, prenom) VALUES (?,?,?,?);", (pseudo, mdp, nom, prenom))
        self.conn.commit()
        

    def testPlayer(self, pseudo, mdp=''):
        """
        testPlayer(str pseudo, str mdp) --> int.
        Permet de tester si le joueur est bien enregistré, et si le mot de passe correspond. La méthode retourne les entiers suivants:
        - Joueur enregistré et bon MdP : 0
        - Joueur enregistré mais mauvais MdP : 1
        - Joueur non-enregistré : 2
        """
        self.cur.execute("SELECT * FROM Players")
        players_list = self.cur.fetchall() #Tous les joueurs enregistrés sont regroupés dans cette liste, sous forme de tuples
        flag = 2 #Le flag est défini comme si le joueur n'était pas encore enregistré
        for elt in players_list:
            if elt[1] == pseudo and elt[2] == mdp:
                flag = 0    #Le joueur est déjà enregistré et le mdp correspond
            elif elt[1] == pseudo and elt[2] != mdp:
                flag = 1
                
        return flag

    def newScore(self, pseudo, score, level):
        """
        newScore(str pseudo, int score) --> None.
        Permet d'entrer un nouveau score dans la table des scores, avec une auto-implémentation de la date.
        """
        self.cur.execute("INSERT INTO Scores(pseudo, score, level, datetime) VALUES (?, ?, ?, ?);", (pseudo, score, level, time.strftime("%Y-%m-%d")))
        self.conn.commit()

    def getScores(self, pseudo=None):
        """
        mewScore(str pseudo) --> list.
        Permet d'obtenir la liste des 5 meilleurs scores, soit de tous les joueurs ('*'), soit du joueur <pseudo>.
        La méthode retourne une liste de tuple, contenant le pseudo, le score et la date des records.
        """
        if pseudo:
            self.cur.execute("SELECT pseudo, score, level, datetime FROM Scores WHERE pseudo = '{}' ORDER BY score DESC".format(pseudo))
        else:
            self.cur.execute("SELECT pseudo, score, level, datetime FROM Scores ORDER BY score DESC")
            
        scores_list = self.cur.fetchall()
        while len(scores_list) > 5:
            del scores_list[-1]
        
        return scores_list

    def close(self):
        """
        close() --> None
        Ferme la connexion à la base de données
        """
        self.cur.close()
        self.conn.close()