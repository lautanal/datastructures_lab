# Implementation

## Program Structure

The program is written in Python version 3.8.8. using object-oriented methods.  

General structure of the code is:

<img src="png/uml-kaavio.png" width="750">

- Pääohjelma bestroute.py käynnistää Ui-luokan määrittelemän käyttöliittymän
- Ui-luokka luo Pygame-kirjaston avulla graafisen käyttöliittymän
- Ui-luokka luo Map-luokan olion, joka mallintaa ruutukarttaa
- Map luokka luo Node-luokan oliot, jotka mallintavat kartan ruutuja
- Ui luokka luo Algorithm-luokan olion, joka käynnistää polun etsinnän
- Algorithm-luokka kutsuu käyttäjän valinnan mukaan tarvittavaa algoritmia (Dijkstra, A*, IDA* tai JPS)
- Dijkstra-algoritmi käyttää minimikeon tietorakenteena Bheap-luokkaa
- Piirtorutiinit on keskitetty Draw-luokkaan
- Tiedostojen luku ja kirjoitus tehdään Files-luokan avulla
- Suorituskykytestit tehdään Perftest-luokan avulla

## Käytetyt algoritmit ja tietorakenteet

Parhaan reitin hakemisessa on käytetty neljää vaihtoehtoista algoritmia:

### Dijkstra
Dijkstran menetelmä käyttää minimikekoa käsiteltävien solmujen tallennukseen.  Ohjelma ottaa keosta käsittelyyn aina solmun, jonka etäisyysarvo lähtösolmusta on pienin.  Tässä ohjelmassa minimikeko on toteutettu omalla Bheap-luokalla.

### A*
A* -menetelmä on hyvin samankaltainen Dijkstran menetelmän kanssa.  Lisäksi käytössä on  heuristiikka, joka ennustaa etäisyyden maaliin.  A* -menetelmän minimikeko on toteutettu Pythonin standardikirjaston heapq-moduulin avulla.

### IDA*
IDA* -menetelmä yhdistää A*-menetelmään syvyyshaun.  Syvyyshaku etenee käsiteltävästä solmusta syvemmälle verkkoon kunnes saavutetaan ennalta määritelty hakukynnys. Seuraavalla hakukierroksella jatketaan solmusta, jolla on pienin hakukynnyksen ylittävä arvo.  IDA* -menetelmän minimikeko on toteutettu Pythonin standardikirjaston heapq-moduulin avulla.

### Jump Point Search
JPS-menetelmä soveltuu polun etsintään kun kyseessä on painottamaton verkko (kaikki ruudut saman arvoisia) ja viistoon siirtymät polussa on sallittu.  Se voi nopeuttaa laskentaa huomattavasti kun tarpeettomien solmujen käsittely voidaan ohittaa.

## Suorituskykyvertailu ja aikavaativuudet

Suorituskykytestit on tehty eri kokoisilla random-kartoilla.  Paras reitti on haettu kullakin kartalla kaikilla soveltuvilla eri menetelmillä. 

### Painotetut kartat

Kullakin ruudulla on painoarvo, joka kertoo ajan tai kustannuksen reitin kulkiessa ruudun kautta.  Reitti voi kulkea ruutujen välillä vain vaaka- ja pystysuoraan.

Verkon koko | Solmut | Kaaret | V + E log V | Algoritmi | Hakuajan keskiarvo (10 karttaa)|
--------|--------|--------|--------|-------------|-------------|
| 100 x 100 | 10000 | 19800 | 273097 | Dijkstra | 0.0896 |
| | | | | A\* | 0.0367 |
| | | | | IDA\* | 0.5331 |
| 200 x 200 | 40000 | 79600 | 1256902 | Dijkstra | 0.3970 |
| | | | | A\*     | 0.1560 |
| | | | | IDA\*   | 3.9088 |
| 300 x 300 | 90000 | 179400 | 2042500 | Dijkstra | 0.9518 |
| | | | | A\*     | 0.3692 |
| | | | | IDA\*   | 13.3590 |
| 400 x 400 | 160000 | 319200 | 5678238 | Dijkstra | 1.7554 |
| | | | | A\*      | 0.6370 |
| | | | | IDA\*    | 29.5708 |
| 500 x 500 | 250000 | 499000 | 9197853 | Dijkstra | 2.8174  |
| | | | | A\*     | 1.0455  |
| | | | | IDA\*   | 56.3359 |


### Painottamattomat kartat

Kartan ruudut ovat saman arvoisia ja polku voi kulkea viistoon ruutujen välillä.

Verkon koko | Solmut | Kaaret | V + E log V | Algoritmi | Hakuajan keskiarvo (10 karttaa)|
--------|--------|--------|--------|-------------|-------------|
| 100 x 100 | 10000 | 39402 | 533562 | Dijkstra | 0.1218 |
| | | | | A\* | 0.0508 |
| | | | | IDA\* | 0.5023 |
| | | | | JPS | 0.0357 |
| 200 x 200 | 40000 | 158802 | 2467719 | Dijkstra | 0.5343 |
| | | | | A\*     | 0.2319 |
| | | | | IDA\*   | 5.5076 |
| | | | | JPS | 0.2637 |
| 300 x 300 | 90000 | 358202 | 5985159 | Dijkstra | 1.2569 |
| | | | | A\*     | 0.5283 |
| | | | | IDA\*   | 18.9459 |
| | | | | JPS | 0.7785 |
| 400 x 400 | 160000 | 637602 | 11182680 | Dijkstra | 2.3001 |
| | | | | A\*      | 0.9362 |
| | | | | IDA\*    | 51.8285 |
| | | | | JPS | 1.6054 |
| 500 x 500 | 250000 | 997002 | 18127810 | Dijkstra | 3.6767  |
| | | | | A\*     | 1.4412  |
| | | | | IDA\*   | 109.4129 |
| | | | | JPS | 2.6955 |


### Aikavaativuudet

Mitatut Dijkstran, A\*- ja JPS-menetelmien aikavaativuudet vastaavat hyvin teorian mukaista O(V + E logV) aikavaativuutta.

<img src="/dokumentaatio/png/aikavaativuus2b.png" width="750">

A\* -menetelmä on melkein kautta linjan nopein vaikka painotetussa verkossa heuristiikka ei toimikaan parhaalla mahdollisella tavalla.  Dijkstran menetelmä toimii myös melko hyvin, mutta IDA\* ei näytä olevan hyvä ratkaisija tämän tapaisissa verkoissa.  JPS-menetelmä toimii hyvin silloin, kun sitä voi käyttää.

## Puutteet ja parannukset

JPS-menetelmää ei voi käyttää painotetussa ruutuverkossa.  JPS-menetelmä edellyttää myös, että vinot siirtymät karttaruutujen välillä sallitaan.

IDA*-algoritmi ei ilmeisesti ole parhaimmillaan tämänkaltaisten ruutukarttojen reitinlaskennassa.  Suorituskykyä pystyisi todennäköisesti parantamaan ottamalla käyttöön erilaisia tarkistuksia ja optimointeja.

Pygame-kirjaston animaatio on toisinaan melko hidas.  En ole ehtinyt perehtyä, mistä tämä johtuu.  Todennäköisesti sitä pystyy nopeuttamaan huomattavasti.

