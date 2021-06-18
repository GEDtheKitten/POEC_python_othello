from Othello_IHM import *
import pickle


class Plateau:

    # classe Plateau de jeu

    #           0 => case vide
    #           1 => pion noir
    #           2 => pion blanc

    #           0 -------Y------->
    #           | 0 0 0 0 0 0 0 0
    #           | 0 0 0 0 0 0 0 0
    #           | 0 0 0 0 0 0 0 0
    #           | 0 0 0 1 2 0 0 0
    #           X 0 0 0 2 1 0 0 0
    #           | 0 0 0 0 0 0 0 0
    #           | 0 0 0 0 0 0 0 0
    #           | 0 0 0 0 0 0 0 0

    # constructeur du plateau
    def __init__(self, taille=8):
        # initialisation de la structure du plateau
        self.plateau = [[0 for i in range(taille)] for i in range(taille)]
        # mise en place des pions de debut de partie
        self.plateau[3][3] = self.plateau[4][4] = 1
        self.plateau[3][4] = self.plateau[4][3] = 2
        # liste des directions possible - vertical / horizontal / diagonal - autour d une case
        #            [-1, -1]    [-1, 0]    [-1, 1]
        #            [ 0, -1]     case      [ 0, 1]
        #            [ 1, -1]    [ 1, 0]    [ 1, 1]
        self.liste_des_directions = [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]

    # affiche les valeurs du plateau sans la syntax des listes [ , , ] - debuggage
    def afficher_plateau(self):
        for ligne in range(len(self.plateau)):
            print('  '.join(map(str, self.plateau[ligne])))

    # renvoi la taille du plateau
    def taille_plateau(self):
        return(len(self.plateau))

    # setter
    def set_value(self, x, y, joueur):
        self.plateau[x][y] = 1 if joueur == 'black' else 2

    # getter
    def get_value(self, x, y):
        return self.plateau[x][y]

    def joueur_adverse_int(self, joueur):
        return 2 if joueur == 'black' else 1

    # test si les coordonnees x et y sont dans les limites du plateau
    def est_sur_le_plateau(self, x, y):
        return 0 <= x <= self.taille_plateau()-1 and 0 <= y <= self.taille_plateau()-1

    # recherche les pions a retouner et les retournes
    # les lignes ne se poursuive pas
    def rechercher_pion(self, x_depart, y_depart, joueur):
        joueur_int = 1 if joueur == 'black' else 2
        # pour chaque direction de la grille
        for dir_x, dir_y in self.liste_des_directions:
            x_arrive = x_depart + dir_x
            y_arrive = y_depart + dir_y
            pions_a_retourner = []
            # tand que l on ne sort pas du plateau et que l on rencontre des poins
            while self.est_sur_le_plateau(x_arrive, y_arrive) and self.plateau[x_arrive][y_arrive] != 0: 
                # si l on recontre un pion de la meme couleur pendant le parcour
                # on retourne les pions recontres sur le parcour
                if self.plateau[x_arrive][y_arrive] == joueur_int:
                    for x_pion, y_pion in pions_a_retourner:
                        self.plateau[x_pion][y_pion] = joueur_int
                    break
                pions_a_retourner.append([x_arrive, y_arrive])
                x_arrive += dir_x
                y_arrive += dir_y
                
    def verifier_si_saisie_valide(self, x_depart, y_depart, joueur):
        joueur_int = 1 if joueur == 'black' else 2
        # pour chaque direction de la grille
        for dir_x, dir_y in self.liste_des_directions:
            x_arrive = x_depart + dir_x
            y_arrive = y_depart + dir_y
            pions_a_retourner = []
            # tand que l on ne sort pas du plateau et que l on rencontre des poins
            while self.est_sur_le_plateau(x_arrive, y_arrive) and self.plateau[x_arrive][y_arrive] != 0: 
                # si l on recontre un pion de la meme couleur pendant le parcour
                # on retourne les pions recontres sur le parcour
                if self.plateau[x_arrive][y_arrive] == joueur_int:
                    for x_pion, y_pion in pions_a_retourner:
                        self.plateau[x_pion][y_pion] = joueur_int
                    break
                pions_a_retourner.append([x_arrive, y_arrive])
                x_arrive += dir_x
                y_arrive += dir_y

    def verifier_si_saisie_valide(self, xc, yc, joueur):
        # x et y compris entre 0 et 7 inclus (nb : contrainte via interface)
        # vérifie la présence d au moins un pion autour des coordonnées saisies
        # any(iterable)
        #   Renvoie True si au moins un élément de iterable est vrai.
        #   False est renvoyé dans le cas où iterable est vide.
        return any(
            # 0 <= (xc + dir_x) <= self.taille_plateau()-1
            # and 0 <= (yc + dir_y) <= self.taille_plateau()-1
            self.est_sur_le_plateau(xc + dir_x, yc + dir_y)
            and self.plateau[xc + dir_x][yc + dir_y] != 0
            and self.plateau[xc + dir_x][yc + dir_y] != joueur
            and self.plateau[xc][yc] == 0
            for dir_x, dir_y in self.liste_des_directions
        )

    # compter le score d'une couleur
    def recuperer_score(self, color):
        score = 0
        # compte les pions de couleur 'color'
        for i in range(self.taille_plateau()):
            for j in range(len(self.plateau[i])):
                if self.plateau[i][j] == color:
                    score += 1
        return score


# Classe principale du jeu
class Othello:
    def __init__(self):
        self.ihm = Othello_IHM(self)  # on passe l'instance de Othello en arg

        self.ihm.dessiner_grille()

        # instancie et initialise tab(i,j) de la classe Tab correspondant à 4 jetons
        self.tab = Plateau()

        self.ihm.dessiner_jeu()  # version actuelle

        # initialisation du radio_bouton
        self.ihm.radio_value.set(1)

        # initialisation du score
        self.ihm.score_noir.set(" : " + str(2))
        self.ihm.score_blnc.set(" : " + str(2))

        # initialisation du joueur - joueur 'black' ou 'white' -  les 'black' commencent
        self.joueur = 'black'

    # initialise une partie
    def nouveau(self):
        # effacement du jeu
        self.tab = Plateau()
        self.ihm.reset_jeu()

    def set_joueur(self, joueur):
        self.joueur = joueur

    def get_joueur(self):
        return self.joueur        

    # sauvegerde une partie dans un fichier binaire
    def sauver(self):
        print("Sauvegarde de la partie.")
        fich = self.ihm.select_enregistrer_fichier()
        if fich == '':
            fich = 'plateau.pkl'
        print('TEST sauver :' + fich)
        with open(fich, 'wb') as output:
            pickle.dump(self.tab, output, pickle.HIGHEST_PROTOCOL)

    # charge une partie sauvee dans le fichier sauvegarde_partie
    def charger(self):
        print("Chargement de la partie.")
        fich = self.ihm.select_ouvrir_fichier()
        if fich == '':
            return
        print('TEST charger :' + fich)
        with open(fich, 'rb') as input:
            # with open('sauvegarde_partie/plateau.pkl', 'rb') as input:
            self.tab = pickle.load(input)
        self.ihm.dessiner_jeu()

    # quitte la partie en sauvegardant la partie en cour
    def quitter(self):
        # self.sauver()
        self.ihm.fen.destroy()


# Programme principal

# Creation de l'objet principal le jeu Othello
oth = Othello()

# Boucle infinie pour ecouter les evenements
oth.ihm.fen.mainloop()
