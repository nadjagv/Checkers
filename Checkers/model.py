class Tabla(object):
    def __init__(self):
        self._obaveznopoj = False           #mod == 0 ako nije obavezno pojesti, promena na 1 ako je obavezno pojesti
        self._dim = 8
        self._crni = "b"
        self._crnidama = "B"
        self._beli = "w"
        self._belidama = "W"
        self._crnopolje = " "
        self._belopolje = "-"
        self._tabla = []
        self.postavi_novu_tablu()
        self.brojbelih = 12
        self.brojcrnih = 12

    def napuni(self):
        for i in range(0, self._dim):
            vrsta = []
            for j in range(0, self._dim):
                vrsta.append(self._belopolje)                   #bela polja
            self._tabla.append(vrsta)

    def postavi_novu_tablu(self):
        self.napuni()
        for i in range(0, self._dim):
            for j in range(0, self._dim):
                if (i+j)%2 != 0:
                    if 3 <= i < 5:
                        self._tabla[i][j] = self._crnopolje     #crna polja
                        continue
                    elif i < 3:
                        self._tabla[i][j] = Figura("b", i, j)     #prvi igrac
                        continue
                    self._tabla[i][j] = Figura("w", i, j)         #drugi igrac
        # self._tabla[2][3] = Figura("w", 2, 3)
        # self._tabla[5][4] = Figura("w", 5, 4)
        # self._tabla[6][3] = Figura("w", 6, 3)
        # self._tabla[6][5] = Figura("w", 6, 5)
        # self._tabla[1][2] = Figura("b", 1, 2)
        # self._tabla[0][1] = Figura("b", 0, 1)

        # self._tabla[7][2] = Figura("w", 7, 2)
        # self._tabla[2][3] = Figura("b", 2, 3)
        # self._tabla[4][3] = Figura("b", 4, 3)
        # self._tabla[6][3] = Figura("b", 6, 3)


    def ispisi_tablu(self):
        print("\n")
        print("   A  B  C  D  E  F  G  H")
        for i in range(0, self._dim):
            vrsta = str(i + 1) + "  "
            for j in range(0, self._dim):
                vrsta = vrsta + str(self._tabla[i][j]) + "  "
            print(vrsta)
        print("\n")

    def kraj(self):
        if self.brojbelih==0 or self.brojcrnih==0:
            return True
        elif self.brojbelih >= 7 and self.brojcrnih <= 2:
            return True
        elif self.brojcrnih >= 7 and self.brojbelih <= 2:
            return True
        elif self.brojbelih <=3 and self.brojbelih<=3:
            return True

        return False


class Figura(object):
    def __init__(self, boja, x, y):
        self.x = x
        self.y = y
        self._boja = boja
        self._dama = False
        self._postoji = True
        self._crnopolje = " "

    def gore_desno(self, tabla):
        """
            vraca 0 kada ne moze da se  pomeri, 1 kada moze, 2 kada jede
        """
        if self.x == 0 or self.y == 7:
            return 0
        if tabla[self.x - 1][self.y + 1] == self._crnopolje:
            return 1
        elif tabla[self.x - 1][self.y + 1]._boja == self._boja:
            return 0
        else:
            return self.proveri_pojedi(-1, 1, tabla)

    def gore_levo(self, tabla):
        """
            vraca 0 kada ne moze da se  pomeri, 1 kada moze, 2 kada jede
        """
        if self.x == 0 or self.y == 0:
            return 0
        if tabla[self.x - 1][self.y - 1] == self._crnopolje:
            return 1
        elif tabla[self.x - 1][self.y - 1]._boja == self._boja:
            return 0
        else:
            return self.proveri_pojedi(-1, -1, tabla)

    def dole_desno(self, tabla):
        """
            vraca 0 kada ne moze da se  pomeri, 1 kada moze, 2 kada jede
        """
        if self.x == 7 or self.y == 7:
            return 0
        if tabla[self.x + 1][self.y + 1] == self._crnopolje:
            return 1
        elif tabla[self.x + 1][self.y + 1]._boja == self._boja:
            return 0
        else:
            return self.proveri_pojedi(1, 1, tabla)

    def dole_levo(self, tabla):
        """
            vraca 0 kada ne moze da se  pomeri, 1 kada moze, 2 kada jede
        """
        if self.x == 7 or self.y == 0:
            return 0
        if tabla[self.x + 1][self.y - 1] == self._crnopolje:
            return 1
        elif tabla[self.x + 1][self.y - 1]._boja == self._boja:
            return 0
        else:
            return self.proveri_pojedi(1, -1, tabla)

    def proveri_pojedi(self, smerx, smery, tabla):
        koordinata_x = self.x + 2 * smerx
        koordinata_y = self.y + 2 * smery
        if koordinata_x > 7 or koordinata_y > 7 or koordinata_x < 0 or koordinata_y < 0:
            return 0
        if tabla[koordinata_x][koordinata_y] == self._crnopolje:
            return 2
        else:
            return 0

    def __str__(self):
        if self._dama:
            return self._boja.capitalize()
        return str(self._boja)

    #def __del__(self):
        #return


if __name__ == '__main__':
    tabla = Tabla()
    tabla.postavi_novu_tablu()
    tabla.ispisi_tablu()