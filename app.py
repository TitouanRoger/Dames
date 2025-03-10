##############################################################
# Importations #

import pyxel

##############################################################
# Chargement #

pyxel.init(160, 160, title="Jeu de Dames")
pyxel.load("res.pyxres")

##############################################################
# Variables #

#  Positions des pions
pions = [["X", "B", "X", "B", "X", "B", "X", "B", "X", "B"],
         ["B", "X", "B", "X", "B", "X", "B", "X", "B", "X"],
         ["X", "B", "X", "B", "X", "B", "X", "B", "X", "B"],
         ["B", "X", "B", "X", "B", "X", "B", "X", "B", "X"],
         ["X", "O", "X", "O", "X", "O", "X", "O", "X", "O"],
         ["O", "X", "O", "X", "O", "X", "O", "X", "O", "X"],
         ["X", "R", "X", "R", "X", "R", "X", "R", "X", "R"],
         ["R", "X", "R", "X", "R", "X", "R", "X", "R", "X"],
         ["X", "R", "X", "R", "X", "R", "X", "R", "X", "R"],
         ["R", "X", "R", "X", "R", "X", "R", "X", "R", "X"]]

joueurs = [["B", "DB", "R", "DR"],
           ["R", "DR", "B", "DB"]]

coord = []  # Utilisé pour vérifier les cases jouables

page = "Jeu"  # page
joueur = 1  # joueur qui commence
select = 0  # sélection du pion (= 0 car aucun pion sélectionné)
play_win = 0  # Utilisé pour jouer une fois le son de la victoire
coup = 0  # compte le nombre de coups joués
PTP = 40  # nombre total de pions au tour précédent (= 40 car 40 pions au départ)
PT = 40  # nombre total de pions (= 40 car 40 pions au départ)
recommencer = 0  # permet de laisser activer la page de confirmation pour recommencer quand c'est égal à 1


##############################################################
# Fonctions #

# Fonctions sons
def son_jouer():

    pyxel.sound(0).set(
        "a1",
        "",
        "3",
        "",
        10,
    )
    pyxel.play(0, 0, loop=False)


def son_dame():

    pyxel.sound(0).set(
        "e1e2e3e2e1",
        "T",
        "3",
        "F",
        18,
    )
    pyxel.play(0, 0, loop=False)


def son_win():

    pyxel.sound(0).set(
        "c3d3 c3d3 c4c4",
        "TS",
        "3",
        "FFFF FF",
        15,
    )
    pyxel.play(0, 0, loop=False)


def son_match_nul():

    pyxel.sound(0).set(
        "e1e3f1f1g1g1",
        "TS",
        "4",
        "F",
        15,
    )
    pyxel.play(0, 0, loop=False)


# Affiche le tableau de jeu
def affichage(x, y):

    pyxel.cls(10)

    # Tableau de jeu
    pyxel.rectb(24, 24, 112, 112, 2)
    for i in range(5):
        for j in range(5):
            pyxel.rect(25 + x[j], 25 + y[i], 11, 11, 7)
            pyxel.rect(36 + x[j], 25 + y[i], 11, 11, 0)
        for j in range(5):
            pyxel.rect(25 + x[j], 36 + y[i], 11, 11, 0)
            pyxel.rect(36 + x[j], 36 + y[i], 11, 11, 7)

    # Titre
    pyxel.blt(18, 4, 0, 0, 32, 125, 16, colkey=0)
    # Joueur 1
    pyxel.blt(7, 60, 0, 0, 56, 10, 34, colkey=0)
    pyxel.blt(6, 95, 0, 0, 0, 11, 11, colkey=0)
    pyxel.blt(6, 106, 0, 32, 0, 11, 11, colkey=0)
    # Joueur 2
    pyxel.blt(143, 60, 0, 12, 56, 10, 34, colkey=0)
    pyxel.blt(142, 95, 0, 16, 0, 11, 11, colkey=0)
    pyxel.blt(142, 106, 0, 48, 0, 11, 11, colkey=0)
    # Explications
    if joueur != 0:
        pyxel.blt(71, 136, 0, 0, 96, 18, 18, colkey=0)
    # Recommencer
    if page == "Jeu" or joueur == 0:
        pyxel.rect(57, 154, 45, 6, 13)
        pyxel.text(58, 155, "Recommencer", 1)


def explications(x, y):

    global page, pions_explications, suivant1, suivant2

    # Position des pions d'explications
    if page == "Explications_1" or page == "Explications_2":
        pions_explications = [["X", "O", "X", "O", "X", "O", "X", "O", "X", "O"],
                              ["O", "X", "O", "X", "O", "X", "O", "X", "O", "X"],
                              ["X", "O", "X", "O", "X", "O", "X", "O", "X", "O"],
                              ["O", "X", "O", "X", "O", "X", "O", "X", "O", "X"],
                              ["X", "O", "X", "O", "X", "O", "X", "O", "X", "O"],
                              ["O", "X", "O", "X", "O", "X", "O", "X", "O", "X"],
                              ["X", "O", "X", "O", "X", "B", "X", "O", "X", "O"],
                              ["O", "X", "O", "X", "O", "X", "O", "X", "O", "X"],
                              ["X", "O", "X", "O", "X", "O", "X", "O", "X", "O"],
                              ["O", "X", "O", "X", "O", "X", "O", "X", "O", "X"]]

    if page == "Explications_3":
        pions_explications = [["X", "O", "X", "O", "X", "O", "X", "O", "X", "O"],
                              ["O", "X", "O", "X", "O", "X", "O", "X", "O", "X"],
                              ["X", "O", "X", "O", "X", "O", "X", "O", "X", "O"],
                              ["O", "X", "O", "X", "O", "X", "O", "X", "O", "X"],
                              ["X", "O", "X", "O", "X", "O", "X", "O", "X", "O"],
                              ["O", "X", "O", "X", "O", "X", "B", "X", "O", "X"],
                              ["X", "O", "X", "O", "X", "O", "X", "O", "X", "O"],
                              ["O", "X", "O", "X", "O", "X", "O", "X", "O", "X"],
                              ["X", "O", "X", "O", "X", "O", "X", "O", "X", "O"],
                              ["O", "X", "O", "X", "O", "X", "O", "X", "O", "X"]]

    if page == "Explications_4":
        pions_explications = [["X", "O", "X", "O", "X", "O", "X", "O", "X", "O"],
                              ["O", "X", "O", "X", "O", "X", "O", "X", "O", "X"],
                              ["X", "O", "X", "O", "X", "O", "X", "O", "X", "O"],
                              ["O", "X", "O", "X", "O", "X", "O", "X", "O", "X"],
                              ["X", "O", "X", "O", "X", "O", "X", "O", "X", "O"],
                              ["O", "X", "O", "X", "R", "X", "O", "X", "O", "X"],
                              ["X", "O", "X", "O", "X", "B", "X", "O", "X", "O"],
                              ["O", "X", "O", "X", "O", "X", "O", "X", "O", "X"],
                              ["X", "O", "X", "O", "X", "O", "X", "O", "X", "O"],
                              ["O", "X", "O", "X", "O", "X", "O", "X", "O", "X"]]

    if page == "Explications_5":
        pions_explications = [["X", "O", "X", "O", "X", "O", "X", "O", "X", "O"],
                              ["O", "X", "O", "X", "O", "X", "O", "X", "O", "X"],
                              ["X", "O", "X", "O", "X", "O", "X", "O", "X", "O"],
                              ["O", "X", "O", "X", "O", "X", "O", "X", "O", "X"],
                              ["X", "O", "X", "B", "X", "O", "X", "O", "X", "O"],
                              ["O", "X", "O", "X", "O", "X", "O", "X", "O", "X"],
                              ["X", "O", "X", "O", "X", "O", "X", "O", "X", "O"],
                              ["O", "X", "O", "X", "O", "X", "O", "X", "O", "X"],
                              ["X", "O", "X", "O", "X", "O", "X", "O", "X", "O"],
                              ["O", "X", "O", "X", "O", "X", "O", "X", "O", "X"]]

    pyxel.cls(10)

    # Tableau de jeu
    pyxel.rectb(24, 24, 112, 112, 2)
    for i in range(5):
        for j in range(5):
            pyxel.rect(25 + x[j], 25 + y[i], 11, 11, 7)
            pyxel.rect(36 + x[j], 25 + y[i], 11, 11, 0)
        for j in range(5):
            pyxel.rect(25 + x[j], 36 + y[i], 11, 11, 0)
            pyxel.rect(36 + x[j], 36 + y[i], 11, 11, 7)

    # Titre
    pyxel.blt(18, 4, 0, 0, 32, 125, 16, colkey=0)

    # Placement des pions d'explications
    l = 0  # ligne
    y = 25  # coordonnée y
    for i in range(10):
        p = 0
        x = 25  # coordonnée x
        for j in range(10):
            if pions_explications[l][p] == "B":  # Pion bleu
                pyxel.blt(x, y, 0, 0, 0, 11, 11, colkey=0)
                x += 11
            elif pions_explications[l][p] == "R":  # Pion rouge
                pyxel.blt(x, y, 0, 16, 0, 11, 11, colkey=0)
                x += 11
            elif pions_explications[l][p] == "O":  # Case vide
                pyxel.blt(x, y, 0, 64, 0, 11, 11, colkey=0)
                x += 11
            elif pions_explications[l][p] == "X":  # Case blanche
                pyxel.blt(x, y, 0, 64, 0, 11, 11, colkey=0)
                x += 11
            elif pions_explications[l][p] == "DB":  # Dame bleue
                pyxel.blt(x, y, 0, 32, 0, 11, 11, colkey=0)
                x += 11
            elif pions_explications[l][p] == "DR":  # Dame rouge
                pyxel.blt(x, y, 0, 48, 0, 11, 11, colkey=0)
                x += 11
            p += 1
        l += 1
        y += 11

        def suivant1(page_explications):

            global page

            pyxel.rect(3, 152, 29, 8, 3)
            pyxel.text(4, 153, "Suivant", 2)
            if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and 3 < pyxel.mouse_x < 3 + 29 and 152 < pyxel.mouse_y < 152 + 8:
                page = page_explications

        def suivant2(page_explications):

            global page

            pyxel.rect(128, 152, 29, 8, 3)
            pyxel.text(129, 153, "Suivant", 2)
            if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and 128 < pyxel.mouse_x < 128 + 29 and 152 < pyxel.mouse_y < 152 + 8:
                page = page_explications

    if page == "Explications_1":  # Explications 1
        pyxel.blt(85, 96, 0, 20, 96, 8, 8, colkey=0)
        pyxel.text(2, 140, "Clique sur un pion pour le selectionner", 3)
        suivant1("Explications_2")

    if page == "Explications_2":  # Explications 2
        pyxel.blt(69, 80, 0, 16, 16, 11, 11, colkey=0)
        pyxel.blt(91, 80, 0, 16, 16, 11, 11, colkey=0)
        pyxel.blt(96, 85, 0, 20, 96, 8, 8, colkey=0)
        pyxel.text(2, 140,
                   "Une fois le pion selectionne, des cases\nvertes apparaissent la ou il peut etre\ndeplace", 3)
        suivant2("Explications_3")

    if page == "Explications_3":  # Explications 3
        pyxel.text(2, 140, "Vous pourrez ensuite cliquer sur une\ncase verte pour le deplacer", 3)
        suivant1("Explications_4")

    if page == "Explications_4":  # Explications 4
        pyxel.blt(58, 69, 0, 16, 16, 11, 11, colkey=0)
        pyxel.blt(63, 74, 0, 20, 96, 8, 8, colkey=0)
        pyxel.text(2, 140,
                   "Le pion peut aussi prendre des pions\n(la prise est obligatoire),que ce soit\nen avant ou en arriere",
                   3)
        suivant2("Explications_5")

    if page == "Explications_5":  # Explications 5
        pyxel.text(25, 140, "Explications termines", 3)
        pyxel.blt(113, 140, 0, 0, 96, 18, 18, colkey=0)
        if pyxel.btn(
                pyxel.MOUSE_BUTTON_LEFT) and 113 < pyxel.mouse_x < 113 + 17 and 140 < pyxel.mouse_y < 140 + 17:
            page = "Jeu"


def positions_pions():

    l = 0  # ligne
    y = 25  # coordonnée y
    for i in range(10):
        p = 0
        x = 25  # coordonnée x
        for j in range(10):
            if pions[l][p] == "B":  # Pion bleu
                pyxel.blt(x, y, 0, 0, 0, 11, 11, colkey=0)
                x += 11
            elif pions[l][p] == "R":  # Pion rouge
                pyxel.blt(x, y, 0, 16, 0, 11, 11, colkey=0)
                x += 11
            elif pions[l][p] == "O":  # Case vide
                pyxel.blt(x, y, 0, 64, 0, 11, 11, colkey=0)
                x += 11
            elif pions[l][p] == "X":  # Case blanche
                pyxel.blt(x, y, 0, 64, 0, 11, 11, colkey=0)
                x += 11
            elif pions[l][p] == "DB":  # Dame bleue
                pyxel.blt(x, y, 0, 32, 0, 11, 11, colkey=0)
                x += 11
            elif pions[l][p] == "DR":  # Dame rouge
                pyxel.blt(x, y, 0, 48, 0, 11, 11, colkey=0)
                x += 11
            p += 1
        l += 1
        y += 11


def detection_dames():

    for p in range(10):
        if pions[0][p] == "R":  # Si pion rouge tout en haut
            pions[0][p] = "DR"  # Se transforme en dame rouge
            son_dame()
        if pions[9][p] == "B":  # Si pion bleu tout en bas
            pions[9][p] = "DB"  # Se transforme en dame bleue
            son_dame()


def selection():

    global joueur, select, c1, c2

    if joueur == 1:
        pyxel.blt(7, 125, 0, 24, 56, 10, 10, colkey=0)
        c1 = "B"  # pion bleu
        c2 = "DB"  # dame bleue

    if joueur == 2:
        pyxel.blt(143, 125, 0, 24, 56, 10, 10, colkey=0)
        c1 = "R"  # pion rouge
        c2 = "DR"  # dame rouge

    x = 35  # coordonnée x
    l = 1  # compteur
    y = 24  # coordonnée y
    p1 = 0  # ligne
    p2 = 1  # colonne
    s = 1  # sélection
    for i in range(10):
        for j in range(5):
            c = c1
            for k in range(2):
                if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and x < pyxel.mouse_x < x + 12 and y < pyxel.mouse_y < y + 12 and \
                        pions[p1][p2] == c:
                    select = s
                c = c2
            x += 22
            p2 += 2
            s += 1
        if l == 1:
            x = 24
            l = 2
        elif l == 2:
            x = 35
            l = 1
        y += 11
        p1 += 1
        if p1 == 0 or p1 == 2 or p1 == 4 or p1 == 6 or p1 == 8:
            p2 = 1
        elif p1 == 1 or p1 == 3 or p1 == 5 or p1 == 7 or p1 == 9:
            p2 = 0


def change_joueur():

    global joueur, select, PTP, PT, PB, PR, coup

    if joueur == 1:
        joueur = 2
    else:
        joueur = 1
    select = 0
    son_jouer()

    PT = PB + PR  # Pions totaux
    if PT == PTP:  # Si pions totaux est égal à pions totaux au coup précédent
        coup += 1
    else:
        coup = 0
    PTP = PT


def affiche_cadre_vert(x, y):

    pyxel.blt(x, y, 0, 16, 16, 11, 11, colkey=0)


def deplacement_pion(l, p, a, dl, dp, prises):

    pions[l][p] = "O"
    if prises >= 1:
        pions[l + a * dl][p + a * dp] = "O"  # Suppression du pion adverse
        if prises >= 1 and jouer == 0:
            change_joueur()


def clic_cadre_vert(l, p, a, dl, dp, x_select, y_select, pion, prises):

    global jouer

    if pyxel.btn(
            pyxel.MOUSE_BUTTON_LEFT) and x_select < pyxel.mouse_x < x_select + 12 and y_select < pyxel.mouse_y < y_select + 12:
        pions[l][p] = "O"
        pions[l + (a + 1) * dl][p + (a + 1) * dp] = pion  # Déplacement du pion du joueur
        if prises >= 1:
            pions[l + a * dl][p + a * dp] = "O"  # Suppression du pion adverse
            if prises >= 1:
                jouer = 1
                change_joueur()
            return prises - 1
        else:
            change_joueur()
    return 0


def deplacement_prise(l, p, x_select, y_select, pion, prises, ex):

    global joueur, joueurs, prise, coord, jouer

    # On ne cherche pas un emplacement de coordonnées l, p déjà traité
    for i in range(len(coord)):
        if coord[i] == l * 10 + p:
            return 0

    # Minimum pour le déplacement d'une dame : [HG,HD,BG,BD]
    if pion == joueurs[joueur - 1][1]:
        a_min = [min([l, p]), min([l, 9 - p]), min([9 - l, p]), min([9 - l, 9 - p])]  # Dame
    else:
        a_min = [2, 2, 2, 2]  # Pion

    # Haut/Gauche
    for m in range(1, a_min[0]):
        if p - m >= 0 and l - m >= 0 and ex != "HG":
            if pions[l - m][p - m] == joueurs[joueur - 1][2] or pions[l - m][p - m] == joueurs[joueur - 1][
                3]:  # Déplacement avec prise de pions adverses
                if p - m - 1 >= 0 and l - m - 1 >= 0 and pions[l - m - 1][p - m - 1] == "O":
                    prises += 1
                    coord.append(l * 10 + p)
                    affiche_cadre_vert(x_select - 11 * (m + 1), y_select - 11 * (m + 1))
                    if deplacement_prise(l - m - 1, p - m - 1, x_select - 11 * (m + 1), y_select - 11 * (m + 1), pion,
                                         prises, "BD") == 0:
                        if clic_cadre_vert(l, p, m, -1, -1, x_select - 11 * (m + 1), y_select - 11 * (m + 1), pion,
                                           prises) != 0:
                            return prises
                    else:
                        deplacement_pion(l, p, m, - 1, - 1, prises)
                        return prises
                    jouer = 0
                    break  # On sort de la boucle à la prise par la dame
                else:
                    break  # On sort de la boucle, on ne peut pas poser le pion derrière le pion adverse - dame

    # Haut/Droite
    for m in range(1, a_min[1]):
        if p + m <= 9 and l - m >= 0 and ex != "HD":
            if pions[l - m][p + m] == joueurs[joueur - 1][2] or pions[l - m][p + m] == joueurs[joueur - 1][
                3]:  # Déplacement avec prise de pions adverses
                if p + m + 1 <= 9 and l - m - 1 >= 0 and pions[l - m - 1][p + m + 1] == "O":
                    prises += 1
                    coord.append(l * 10 + p)
                    affiche_cadre_vert(x_select + 11 * (m + 1), y_select - 11 * (m + 1))
                    if deplacement_prise(l - m - 1, p + m + 1, x_select + 11 * (m + 1), y_select - 11 * (m + 1), pion,
                                         prises, "BG") == 0:
                        if clic_cadre_vert(l, p, m, -1, 1, x_select + 11 * (m + 1), y_select - 11 * (m + 1), pion,
                                           prises) != 0:
                            return prises
                    else:
                        deplacement_pion(l, p, m, -1, 1, prises)
                        return prises
                    jouer = 0
                    break  # On sort de la boucle à la prise par la dame
                else:
                    break  # On sort de la boucle, on ne peut pas poser le pion derrière le pion adverse - dame

    # Bas/Gauche
    for m in range(1, a_min[2]):
        if p - m >= 0 and l + m <= 9 and ex != "BG":
            if pions[l + m][p - m] == joueurs[joueur - 1][2] or pions[l + m][p - m] == joueurs[joueur - 1][
                3]:  # Déplacement avec prise de pions adverses
                if p - m - 1 >= 0 and l + m + 1 <= 9 and pions[l + m + 1][p - m - 1] == "O":
                    prises += 1
                    coord.append(l * 10 + p)
                    affiche_cadre_vert(x_select - 11 * (m + 1), y_select + 11 * (m + 1))
                    if deplacement_prise(l + m + 1, p - m - 1, x_select - 11 * (m + 1), y_select + 11 * (m + 1), pion,
                                         prises, "HD") == 0:
                        if clic_cadre_vert(l, p, m, 1, -1, x_select - 11 * (m + 1), y_select + 11 * (m + 1), pion,
                                           prises) != 0:
                            return prises
                    else:
                        deplacement_pion(l, p, m, 1, -1, prises)
                        return prises
                    jouer = 0
                    break  # On sort de la boucle à la prise par la dame
                else:
                    break  # On sort de la boucle, on ne peut pas poser le pion derrière le pion adverse - dame

    # Bas/Droite
    for m in range(1, a_min[3]):
        if p + m <= 9 and l + m <= 9 and ex != "BD":
            if pions[l + m][p + m] == joueurs[joueur - 1][2] or pions[l + m][p + m] == joueurs[joueur - 1][
                3]:  # Déplacement avec la prise de pions adverses
                if p + m + 1 <= 9 and l + m + 1 <= 9 and pions[l + m + 1][p + m + 1] == "O":
                    prises += 1
                    coord.append(l * 10 + p)
                    affiche_cadre_vert(x_select + 11 * (m + 1), y_select + 11 * (m + 1))
                    if deplacement_prise(l + m + 1, p + m + 1, x_select + 11 * (m + 1), y_select + 11 * (m + 1), pion,
                                         prises, "HG") == 0:
                        if clic_cadre_vert(l, p, m, 1, 1, x_select + 11 * (m + 1), y_select + 11 * (m + 1), pion,
                                           prises) != 0:
                            return prises
                    else:
                        deplacement_pion(l, p, m, 1, 1, prises)
                        return prises
                    jouer = 0
                    break  # On sort de la boucle à la prise par la dame
                else:
                    break  # On sort de la boucle, on ne peut pas poser le pion derrière le pion adverse - dame

    if prises > 0:
        prise = True
    return 0


def lancement_deplacement(l, p, x_select, y_select, pion):

    global joueurs, joueur, pions

    if joueurs[joueur - 1][0] == "R" or pions[l][p] == joueurs[joueur - 1][1]:
        deplacement_haut(l, p, x_select, y_select, pion)
    if joueurs[joueur - 1][0] == "B" or pions[l][p] == joueurs[joueur - 1][1]:
        deplacement_bas(l, p, x_select, y_select, pion)


def deplacement_haut(l, p, x_select, y_select, pion):

    global joueurs, joueur, pions

    # Minimum pour le déplacement d'une dame : [HG,HD,BG,BD]
    if pion == joueurs[joueur - 1][1]:
        a_min = [min([l, p]) + 1, min([l, 9 - p]) + 1, min([9 - l, p]) + 1,
                 min([9 - l, 9 - p]) + 1]  # Dame / + 1 à cause du range
    else:
        a_min = [2, 2, 2, 2]  # Pion / + 1 à cause du range

    # A Gauche
    for m in range(1, a_min[0]):
        if p - m >= 0 and l - m >= 0 and pions[l - m][p - m] == "O":  # Déplacement simple
            affiche_cadre_vert(x_select - 11 * m, y_select - 11 * m)
            clic_cadre_vert(l, p, m - 1, -1, -1, x_select - 11 * m, y_select - 11 * m, pion,
                            0)  # (m - 1) car on ne mange pas de pion adverse
        else:
            break

    # A droite
    for m in range(1, a_min[1]):
        if p + m <= 9 and l - m >= 0 and pions[l - m][p + m] == "O":  # Déplacement simple
            affiche_cadre_vert(x_select + 11 * m, y_select - 11 * m)
            clic_cadre_vert(l, p, m - 1, -1, 1, x_select + 11 * m, y_select - 11 * m, pion,
                            0)  # (m - 1) car on ne mange pas de pion adverse
        else:
            break


def deplacement_bas(l, p, x_select, y_select, pion):

    global joueurs, joueur, pions

    # Minimum pour le déplacement d'une dame : [HG,HD,BG,BD]
    if pion == joueurs[joueur - 1][1]:
        a_min = [min([l, p]) + 1, min([l, 9 - p]) + 1, min([9 - l, p]) + 1,
                 min([9 - l, 9 - p]) + 1]  # reine / + 1 à cause du range
    else:
        a_min = [2, 2, 2, 2]  # Pion / +1 à cause du range

    # A gauche
    for m in range(1, a_min[2]):
        if p - m >= 0 and l + m <= 9 and pions[l + m][p - m] == "O":  # Déplacement simple
            affiche_cadre_vert(x_select - 11 * m, y_select + 11 * m)
            clic_cadre_vert(l, p, m - 1, 1, -1, x_select - 11 * m, y_select + 11 * m, pion,
                            0)  # (m - 1) car on ne mange pas de pion adverse
        else:
            break

    # A droite
    for m in range(1, a_min[3]):
        if p + m <= 9 and l + m <= 9 and pions[l + m][p + m] == "O":  # Déplacement simple
            affiche_cadre_vert(x_select + 11 * m, y_select + 11 * m)
            clic_cadre_vert(l, p, m - 1, 1, 1, x_select + 11 * m, y_select + 11 * m, pion,
                            0)  # (m - 1) car on ne mange pas de pion adverse
        else:
            break


def deplacement():

    global joueur, select, prise, coord

    compteur = 0
    y_select = 25 - 11
    delta = 0
    for l in range(10):  # Pour chaque ligne
        if l % 2 == 1:  # Déplacement en fonction de la ligne pour la position de la première case noire
            x_select = 25 - 11
        else:
            x_select = 25 - 11
        y_select += 11  # Déplacement d'une ligne

        for p in range(10):  # Pour chaque pion
            x_select += 11  # Déplacement d'une case vers la droite
            compteur += 0.5 + delta  # Compteur pour la sélection du pion

            # Changement de delta pour changer le compteur pour le passage à la ligne suivante en fonction de la case de la fin et du début
            if delta != 0:
                delta = 0
            if p == 9 and pions[l][p] != "X":
                delta = 0.5
            elif p == 9 and pions[l][p] == "X":
                delta = -0.5

            if compteur == select:  # Sélection du pion
                prises = 0
                prise = False
                coord = []
                pyxel.blt(x_select, y_select, 0, 0, 16, 11, 11,
                          colkey=0)  # Place un cadre orange autour du pion sélectionné

                if pions[l][p] == joueurs[joueur - 1][0] or pions[l][p] == joueurs[joueur - 1][1]:  # Pion
                    deplacement_prise(l, p, x_select, y_select, pions[l][p], prises, "ALL")
                    if not prise:
                        lancement_deplacement(l, p, x_select, y_select, pions[l][p])


def compteur_de_pions():

    global PB, PR

    rr = rb = 0
    PB = 0  # compteur de pions bleus
    PR = 0  # compteur de pions rouges
    for l in range(10):  # Pour chaque ligne
        for p in range(10):  # Pour chaque pion
            if pions[l][p] == "B" or pions[l][p] == "DB":  # Compte les pions bleus
                PB += 1
            if pions[l][p] == "R" or pions[l][p] == "DR":  # Compte les pions rouges
                PR += 1
    if PB <= 9:
        rb = 2  # Décale le chiffre affichant le nombre de pions bleu
    if PR <= 9:
        rr = 2  # Décale le chiffre affichant le nombre de pions rouge
    pyxel.text(8 + rb, 118, f"{PB}", 2)
    pyxel.text(144 + rr, 118, f"{PR}", 2)


def conditions_win():

    global joueur, select, PB, PR, play_win, coup

    if PB == 0:  # Si le joueur 1 (pions bleus) n'a plus de pions, victoire du joueur 2
        joueur = 0
        select = 0
        # Le joueur 2 a gagné
        pyxel.rectb(141, 58, 14, 67, 3)
        pyxel.blt(31, 72, 0, 0, 120, 97, 16, colkey=0)
        pyxel.text(43, 145, "Le joueur 2 a win !", 3)
        if play_win == 0:
            play_win = 1
            son_win()

    if PR == 0:  # Si le joueur 2 (pions rouges) n'a plus de pions, victoire du joueur 1
        joueur = 0
        select = 0
        # Le joueur 1 a gagné
        pyxel.rectb(5, 58, 14, 67, 3)
        pyxel.blt(31, 72, 0, 0, 120, 97, 16, colkey=0)
        pyxel.text(43, 145, "Le joueur 1 a win !", 3)
        if play_win == 0:
            play_win = 1
            son_win()

    if coup >= 26:  # S'il y a plus de 26 coups sans prise de pion, match nul
        joueur = 0
        select = 0
        # Match nul
        pyxel.rectb(5, 58, 14, 67, 3)
        pyxel.rectb(141, 58, 14, 67, 3)
        pyxel.blt(31, 72, 0, 0, 120, 97, 16, colkey=0)
        pyxel.text(59, 145, "Match nul !", 3)
        if play_win == 0:
            play_win = 1
            son_match_nul()


##############################################################
# Programme #


def update():
    global page, recommencer

    pyxel.mouse(True)
    x_lignes = [22 * i for i in range(5)]
    y_lignes = [22 * i for i in range(5)]

    if page == "Jeu" and play_win == 0:
        if pyxel.btn(
                pyxel.MOUSE_BUTTON_LEFT) and 71 < pyxel.mouse_x < 71 + 17 and 136 < pyxel.mouse_y < 136 + 17 and recommencer != 1:
            page = "Explications_1"

    if page == "Jeu":
        affichage(x_lignes, y_lignes)
        positions_pions()
        if joueur != 0 and recommencer != 1:
            selection()
            deplacement()
        compteur_de_pions()
        conditions_win()

    if page != "Jeu":
        explications(x_lignes, y_lignes)


def draw():
    global pions, page, joueur, select, play_win, coup, PTP, PT, recommencer

    if page == "Jeu":
        detection_dames()

        # Redémarrer la partie
        if pyxel.btn(
                pyxel.MOUSE_BUTTON_LEFT) and 57 < pyxel.mouse_x < 57 + 45 and 154 < pyxel.mouse_y < 154 + 6 or recommencer == 1:
            recommencer = 1
            pyxel.rect(36, 47, 88, 66, 6)
            pyxel.rectb(36, 47, 88, 66, 3)
            pyxel.rectb(37, 48, 86, 64, 2)
            pyxel.text(41, 52, f"Etes-vous sur(e)s de\nvouloir recommencer\n     la partie ?", 1)
            pyxel.text(41, 77, f"********************", 1)
            pyxel.rect(42, 88, 35, 18, 15)
            pyxel.rectb(42, 88, 35, 18, 8)
            pyxel.text(50, 94, f"-NON-", 8)
            pyxel.rect(82, 88, 35, 18, 7)
            pyxel.rectb(82, 88, 35, 18, 3)
            pyxel.text(90, 94, f"-OUI-", 3)
            if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and 82 <= pyxel.mouse_x <= 82 + 35 and 88 <= pyxel.mouse_y <= 88 + 18:
                joueur = 1
                select = 0
                recommencer = 0
                play_win = 0
                coup = 0
                PTP = 40
                PT = 40
                pions = [["X", "B", "X", "B", "X", "B", "X", "B", "X", "B"],
                         ["B", "X", "B", "X", "B", "X", "B", "X", "B", "X"],
                         ["X", "B", "X", "B", "X", "B", "X", "B", "X", "B"],
                         ["B", "X", "B", "X", "B", "X", "B", "X", "B", "X"],
                         ["X", "O", "X", "O", "X", "O", "X", "O", "X", "O"],
                         ["O", "X", "O", "X", "O", "X", "O", "X", "O", "X"],
                         ["X", "R", "X", "R", "X", "R", "X", "R", "X", "R"],
                         ["R", "X", "R", "X", "R", "X", "R", "X", "R", "X"],
                         ["X", "R", "X", "R", "X", "R", "X", "R", "X", "R"],
                         ["R", "X", "R", "X", "R", "X", "R", "X", "R", "X"]]

            if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and 42 <= pyxel.mouse_x <= 42 + 35 and 88 <= pyxel.mouse_y <= 88 + 18:
                recommencer = 0


pyxel.run(update, draw)
##############################################################