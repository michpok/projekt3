import bs4
import requests
from functools import reduce
from operator import add
from bs4 import BeautifulSoup
import re
import csv


def posli_pozadavek_get(urll: str) -> str:
    response = requests.get(urll)
    return response.text


# Získej rozdělenou odpověď na požadavek typu GET.
def ziskej_parsovanou_odpoved(odpovedi: str) -> bs4.BeautifulSoup:
    return bs4.BeautifulSoup(odpovedi, features="html.parser")


# Ze zdrojového kódu stránky vyber všechny tagy "tr".
def vyber_tr_tagy(odpoved_serveru: bs4.BeautifulSoup) -> bs4.element.ResultSet:
    return odpoved_serveru.find_all("tr")


# Ze zdrojového kódu stránky vyber všechny tagy "tr".
# a proved kontrolu vstupni weboveho odkazu
def ziskej_trtagy(trs: bs4.element.ResultSet) -> tuple:
    try:
        kontrol, *trTagy = trs
        kontrola: list = kontrol.get_text().splitlines()
        return kontrola, trTagy
    except ValueError:
        print('spatny web odkaz')
        exit()


def vrat_web_odkaz(webcisla, rok, kraj, odkazi):
    odkaz = []
    for cisloVyber in webcisla:
        odkaz.append(naformatuj_odkaz(rok, kraj, cisloVyber, odkazi))
    return odkaz


def naformatuj_odkaz(cislo0, cislo1, cislo2, cislo3):
    return f"https://volby.cz/pls/{cislo0}/ps311?xjazyk=CZ&xkraj={cislo1}&xobec={cislo2}&xvyber={cislo3}"


def vrat_web_odkaz_internacional(webcisla, rok, kraj, odkazi, zeme, svet):
    odkaz = []
    for odka, zem, sveti in zip(odkazi, zeme, svet):

        odkaz.append(naformatuj_odkaz_internaacional(rok, kraj, webcisla, odka, zem, sveti))
    return odkaz


def naformatuj_odkaz_internaacional(cislo0, cislo1, cislo2, cislo3, cislo4, slovo):
    return (f"https://www.volby.cz/pls/{cislo0}/ps311?xjazyk=CZ&xkraj={cislo1}&xobec={cislo2}&xsvetadil={slovo}&xzeme="
            f"{cislo3}&xokrsek={cislo4}")


# vrati tr tagy z html
def vrat_tr_tagy(vstup):
    url: str = vstup
    odpoved = ziskej_parsovanou_odpoved(posli_pozadavek_get(url))
    kontrola, tagy = ziskej_trtagy(vyber_tr_tagy(odpoved))
    return tagy


# kontrola spravnosti delek v stupnich dat
def kontola_delek(data1, data2):
    if data1 > data2:
        print('spatnz pocet vstupu')
        exit()


# kontrola spravnosti poradi v stupnich dat
def kontrola_vstupu(string, data, text):
    if string not in data:
        print(text)
        exit()


# spoje slova v listu napr:[[ahoj Tondo]] -> [ahoj Tondo]
def spojeni_listu(spoj, data):
    delim = spoj
    spojeni = reduce(add, [x + delim for x in data[:-1]] + [data[-1]])
    spojene = [spojeni]
    return spojene


# vycisti z listu vse krome cisel
def vrat_cislo(cislo):
    return re.findall(r'\d+', cislo)


def zpracovani_tagu(listz, tr_split):
    for tag in tr_split:
        if 'xobec' in tag:
            listz.append(tag)
        if 'xpm' in tag:
            print('zadej web obce ne prebiraciho mista')
            exit()
    return listz


def extraxe_cisel(data, odkaz, obvod, kraj, svetadil):
    for cislo in data:
        extraxe = vrat_cislo(cislo)
        if len(extraxe) > 4:
            odkaz.append(extraxe[3])
            obvod.append(extraxe[2])
            kraj.append(extraxe[1])
            svetadil.append(extraxe[4])
    return odkaz, obvod, kraj, svetadil


def tvorba_hlavicka(index, informace, hlavicka):
    while index < len(informace):
        strany = str(informace[index].text).split()

        index = index + 1
        strany.pop(-1)
        strany.pop(-1)
        strany.pop(-1)
        strany.pop(0)
        if len(strany) > 1:
            hlavicka.append(spojeni_listu(' ', strany))
        else:
            hlavicka.append(strany)
    return hlavicka


def ziskani_inf_hlavicka(informace, zpracovane, celkove):
    for k in informace:
        if '</td>' in k:
            zpracovane.append(k)
        if 'sa2' in k:
            celkove.append(k)
        if 'sa3' in k:
            celkove.append(k)
        if 'sa6' in k:
            celkove.append(k)
    return zpracovane, celkove


def ziskani_inf_hlavicka_zpracovani_stovky(celkove, cisla):
    for cislo in celkove:
        extraxe = vrat_cislo(cislo)
        if len(extraxe) == 2:
            cisla.append(extraxe[1])
        else:
            cisla.append(extraxe[0])
    return cisla


def ziskani_inf_hlavicka_zpracovani_tisice(celkove, cisla):
    for cislo in celkove:
        extraxe2 = vrat_cislo(cislo)
        cisla.append(extraxe2[1])
    return cisla


def ziskani_inf_hlavicka_zpracovani_kompletace(cisla, cisla2, final):
    rada = range(3)
    for cifri in rada:
        if int(cisla2[cifri]) > 0 and cisla[cifri] != cisla2[cifri]:
            final.append(cisla2[cifri] + cisla[cifri])  # cislo > 999
        else:
            final.append(cisla[cifri])
    return final


def tvorba_csv(data):
    with open("nove.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(data)


# zpracuje tr tag tak ze vyjme jednotlive vysledky stran
def hlasy_starn(stran, informace):
    soup = BeautifulSoup(str(informace), 'html.parser')
    vysledky = soup.find_all('td')

    for cisloStran in vysledky:
        if 'sb3"' in str(cisloStran):
            stran.append(cisloStran.get_text())
    return stran


# zpracuje tr tag tak ze vyjme znich jmena obci/ jmena mest(zahranici)
def nazvy_obci(index, tr, jmena, klic):
    while index < len(tr):
        obec = str(tr[index])  # str(trTagy[index].text).split()
        soup = BeautifulSoup(obec, 'html.parser')

        # Nalezení elementu <td> s hodnotou "Brusel" (je ve druhém <td> s headers="s3")
        if klic == "s3":
            obec_td = soup.find('td', headers=klic)
        else:
            obec_td = soup.find('td', klic)

        # Získání textu z nalezeného <td> elementu
        jmena.append(obec_td.text if obec_td else 'None')

        index = index + 1
    return jmena


def kopletace_dat(web, finalc, stran, indexi, listi):

    listi.append(web[indexi])
    listi.append(finalc)
    listi.append(stran)
    listi = str(listi).split()
    return listi


def finalni_kompletace(informace, zpracovani, obce, indexi):
    for cislo in str(informace).split():
        zpracovani.append(vrat_cislo(cislo))
    nazvy = spojeni_listu(" ", str(obce[indexi]).split())
    zpracovani.insert(1, nazvy)
    return zpracovani