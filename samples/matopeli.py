import pygame
from random import choice, randint

#
# INPUT = ARROW-KEYS TO MOVE AND SPACE TO USE SNAKE'S TONGUE.
#

pygame.init()
leveys = 500
korkeus = 600
display = pygame.display.set_mode((leveys, korkeus))
pygame.display.set_caption("Mato")
clock = pygame.time.Clock()
gameon = False


def inbut():
    global gameon
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            pygame.quit()
            exit()
        if(event.type == pygame.MOUSEBUTTONDOWN):
            for valinta in valinnat:
                if(valinta.valittu):
                    if(valinta.msg == "Uusi peli"):
                        gameon = True
                        peli()
                    elif(valinta.msg == "Lopeta"):
                        pygame.quit()
                        exit()
        if(event.type == pygame.KEYDOWN):
            if(gameon):
                if(event.key == pygame.K_LEFT and mato.xnopeus != 10):
                    mato.xnopeus = -10
                    mato.ynopeus = 0
                if(event.key == pygame.K_RIGHT and mato.xnopeus != -10):
                    mato.xnopeus = 10
                    mato.ynopeus = 0
                if(event.key == pygame.K_UP and mato.ynopeus != 10):
                    mato.ynopeus = -10
                    mato.xnopeus = 0
                if(event.key == pygame.K_DOWN and mato.ynopeus != -10):
                    mato.ynopeus = 10
                    mato.xnopeus = 0
                if(event.key == pygame.K_SPACE):
                    mato.kieli = True
            else:
                if(event.key == pygame.K_m):
                    main()


class Teksti:
    def __init__(self, msg, koko, x, y, vari):
        self.msg = msg
        self.koko = koko
        self.x = x
        self.y = y
        self.vari = vari
        self.valittu = False

    def piirto(self):
        self.teksti = pygame.font.SysFont("Arial", self.koko)
        self.rend = self.teksti.render(self.msg, True, self.vari)

        self.rect = self.rend.get_rect(center=(leveys/2, self.y))
        display.blit(self.rend, self.rect)

    def klik(self):
        mx, my = pygame.mouse.get_pos()
        self.x2, self.y2, self.w, self.h = self.rend.get_rect()
        if(self.y - self.h/2 < my < self.y + self.h/2 and 200 < mx < 400):
            self.vari = (0, 255, 0)
            self.valittu = True
        else:
            self.vari = (0, 0, 0)
            self.valittu = False


valinnat = [Teksti("Uusi peli", 24, 0, 350, (0, 0, 0)),
            Teksti("Lopeta", 24, 0, 450, (0, 0, 0))]


def menukuva():
    x = 100
    y = 200
    for i in range(5):
        pygame.draw.rect(display, (0, 255, 0), [x, y, 40, 40], 4)
        x += 40
    pygame.draw.rect(display, (255, 0, 0), [x+40, y, 40, 40], 4)


def main():
    global mato
    mato = Mato(0, 100)
    while(True):
        display.fill(pygame.Color("white"))
        inbut()
        otsikko = Teksti("Matopeli", 36, 0, 100, (0, 0, 0))
        otsikko.piirto()
        for valinta in valinnat:
            valinta.piirto()
            valinta.klik()
        menukuva()
        clock.tick(30)
        pygame.display.update()


class Mato:
    def __init__(self, x, y):
        self.xnopeus = 0
        self.ynopeus = 0
        self.kokomato = []
        self.paa = pygame.Rect(x, y, 10, 10)
        self.kokomato.append(self.paa)
        self.pituus = 1
        self.kieli = False

    def matopiirto(self):
        for osa in self.kokomato:
            pygame.draw.rect(display, (0, 255, 0), osa, 3)

        if(self.kieli):
            pygame.draw.line(display, (255, 0, 0), self.kielistartPos, self.kieliendPos, 3)
            pygame.draw.circle(display, (255,0,0), self.kieliendPos, 5, 0)
            self.kieli = False

    def matoliiku(self):
        global gameon
        uusipaa = pygame.Rect(self.paa.x + self.xnopeus,
                              self.paa.y + self.ynopeus,
                              10, 10)
        if(uusipaa in self.kokomato and self.ynopeus + self.xnopeus != 0):
            mato.xnopeus = 0
            mato.ynopeus = 0
            gameon = False
            loppu()
        if(uusipaa.x > 490):
            uusipaa.x = 0
        elif(uusipaa.x < 0):
            uusipaa.x = 490
        if(uusipaa.y > 590):
            uusipaa.y = 100
        elif(uusipaa.y < 100):
            uusipaa.y = 590
        self.kokomato.insert(0, uusipaa)

        try:
            omenapaikat.remove([uusipaa.x, uusipaa.y])
        except ValueError:
            pass
        self.paa = uusipaa

        if(len(self.kokomato) > self.pituus):
            omenapaikat.append([self.kokomato[-1].x, self.kokomato[-1].y])
            self.kokomato.pop()

        if(self.kieli):
            if(abs(self.xnopeus) > abs(self.ynopeus)):
                if(self.xnopeus > 0):
                    # oikea
                    self.kielistartPos = [self.paa.x+10, self.paa.y+5]
                    self.kieliendPos = [self.paa.x+50, self.paa.y+5]
                else:
                    # Vasen
                    self.kielistartPos = [self.paa.x, self.paa.y+5]
                    self.kieliendPos = [self.paa.x-40, self.paa.y+5]
            else:
                if(self.ynopeus > 0):
                    # alas
                    self.kielistartPos = [self.paa.x+5, self.paa.y+10]
                    self.kieliendPos = [self.paa.x+5, self.paa.y+50]
                else:
                    # ylos
                    self.kielistartPos = [self.paa.x+5, self.paa.y]
                    self.kieliendPos = [self.paa.x+5, self.paa.y-40]

    def matosyo(self):
        uusiomena = False
        if(self.kieli):
            if(omena.omppu.y-5 < self.kieliendPos[1] < omena.omppu.y+15 and
               omena.omppu.x-5 < self.kieliendPos[0] < omena.omppu.x+15):
                uusiomena = True

        if(self.paa.x == omena.omppu.x and self.paa.y == omena.omppu.y):
            uusiomena = True

        if(uusiomena):
            tmp = choice(omenapaikat)
            omena.omppu = pygame.Rect(tmp[0], tmp[1], 10, 10)
            self.pituus += 1
            if(randint(0, 100) > 80):
                omena.spessu = True
            else:
                omena.spessu = False


class Omena:
    def __init__(self, sijainti, spessu):
        self.omppu = pygame.Rect(sijainti[0], sijainti[1], 10, 10)
        self.spessu = spessu

    def omenapiirto(self):
        if(self.spessu):
            self.vari = (0, 0, 255)
            if(0 < self.omppu.x < 490):
                self.omppu.x += randint(-1, 1)*10
            if(100 < self.omppu.y < 590):
                self.omppu.y += randint(-1, 1)*10
        else:
            self.vari = (255, 0, 0)

        pygame.draw.rect(display, self.vari, self.omppu, 3)


omenapaikat = []
ox = 0
oy = 100
for i in range(50):
    for j in range(50):
        omenapaikat.append([ox, oy])
        ox += 10
    oy += 10
    ox = 0
mato = Mato(0, 100)
omena = Omena(choice(omenapaikat), False)


def tulostaulu():
    pygame.draw.rect(display, (224, 224, 224), [0, 0, 500, 100], 0)
    Teksti("Syödyt omenat: "+str(mato.pituus-1), 18, 0, 10, (0,0,0)).piirto()
    if(omena.spessu):
        Teksti("Voi ei, villi omena!", 24, 0, 40, (0,0,0)).piirto()


def loppu():
    Teksti("PELI LOPPUI", 18, 0, 200, (0,0,0)).piirto()
    Teksti("Paina M-näppäintä palataksesi valikkoon", 18, 0, 250, (0,0,0)).piirto()


def peli():
    global gameon
    while(True):
        display.fill(pygame.Color("white"))
        inbut()
        if(gameon):
            mato.matoliiku()
            mato.matosyo()
            mato.matopiirto()
            omena.omenapiirto()
        else:
            mato.matopiirto()
            loppu()
        tulostaulu()
        clock.tick(10)
        pygame.display.update()


if(__name__ == "__main__"):
    main()
