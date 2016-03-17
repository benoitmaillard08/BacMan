"""Gestion de la base de données du jeu >BacMan the baccalaureates Adventure!<"""

import sqlite3
import constantes

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
                playerID INT PRIMARY KEY AUTO_INCREMENT,
                pseudo VARCHAR(16) NOT NULL,
                password VARCHAR(16) NOT NULL)
                """)
            self.cur.execute("""CREATE TABLE Scores (
                scoreID INT PRIMARY KEY AUTO_INCREMENT,
                pseudo VARCHAR(16) NOT NULL,
                score INT,
                date DATE AUTO_INCREMENT)
                """)
        except:
            break # Rien n'est fait, vu que les tables ont déjà été créées.
        else:
            self.conn.commit()  #Les nouvelles tables sont enregistrées


    def newPlayer(self, pseudo, mdp):
        """
        newPlayer(str pseudo, str mdp) --> None.
        Permet d'enregistrer un nouveau joueur dans la base de données.
        """
        self.cur.execute("INSERT INTO Players(pseudo, password) VALUES (''"+ str(pseudo) + "'',''" + str(mdp) + "'');")
        self.conn.commit()
        

    def testPlayer(self, pseudo, mdp):
        """
        testPlayer(str pseudo, str mdp) --> int.
        Permet de tester si le joueur est bien enregistré, et si le mot de passe correspond. La méthode retourne les entiers suivants:
        - Joueur enregistré et bon MdP : 0
        - Joueur enregistré mais mauvais MdP : 1
        - Joueur non-enregistré : 2
        """
        pass

    def newScore(self, pseudo, score):
        """
        newScore(str pseudo, int score) --> None.
        Permet d'entrer un nouveau score dans la table des scores, avec une auto-implémentation de la date.
        """
        pass

    def getScores(self, pseudo=None):
        """
        mewScore(str pseudo) --> list.
        Permet d'obtenir la liste des 5 meilleurs scores, soit de tous les joueurs, soit du joueur <pseudo>.
        La méthode retourne une liste de tuple, contenant le pseudo, le score et la date des records.
        """
        pass


##### MAIN #####

Database()