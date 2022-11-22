<img src="png/reittikartta.png" width="750">

## Aihe

Sovellus on ruutukarttaa hyväksi käyttävä navigaattori, joka löytää parhaan reitin kahden pisteen välillä.  

Kartan jokaisella ruuduilla on tietty painoarvo (esim. välillä 1-9), joka kertoo kustannuksen tai ajan lisäyksen reitin kulkiessa ruudun kautta.  Polku voi kulkea ruutujen välillä käyttäjän valinnan mukaan joko ainoastaan vaaka- ja pystysuoraan tai valinnaisesti myös viistoon ns. väli-ilmansuuntiin.

Polun etsinnän ohella vertaillaan myös algoritmien tehokkuutta toisiinsa nähden.

## Programming language

The program is written in Python (version 3.8.8).  Visualisation and user interface are written using Pygame-library.

## Algorithms and data structures

Route finding is tested with Dijkstra, A*, IDA* ja Jump Point Search algorithms.

## Program inputs

The program generates a grid map or the user can load a map from file.

The user selects start and end points, route finding algorithm and other parameters.

The program shows the calculated route visually.  Path finding can be animated.

## Time and space complexity

Time complexity: O((V + E log V)

Space complexity: O(V)

## Sources

[Dijkstra Wikipedia](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)

[A* Wikipedia](https://en.wikipedia.org/wiki/A*_search_algorithm)

[IDA* Wikipedia](https://en.wikipedia.org/wiki/Iterative_deepening_A*)

[JPS Wikipedia](https://en.wikipedia.org/wiki/Jump_point_search)
