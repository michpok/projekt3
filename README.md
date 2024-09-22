# projekt3

Tento projekt je zaměřený na získáni zdrojoveho kódu webu jednotlivých obcí v zadaném okrsku a zpracování dat z voleb do Poslanecké sněmovny na stránce Českého statistického úřadu. Projekt dokáže zpracovat výsledky do Poslanecké sněmovy od voleb 2006 až po poslední.

Kromě projekt_3.py je potřeba si spustit soubor funkce.py, který obsahuje uživatelské funkce. Dále před spuštěním je důležité ze souboru requirements.txt nainstalovat do vašeho prostředí potřebné knihovny za pomoci příkazu pip install -r requirements.txt zadaného v terminálu.

Pro spuštění  je potřeba zadat v terminálu nejdřív python projekt.py následně v tomto pořadí webovou adresu v uvozovkách požadované obce a název výstupního csv souboru.
např.: 

python projekt_3.py 'https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6203' zpracovane_data.csv 

Pro ukázku jsem v projekt3 na githubu nahrál zpracovane_data.csv zvýše ukázaného odkazu pro okres Brno-venkov.

