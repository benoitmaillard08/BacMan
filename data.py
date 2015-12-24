"""Gestion de la base de données du jeu >BacMan the baccalaureates Adventure!<"""
import menus
import constantes



class Register:
    """
    Classe gérant l'enregistrement du joueur dans la base de données
    """
    def __init__(self, pseudo='test', password='test'):
        """
        __init__(str pseudo, str password, str data_dir) --> None.
        <data_dir> est le chemin vers la base de données (fichier txt).
        """
        self.pseudo = pseudo
        self.password = password

        self.file_read = open(constantes.PLAYERS_DATAS, 'r')
        datas = self.file_read.read().split()

        l = []
        for elt in datas:
            l.append(tuple(elt.split('%')))

        self.database = {} # Les données s'enregistrent dans un dictionnaire, tel que database[PSEUDO] --> PASSWORD

        for elt in l:
            self.database[elt[0]] = elt[1]

    def test_infos(self, onRegisterPage):
        """
        Méthode testant si le joueur est déjà enregistré et si le mot de passe est correct.
        """
        if self.pseudo not in self.database and onRegisterPage == True:
            self.file_read.close()
            Register.newPlayer(self)
            return 'NewRegistered'

        elif self.pseudo not in self.database and onRegisterPage == False:
            return 'NotRegistered'

        elif self.pseudo in self.database and self.database[self.pseudo] !=  self.password:
            if onRegisterPage == False:# Retourne une erreur "le mot de passe ne correspond pas au pseudo, réessayez ou choisissez un autre pseudo"
                return False
            else:
                return 'TakenPseudo'
        else:
            return 'Logged'


    def newPlayer(self):
        """
        Méthode enregistrant le nouveau joueur dans la base de données.
        """
        file_write = open(constantes.PLAYERS_DATAS, 'w')
        file_write.write('{}%{}\n'.format(self.pseudo, self.password))
        file_write.close()

class Scores:
    """
    Classe gérant l'enregistrement et la lecture des scores.
    """

    def __init__(self, pseudo, score, date):
        """
        __init__(str pseudo, int score) --> None.
        """
        self.pseudo = pseudo
        self.score = score
        self.date = date

        action = 'r' # 'r' pour la lecture et 'w' pour l'écriture.
        self.file = open(constantes.SCORES, action)

    def save(self):
        """
        Sauvegarde de nouveaux scores.
        """
        self.file.close() #Le fichier est fermé, pour être ensuite réouvert avec l'<action> désirée.

        action = 'w'
        self.file.write('{}%{}%{}\n'.format(self.pseudo, self.score, self.date))

    def get_scores(self):
        """
        Obtention des 3 meilleurs scores globaux ET du joueur.
        """
        self.file.close()

        action = 'r'
        datas = self.file.read().split()

        scores = []
        for elt in datas:
            scores.append(tuple(elt.split('%')))

        #On a une liste <scores>, composée de tuples, composés du pseudo, score et date d'une partie

        # Selection du meilleur score

        bestScore = ('',0,'')
        for elt in scores:
            if elt[1] > bestScore[1]:
                bestScore = elt
