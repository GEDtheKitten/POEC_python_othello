from tkinter import *


class Othello_IHM:
    def __init__(self, oth):
        self.cmpt_noir = 2
        self.cmpt_blnc = 2
        self.othello = oth

        # Creation de la fenetre
        self.fen = Tk()
        self.fen.title('Othello')

        # Création d'un canvas pour dessiner
        self.cnv = Canvas(self.fen, width=400, height=400, bg='green')
        self.cnv.pack(padx=5, pady=5)
        self.cnv.bind("<Button-1>", self.clic)

        # Frame pour les commandes
        fr = Frame(self.fen, bg='bisque')
        fr.pack(side=TOP, padx=5, pady=5)

        # Frame des radio_buttons et labels
        frt = Frame(self.fen, bg='blue')
        frt.pack(side=TOP, padx=5, pady=5)

        # Frame des boutons
        frb = Frame(self.fen, bg='blue')
        frb.pack(side=TOP, padx=5, pady=5)

        # Frame des radio_buttons et labels
        frl = Frame(frt)
        frl.pack(side=LEFT)
        frr = Frame(frt)
        frr.pack(side=RIGHT)

        # initialisation des variables pour les controle radio_button & label
        self.radio_value = IntVar()
        self.score_noir = StringVar()
        self.score_blnc = StringVar()

        # Labels pour afficher les scores
        lab_noir = Label(frl, textvariable=self.score_noir)
        lab_blnc = Label(frr, textvariable=self.score_blnc)

        # Création du controle RadioButton avec deux possibilités
        rdio_noir = Radiobutton(frl, text='NOIR',
                                variable=self.radio_value, value=1)

        rdio_blnc = Radiobutton(frr, text='BLANC',
                                variable=self.radio_value, value=2)

        # Agencement NOIR
        rdio_noir.pack(side=LEFT)
        lab_noir.pack(side=LEFT)

        # Agencement BLANC
        lab_blnc.pack(side=RIGHT)
        rdio_blnc.pack(side=RIGHT)

        # Création des boutons
        btn_nouveau = Button(frb, text='Nouveau', command=oth.nouveau)
        btn_nouveau.pack(side=LEFT, padx=5, pady=5)
        btn_sauver = Button(frb, text='Sauver', command=oth.sauver)
        btn_sauver.pack(side=LEFT, padx=5, pady=5)
        btn_charger = Button(frb, text='Charger', command=oth.charger)
        btn_charger.pack(side=LEFT, padx=5, pady=5)
        btn_quit = Button(frb, text='Quitter', command=oth.quitter)
        btn_quit.pack(side=LEFT, padx=5, pady=5)

    def convertirPixtoIndex(self, x):
        return (x-25)//50

    def convertirIndextoPix(self, i):
        return (i*50) + 25

    def dessiner_grille(self):
        gr = [0, 50, 100, 150, 200, 250, 300, 350, 400]
        for xi in gr:
            self.cnv.create_line(xi, 0, xi, 400)
        for yi in gr:
            self.cnv.create_line(0, yi, 400, yi)

    def dessiner_jeton(self, x, y, color):
        r = 20
        self.cnv.create_oval(x - r, y - r, x + r, y + r,
                             outline='black', fill=color)

 # Recupere les compteurs de noirs et de blancs  
    def dessiner_score(self):
        self.cmpt_noir = self.othello.tab.recuperer_score(1)
        self.cmpt_blnc = self.othello.tab.recuperer_score(2)

        # Met a jour les label (affichage graphique des compteurs)
        self.score_noir.set(" : " + str(self.cmpt_noir))
        self.score_blnc.set(" : " + str(self.cmpt_blnc))

    def dessiner_jeu(self):
        self.cnv.delete(ALL)
        self.dessiner_grille()
        print("####################################")
        self.othello.tab.afficher_plateau()
        print("####################################")

        for i in range(8):
            for j in range(8):
                yc = self.convertirIndextoPix(i)
                xc = self.convertirIndextoPix(j)
                val = self.othello.tab.get_value(i, j)
                if val == 1:
                    self.dessiner_jeton(xc, yc, 'black')
                elif val == 2:
                    self.dessiner_jeton(xc, yc, 'white')

        self.dessiner_score()

    def reset_jeu(self):
        self.cnv.delete(ALL)
        self.dessiner_grille()
        self.dessiner_jeu()
        self.score_noir.set(" : " + str(2))
        self.score_blnc.set(" : " + str(2))

    def clic(self, event):
        # c'est ici que l'on ajoute des jetons en cliquant,
        # que tab(i,j) se met à jour et que les algos de validité et de retournement
        # se mettent en action...

        # on récupère les coordonnées (x,y) sur l'évènement "clic"
        x = event.x
        y = event.y

        # astuce de division entière ( ou // en python) pour positionner
        # le jeton sur la case cliquée
        xc = int(x / 50) * 50 + 25
        yc = int(y / 50) * 50 + 25

        ic = self.convertirPixtoIndex(yc)
        jc = self.convertirPixtoIndex(xc)

        if self.radio_value.get() == 1:
            color = 'black'
            valColor = 1
            self.radio_value.set(2)  # on alterne les couleurs à chaque clic...
        else:
            color = 'white'
            valColor = 2
            self.radio_value.set(1)  # ...pour le tour suivant (noir, blanc, noir...)

        if self.othello.tab.verifier_si_saisie_valide(ic, jc):
            # inscrit valeur du pion sur le plateau
            self.othello.tab.set_value(ic, jc, valColor)
            self.dessiner_jeton(xc, yc, color)

            # recherche des pions a retourner et retournement
            self.othello.tab.rechercher_pion(ic, jc, valColor)          

            # Mise a jour graphique du jeu apres retournement des pions
            self.dessiner_jeu()

