import bs4
import requests
from functools import reduce
from operator import add
import re


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