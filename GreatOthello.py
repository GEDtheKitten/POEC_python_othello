from tkinter import *

# TODO :
# ici importer la classe Tab  de Gerard ( pour utiliser tab(i,j) )
# importer d'autres classes ? Classe algo ?

class plateau :

    # classe plateau de jeu  
    # 0 => case vide 
    # 1 => pion noir
    # 2 => pion blanc 

    # constructeur du plateau
    def __init__(self, taille=8):
        self.plateau = [[0 for i in range(taille)] for i in range(taille)]
    
    # affiche les valeurs du plateau sans la syntax des listes [ , , ]
    def afficher_plateau(self):
        for ligne in range(len(self.plateau)):
            print('  '.join(map(str, self.plateau[ligne]))) 

    # renvoi le nombre de lignes du plateau
    def nombre_ligne(self):
        return(len(self.plateau))

    #setter
    def set_value(self, i,j, value):
        self.plateau[i][j] = value


    # paramètre 'color' --> 0 : pas de pion, 1 : noir, 2 : blanc

    def retourner_pions (self, xInitial, yInitial, xc, yc, color):
        for i in range(xInitial, xc):
            for j in range(yInitial, yc):
                self.plateau[i, j] = color
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
            print("i = ", i, " j = ", j, " x = ", xc, " y = ", yc)
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
        print(self.plateau[xInitial][yInitial])
        print(xInitial)
        print(yInitial)
        print(self.plateau[4][4])


    # vérifie la présence d'un autre pion à côté du pion placé
    def verifier_si_saisie_valide (self, xc,yc):
        # return True or False
        # x et y compris entre 0 et 7 inclus (nb : contrainte via interface)
        # ne doit pas écraser un pion déjà saisi

        tabSens = [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]
        print("abcisse initiale : ", xc)
        print("ordonnée initiale : ", yc)

        for i, j in tabSens:
            # print("abcisse initiale : ", xc)
            print(xc+i)
            # print("ordonnée initiale : ", yc)
            print(yc+j)
            if 0 <= (xc+i) <= 7 and 0 <= (yc+j) <= 7:
                if self.plateau[xc+i][yc+j] != 0 and self.plateau[xc][yc] == 0:
                    # vérifie la présence d au moins un pion autour des coordonnées saisies
                    return True
        return False

    # compter le score d'une couleur
    def recuperer_score (self, color):
        score = 0
        # compte les pions de couleur 'color'
        for i in self.nombre_ligne():
            for j in len(self.plateau[i]):
                if self.plateau[i][j] == color:
                    score += 1
        return score



class Othello:
    def __init__(self, fen):
        # Création d'un canvas pour dessiner
        self.cnv = Canvas(fen, width = Largeur, height = Hauteur, bg = 'bisque')
        self.cnv.pack(padx = 5, pady = 5)
    
    def dessiner_grille(self):
        gr = [0, 50, 100, 150, 200, 250, 300, 350, 400]
        for xi in gr:
            self.cnv.create_line(xi, 0, xi, 400)
        for yi in gr:
            self.cnv.create_line(0, yi, 400, yi)
    
    def dessiner_jeton(self,x, y, color):
        r = 20
        self.cnv.create_oval(x-r, y-r, x+r, y+r, outline = 'black', fill = color)

    #def dessiner_jeu(self, tab): version definitive
    def dessiner_jeu(self): # version actuelle
        self.dessiner_jeton(175, 175, 'white') # les coordonnées seront remplacées
        self.dessiner_jeton(225, 225, 'white') # par la lecture de tab(i,j)
        self.dessiner_jeton(175, 225, 'black')
        self.dessiner_jeton(225, 175, 'black')

    def init_jeu(self):
        self.dessiner_grille()
        # TODO :
        # instancier et initialiser tab(i,j) de la classe Tab correspondant à 4 jetons
        # self.dessiner_jeu(tab)  # version definitive
        self.dessiner_jeu()   # version actuelle
    
    def nouveau(self):
        # effacement du jeu
        # TODO : réinitialiser le tableau tab(i,j)
        self.cnv.delete(ALL)
        self.init_jeu()
    
    def clic(self, plateau, event):
        # c'est ici que l'on ajoute des jetons en cliquant,
        # que tab(i,j) se met à jour et que les algos de validité et de retournement
        # se mettent en action...

        # on récupère les coordonnées (x,y) sur l'évènement "clic"
        x = event.x
        y = event.y

        # astuce de division entière ( ou // en python) pour positionner
        # le jeton sur la case cliquée
        xc = int(x/50)*50 + 25
        yc = int(y/50)*50 + 25

        # TODO : vérifier la validité du positionnement d'un jeton (xc, yc)
        if plateau.verifier_si_saisie_valide(plateau, xc, yc) == False :
            # variable Plateau ? A PRECISER ------------------------------------------------------------
            return

        if radioValue.get() == 1:
            color = 'black'
            radioValue.set(2)   # on alterne les couleurs à chaque clic...
        else:
            color = 'white'     
            radioValue.set(1)   # ...pour le tour suivant (noir, blanc, noir...)     
        
        self.dessiner_jeton(xc, yc, color)
        # TODO :
        # Tab.update(xc, yc)
        # algo de recherche des lignes à retourner
        # Tab.rechercherPion (xc, yc, plateau, xo)

        # mise à jour de tab(i,j)
        # def recupererScore (xo, plateau)
        # mise à jour graphique ==> self.dessiner_jeu(tab)
        
    def sauver(self):
        print("On sauve la partie")
        # TODO
        # copier le tableau : def sauvegarderPlateau (plateau)
        # 1 fichier, 1 partie (GG)
    
    def charger(self):
        print("On charge la partie")
        # TODO
        # mettre à jour le tableau tab(i,j)
        #self.dessiner_jeu(tab)   # version definitive
        self.dessiner_jeu()  # version actuelle



# Programme principal
# En principe il n'y a rien à ajouter dans le programme principal
# à part un afficheur de score : controle de type label


# Creation de la fenetre
fen = Tk()
fen.title('Othello')

# Largeur hauteur fenetre
Largeur = 400
Hauteur = 400

# Creation de l'objet principal le jeu Othello
oth = Othello(fen)

# Reflexe : appel de la methode clic qd on clique sur canvas avec bouton gauche
# Attention : pour cliquer sur un bouton c'est différent (voir plus bas)
# ici on clique SUR LE CANVAS ET NON SUR UN BOUTON
oth.cnv.bind("<Button-1>", oth.clic)

# initialisation du jeu
oth.init_jeu()


# ATTENTION : les controles Tkinter utilisent des variables globales
radioValue = IntVar() # radioValue est globale (objet de type IntVar)

radioValue.set(1) # on lui affecte la valeur 1 pour initialiser le controle coché

# Création du controle RadioButton avec deux possibilités
rdio_noir = Radiobutton(fen, text = 'NOIR', variable = radioValue, value = 1).pack(anchor = W)
rdio_blnc = Radiobutton(fen, text = 'BLANC', variable = radioValue, value = 2).pack(anchor = W)

# Création des boutons
# la méthode appelée est définie par "command = "  (nouveau)
btn_nouveau = Button(fen, text = 'Nouveau', command = oth.nouveau)
btn_nouveau.pack(side = LEFT, padx = 5, pady = 5)

btn_sauver = Button(fen, text = 'Sauver', command = oth.sauver)
btn_sauver.pack(side = LEFT, padx = 5, pady = 5)

btn_charger = Button(fen, text = 'Charger', command = oth.charger)
btn_charger.pack(side = LEFT, padx = 5, pady = 5)

btn_quit = Button(fen, text = 'Quitter', command = fen.destroy)
btn_quit.pack(side = LEFT, padx = 5, pady = 5)
# si oth.quitter : oth.sauver + fen.destroy

# Boucle infinie pour ecouter les evenements
fen.mainloop()

