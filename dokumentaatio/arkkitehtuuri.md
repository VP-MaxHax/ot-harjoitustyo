# Arkkitehtuurikuvaus

## Ohjelman rakenne

Ohjelman arkkitehtuuri noudattaa seuraavaa rakennetta:

![Pakkausrakenne](https://raw.githubusercontent.com/VP-MaxHax/ot-harjoitustyo/master/dokumentaatio/images/pakkausrakenne_vk4.jpg "Pakkausrakenne")

## Sovelluslogiikkaa

Game luokka sisällyttää kaikki pelissä oleva spritet omiin listoihinsa. Nämä kaikki erittäiset listat sisällytetään sitten all sprites listaan jota päivittämällä saadaan helposti päivitettyä kaikki ruudulla näkyvät spritet. Alla oleva kaavio näyttää tämän toimintaa.

```mermaid
 classDiagram
    Player --|> PlayerGroup
    Player : Player sprite
    PlayerGroup : pygame.sprite.Group()"self.players"
    Vampire --|> VampireGroup
    Vampire : Vampire sprite
    VampireGroup : pygame.sprite.Group()"self.Vampires"
    Bullet --|> BulletGroup
    Bullet : Bullet sprite
    BulletGroup : pygame.sprite.Group()"self.Bullets"
    Pickup --|> PickupGroup
    Pickup : Pickup sprite
    PickupGroup : pygame.sprite.Group()"self.Pickups"
    PlayerGroup --|> AllSprites
    VampireGroup --|> AllSprites
    BulletGroup --|> AllSprites
    PickupGroup --|> AllSprites
    AllSprites : pygame.sprite.Group()"self.all_sprites"
    AllSprites --|> UpdateAllSprites
    UpdateAllSprites : self.all_sprites.update()
```

Näistä joukoista tarkistetaan myös niiden väliset osumat (collisions) pygame.sprite.groupcollide() funktion avulla ja sen jälkeen suoritetaan osumasta aktivoituvat tapahtumat.

```mermaid
 classDiagram
    Player --|> PlayerGroup
    Player : Player sprite
    PlayerGroup : pygame.sprite.Group()"self.players"
    Vampire --|> VampireGroup
    Vampire : Vampire sprite
    VampireGroup : pygame.sprite.Group()"self.Vampires"
    Bullet --|> BulletGroup
    Bullet : Bullet sprite
    BulletGroup : pygame.sprite.Group()"self.Bullets"
    Pickup --|> PickupGroup
    Pickup : Pickup sprite
    PickupGroup : pygame.sprite.Group()"self.Pickups"
    PlayerGroup --|> GroupCollidePlayerVampire
    VampireGroup --|> GroupCollidePlayerVampire
    GroupCollidePlayerVampire --|> GameOver
    BulletGroup --|> GroupCollideBulletVampire
    VampireGroup --|> GroupCollideBulletVampire
    GroupCollideBulletVampire --|> VampireDies
    PickupGroup --|> GroupCollidePickupPlayer
    PlayerGroup --|> GroupCollidePickupPlayer
    GroupCollidePickupPlayer --|> GetPickup
    GetPickup : handle_pickup_collisions()
    VampireDies : handle_bullet_hit()
    VampireDies : handle_vampire_hit()
    GameOver : self.gameover()
```

## Tietokantapyyntöjen logiikkaa

Meta päivitysten haku ja niiden asettaminen pelaajahahmolle uuden pelin alussa toimii seuraavalla kaavalla.

```mermaid
 sequenceDiagram
    MainMenu ->> ProfileSelect:Profiilin valinta
    ProfileSelect ->> MainMenu:Palauta profiili
    Player ->> Upgrades:Annetaan muokattava pelaaja olio
    Upgrades ->> MetaUpgrades:Annetaan rajapinta hahmon päivittämiseen
    MainMenu ->> MetaUpgrades:Antaa profiilin
    MetaUpgrades ->> Meta.db:Pyytää profiilin tiedot tietokannasta
    Meta.db ->> MetaUpgrades:Palauttaa profiilin päivitys tiedot
    MetaUpgrades ->> Upgrades:Kutsutaan päivitysfunktioita metatietoja vastaava määrä
    Upgrades ->> Player:Päivittää pelaajan arvoja
```

Meta päivitysten lisääminen voitetun pelin päätteeksi ja näiden lisäysten kirjoitus tietokantaan toimii seuraavalla kaavalla. Tämä siis jatkoa ylemmästä kaaviosta, eli voidaan olettaa että MetaUpgrades luokalla on tiedossa pelin alussa saatu profiili ja tietokannasta haettu meta_status.

```mermaid
 sequenceDiagram
    create participant GameLoop
    create participant MetaUpgrades
    Note right of GameLoop: Peli päättyy voittoon
    GameLoop ->> MetaUpgrades:Välitetään pelajan valitsema päivitys
    Note right of MetaUpgrades: Päivitetään self.meta_status valintaa vastaavaan muotoon
    create participant Meta.db
    MetaUpgrades ->> Meta.db:kirjoitetaan päivitetty meta_status tietokantaan
```