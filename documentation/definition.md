<img src="png/reittikartta.png" width="750">

## Aihe

Sovellus on ruutukarttaa hyväksi käyttävä navigaattori, joka löytää parhaan reitin kahden pisteen välillä.  

Kartan jokaisella ruuduilla on tietty painoarvo (esim. välillä 1-9), joka kertoo kustannuksen tai ajan lisäyksen reitin kulkiessa ruudun kautta.  Polku voi kulkea ruutujen välillä käyttäjän valinnan mukaan joko ainoastaan vaaka- ja pystysuoraan tai valinnaisesti myös viistoon ns. väli-ilmansuuntiin.

Polun etsinnän ohella vertaillaan myös algoritmien tehokkuutta toisiinsa nähden.

## Ohjelmointikieli

Ohjelmointikielenä käytetään Pythonia (versio 3.8.8).  Visualisointi ja käyttöliittymä toteutetaan Pygame-kirjaston avulla.

## Algoritmit ja tietorakenteet

Polunetsinnän nopeutta testataan ainakin usealla eri algoritmilla, joita ovat Dijkstran perinteinen, A*, IDA* ja Jump Point Search.

## Ohjelman syötteet ja tulosteet

Ohjelma generoi itse ruutukartan tai käyttäjä voi ladata tiedostosta kartan.

Käyttäjä valitsee graafisen käyttöliittymän kautta reitin lähtö- ja maaliruudut sekä käytetyn algoritmin ja muut tarvittavat parametrit.  Graafisen käyttöliittymän kautta voidaan myös lisätä läpäisemättömiä esteitä kartalle.

Ohjelma näyttää polun visuaalisesti.  Polun haku voidaan animoida realiaikaisesti.

## Aika- ja tilavaativuudet

Aikavaatimus: O((V + E log V)

Tilavaatimus: O(V)

## Lähteet

[Dijkstra Wikipedia](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)

[A* Wikipedia](https://en.wikipedia.org/wiki/A*_search_algorithm)

[IDA* Wikipedia](https://en.wikipedia.org/wiki/Iterative_deepening_A*)

[JPS Wikipedia](https://en.wikipedia.org/wiki/Jump_point_search)

## Opinto-ohjelma

Tietojenkäsittelyn kandidaatti

## Dokumentaation kieli

Suomi
