from Othello_IHM import *
import os
import pickle

class Plateau:

    # classe Plateau de jeu
    # 0 => case vide 
    # 1 => pion noir
    # 2 => pion blanc 

    # constructeur du plateau
    def __init__(self, taille=8):
        self.plateau = [[0 for i in range(taille)] for i in range(taille)]
        self.plateau[3][3] = 1
        self.plateau[4][4] = 1
        self.plateau[3][4] = 2
        self.plateau[4][3] = 2

    # affiche les valeurs du plateau sans la syntax des listes [ , , ]
    def afficher_plateau(self):
        for ligne in range(len(self.plateau)):
            print('  '.join(map(str, self.plateau[ligne]))) 

    # renvoi la taille du plateau
    def taille_plateau(self):
        return(len(self.plateau))

    #setter
    def set_value(self, i, j, value):
        self.plateau[i][j] = value

    #getter
    def get_value(self, i, j):
        return self.plateau[i][j]

    def est_sur_le_plateau(self, x_arrive, y_arrive):
        return 0 <= x_arrive <= self.taille_plateau()-1 and 0 <= y_arrive <= self.taille_plateau()-1


#       1 => pion noir
#       2 => pion blanc 

#           0 -------Y------->
#           | 0 0 0 0 0 0 0 0
#           | 0 0 0 0 0 0 0 0
#           | 0 0 0 0 0 0 0 0
#           | 0 0 0 1 2 0 0 0
#           X 0 0 0 2 1 0 0 0
#           | 0 0 0 0 0 0 0 0
#           | 0 0 0 0 0 0 0 0
#           | 0 0 0 0 0 0 0 0

    def rechercher_pion(self, x_depart, y_depart, color):
        tabSens = [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]
        for dir_x, dir_y in tabSens:
            x_arrive = x_depart
            y_arrive = y_depart
            nb_pions_a_retourner = []
            while self.est_sur_le_plateau(x_arrive, y_arrive) and self.plateau[x_arrive][y_arrive] != 0:
                nb_pions_a_retourner.append([x_arrive, y_arrive])
                if self.plateau[x_arrive][y_arrive] == color:
                    for x_pion, y_pion in nb_pions_a_retourner:
                        self.plateau[x_pion][y_pion] = color
                x_arrive += dir_x
                y_arrive += dir_y

    # vérifie la présence d'un autre pion à côté du pion placé
    def verifier_si_saisie_valide(self, xc,yc):
        # return True or False
        # x et y compris entre 0 et 7 inclus (nb : contrainte via interface)
        tabSens = [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]
        # vérifie la présence d au moins un pion autour des coordonnées saisies
        # any(iterable)
        #   Renvoie True si au moins un élément de iterable est vrai. 
        #   False est renvoyé dans le cas où iterable est vide.
        return any(
            0 <= (xc + i) <= 7
            and 0 <= (yc + j) <= 7
            and self.plateau[xc + i][yc + j] != 0
            and self.plateau[xc][yc] == 0
            for i, j in tabSens
        )

    # compter le score d'une couleur
    def recuperer_score (self, color):
        score = 0
        # compte les pions de couleur 'color'
        #for i in self.taille_plateau():
        for i in range(self.taille_plateau()):
            #for j in len(self.plateau[i]):
            for j in range(len(self.plateau[i])):
                if self.plateau[i][j] == color:
                    score += 1
        return score

    # enregistre l'objet plateau dans un fichier binaire
    def sauver_plateau(self):
        os.makedirs('sauvegarde_partie', exist_ok=True)
        with open('sauvegarde_partie/plateau.pkl', 'wb') as output:
            pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)



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

    def nouveau(self):
        # effacement du jeu
        self.tab = Plateau()
        self.ihm.reset_jeu()

    def sauver(self):
        self.tab.sauver_plateau()
        print("Sauvegarde de la partie.")
        # TODO -------------------------------------------------------------------
        # copier le tableau : def sauvegarderPlateau (plateau)
        # 1 fichier, 1 partie (GG)

    def charger(self):
        print("Chargement de la partie.")
        with open('sauvegarde_partie/plateau.pkl', 'rb') as input:
            self.tab = pickle.load(input)
        self.ihm.dessiner_jeu()  # version actuelle

    def quitter(self):
        self.sauver()
        self.ihm.fen.destroy()


# Programme principal

# Creation de l'objet principal le jeu Othello
oth = Othello()

# Boucle infinie pour ecouter les evenements
oth.ihm.fen.mainloop()
