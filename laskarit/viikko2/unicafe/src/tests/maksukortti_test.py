import unittest
from maksukortti import Maksukortti

class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(1000)

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)

    def test_maksukortti_saldo_alussa_oikein(self):
        self.assertEqual(self.maksukortti.saldo, 1000)

    def test_maksukortin_saldo_tulostus_euroissa_oikein(self):
        self.assertEqual(self.maksukortti.saldo_euroina(), 10)
    
    def test_maksukortin_saldon_sanallinen_tulostus_oikein(self):
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 10.00 euroa")

    def test_saldon_lisääminen_kasvattaa_saldoa_oikein(self):
        self.maksukortti.lataa_rahaa(500)

        self.assertEqual(self.maksukortti.saldo, 1500)

    def test_saldon_ottaminen_vahentaa_oikein(self):
        self.maksukortti.ota_rahaa(400)

        self.assertEqual(self.maksukortti.saldo, 600)

    def test_kortilta_ei_voi_ottaa_yli_saldon(self):
        self.maksukortti.ota_rahaa(1500)

        self.assertEqual(self.maksukortti.saldo, 1000)

    def test_saldon_ottaminen_paluttaa_oikean_boolin(self):
        palautusarvo = self.maksukortti.ota_rahaa(400)

        self.assertEqual(palautusarvo, True)

    def test_saldon_yliottaminen_paluttaa_oikean_boolin(self):
        palautusarvo = self.maksukortti.ota_rahaa(1500)

        self.assertEqual(palautusarvo, False)

    