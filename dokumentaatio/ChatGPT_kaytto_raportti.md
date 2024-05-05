# Selvitys ChatGPT:n käytöstä sovellusta tehdessä

## Yleiskatsaus

Käytin projektin alussa ChatGPT:tä luodakseni perustan projektille. Tämä tarkoittaa siis lopullisessa muodossa tiedostoja **entities.py**, **gameloop.py**. Lisäsin näihin kyllä tämän jälkeen jotain omaakin toiminnallisuutta.

**profile_select.py** on myös laajalti ChatGPT tuotosta. 

**meta_upgrades.py** tietokantapyynnöt ja tietokannan luonti kyselyt/komennot kysyin myös ChatGPT:ltä. Muuten tietokanta logiikka on itseni luomaa.

**upgrades.py** on kokonaan omaa käsialaani.

## Yksityiskohtaisempaa läpikäyntiä

### entities.py 

90% ChatGPT tekemä. Tein jotain muokkauksia testejä tehdessäni sekä pylint virheisiin liittyviä muokkauksia.

### gameloop.py

**ChatGPT:** __init__, setup_vampire_spawn(), draw(), find_closest_vampire(), handle_events(), spawn_vampire(), update_sprites(), check_collisions(), handle_pickup_collisions(), handle_bullet_hit(), handle_vampire_hit().

**Oma tekemä:** simulate_key_press(), draw_levelup(), level_up_check_event(), draw_levelup_choices(), upgrade_choices(), run(), winner(), draw_metaupgrade_choices(), draw_meta_upgrades(), check_meta_event(), gameover(), check_gameover_events(), update_score_display(), handle_levelup().

Loppujenlopuksi tämän osalta näyttöisi olevan aika 50/50. Kaikki pelin perustoiminnallisuudet ovat ChatGPT käsialaa ja kaikki jälkeenpäin lisätyt (lvlup, gameover, voitto, meta päivitykset) ovat minun itseni kehityksen aikana tekemiä.

### mainmenu.py

It's all me. 😎

### meta_upgrades.py

Selvitin ChatGPT:ltä kuinka käyttää SQLiteä pythonilla (yhteydet kursorit yms.) näiden pohjalta suunnitelin itse tietokantapyyntöjen logiikan. Kaikki tietokanta pyynnöt ja tietokantojen luonti (CRATE TABLE, SELECT, UPDATE, INSERT, DELETE) oikeat kirjoitusasut selvitetty ChatGPT kautta.

### profile_select.py

Melko suoraa ChatGPT kopioitu. Hieman piti viilata rajapintaa mainmenun kanssa, että sain palauttamaan profiilin oikein.

### upgrades.py

Ainoa mikä tässä piti katsoa ChatGPT oli random.sample() toiminnallisuus. Muuten kaikki on itseni ideoimaa ja tekemää.

## Testit

Kaikki testit ja niihin liittyvä lisätty toiminnallisuus ovat itseni kirjoittamia enkä käyttänyt näissä ChatGPTtä apuna.

## Yhteenveto

Sanoisin että koko projektista noin 50% on ChatGPT tekemää ja toiset 50% omaa tuotostani. Tällä jaolla minun kuitenkin piti itsenikin ymmärtää kaikki mitä ChatGPT toiminnallisuutta sovelluksessa oli, että sain itse kirjoitetun osani projektista toimimaan sen kanssa.

Voin kuitenkin myöntää etten ikinä olisi saanut näin laajaa projektia tehtyä tässä aikataulussa, ellen olisi käyttänyt ChatGPT:tä apuna.