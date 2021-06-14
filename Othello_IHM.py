from tkinter import *

class Othello_IHM:
    def __init__(self, oth):
        self.cmpt = 2
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
        rdio_noir = Radiobutton(frl, text='NOIR', \
                                variable=self.radio_value, value=1)

        rdio_blnc = Radiobutton(frr, text='BLANC', \
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
        print("conversion : ",(x-25)//50)
        return ((x-25)//50)

    def dessiner_grille(self):
        gr = [0, 50, 100, 150, 200, 250, 300, 350, 400]
        for xi in gr:
            self.cnv.create_line(xi, 0, xi, 400)
        for yi in gr:
            self.cnv.create_line(0, yi, 400, yi)

    def dessiner_jeton(self, x, y, color):
        r = 20
        self.cnv.create_oval(x - r, y - r, x + r, y + r, outline='black', fill=color)

    def dessiner_jeu(self):
        print("tab = ", self.othello.tab)
        gr = [0, 50, 100, 150, 200, 250, 300, 350, 400]
        self.cnv.delete(ALL)
        self.dessiner_grille()
        self.dessiner_jeton(175, 175, 'white')  # les coordonnées seront remplacées
        self.dessiner_jeton(225, 225, 'white')  # par la lecture de tab(i,j)
        self.dessiner_jeton(175, 225, 'black')
        self.dessiner_jeton(225, 175, 'black')

    def reset_jeu(self):
        self.cnv.delete(ALL)
        self.dessiner_grille()
        self.dessiner_jeu()
        self.cmpt = 2
        self.score_noir.set(" : " + str(self.cmpt))
        self.score_blnc.set(" : " + str(self.cmpt))

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

        ic = self.convertirPixtoIndex(xc)
        jc = self.convertirPixtoIndex(yc)

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
            print('on veut dessiner le jeton !!!!')
            self.dessiner_jeton(xc, yc, color)
            self.cmpt += 1
            self.score_noir.set(" : " + str(self.cmpt))
            self.score_blnc.set(" : " + str(self.cmpt))

            self.othello.tab.rechercher_pion(ic, jc, valColor)
            # self.dessiner_jeu()