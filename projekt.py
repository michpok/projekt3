"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie
author: Michal Pokorny
email: my.pokorny@gmail.com
discord: michalpokorny.
"""
import sys
from bs4 import BeautifulSoup
import csv
from funkce import (vrat_web_odkaz, vrat_tr_tagy,
                    kontrola_vstupu, spojeni_listu, vrat_cislo,
                    kontola_delek,)

# zpracovani vstupnich informci do listu a kontrola poradi
# a poctu informaci a jestli hodnota 2 je csv soubor
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
volby = []
for tag in obec:
    if 'xobec' in tag:
        volby.append(tag)
    if 'xpm' in tag:
        print('zadej web obce ne prebiraciho mista')
        exit()

    # extraxe jendotlivzch cisel obvodu kraje a odkazu
cisloKraj = []
cisloObvod = []
cisloOdkaz = []
for cislo in volby:
    extraxeCisla = vrat_cislo(cislo)
    cisloObvod.append(extraxeCisla[2])
    cisloKraj.append(extraxeCisla[1])
    if len(extraxeCisla) > 4:
        cisloOdkaz.append(extraxeCisla[3])
# odstraneni duplicitnich elementu
webcisla = list(dict.fromkeys(cisloObvod))
cisloKraj = list(dict.fromkeys(cisloKraj))
cisloOdkaz = list(dict.fromkeys(cisloOdkaz))

# extraxce jmen obci
jmenaObce = []
odebrani = []
index = 1
while index <= len(trTagy) - 1:
    obec = str(trTagy[index].text).split()
    lokace = []

    for nazev in obec:
        if nazev != 'X':
            lokace.append(nazev)
        # priprava na odtraneni nevzhovujicich dat
        if 'Výběr' in nazev:
            odebrani.append(index - 1)
    if 0 < index:     # odtraneni kodu obce bez pouziti isnum kvuli napr Praha 1
        lokace.pop(0)
    index = index + 1

    # spojeni slov jmena obce do jednoho elementu
    jmenaObce.append(spojeni_listu(" ", lokace))

# odstraneni elementu 'cislo obce' a 'vyber okresku'
index = 0
while index < len(odebrani):
    jmenaObce.pop(odebrani[index] - (2 * index))
    jmenaObce.pop(odebrani[index] - (2 * index))
    index = index + 1

# tvorba weboveho odkazu
webOdkaz = vrat_web_odkaz(webcisla, cisloRok, cisloKraj[0], cisloOdkaz[0])

# tvorba hlavicky a extraxe jmen stran
informace = vrat_tr_tagy(webOdkaz[0])
hlavicka = [['kod'], ['lokace'], ['registrovany volic '], ['obalky'], ['platne hlasy']]
index = 4
oznaceni = 0
while index < len(informace):
    strany = str(informace[index].text).split()
    info = []
    index = index + 1

    for popis in strany:
        if popis.isnumeric() is False and popis != 'X':
            info.append(popis)
    if info[-1] == '-':
        info.pop(-1)
    if info[-1].isalpha() is False:
        info.pop(-1)
    if 'hlasy' in info:
        oznaceni = index
    if 'TOP' in info:
        info.append('09')
    if 'ANO' in info:
        info.append('2011')
    if 'volba' in info:
        info.append('2016')

    # spojeni slov nazvu stran
    hlavicka.append(spojeni_listu(" ", info))
hlavicka.pop(oznaceni)
hlavicka.pop(oznaceni)

# zruseni [[]]
hlavicka = [item for sublist in hlavicka for item in sublist]

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
    for k in Informace:
        if '</td>' in k:
            zpracovaneInformace.append(k)
        if 'sa2' in k:
            celkoveinformace2.append(k)
        if 'sa3' in k:
            celkoveinformace2.append(k)
        if 'sa6' in k:
            celkoveinformace2.append(k)
    # odstraneni dupliciti obalek
    celkoveInformace = []
    for r in selekce:
        celkoveInformace.append(zpracovaneInformace[r])

    # reg. volic, obaka, platny hlas
    cisla = []
    for cislo in celkoveInformace:
        extraxeCisla = vrat_cislo(cislo)
        if len(extraxeCisla) == 2:
            cisla.append(extraxeCisla[1])
        else:
            cisla.append(extraxeCisla[0])

    # pokud cislo > 999 hledam cifry tisicu
    cisla2 = []
    for cislo in celkoveinformace2:
        extraxeCisla2 = vrat_cislo(cislo)
        cisla2.append(extraxeCisla2[1])

    finalCislo = []
    rada = range(3)
    for cifri in rada:
        if int(cisla2[cifri]) > 0 and cisla[cifri] != cisla2[cifri]:
            finalCislo.append(cisla2[cifri] + cisla[cifri])  # cislo > 999
        else:
            finalCislo.append(cisla[cifri])

    # jednotlive hlasy stran
    soup = BeautifulSoup(str(informace), 'html.parser')
    vysledky = soup.find_all('td')

    vysledkyStran = []
    for cisloStran in vysledky:
        if 'sb3"' in str(cisloStran):
            vysledkyStran.append(cisloStran.get_text())

    vysledkyStran = [s.replace('\xa0', '') for s in vysledkyStran]
    vysledkyStran.pop(0)  # odtraneni 100.00

    # kompletace dat
    finalInformace = list()
    finalInformace.append(webcisla[index])
    finalInformace.append(finalCislo)
    finalInformace.append(vysledkyStran)
    finalInformace = str(finalInformace).split()

    finalzpracovani = []
    for cislo in finalInformace:
        finalzpracovani.append(vrat_cislo(cislo))

    finalzpracovani.insert(1, jmenaObce[index])
    finalzpracovani = [item for sublist in finalzpracovani for item in sublist]
    final.append(finalzpracovani)

    # tvorba csv souboru a kladani dat
    data = final
    with open("nove.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(data)

    with open("nove.csv", newline="") as csvfile:
        csv_data = csv.reader(csvfile, delimiter=" ")

    print('zbyva zpracovat: ', len(webcisla) - index, ' okresku|',
          '|zpracovavam data okresku: ', finalzpracovani[0], ' ', finalzpracovani[1], )
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