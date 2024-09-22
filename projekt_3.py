"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie
author: Michal Pokorny
email: my.pokorny@gmail.com
discord: michalpokorny.
"""

import re
import sys
import csv
from funkce import (vrat_web_odkaz, vrat_tr_tagy, kontrola_vstupu, vrat_cislo,
                    kontola_delek, vrat_web_odkaz_internacional, zpracovani_tagu,
                    extraxe_cisel, tvorba_hlavicka, ziskani_inf_hlavicka,
                    ziskani_inf_hlavicka_zpracovani_stovky, ziskani_inf_hlavicka_zpracovani_tisice,
                    ziskani_inf_hlavicka_zpracovani_kompletace, tvorba_csv,
                    hlasy_starn, nazvy_obci, kopletace_dat, finalni_kompletace)

kontola_delek(3, len(sys.argv))
kontola_delek(len(sys.argv), 3)

vstup = [sys.argv[1], sys.argv[2]]

kontrola_vstupu('https://', vstup[0], 'spatny vstupni hodnoty')
kontrola_vstupu('.csv', vstup[1], 'spatny csv vstup')

# extraxe roku voleb
url = vstup[0]
parts = url.split('/')
cisloRok = parts[4]


# extraxe jednotlvivich tagu
trTagy = vrat_tr_tagy(vstup[0])
obec = (str(trTagy).split())

# vnitro statni
if 'xnumnuts' in vstup[0]:
    volby = []
    zpracovani_tagu(volby, obec)

    # extraxe jendotlivzch cisel obvodu kraje a odkazu
    cisloKraj = []
    cisloObvod = []
    cisloOdkaz = []
    none = []
    extraxe_cisel(volby, cisloOdkaz, cisloObvod, cisloKraj, none)

    # odstraneni duplicitnich elementu
    webcisla = list(dict.fromkeys(cisloObvod))
    cisloKraj = list(dict.fromkeys(cisloKraj))
    cisloOdkaz = list(dict.fromkeys(cisloOdkaz))

    # extraxce jmen obci
    jmenaObce = []
    odebrani = []
    index = 1
    klic = "overflow_name"
    nazvy_obci(index, trTagy, odebrani, klic)
    for jmena in odebrani:
        if 'None' not in jmena:
            jmenaObce.append(jmena)

    # tvorba weboveho odkazu
    webOdkaz = vrat_web_odkaz(webcisla, cisloRok, cisloKraj[0], cisloOdkaz[0])

    # tvorba hlavicky a extraxe jmen stran
    informace = vrat_tr_tagy(webOdkaz[0])
    hlavicka = [['kod'], ['lokace'], ['registrovany volic '], ['obalky'], ['platne hlasy']]
    index = 4
    tvorba_hlavicka(index, informace, hlavicka,)

    # zruseni [[]]
    hlavicka = [item for sublist in hlavicka for item in sublist]
    hlavicka.remove('název')

    # kompletace dat, ziskani poctu hlasu stran, registrovani vol, obalky, platne hlasy
    final = list()
    final.append(hlavicka)
    index = 0
    selekce = [3, 4, 7]

    while index < len(webcisla):
        informace = vrat_tr_tagy(webOdkaz[index])
        Informace = str(informace[1]).split()
        zpracovaneInformace = []
        celkoveinformace2 = []
        ziskani_inf_hlavicka(Informace, zpracovaneInformace, celkoveinformace2)

        # odstraneni dupliciti obalek
        celkoveInformace = []
        for r in selekce:
            celkoveInformace.append(zpracovaneInformace[r])

        # reg. volic, obaka, platny hlas
        cisla = []
        ziskani_inf_hlavicka_zpracovani_stovky(celkoveInformace, cisla)

        # pokud cislo > 999 hledam cifry tisicu
        cisla2 = []
        ziskani_inf_hlavicka_zpracovani_tisice(celkoveinformace2, cisla2)

        finalCislo = []
        ziskani_inf_hlavicka_zpracovani_kompletace(cisla, cisla2, finalCislo)

        # jednotlive hlasy stran
        vysledkyStran = []
        hlasy_starn(vysledkyStran, informace)
        vysledkyStran = [s.replace('\xa0', '') for s in vysledkyStran]
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

# internacional
else:
    volby = ['']
    zpracovani_tagu(volby, obec)
    volby.pop(0)

    # extraxe jendotlivzch cisel obvodu kraje a odkazu
    cisloKraj = []
    cisloObvod = []
    cisloOdkaz = []
    contry = []
    stetadil = []
    for cislo in volby:
        a = re.search(r'xsvetadil=([A-Z]+)', cislo)
        extraxeCisla = vrat_cislo(cislo)
        if len(extraxeCisla) > 4:
            contry.append(a[1])
    extraxe_cisel(volby, cisloOdkaz, cisloObvod, cisloKraj, stetadil)

    # odstraneni duplicitnich elementu
    webcisla = cisloObvod
    cisloKraj = list(dict.fromkeys(cisloKraj))
    cisloOdkaz = cisloOdkaz  # zeme

    # extraxce jmen obci
    jmenaObce = []
    index = 0
    klic = "s3"
    nazvy_obci(index, trTagy, jmenaObce, klic)

    # tvorba weboveho odkazu
    webOdkaz = vrat_web_odkaz_internacional(webcisla[0], cisloRok, cisloKraj[0], cisloOdkaz, stetadil, contry)

    # tvorba hlavicky a extraxe jmen stran
    informace = vrat_tr_tagy(webOdkaz[0])
    hlavicka = [['kod'], ['lokace'], ['registrovany volic '], ['obalky'], ['platne hlasy']]
    index = 3
    tvorba_hlavicka(index, informace, hlavicka)

    # zruseni [[]]
    hlavicka = [item for sublist in hlavicka for item in sublist]
    hlavicka.remove('název')

    # kompletace dat, ziskani poctu hlasu stran, registrovani vol, obalky, platne hlasy
    final = list()
    final.append(hlavicka)
    index = 0
    selekce = [0, 1, 4]

    while index < len(webcisla):
        informace = vrat_tr_tagy(webOdkaz[index])
        Informace = str(informace[0]).split()
        zpracovaneInformace = []
        celkoveinformace2 = []
        ziskani_inf_hlavicka(Informace, zpracovaneInformace, celkoveinformace2)

        # odstraneni dupliciti obalek
        celkoveInformace = []
        for r in selekce:
            celkoveInformace.append(zpracovaneInformace[r])

        # reg. volic, obaka, platny hlas
        cisla = []
        ziskani_inf_hlavicka_zpracovani_stovky(celkoveInformace, cisla)

        # pokud cislo > 999 hledam cifry tisicu
        cisla2 = []
        ziskani_inf_hlavicka_zpracovani_tisice(celkoveinformace2, cisla2)

        finalCislo = []
        ziskani_inf_hlavicka_zpracovani_kompletace(cisla, cisla2, finalCislo)

        # jednotlive hlasy stran
        vysledkyStran = []
        hlasy_starn(vysledkyStran, informace)
        vysledkyStran = [s.replace('\xa0', '') for s in vysledkyStran]

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

input_file = 'nove.csv'
output_file = vstup[1]

# formatovani vzstupu, zarovnani do sloupcu
with open(input_file, 'r', newline='') as infile:
    reader = csv.reader(infile)
    rows = list(reader)

# Určeni maximální šířky každého
column_widths = [max(len(str(item)) for item in col) for col in zip(*rows)]

# Prepsani do noveho souboru
with open(output_file, 'w', newline='') as outfile:
    writer = csv.writer(outfile)
    for row in rows:
        aligned_row = [str(item).ljust(width) for item, width in zip(row, column_widths)]
        writer.writerow(aligned_row)