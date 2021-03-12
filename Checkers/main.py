from model import *
from korisnik import *
from kompjuter import *
from time import time


def ispisi_stanje(gl_tabla):
    print("Broj belih: " + str(gl_tabla.brojbelih))
    print("Broj crnih: " + str(gl_tabla.brojcrnih))
    print("\n")


def odaberi_mod_igre():
    while True:
        try:
            mod = eval(input("Odabrati tip igre:\n 1 - obavezno pojesti\n 2 - nije obavezno pojesti "))
            if mod != 1 and mod !=2:
                print("Proveriti unos!")
                continue
            elif mod == 1:
                return True
            return False
        except:
            print("Proveriti unos!")


def main():
    gl_tabla = Tabla()
    gl_tabla._obaveznopoj = odaberi_mod_igre()
    gl_tabla.ispisi_tablu()
    while True:

        odigraoK = korisnik_igra(gl_tabla)
        if odigraoK == False:
            print("Pat pozicja. Igra je završena.")
        if gl_tabla.kraj():
            print("Igra je završena. Pobedili ste!")
            break
        ispisi_stanje(gl_tabla)

        print("Računar je na potezu.")
        start = time()
        gl_tabla, odigraoR, pojeden = minmax_main(gl_tabla)
        if odigraoK == False:
            print("Pat pozicja. Igra je završena.")
        if gl_tabla == None:
            print("Igra je završena. Pobedili ste!")
            break
        gl_tabla.ispisi_tablu()
        end = time()
        print("Vreme izvršavanja: {}".format(str(end - start)))
        if pojeden != 0:
            print("Broj pojedenih figura: " + str(pojeden))
        ispisi_stanje(gl_tabla)
        if gl_tabla.kraj():
            print("Igra je završena. Računar je pobedio.")
            break


if __name__ == '__main__':
    main()