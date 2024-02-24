import pygame
import random

class ReaktioPeli:
    def __init__(self):
        pygame.init()
        self.aloitusnaytto()
    
    # Määritetään pelin aloitusnäyttö, asetetaan ruudun koko, ikkunan otsikko, tekstien fontit, ikkunan keskipisteet myöhempää tekstien
    # keskittämistä varten.
        
    def aloitusnaytto(self):
        self.nayton_leveys, self.nayton_korkeus = 960, 720
        self.naytto = pygame.display.set_mode((self.nayton_leveys, self.nayton_korkeus))
        self.isofontti = pygame.font.SysFont("Arial", 48) 
        self.fontti = pygame.font.SysFont("Arial", 24)
        self.keskipiste_x = self.nayton_leveys // 2
        self.keskipiste_y = self.nayton_korkeus // 2
        pygame.display.set_caption("Reaktiopeli - Aloitusnäyttö")
        self.kello = pygame.time.Clock()

        aloita_nappi = pygame.Rect(350, 200, 250, 50)
        tulostaulukko_nappi = pygame.Rect(350, 400, 250, 50)

        # Luodaan aloitus ruutu näkyviin, asetetaan pohjaväriksi valkoinen sekä luodaan painikkeet itse pelille, sekä tulostaulukon avaamista
        # varten. 

        while True:
            self.naytto.fill((255, 255, 255))
            pygame.draw.rect(self.naytto, (0, 0, 0), aloita_nappi)
            pygame.draw.rect(self.naytto, (0, 0, 0), tulostaulukko_nappi)

            aloita_teksti = self.fontti.render("Aloita peli", True, (255, 255, 255))
            tulostaulukko_teksti = self.fontti.render("Tulostaulukko", True, (255, 255, 255))
            pelin_sammutus_teksti = self.fontti.render("ESC = Lopeta peli", True, (255, 0, 0))

            self.naytto.blit(aloita_teksti, (aloita_nappi.x + 90, aloita_nappi.y + 10))
            self.naytto.blit(tulostaulukko_teksti, (tulostaulukko_nappi.x + 75, tulostaulukko_nappi.y + 10))
            self.naytto.blit(pelin_sammutus_teksti, (800, self.nayton_korkeus - 25))

            # Tehdään määritys jos pelaaja painaa ESC - näppäintä tai painaa ikkunan kiinni ruksista. Sekä ohjataan koodia eteenpäin jos painetaan
            # Aloita peli tai tulostaulukko nappia.

            for tapahtuma in pygame.event.get():
                if tapahtuma.type == pygame.QUIT:
                    exit()
                if tapahtuma.type == pygame.KEYDOWN:
                    if tapahtuma.key == pygame.K_ESCAPE:
                        exit()
                if tapahtuma.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = tapahtuma.pos

                    if aloita_nappi.collidepoint(mouse_pos):
                        self.peli()
                    elif tulostaulukko_nappi.collidepoint(mouse_pos):
                        self.tulostaulukko_naytto()

            pygame.display.update()
            self.kello.tick(60)
    
    # Alustetaan ruutu, mikä tulee, kun pelin häviää.

    def pelin_paattymis_naytto(self):
        pygame.display.set_caption("Reaktiopeli - Hävisit!")
        self.naytto.fill((0,0,0))
        teksti = self.isofontti.render("Hävisit pelin", True, (255,0,0))
        self.naytto.blit(teksti, (self.keskipiste_x - teksti.get_width() // 2,self.keskipiste_y - teksti.get_height() // 2))
        pisteteksti = self.fontti.render(f"Pisteesi: {self.pisteet}", True, (255,0,0))
        self.naytto.blit(pisteteksti, (self.keskipiste_x - pisteteksti.get_width() // 2, self.keskipiste_y - pisteteksti.get_height() // 2 + 75))
        ohjeteksti = self.fontti.render("Paina ESC näppäintä jatkaaksesi", True, (255,0,0))
        self.naytto.blit(ohjeteksti, (self.keskipiste_x - ohjeteksti.get_width() // 2, self.keskipiste_y - ohjeteksti.get_height() // 2 + 150))
        
        # Päättymisruutuun päästyä pisteet merkitään tekstitiedostoon funktion lisaa_tulos avulla. Myöhemmässä vaiheessa merkityt pisteet saadaan
        # merkittyä pelissä käytettävään tulostaulukkoon. 

        self.lisaa_tulos(f'Pisteet: {self.pisteet}')

        pygame.display.update()
        while True:
            for tapahtuma in pygame.event.get():
                if tapahtuma.type == pygame.QUIT:
                    exit()
                if tapahtuma.type == pygame.KEYDOWN:
                    if tapahtuma.key == pygame.K_ESCAPE:        # Kun ESC nappia painetaan, palaa pelaaja takaisin aloitus ruutuun
                        self.aloitusnaytto()


    # Alustetetaan ruutu, josta voidaan lukea ennätyspisteet.
    # Ruudulle listautuu 10 parasta tulosta.
    
    def tulostaulukko_naytto(self):
        pygame.display.set_caption("Reaktiopeli - Tulostaulukko")
        self.naytto.fill((255, 255, 255))
        tulokset = self.lue_tulokset()      # Haetaan tulokset tiedostosta "tulokset.txt" erillisen funktion avulla.
        tulokset.sort(key=lambda x: int(x.split(": ")[1]), reverse=True)
        parhaat_tulokset = tulokset[:10]

        teksti =  self.fontti.render("Ennätystulokset", True, (255,0,0))
        self.naytto.blit(teksti, (self.keskipiste_x - teksti.get_width() // 2, 50))
        y = 100
        for indeksi, tulos in enumerate(parhaat_tulokset):      # Otetaan parhaat tulokset listalta tulokset
            teksti = self.fontti.render(tulos, True, (0,0,0))   # ja tehdään niistä kirjoitettavat tekstit
            x = self.keskipiste_x - teksti.get_width() // 2     # tulos taulukkoon.
            self.naytto.blit(teksti, (x, y))
            y += 30
        pygame.display.update()
        while True:
            for tapahtuma in pygame.event.get():
                if tapahtuma.type == pygame.QUIT:
                    exit()
                if tapahtuma.type == pygame.KEYDOWN:
                    if tapahtuma.key == pygame.K_ESCAPE:
                        self.aloitusnaytto()

    # Luetaan tekstitiedoston sisältä pisteet ja palautetaan erilinen lista tuloksista.

    def lue_tulokset(self):
        try:
            with open("tulokset.txt", "r") as tiedosto:
                tulokset = tiedosto.readlines()
            tulokset = [tulos.strip() for tulos in tulokset]
            return tulokset
        except FileNotFoundError:
            return []
    
    # Lisätään saadut pisteet tiedostoon pelin päätteksi.

    def lisaa_tulos(self, tulos):
        with open("tulokset.txt", "a") as tiedosto:
            tiedosto.write(tulos + "\n")

    # Määritetään peli. Peli funktiossa ei itsessään ole mitään muuta, kuin ruudun koon määritys.
    # Pelifunktio kutsuu muita funktioita, joiden avulla peli toimii.            

    def peli(self):
        self.naytto = pygame.display.set_mode((960, 720))
        self.lataa_kuvat()
        self.uusi_peli()
        self.suorita()

    # Ladataan robo kuva (olisi voinut lisätä vaan yhtenä rivinä kohdassa missä roboa tarvitaan, mutta
    # jos kuvia olisi enemmän käytössä, olisi helpompi se tehdä funktion avulla)

    def lataa_kuvat(self):
        self.kuvat = [pygame.image.load(nimi + ".png") for nimi in ["robo"]]

    def uusi_peli(self):
        pygame.display.set_caption("Reaktiopeli")
        self.pisteet = 0    # Asetetaan pisteet 0
        self.reagointiaika = 5.0    # Pelin alku reagointiaika = 5 sec
        self.reagoitu_aika = pygame.time.get_ticks() / 1000 # muutetaan reagoitu aika sekunneiksi.
        self.varit = [(255,255,255), (255,192,203), (135,206,250), (152, 251, 152), (221,160,221), (225, 250, 205), (250,128,114), (64, 224, 208)]      # Pelissä vaihtuu näytön väri mitä enemmmän pisteitä saa. Helpoiten vaihdon saa tehtyä asettamalla värit listaan.
        self.vari_indexi = 0    # Aloiteteaan indeksi 0, jolloin näytön väri on aina aluksi valkoinen.
        self.robotti()      # Luodaan robotti peliin


    def robotti(self):
        self.robo = self.kuvat[0]   # Valitaan robotin kuva listalta, jonka lataa_kuvat funktio loi
        self.robo_leveys, self.robo_korkeus = self.robo.get_size()    # Hankitaan robotin koko pygamen get_size komennolla
        self.robo_x = random.randint(0, 960 - self.robo_leveys)       # Määritetään robolle satunnaiset pisteet, jossa se esiintyy ruudulla.
        self.robo_y = random.randint(0, 720 - self.robo_korkeus)

    def tutki_tapahtumat(self):
        for tapahtuma in pygame.event.get():
            if tapahtuma.type == pygame.MOUSEBUTTONDOWN:
                self.kasittele_hiiren_painallus(tapahtuma)      # Tarkistetaan eri funktion avulla hiiren klikkaus
            elif tapahtuma.type == pygame.QUIT:
                exit()
            elif tapahtuma.type == pygame.KEYDOWN:
                if tapahtuma.key == pygame.K_ESCAPE:
                    self.aloitusnaytto()

        # Jos pelaaja ei onnistu klikkaamaa robottia tarpeeksi nopeasti, peli päättyy.
        if self.nyt - self.reagoitu_aika > self.reagointiaika:
            self.pelin_paattymis_naytto()

    # Asetetaan koordinaatti pisteet kohdalle, jota pelaaja klikkaa. tarkistetaan osuu_roboon funtkiolla, onko klikattu piste sama, missä robotti on. 
    # Jos klikattu piste on sama, kutstutaan paivita.peli funktiota.

    def kasittele_hiiren_painallus(self, tapahtuma):
        self.kohde_x, self.kohde_y = tapahtuma.pos
        if hasattr(self, 'robo') and self.osuu_roboon():
            self.paivita_peli()

    # Verrataan pisteitä ja palautetaan True/False arvo.

    def osuu_roboon(self):
        return (self.robo_x < self.kohde_x < self.robo_x + self.robo_leveys and
                self.robo_y < self.kohde_y < self.robo_y + self.robo_korkeus)

    # Jos pelaaja osui roboon, päivitetään koodia niin että lisätään 1 piste, lasketaan reagointi aikaa, 
    # tarkastetaan pistemäärää sekä vaihdetaan robon paikkaa.  
    # Joka tasakymppi pistemäärällä pelin pohjaväri vaihtuu aikasemmin määriteltyihin väreihin.

    def paivita_peli(self):
        self.pisteet += 1
        self.reagointiaika *= 0.97
        self.reagoitu_aika = self.nyt
        if self.pisteet % 10 == 0:
            self.vaihda_vari()
        self.robotti()

    def vaihda_vari(self):
        self.vari_indexi = (self.vari_indexi + 1) % len(self.varit)
        self.naytto.fill(self.varit[self.vari_indexi])

    # Piirretään pelinäytölle kaikki tarvittava. Teksti jossa kerrotaan sen hetkinen pelaajan pistemäärä,
    # teksti jossa kerrotaan pelin lopettamisesta sekä robon piirtäminen ruutuun. 

    def piirra_naytto(self):
        self.naytto.fill(self.varit[self.vari_indexi])
        teksti = self.fontti.render("Pisteet: " + str(self.pisteet), True, (255, 0, 0))
        self.naytto.blit(teksti, (25, self.nayton_korkeus - 25))
        teksti = self.fontti.render("ESC = Sulje peli", True, (255, 0, 0))
        self.naytto.blit(teksti, (800, self.nayton_korkeus - 25))
        if hasattr(self, 'robo'):
            self.naytto.blit(self.robo, (self.robo_x, self.robo_y))
        pygame.display.flip()
        self.kello.tick(60)

    # Pääkomento, mikä kutsuu funktiot tutki_tapahtumat sekä piirra_naytto peliä varten.

    def suorita(self):
        while True:
            self.nyt = pygame.time.get_ticks() / 1000
            self.tutki_tapahtumat()
            self.piirra_naytto()

if __name__ == "__main__":
    peli = ReaktioPeli()
    peli.suorita()
