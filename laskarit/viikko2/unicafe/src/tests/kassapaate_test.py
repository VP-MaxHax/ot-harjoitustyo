import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()
        self.maksukortti = Maksukortti(1000)

    def test_kassa_alustuksessa_oikea_rahamaara(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_kassan_rahamaaran_tulostus_euroina_oikein(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)

    def test_kassan_myytyjen_edullisten_annosten_alustus_oikein(self):
        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_kassan_myytyjen_maukkaiden_annosten_alustus_oikein(self):
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_kassan_saldo_kasvaa_edullisen_annoksen_maksussa(self):
        self.kassapaate.syo_edullisesti_kateisella(500)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100240)

    def test_kassan_saldo_kasvaa_maukkaan_annoksen_maksussa(self):
        self.kassapaate.syo_maukkaasti_kateisella(500)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100400)

    def test_oikea_vaihtoraha_edullisen_annoksen_maksussa(self):
        vaihtoraha = self.kassapaate.syo_edullisesti_kateisella(500)
        self.assertEqual(vaihtoraha, 260)

    def test_oikea_vaihtoraha_maukkaan_annoksen_maksussa(self):
        vaihtoraha = self.kassapaate.syo_maukkaasti_kateisella(500)
        self.assertEqual(vaihtoraha, 100)

    def test_edulllisten_lounauden_maara_kasvaa_edullisen_annoksen_maksussa(self):
        self.kassapaate.syo_edullisesti_kateisella(240)
        self.assertEqual(self.kassapaate.edulliset, 1)

    def test_maukkaiden_lounauden_maara_kasvaa_maukkaan_annoksen_maksussa(self):
        self.kassapaate.syo_maukkaasti_kateisella(400)
        self.assertEqual(self.kassapaate.maukkaat, 1)

    def test_edulllisten_lounauden_maara_ei_kasva_maukkaan_annoksen_maksussa(self):
        self.kassapaate.syo_edullisesti_kateisella(240)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_maukkaiden_lounauden_maara_ei_kasva_edullisen_annoksen_maksussa(self):
        self.kassapaate.syo_maukkaasti_kateisella(400)
        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_kassan_saldo_ei_kasvaa_edullisen_annoksen_maksussa_riittämättömällä_käteisellä(self):
        self.kassapaate.syo_edullisesti_kateisella(200)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_kassan_saldo_ei_kasva_maukkaan_annoksen_maksussa_riittämättömällä_käteisellä(self):
        self.kassapaate.syo_maukkaasti_kateisella(350)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_oikea_vaihtoraha_edullisen_annoksen_maksussa(self):
        vaihtoraha = self.kassapaate.syo_edullisesti_kateisella(200)
        self.assertEqual(vaihtoraha, 200)

    def test_oikea_vaihtoraha_maukkaan_annoksen_maksussa(self):
        vaihtoraha = self.kassapaate.syo_maukkaasti_kateisella(350)
        self.assertEqual(vaihtoraha, 350)

    def test_edulllisten_lounauden_maara_ei_kasva_edullisen_annoksen_maksussa_riittämättömällä_käteisellä(self):
        self.kassapaate.syo_edullisesti_kateisella(200)
        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_maukkaiden_lounauden_maara_ei_kasva_maukkaan_annoksen_maksussa_riittämättömällä_käteisellä(self):
        self.kassapaate.syo_maukkaasti_kateisella(350)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_kortin_saldo_vahenee_edullisen_annoksen_maksussa(self):
        self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)
        self.assertEqual(self.maksukortti.saldo, 760)

    def test_kortin_saldo_vahenee_maukkaan_annoksen_maksussa(self):
        self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti)
        self.assertEqual(self.maksukortti.saldo, 600)

    def test_palautusarvo_oikea_edullisen_annoksen_maksussa(self):
        osto_onnistui = self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)
        self.assertEqual(osto_onnistui, True)

    def test_palautusarvo_oikea_maukkaan_annoksen_maksussa(self):
        osto_onnistui = self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti)
        self.assertEqual(osto_onnistui, True)

    def test_edulllisten_lounauden_maara_kasvaa_edullisen_annoksen_maksussa_kortilla(self):
        self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)
        self.assertEqual(self.kassapaate.edulliset, 1)

    def test_maukkaiden_lounauden_maara_kasvaa_maukkaan_annoksen_maksussa_kortilla(self):
        self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti)
        self.assertEqual(self.kassapaate.maukkaat, 1)

    def test_kortin_saldo_ei_vahene_edullisen_annoksen_maksussa_kun_saldo_ei_riita(self):
        self.maksukortti = Maksukortti(200)
        self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)
        self.assertEqual(self.maksukortti.saldo, 200)

    def test_kortin_saldo_ei_vahene_maukkaan_annoksen_maksussa_kun_saldo_ei_riita(self):
        self.maksukortti = Maksukortti(200)
        self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti)
        self.assertEqual(self.maksukortti.saldo, 200)

    def test_palautusarvo_oikea_edullisen_annoksen_maksussa_kun_saldo_ei_riita(self):
        self.maksukortti = Maksukortti(200)
        osto_onnistui = self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)
        self.assertEqual(osto_onnistui, False)

    def test_palautusarvo_oikea_maukkaan_annoksen_maksussa_kun_saldo_ei_riita(self):
        self.maksukortti = Maksukortti(200)
        osto_onnistui = self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti)
        self.assertEqual(osto_onnistui, False)

    def test_edulllisten_lounauden_maara_ei_kasva_edullisen_annoksen_maksussa_kortilla_kun_saldo_ei_riita(self):
        self.maksukortti = Maksukortti(200)
        self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)
        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_maukkaiden_lounauden_maara_ei_kasva_maukkaan_annoksen_maksussa_kortilla_kun_saldo_ei_riita(self):
        self.maksukortti = Maksukortti(200)
        self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_kassassa_oleva_saldo_ei_kasva_kortilla_ostettaessa_edullista_ateriaa(self):
        self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_kassassa_oleva_saldo_ei_kasva_kortilla_ostettaessa_maukasta_ateriaa(self):
        self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_korttia_ladatessa_rahat_kassan_saldo_kasvaa(self):
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, 500)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100500)

    def test_korttia_ladatessa_rahat_kortin_saldo_kasvaa(self):
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, 500)
        self.assertEqual(self.maksukortti.saldo, 1500)

    def test_kortille_ei_voi_ladata_negatiivista_summaa(self):
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, -500)
        self.assertEqual(self.maksukortti.saldo, 1000)

    def test_kassan_saldo_ei_muutu_kun_kortille_ladataan_negatiivista_summaa(self):
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, -500)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)