from model import *


def pomeri_figuru(pocx, pocy, krx, kry, gl_tabla, pojeo, boja):
    stara = gl_tabla._tabla[pocx][pocy]
    gl_tabla._tabla[krx][kry] = Figura(boja, krx, kry)
    if stara._dama:
        gl_tabla._tabla[krx][kry]._dama = True
    gl_tabla._tabla[pocx][pocy] = " "
    if pojeo:
        gl_tabla._tabla[(pocx + krx)//2][(pocy + kry)//2] = " "
        if boja == "w":
            gl_tabla.brojcrnih -= 1
        else:
            gl_tabla.brojbelih -= 1
    if krx == 0 and boja == "w":
        gl_tabla._tabla[krx][kry]._dama = True
    elif krx == 7 and boja == "b":
        gl_tabla._tabla[krx][kry]._dama = True
    return gl_tabla


def kreiraj_listu_poteza(gl_tabla, figurica, jedi):
    koordinate = []
    lista = []
    za_pojesti = []
    tabla = gl_tabla._tabla
    gd = figurica.gore_desno(tabla)
    gl = figurica.gore_levo(tabla)
    if figurica._dama:
        dd = figurica.dole_desno(tabla)
        dl = figurica.dole_levo(tabla)
        if (dd == 2 or dl == 2) and gl_tabla._obaveznopoj == True:
            jedi = True
    if (gd == 2 or gl ==2) and gl_tabla._obaveznopoj == True:
        jedi = True


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

    if figurica._dama:
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


    return lista, za_pojesti


def ispisi_poteze(moguci_potezi):
    i = 1
    print("Vi ste na potezu! Moguće je odigrati: ")
    for potez in moguci_potezi:

        poct = "(" + str(potez[0] + 1) + ", " + chr(potez[1] + 65) + ")"
        krajnjat = "(" + str(potez[2] + 1) + ", " + chr(potez[3] + 65) + ")"
        print(str(i) + ". " + poct + " -> " + krajnjat)
        i += 1


def odaberi_potez(n):
    while True:
        try:
            opcija = eval(input("Uneti broj poteza koji želite da odigrate: "))
            if 0 < opcija <= n:
                return opcija - 1
            else:
                print("Proveriti unos!")
                continue
        except:
            print("Proveriti unos!")


def korisnik_igra(gl_tabla):
    tabla = gl_tabla._tabla
    moguci_potezi = []
    lista_pojedi = []
    for i in range(0, 8):
        for j in range(0, 8):
            if tabla[i][j] == " " or tabla[i][j] == "-":
                continue
            figurica = tabla[i][j]
            if figurica._boja == "w":
                figurica = tabla[i][j]
                potezi_figurice, za_pojesti = kreiraj_listu_poteza(gl_tabla, figurica, False)
                if len(za_pojesti) != 0:
                    lista_pojedi = lista_pojedi + za_pojesti
                    #print(lista_pojedi)
                if len(potezi_figurice) != 0:
                    moguci_potezi = moguci_potezi + potezi_figurice

    if gl_tabla._obaveznopoj == True and len(lista_pojedi)!=0:
        moguci_potezi = lista_pojedi

    if moguci_potezi == []:
        return False
    ispisi_poteze(moguci_potezi)
    indeks = odaberi_potez(len(moguci_potezi))
    odabrani = moguci_potezi[indeks]
    indikator_pojeo = False
    pojeo = abs(odabrani[1] - odabrani[3])
    if pojeo == 2:
        indikator_pojeo = True
    gl_tabla = pomeri_figuru(odabrani[0], odabrani[1], odabrani[2], odabrani[3], gl_tabla, indikator_pojeo, "w")
    gl_tabla.ispisi_tablu()

    while abs(odabrani[1] - odabrani[3]) == 2:
        moguci_potezi = []
        lista_pojedi = []
        potezi_figurice, za_pojesti = kreiraj_listu_poteza(gl_tabla, tabla[odabrani[2]][odabrani[3]], True)
        if len(za_pojesti) != 0:
            lista_pojedi = lista_pojedi + za_pojesti
        if len(potezi_figurice) != 0:
            moguci_potezi = moguci_potezi + potezi_figurice
        if gl_tabla._obaveznopoj == True and len(lista_pojedi) != 0:
            moguci_potezi = lista_pojedi
        if moguci_potezi == []:
            break
        ispisi_poteze(moguci_potezi)
        indeks = odaberi_potez(len(moguci_potezi))
        odabrani = moguci_potezi[indeks]
        gl_tabla = pomeri_figuru(odabrani[0], odabrani[1], odabrani[2], odabrani[3], gl_tabla, indikator_pojeo, "w")
        gl_tabla.ispisi_tablu()
        #if abs(odabrani[1] - odabrani[3]) == 2:             #proveriiii
            #break
    return True

