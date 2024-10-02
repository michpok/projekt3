"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie
author: Michal Pokorny
email: my.pokorny@gmail.com
discord: michalpokorny.
"""

import re
from funkce import (vrat_web_odkaz, vrat_tr_tagy, vrat_cislo, hlasy_starn, extraxe_cisel, kopletace_dat,
                    finalni_kompletace, internacional_nebo_nacional, extraxe_jem_obci,
                    vrat_web_odkaz_internacional, preformatovani_csv, info_hlavicka, tvorba_hlavicka,
                    tvorba_csv, kontrola)

# vstupni data / kontrola dat
vstup = kontrola()

# extraxe roku voleb
url = vstup[0]
parts = url.split('/')
cisloRok = parts[4]

# extraxe jednotlvivich tagu
trTagy = vrat_tr_tagy(vstup[0])
obec = (str(trTagy).split())

internacional_nebo_nacional(vstup[0], obec)
volby = internacional_nebo_nacional(vstup[0], obec)[0]

# urci jestli zpracovava vydledky v cr nebo ze sveta
obvod = internacional_nebo_nacional(vstup[0], obec)[1]
index = internacional_nebo_nacional(vstup[0], obec)[2]

# pro ziskani cile rag. volicu obalek a plat hlasu
selekce = internacional_nebo_nacional(vstup[0], obec)[-1]

# extraxe jendotlivzch cisel obvodu kraje a odkazu
cisloKraj = []
cisloObvod = []
cisloOdkaz = []
none = []  # abych mohl pozit stejnou funkci dvakrat
contry = []
svetadil = []
if obvod == 0:
    extraxe_cisel(volby, cisloOdkaz, cisloObvod, cisloKraj, none)
else:
    for cislo in volby:
        zeme = re.search(r'xsvetadil=([A-Z]+)', cislo)
        extraxeCisla = vrat_cislo(cislo)
        if len(extraxeCisla) > 4:
            contry.append(zeme[1])
    extraxe_cisel(volby, cisloOdkaz, cisloObvod, cisloKraj, svetadil)

# extraxce jmen obci
jmenaObce = []
extraxe_jem_obci(obvod, jmenaObce, trTagy)
cisloKraj = list(dict.fromkeys(cisloKraj))

# tvorba weboveho odkazu
if obvod == 0:
    webcisla = list(dict.fromkeys(cisloObvod))
    cisloOdkaz = list(dict.fromkeys(cisloOdkaz))
    webOdkaz = vrat_web_odkaz(webcisla, cisloRok, cisloKraj[0], cisloOdkaz[0])
else:
    webcisla = cisloObvod
    cisloOdkaz = cisloOdkaz  # zeme
    webOdkaz = vrat_web_odkaz_internacional(webcisla[0], cisloRok, cisloKraj[0], cisloOdkaz, svetadil, contry)

    # tvorba hlavicky a extraxe jmen stran
informace = vrat_tr_tagy(webOdkaz[0])
hlavicka = [['kod'], ['lokace'], ['registrovany volic '], ['obalky'], ['platne hlasy']]
tvorba_hlavicka(index, informace, hlavicka)

# zruseni [[]]
hlavicka = [item for sublist in hlavicka for item in sublist]
hlavicka.remove('název')

# kompletace dat, ziskani poctu hlasu stran, registrovani vol, obalky, platne hlasy
final = list()
final.append(hlavicka)
index = 0

while index < len(webcisla):
    informace = vrat_tr_tagy(webOdkaz[index])
    if obvod == 0:
        Informace = str(informace[1]).split()
    else:
        Informace = str(informace[0]).split()

    # reg. volic, obaka, platny hlas
    finalCislo = []
    info_hlavicka(Informace, selekce, finalCislo)

    # jednotlive hlasy stran
    vysledkyStran = []
    hlasy_starn(vysledkyStran, informace)
    vysledkyStran = [s.replace('\xa0', '') for s in vysledkyStran]
    if obvod == 0:
        vysledkyStran.pop(0)  # odtraneni 100.00

    # kompletace dat
    finalInformace = list()
    kopletace_dat(webcisla, finalCislo, vysledkyStran, index, finalInformace)

    finalZpracovani = []
    finalni_kompletace(finalInformace, finalZpracovani, jmenaObce, index)
    finalZpracovani = [item for sublist in finalZpracovani for item in sublist]
    final.append(finalZpracovani)

    # tvorba csv souboru a kladani dat
    data = final
    tvorba_csv(data)

    print('zbyva zpracovat: ', len(webcisla) - index, ' okresku|',
          '|zpracovavam data okresku: ', finalZpracovani[0], ' ', finalZpracovani[1], )
    index = index + 1
print('hotovo || vsechny okresky zpracovany || data jsou nahrany do souboru:', vstup[1])

preformatovani_csv('nove.csv', vstup[1])
