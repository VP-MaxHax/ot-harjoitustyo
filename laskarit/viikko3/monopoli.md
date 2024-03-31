```mermaid
 classDiagram
    Monopolipeli "1" -- "2" Noppa
    Monopolipeli "1" -- "1" Pelilauta
    Pelilauta "1" -- "40" Ruutu
    Ruutu "1" -- "1" Ruutu : seuraava
    Ruutu "1" -- "0..8" Pelinappula
    Pelinappula "1" -- "1" Pelaaja
    Pelaaja "2..8" -- "1" Monopolipeli
    Ruutu -- "1" Aloitusruutu
    Ruutu -- "1" Vankila
    Ruutu -- "3" Sattuma
    Ruutu -- "3" Yhteismaa
    Ruutu -- "4" Asemat
    Ruutu -- "2" Laitokset
    Ruutu -- "22" Kadut
    Ruutu -- "1" Vapaapysäköinti
    Ruutu -- "1" Mene vankilaan
    Yhteismaa -- Korttipakka
    Sattuma -- Korttipakka
    Kadut -- "4" Talot
    Kadut -- "1" Hotellit
    Kadut -- Osakkeet
    Asemat -- Osakkeet
    Laitokset -- Osakkeet
    Osakkeet -- Pelaaja
    Talot -- Pelaaja
    Hotellit -- Pelaaja
    Korttipakka -- Pelaaja
```