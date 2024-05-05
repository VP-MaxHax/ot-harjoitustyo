# Testausdokumentti

Sovellusta testataan kattavasti automatisoiduilla testeillä, sekä joitakin erikoistilanteita on käyty läpi myös manuaalisesti.

## Yksikkötestaus

**Entities** ja **gameloop** luokilla on kattavahkot testit. Nämä olivat sovelluksen mutkikkaimmat osat testata, koska suurin osa näistä toteutetaan pygamen sisällä eivätkä anna mitään selvää ylosantoa testattavaksi. Joihinkin funtioihin piti jälkeenpäin lisätä joku testattava arvo, että saatiin selkeitä testituloksia. Projektin edetessä kuitenkin kehitin hyviä ja mmonipuolisia tapoja testatakaseni näitä funtioita.

**Meta upgrades** testaus hoidetaan laajalti meta.db:ssä olevan 'test' käyttäjän avulla jonka arvoja muokataan funtioilla ja verrataan oletettuun tulokseen näiden muokkausten jälkeen. testien aikana tämä testikäyttäjä poistetaan ja lisätään tietokantaan toistuvasti. Uuden tietokannan luomista testataan myös luomalla test.db tietokanta.

**Profile select** testataan myös kattavasti. Ainoa jota ei testata on ohjelmasta poistuminen. Tämä koska pygamen poistumisessa käytettävä sys.exit() komento postuu myös testauksesta jos tätä kutsutaan kesken testien. Joihinkin aikasempiin vastaaviin kohtiin olen keksinyt jonkun kierto tavan, mutta tähän en jaksanut alkaa säätämään, koska en näe tämän testausta tarpeelliseksi. Tähän testejä tehdessäni keksin käyttää simulate_key_press(): funtiota joka injektoi napin painalluksen suoraa pygame events listaan. Tämä olisi tullut käyttöö muuallakin, mutta muilta osin olin aikalailla jo testit tehnyt kun keksin käyttää tätä täällä.

**Upgrades** testataan kokonaan. Tämä oli helpoin luokka suorittaa testit, koska jokainen funktio muokkaa jotain arvoa tai antaa ulos jonkin arvon.

## Manuaalitestaus

Olen myös itse käyttänyt sovellusta ja korjannut vastaan tulleita vikoja siinä. Koodikatselmoinnissa annetussa palautteessa tuli myös ilmi jotain vikoja joita korjailin jossain määrin.

## Testikattavuus

Sovelluksen kokonais testikattauvvun on projektin lopussa 75%. Alla olevassa kuvassa näkyy miten tämä jakautuu.

![Testikattavuusraportti](https://raw.githubusercontent.com/VP-MaxHax/ot-harjoitustyo/master/dokumentaatio/images/testikattavuusraportti.jpg "Testikattavuusraportti")