from copy import deepcopy
from math import *
from model import *
from korisnik import kreiraj_listu_poteza, pomeri_figuru                    #napraviti da hasa za redom

najbolja_tabla = None

def kreiraj_listu_poteza_racunar(gl_tabla, figurica, jedi):
    koordinate = []
    lista = []
    za_pojesti = []
    tabla = gl_tabla._tabla
    dd = figurica.dole_desno(tabla)
    dl = figurica.dole_levo(tabla)
    if figurica._dama:
        gd = figurica.gore_desno(tabla)
        gl = figurica.gore_levo(tabla)
        if (gd == 2 or dl == 2) and gl_tabla._obaveznopoj == True:
            jedi = True
    if (dd == 2 or dl ==2) and gl_tabla._obaveznopoj == True:
        jedi = True


    if dd == 1 and jedi == False:
        koordinate = [figurica.x, figurica.y, figurica.x + 1, figurica.y + 1]
        lista.append(koordinate)
    elif dd == 2:
        koordinate = [figurica.x, figurica.y, figurica.x + 2, figurica.y + 2]
        lista.append(koordinate)
        za_pojesti.append(koordinate)

    if dl == 1 and jedi == False:
        koordinate = [figurica.x, figurica.y, figurica.x + 1, figurica.y - 1]
        lista.append(koordinate)
    elif dl == 2:
        koordinate = [figurica.x, figurica.y, figurica.x + 2, figurica.y - 2]
        lista.append(koordinate)
        za_pojesti.append(koordinate)

    if figurica._dama:
        if gd == 1 and jedi == False:
            koordinate = [figurica.x, figurica.y, figurica.x - 1, figurica.y + 1]
            lista.append(koordinate)
        elif gd == 2:
            koordinate = [figurica.x, figurica.y, figurica.x - 2, figurica.y + 2]
            lista.append(koordinate)
            za_pojesti.append(koordinate)

        if gl == 1 and jedi == False:
            koordinate = [figurica.x, figurica.y, figurica.x - 1, figurica.y - 1]
            lista.append(koordinate)
        elif gl == 2:
            koordinate = [figurica.x, figurica.y, figurica.x - 2, figurica.y - 2]
            lista.append(koordinate)
            za_pojesti.append(koordinate)

    return lista, za_pojesti

def kreiraj_listu_svih_poteza(gl_tabla, boja):
    tabla = gl_tabla._tabla
    moguci_potezi = []
    lista_pojedi = []
    for i in range(0, 8):
        for j in range(0, 8):
            if tabla[i][j] == " " or tabla[i][j] == "-":
                continue
            figurica = tabla[i][j]
            if figurica._boja == boja:
                figurica = tabla[i][j]
                if boja == "w":
                    potezi_figurice, za_pojesti = kreiraj_listu_poteza(gl_tabla, figurica, False)
                else:
                    potezi_figurice, za_pojesti = kreiraj_listu_poteza_racunar(gl_tabla, figurica, False)
                if len(za_pojesti) != 0:
                    lista_pojedi = lista_pojedi + za_pojesti
                if len(potezi_figurice) != 0:
                    moguci_potezi = moguci_potezi + potezi_figurice

    return moguci_potezi, lista_pojedi

def minmax_main(gl_tabla):
    dubina = 3
    max_cvor(gl_tabla, dubina, -inf, inf)
    global najbolja_tabla
    odigrano = False
    if najbolja_tabla == None:
        return najbolja_tabla, True
    for i in range(0, 8):
        for j in range(0, 8):
            if gl_tabla._tabla[i][j] != najbolja_tabla._tabla[i][j]:
                odigrano = True
                break

    pojeden = gl_tabla.brojbelih - najbolja_tabla.brojbelih
    gl_tabla = najbolja_tabla
    return gl_tabla, odigrano, pojeden

def max_cvor(gl_tabla, dubina, alfa, beta):
    return minmax_algoritam(gl_tabla, dubina, -inf, alfa, beta)

def min_cvor(gl_tabla, dubina, alfa, beta):
    return minmax_algoritam(gl_tabla, dubina, inf, alfa, beta)

def minmax_algoritam(gl_tabla, dubina, najbolja_vrednost, alfa, beta):
    global najbolja_tabla

    if gl_tabla.kraj() or dubina == 0:
        bodovi = heuristika(gl_tabla)
        return bodovi


    if najbolja_vrednost == -inf:
        moguci_potezi, lista_pojedi = kreiraj_listu_svih_poteza(gl_tabla, "b")
        potezi = lista_pojedi
        if potezi == [] and gl_tabla._obaveznopoj:
            potezi = moguci_potezi
        elif gl_tabla._obaveznopoj == False:
            potezi = moguci_potezi

        for jedan_potez in potezi:
            pojeo = False
            kopija_table = deepcopy(gl_tabla)
            if abs(jedan_potez[1] - jedan_potez[3]) == 2:
                pojeo = True
            kopija_table = pomeri_figuru(jedan_potez[0], jedan_potez[1], jedan_potez[2], jedan_potez[3], kopija_table, pojeo, "b")
            krx = jedan_potez[2]
            kry = jedan_potez[3]
            if pojeo:
                while pojeo:
                    moguci_potezi2 = []
                    lista_pojedi2 = []
                    nova_tabla = kopija_table._tabla
                    potezi_figurice, za_pojesti = kreiraj_listu_poteza_racunar(kopija_table, nova_tabla[krx][kry], True)
                    if len(za_pojesti) != 0:
                        lista_pojedi2 = lista_pojedi2 + za_pojesti
                    if len(potezi_figurice) != 0:
                        moguci_potezi2 = moguci_potezi2 + potezi_figurice
                    if gl_tabla._obaveznopoj == True and len(lista_pojedi2) != 0:
                        moguci_potezi2 = lista_pojedi2
                    if moguci_potezi2 == []:
                        break
                    odabran = moguci_potezi2[0]

                    kopija_table = pomeri_figuru(odabran[0], odabran[1], odabran[2], odabran[3], kopija_table, pojeo, "b")
                    krx = odabran[2]
                    kry = odabran[3]
                    if abs(odabran[1] - odabran[3]) == 2:
                        pojeo = True
                    else:
                        break

            if kopija_table.kraj():
                najbolja_tabla = deepcopy(kopija_table)

            bodovi = min_cvor(kopija_table, dubina - 1, alfa, beta)
            if bodovi > najbolja_vrednost:
                najbolja_vrednost = bodovi
                if dubina == 3:
                    najbolja_tabla = deepcopy(kopija_table)
            if bodovi > beta:
                break
            if bodovi > alfa:
                alfa = bodovi



    elif najbolja_vrednost == inf:
        moguci_potezi, lista_pojedi = kreiraj_listu_svih_poteza(gl_tabla, "w")
        potezi = lista_pojedi
        if potezi == [] and gl_tabla._obaveznopoj:
            potezi = moguci_potezi
        elif gl_tabla._obaveznopoj == False:
            potezi = moguci_potezi

        for jedan_potez in potezi:
            pojeo = False
            kopija_table = deepcopy(gl_tabla)
            if abs(jedan_potez[1] - jedan_potez[3]) == 2:
                pojeo = True
            kopija_table = pomeri_figuru(jedan_potez[0], jedan_potez[1], jedan_potez[2], jedan_potez[3], kopija_table, pojeo, "w")
            krx = jedan_potez[2]
            kry = jedan_potez[3]
            if pojeo:
                while pojeo:
                    moguci_potezi2 = []
                    lista_pojedi2 = []
                    nova_tabla = kopija_table._tabla
                    potezi_figurice, za_pojesti = kreiraj_listu_poteza_racunar(kopija_table, nova_tabla[krx][kry], True)
                    if len(za_pojesti) != 0:
                        lista_pojedi2 = lista_pojedi2 + za_pojesti
                    if len(potezi_figurice) != 0:
                        moguci_potezi2 = moguci_potezi2 + potezi_figurice
                    if gl_tabla._obaveznopoj == True and len(lista_pojedi2) != 0:
                        moguci_potezi2 = lista_pojedi2
                    if moguci_potezi2 == []:
                        break
                    odabran = moguci_potezi2[0]

                    kopija_table = pomeri_figuru(odabran[0], odabran[1], odabran[2], odabran[3], kopija_table, pojeo, "w")
                    krx = odabran[2]
                    kry = odabran[3]
                    if abs(krx - kry) == 2:
                        pojeo = True
                    else:
                        break

            bodovi = max_cvor(kopija_table, dubina - 1, alfa, beta)
            if bodovi < najbolja_vrednost:
                najbolja_vrednost = bodovi
            if bodovi < alfa:
                break
            if bodovi < beta:
                beta = bodovi

    return najbolja_vrednost


def prebroj(gl_tabla, boja):
    tabla = gl_tabla._tabla
    brojdama = 0
    prekopola = 0
    damauzivicu = 0
    uzivicu = 0
    brojfigura = 0
    for i in range(0, 8):
        for j in range(0, 8):
            if tabla[i][j] == " " or tabla[i][j] == "-":
                continue
            figurica = tabla[i][j]
            if figurica._boja == boja:
                brojfigura += 1
                if figurica._dama:
                    brojdama += 1
                    if figurica.y == 7 or figurica.y == 0 or figurica.x == 0 or figurica.x == 7:
                        damauzivicu += 1

                if boja == "b" and figurica.x > 3:
                    prekopola += 1

                if boja == "w" and figurica.x < 4:
                    prekopola += 1

                if figurica._dama == False:
                    if figurica.y == 7 or figurica.y == 0 or figurica.x == 0 or figurica.x == 7:
                        uzivicu += 1

    return brojfigura, brojdama, prekopola, uzivicu, damauzivicu

def heuristika(gl_tabla):
    if gl_tabla.kraj():
        return inf
    B_brojfigura, B_brojdama, B_prekopola, B_uzivicu, B_damauzivicu = prebroj(gl_tabla, "b")
    W_brojfigura, W_brojdama, W_prekopola, W_uzivicu, W_damauzivicu = prebroj(gl_tabla, "w")

    crnibodovi = 7 * B_brojfigura + 10 * B_brojdama + 3 * B_prekopola + 9 * B_uzivicu + 5 * B_damauzivicu
    belibodovi = 7 * W_brojfigura + 10 * W_brojdama + 3 * W_prekopola + 9 * W_uzivicu + 5 * W_damauzivicu
    return crnibodovi - belibodovi

