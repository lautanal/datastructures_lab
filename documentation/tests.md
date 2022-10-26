## Testausdokumentti

### Yksikkötestit

Yksikkötestit eivät ole niin tärkeitä tässä sovelluksessa, koska ohjelman toiminta varmistetaan parhaiten vertailemalla visuaalisesti eri menetelmien tuloksia testikartoilla.  Olen kuitenkin tehnyt melko kattavat yksikkötestit, jotka ovat hyödyksi jos ohjelmaan tehdään jatkossa muutoksia.  Käyttöliittymä ja Pygame-piirtorutiinit on jätetty testauksen ulkopuolelle.

Yksikkötestit suoritetaan komennolla: poetry run coverage run --branch -m pytest src

Testikattavuus voidaan raportoida komennolla: poetry run coverage report -m 

Kattavuusraportti:

<img src="/dokumentaatio/png/testikattavuus.png" width="750">

### Empiirinen testaus

Testaus on ollut pääosin kokeilevaa, manuaalista empiiristä testaamista.  Graafinen käyttöliittymä antaa tähän hyvän mahdollisuuden.

Graafinen käyttöliittymä helpottaa huomattavasti ohjelman toiminnan varmistamisessa ja räikeimpien ongelmien selvittämisessä. Esimerkiksi voidaan havaita, poikkeaako laskennan antama "paras" polku merkittävästi silmämääräisesti parhaalta tai lyhimmältä polulta. 

Graafisen käyttöliittymän avulla varmistetaan helposti, että eri algoritmit antavat aina saman lopputuloksen samalla karttapohjalla ja samoilla lähtöarvoilla.

Ottamalla animaatio käyttöön, voidaan lisäksi tarkastella eri algoritmien etenemistä ja mitkä solmut ovat kulloinkin käsittelyssä ja missä järjestyksessä.  

\
<img src="/dokumentaatio/png/testi06a.png" width="750">

### Suorituskyvyn testaus

Suorituskykyä on vertailu eri kokoisilla random-kartoilla.  Paras reitti on haettu samalla kartalla eri menetelmillä.  Suorituskykyvertailun lisäksi on tarkastettu, että menetelmät antavat yhtäpitävät tulokset (polut voivat joskus olla hieman eroavat jos löytyy useampi yhtä hyvä reitti).  Suorituskykytestin tulokset löytyvät toteutusdokumentista.