from Othello_IHM import *

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

    # renvoi le nombre de lignes du plateau
    def nombre_ligne(self):
        return(len(self.plateau))

    #setter
    def set_value(self, i, j, value):
        self.plateau[i][j] = value

    #getter
    def get_value(self, i, j):
        return self.plateau[i][j]

    def retourner_pions (self, xInitial, yInitial, xc, yc, color):
        for i in range(xInitial, xc):
            for j in range(yInitial, yc):
                self.plateau[i][j] = color
                i -= 1
                j -= 1

    # recherche le pion de couleur + retourner les pions entre le pion posé et le pion de même couleur le plus proche
    def rechercher_pion(self, xc, yc, color):
        tabSens = [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]

        xInitial = xc
        yInitial = yc

        # recherche le pion de couleur 'color' le plus proche dans chaque direction
        for i, j in tabSens:
            xc += i
            yc += j
            while 0 <= xc <= 7 and 0 <= yc <= 7:
                if self.plateau[xc][yc] == color:
                    # on a repéré le pion [xc,yc] le plus proche dans cette direction
                    # on transforme les points entre le point [xInitial, yInitial] et le point repéré [xc, yc]
                    self.retourner_pions(xInitial, yInitial, xc, yc, color)
                    xc += i
                    yc += j
                # vérifie la présence d'une case vide
                elif self.plateau[xc][yc] == 0:
                    break
                else:
                    break
        '''
        print(self.plateau[xInitial][yInitial])
        print(xInitial)
        print(yInitial)
        print(self.plateau[4][4])
        '''

    # vérifie la présence d'un autre pion à côté du pion placé
    def verifier_si_saisie_valide (self, xc,yc):
        # return True or False
        # x et y compris entre 0 et 7 inclus (nb : contrainte via interface)

        tabSens = [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]
        
        for i, j in tabSens:
            if 0 <= (xc + i) <= 7 and 0 <= (yc + j) <= 7:
                if self.plateau[xc + i][yc + j] != 0 and self.plateau[xc][yc] == 0:
                    # vérifie la présence d au moins un pion autour des coordonnées saisies
                    return True
        return False

    # compter le score d'une couleur
    def recuperer_score (self, color):
        score = 0
        # compte les pions de couleur 'color'
        #for i in self.nombre_ligne():
        for i in range(self.nombre_ligne()):
            #for j in len(self.plateau[i]):
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

    def nouveau(self):
        # effacement du jeu
        self.tab = Plateau()
        self.ihm.reset_jeu()

    def sauver(self):
        print("Sauvegarde de la partie.")
        # TODO -------------------------------------------------------------------
        # copier le tableau : def sauvegarderPlateau (plateau)
        # 1 fichier, 1 partie (GG)

    def charger(self):
        print("Chargement de la partie.")
        # TODO -------------------------------------------------------------------
        # lecture tableau depuis fichier
        # self.tab = tableau qui vient d'être lu ---------------------------------
        self.ihm.dessiner_jeu()  # version actuelle

    def quitter(self):
        self.sauver()
        self.ihm.fen.destroy()


# Programme principal

# Creation de l'objet principal le jeu Othello
oth = Othello()

# Boucle infinie pour ecouter les evenements
oth.ihm.fen.mainloop()
