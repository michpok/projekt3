import sys
import bs4
import re
import requests
import csv
from requests import get
from functools import reduce
from operator import add

# zpracovani vstupnich informci do listu a kontrola poradi a poctu informaci a jestli hodnota 2 je csv soubor
vstup = []
if len(sys.argv) <= 2:
    print('spatnz pocet vstupu')
    exit()
if len(sys.argv) > 3:
    print('spatnz pocet vstupu')
    exit()

hodnota1 = sys.argv[1]
hodnota2 = sys.argv[2]

vstup.append(hodnota1)
vstup.append(hodnota2)

if 'https://volby.cz/' not in vstup[0]:
    print('spatny vstupni hodnoty')
    exit()
if 'csv' not in vstup[1]:
    print('spatny csv vstup')
    exit()

# extraxe roku voleb
url = vstup[0]
parts = url.split('/')
cisloRok = parts[4]


def posli_pozadavek_get(urll: str) -> str:
    response = requests.get(urll)
    return response.text


# Získej rozdělenou odpověď na požadavek typu GET.
def ziskej_parsovanou_odpoved(odpovedi: str) -> bs4.BeautifulSoup:
    return bs4.BeautifulSoup(odpovedi, features="html.parser")


# Ze zdrojového kódu stránky vyber všechny tagy "tr".
def vyber_tr_tagy(odpoved_serveru: bs4.BeautifulSoup) -> bs4.element.ResultSet:
    return odpoved_serveru.find_all("tr")


# Ze zdrojového kódu stránky vyber všechny tagy "tr". a proved kontrolu vstupni weboveho odkazu
def ziskej_trtagy(trs: bs4.element.ResultSet) -> tuple:
    try:
        kontrol, *trTagy = trs
        kontrola: list = kontrol.get_text().splitlines()
        return kontrola, trTagy
    except ValueError:
        print('spatny web odkaz')
        exit()


def naformatuj_odkaz(cislo0, cislo1, cislo2, cislo3):
    return f"https://volby.cz/pls/{cislo0}/ps311?xjazyk=CZ&xkraj={cislo1}&xobec={cislo2}&xvyber={cislo3}"


def projdi_vsechny_cisla():
    for cisloVyber in webcisla:
        webOdkaz.append(naformatuj_odkaz(cisloRok, cisloKraj[0], cisloVyber, cisloOdkaz[0]))


if __name__ == "__main__":
    url: str = \
        vstup[0]
    odpoved = ziskej_parsovanou_odpoved(posli_pozadavek_get(url))
    kontrola, trTagy = ziskej_trtagy(vyber_tr_tagy(odpoved))

    # extraxe jednotlvivich tagu
    obec = (str(trTagy).split())
    volby = []
    for tag in obec:
        if 'xobec' in tag:
            volby.append(tag)
        if 'xpm' in tag:
            print('zadej web obce ne prebiraciho mista')
            exit()

    # extraxe jendotlivzch cisel obvodu kraje
    cisloKraj = []
    cisloObvod = []
    cisloOdkaz = []

    for cislo in volby:
        extraxeCisla = re.findall(r'\d+', cislo)

    # print(extraxeCisla)
        cisloObvod.append(extraxeCisla[2])
        cisloKraj.append(extraxeCisla[1])
        if len(extraxeCisla) > 4:
            cisloOdkaz.append(extraxeCisla[3])

    webcisla = list(dict.fromkeys(cisloObvod))
    cisloKraj = list(dict.fromkeys(cisloKraj))
    cisloOdkaz = list(dict.fromkeys(cisloOdkaz))

    # extraxce jmen obci
    jmenaObce = []
    index = 1
    odebrani = []

    while index <= len(trTagy) - 1:
        obec = str(trTagy[index].text).split()
        lokace = []

        for nazev in obec:
            if nazev != 'X':
                lokace.append(nazev)
            if 'Obec' in nazev:
                odebrani.append(index - 1)
        if 0 < index:     # odtraneni kodu obce bez pouziti isnum kvuli napr Praha 1
            lokace.pop(0)

        # spojeni slov jmena obce do jednoho elementu
        delim = " "
        spojeni = reduce(add, [x + delim for x in lokace[:-1]] + [lokace[-1]])
        spojene = [spojeni]
        jmenaObce.append(spojene)
        index = index + 1

    # odstraneni elementu 'cislo obce' a 'vyber okresku'
    index = 0
    while index < len(odebrani):
        jmenaObce.pop(odebrani[index] - (2 * index))
        jmenaObce.pop(odebrani[index] - (2 * index))
        index = index + 1

    # tvorba weboveho odkazu
    webOdkaz = []

    projdi_vsechny_cisla()

# tvorba hlavicky a extraxe jmen stran
    adresa = webOdkaz[0]
    odpoved = get(adresa)

    if __name__ == "__main__":
        url: str = \
            adresa
    odpoved = ziskej_parsovanou_odpoved(posli_pozadavek_get(url))
    kontrola, informace = ziskej_trtagy(vyber_tr_tagy(odpoved))

    hlavicka = [['kod'], ['lokace'], ['registrovany volic '], ['obalky'], ['platne hlasy']]
    index = 4
    while index < len(informace):
        strany = str(informace[index].text).split()
        info = []
        index = index + 1
        for popis in strany:
            if popis.isnumeric() is False and popis != 'X':
                info.append(popis)
        info.pop(-1)

        if info[-1] == '0,00':
            info.pop(-1)

        # spojeni slov nazvu stran
        delim = " "
        jmenaStran = reduce(add, [x + delim for x in info[:-1]] + [info[-1]])
        jmenaStran = [jmenaStran]
        hlavicka.append(jmenaStran)

    # zruseni [[]]
    hlavicka = [item for sublist in hlavicka for item in sublist]

    # kompletace dat, ziskani poctu hlasu stran, registrovani vol, obalky, platn0 hlasy
    final = list()
    final.append(hlavicka)
    index = 0
    selekce = [3, 4, 7]

    while index < len(webcisla):
        adresa = webOdkaz[index]
        odpoved = get(adresa)

        if __name__ == "__main__":
            url: str = \
                adresa
            odpoved = ziskej_parsovanou_odpoved(posli_pozadavek_get(url))
            informace = ziskej_trtagy(vyber_tr_tagy(odpoved))

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

        celkoveInformace = []
        for r in selekce:
            celkoveInformace.append(zpracovaneInformace[r])

        # reg. volic, obaka, platny hlas
        cisla = []
        for cislo in celkoveInformace:
            extraxeCisla = re.findall(r'\d+', cislo)
            if len(extraxeCisla) == 2:
                cisla.append(extraxeCisla[1])
            else:
                cisla.append(extraxeCisla[0])

        # pokud cislo > 999
        cisla2 = []
        for cislo in celkoveinformace2:
            extraxeCisla2 = re.findall(r'\d+', cislo)
            cisla2.append(extraxeCisla2[1])

        finalCislo = []
        rada = range(3)
        for cifri in rada:
            if int(cisla2[cifri]) > 0 and cisla[cifri] != cisla2[cifri]:
                finalCislo.append(cisla2[cifri] + cisla[cifri])  # cislo > 999
            else:
                finalCislo.append(cisla[cifri])

        # jednotlive hlasy stran
        vysledky = informace
        Vysledky = str(vysledky).split()
        vysledek = []
        strany = []

        for cisloStran in Vysledky:
            if 'sb3' in cisloStran:
                vysledek.append(cisloStran)

        vysledkyStran = []
        for cislo in vysledek:
            extraxeCisla = re.findall(r'\d+', cislo)
            if len(extraxeCisla) == 3:
                vysledkyStran.append(extraxeCisla[2])

        vysledkyStran.pop(0)  # odstraneni 0,00 z vysledku

        # kompletace dat
        finalInformace = list()
        finalInformace.append(webcisla[index])
        finalInformace.append(finalCislo)
        finalInformace.append(vysledkyStran)
        finalInformace = str(finalInformace).split()

        finalzpracovani = []
        for cislo in finalInformace:
            extraxeCisla = re.findall(r'\d+', cislo)
            finalzpracovani.append(extraxeCisla)

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
