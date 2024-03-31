# Vampire Survivor-like-peli

Sovellus on peli jonka idea on mukailla tämän hetken villitystä Vampire Survivor-like tyylisistä peleistä. 

# Dokumentaatio

[Vaatimusmäärittely](https://github.com/VP-MaxHax/ot-harjoitustyo/blob/master/dokumentaatio/vaatimusm%C3%A4%C3%A4rittely.md)

[Työaikakirjanpito](https://github.com/VP-MaxHax/ot-harjoitustyo/blob/master/dokumentaatio/tuntikirjanpito.md)

[Changelog](https://github.com/VP-MaxHax/ot-harjoitustyo/blob/master/dokumentaatio/changelog.md)

# Asennus

1. Asenna vaaditut riippuvuudet komennolla 
    
        poetry install

2. Käynnistä peli komennolla

        poetry run invoke start

## Muut komentorivi toiminnot

Suorita testit komennolla

    poetry run invoke test

Luo testikattavuusraportti komennolla

    poetry run invoke coverage-report

Suorita pylint tiedoston .pylintrc asetetuilla määreillä

    poetry run invoke lint