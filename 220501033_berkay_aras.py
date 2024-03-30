import pygame
import sys
import random

# Savaşçı sınıfı ve türetilmiş sınıflar
class Savasci:
    def __init__(self, isim, kaynak, can, saldiri_menzili):
        self.isim = isim
        self.kaynak = kaynak
        self.can = can
        self.saldiri_menzili = saldiri_menzili

    def saldir(self, hedef):
        pass

class Muhafiz(Savasci):
    def __init__(self):
        super().__init__("Muhafız", 10, 80, (1, 1, 1))

    def saldir(self, hedef):
        hedef.can -= 20

class Okcu(Savasci):
    def __init__(self):
        super().__init__("Okçu", 20, 30, (2, 2, 2))

    def saldir(self, hedef):
        hedef.can -= hedef.can * 0.6

class Topcu(Savasci):
    def __init__(self):
        super().__init__("Topçu", 50, 30, (2, 2, 0))

    def saldir(self, hedef):
        hedef.can = 0

class Atlı(Savasci):
    def __init__(self):
        super().__init__("Atlı", 30, 40, (0, 0, 3))

    def saldir(self, hedef):
        hedef.can -= 30

class Saglikci(Savasci):
    def __init__(self):
        super().__init__("Sağlıkçı", 10, 100, (2, 2, 2))

    def saldir(self, hedef):
        hedef.can += hedef.can * 0.5

# Dünya sınıfı
class Dunya:
    def __init__(self, boyut):
        self.boyut = boyut
        self.matris = [['.' for _ in range(boyut)] for _ in range(boyut)]

    def savasci_yerlestir(self, x, y, savasci):
        self.matris[x][y] = savasci.isim[0].upper()

# Oyuncu sınıfı
class Oyuncu:
    def __init__(self, isim):
        self.isim = isim
        self.kaynak = 200
        self.can = 1
        self.savascilar = []

    def savasci_uret(self, savasci):
        if self.kaynak >= savasci.kaynak:
            self.savascilar.append(savasci)
            self.kaynak -= savasci.kaynak

# Yapay Zeka sınıfı
class YapayZeka(Oyuncu):
    def __init__(self):
        super().__init__("Yapay Zeka")

    def savasci_uret(self, savasci):
        self.savascilar.append(savasci)

# Pygame başlat
pygame.init()

# Ekran boyutu ve renkler
ekran_boyutu = (800, 800)
arka_plan_renk = (255, 255, 255)

# Oyun ekranı oluştur
ekran = pygame.display.set_mode(ekran_boyutu)
pygame.display.set_caption("LORDS OF THE POLYWARPHISM")

# Dünya oluştur
dunya = Dunya(16)  # Örnek olarak 16x16 bir dünya oluşturuldu

# Oyuncuları oluştur
oyuncu1 = Oyuncu("Oyuncu 1")
oyuncu2 = Oyuncu("Oyuncu 2")
yapay_zeka = YapayZeka()

# Muhafızları üret ve yerleştir
oyuncu1.savasci_uret(Muhafiz())
oyuncu2.savasci_uret(Muhafiz())
yapay_zeka.savasci_uret(Muhafiz())

dunya.savasci_yerlestir(0, 0, oyuncu1.savascilar[0])  # Oyuncu 1'in Muhafızı
dunya.savasci_yerlestir(15, 15, oyuncu2.savascilar[0])  # Oyuncu 2'in Muhafızı
dunya.savasci_yerlestir(0, 15, yapay_zeka.savascilar[0])  # Yapay Zeka'nın Muhafızı

# Diğer savaşçıları üret ve yerleştir
oyuncu1.savasci_uret(Okcu())
oyuncu1.savasci_uret(Atlı())
oyuncu2.savasci_uret(Topcu())
oyuncu2.savasci_uret(Okcu())
yapay_zeka.savasci_uret(Atlı())
yapay_zeka.savasci_uret(Saglikci())

dunya.savasci_yerlestir(1, 1, oyuncu1.savascilar[1])  # Okçu
dunya.savasci_yerlestir(2, 2, oyuncu1.savascilar[2])  # Atlı
dunya.savasci_yerlestir(14, 14, oyuncu2.savascilar[1])  # Topçu
dunya.savasci_yerlestir(13, 13, oyuncu2.savascilar[0])  # Okçu
dunya.savasci_yerlestir(1, 15, yapay_zeka.savascilar[0])  # Atlı
dunya.savasci_yerlestir(2, 14, yapay_zeka.savascilar[1])  # Sağlıkçı

# Ana oyun döngüsü
while True:
    # Olayları işle
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Arka planı temizle
    ekran.fill(arka_plan_renk)

    # Dünyadaki savaşçıları ekrana çiz
    for i in range(16):
        for j in range(16):
            if dunya.matris[i][j] != '.':
                pygame.draw.rect(ekran, (0, 0, 0), (50*i, 50*j, 50, 50), 1)  # Hücreyi çiz
                pygame.draw.rect(ekran, (0, 0, 0), (50*i + 5, 50*j + 5, 40,40), 1)  # Hücreyi çiz
                font = pygame.font.Font(None, 36)
                text = font.render(dunya.matris[i][j], True, (0, 0, 0))
                ekran.blit(text, (50*i + 18, 50*j + 18))  # Savaşçı ismini yaz

    # Ekranı güncelle
    pygame.display.flip()
