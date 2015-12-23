"""Gestion de la base de données du jeu >BacMan the baccalaureates Adventure!<"""
import menus
import constantes



class Register:
    """
    Classe gérant l'enregistrement du joueur dans la base de données
    """
    def __init__(self, pseudo='test', password='test', data_dir=constantes.PLAYERS_DATAS):
        """
        __init__(str pseudo, str password, str data_dir) --> None.
        <data_dir> est le chemin vers la base de données (fichier txt).
        """
        self.pseudo = pseudo
        self.password = password
        self.data_dir = data_dir

        self.file_read = open(self.data_dir, 'r')
        datas = self.file_read.read().split()

        l = []
        for elt in datas:
            l.append(tuple(elt.split('%')))

        self.database = {} # Les données s'enregistrent dans un dictionnaire, tel que database[PSEUDO] --> PASSWORD

        for elt in l:
            self.database[elt[0]] = elt[1]

    def test_infos(self):
        """
        Méthode testant si le joueur est déjà enregistré et si le mot de passe est correct.
        """
        if self.pseudo not in self.database:
            self.file_read.close()
            Register.newPlayer(self)
            print(self.pseudo, self.password)
            return True

        elif self.pseudo in self.database and self.database[self.pseudo] !=  self.password:
            # Retourne une erreur "le mot de passe ne correspond pas au pseudo, réessayez ou choisissez un autre pseudo"
            return False
        else:
            # Redirection sur la page de login ou redirection directe sur la page de jeu, avec le login (?)
            return 'Logged'


    def newPlayer(self):
        """
        Méthode enregistrant le nouveau joueur dans la base de données.
        """
        file_write = open(self.data_dir, 'w')
        file_write.write('{}%{}\n'.format(self.pseudo, self.password))
        file_write.close()