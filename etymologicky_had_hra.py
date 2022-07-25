import pyglet

from pyglet.window import key
from pyglet import gl
from random import randrange, choice, shuffle
from data import data, data_napl

zakladni_ctverec = (64, 64)
window = pyglet.window.Window(width=zakladni_ctverec[0]*20, height=zakladni_ctverec[0]*10, caption = "Etymologický had")


# nacitani obrazku
obrazek_had = pyglet.image.load("tail-head.png")
obrazek_had_hlava_dolu = pyglet.image.load("tail-head_hlava_dolu.png")
obrazek_had_hlava_nahoru = pyglet.image.load("tail-head_hlava_nahoru.png")
obrazek_had_hlava_vpravo = pyglet.image.load("tail-head_hlava_vpravo.png")
obrazek_had_hlava_vlevo = pyglet.image.load("tail-head_hlava_vlevo.png")
obrazek_a = pyglet.image.load("acko.png")
obrazek_b = pyglet.image.load("becko.png")
obrazek_c = pyglet.image.load("cecko.png")
ramecek_zeleny = pyglet.image.load("okenko_zelene.png")
ramecek_cerveny = pyglet.image.load("okenko_cervene.png")
ramecek_uvodni = pyglet.image.load("okenko_uvodni.png")

def nakresli_obdelnik(x1, y1, x2, y2):
    gl.glBegin(gl.GL_TRIANGLE_FAN)   # zacni kreslit spojene trojuhelniky
    gl.glVertex2f(int(x1), int(y1))  # vrchol A
    gl.glVertex2f(int(x1), int(y2))  # vrchol B
    gl.glVertex2f(int(x2), int(y2))  # vrchol C, nakresli trojuhelnik ABC
    gl.glVertex2f(int(x2), int(y1))  # vrchol D, nakresli trojuhelnik BCD
    gl.glEnd()  # ukonci kresleni trojuhelniku

# definovani trid
class Stav_hry:
    def __init__(self, souradnice):
        self.souradnice = souradnice
        self.smer = 0
        self.stav = 0
    
class Odpoved:
    def __init__(self, slovo):
        self.slovo = slovo

    def lokace(self):  # proc to je podtrzene?!
        self.lokace = randrange(3)
        return self.lokace

class Vyber():
    def novy_vyber(self):
        otazka, text_odpoved_a, text_odpoved_b, text_odpoved_c, etymologie, spatne, odpoved_a, odpoved_b, odpoved_c, seznam_obrazky  = hra()
        self.otazka = otazka
        self.text_odpoved_a = text_odpoved_a
        self.text_odpoved_b = text_odpoved_b
        self.text_odpoved_c = text_odpoved_c
        self.etymologie = etymologie
        self.spatne = spatne
        self.odpoved_a = odpoved_a
        self.odpoved_b = odpoved_b
        self.odpoved_c = odpoved_c
        self.seznam_obrazky = seznam_obrazky

class Seznam():
    def plneni(self):
        self.seznam = list(data_napl)

stav = [-1]
spoustim = [0]
seznam = Seznam()
seznam.plneni()
odpoved_spravna_lokace = [0]
odpoved_a_souradnice = [0,0]
odpoved_b_souradnice = [0,0]
odpoved_c_souradnice = [0,0]
skore = [0]

# zakladni poloha hada
zakladni_souradnice_had = [(0,0), (zakladni_ctverec[0],0), (zakladni_ctverec[0]*2, 0), (zakladni_ctverec[0]*3, 0), (zakladni_ctverec[0]*4, 0), (zakladni_ctverec[0]*5, 0), (zakladni_ctverec[0]*6, 0)]
had = Stav_hry(zakladni_souradnice_had)

# vybirani aktualniho slova a odpovedi  
def vybirani():
    shuffle(seznam.seznam)
    aktualni = seznam.seznam.pop()
    mozne_odpovedi = ["anglického", "praslovanského", "ruského", "řeckého", "praindoevropského", "latinského", "arabského", "perského", "indického", "italského", "malajského", "kečuánského", "laponského"]   
    aktualni_jazyk = aktualni["jazyk"]
    if aktualni_jazyk in mozne_odpovedi:
        mozne_odpovedi.remove(aktualni_jazyk)
    aktualni_slovo = aktualni["slovo"]
    spravna = aktualni["jazyk"]
    spatna_1 = choice(mozne_odpovedi)
    mozne_odpovedi.remove(spatna_1)
    spatna_2 = choice(mozne_odpovedi)

    return aktualni, aktualni_slovo, spravna, spatna_1, spatna_2

def klavesa(symbol, modifikatory):
    if symbol == key.UP:
        had.smer = "nahoru"
    if symbol == key.DOWN:
        had.smer = "dolů"
    if symbol == key.LEFT:
        had.smer = "vlevo"
    if symbol == key.RIGHT:
        had.smer = "vpravo"
    if symbol == key.ENTER:
        spoustim[0] = "ano"
    if symbol == key.SPACE:
        spoustim[0] = "od začátku"
        skore[0] = 0
    if symbol == key.S:
        stav[0] = 0
        
   
def pohyb(t):
    if stav[0] == 1 and spoustim[0] == "ano":
        if len(seznam.seznam) == 0 and skore[0] < 20:
            stav[0] = 3
        elif len(seznam.seznam) == 0 and skore[0] >= 20:
            stav[0] = 4
        else:
            nova_napln.novy_vyber()
            had.smer = 0  # tohle smazat, když chci, aby se had hýbal hned po přepnutí na nové slovo - je to tak krapet těžší bo může rychle sežrat odpověď
            stav[0] = 0
            spoustim[0] = 0

    if len(had.souradnice) == 3:
        stav[0] = 2

    if stav[0] == 2 and spoustim[0] == "od začátku":
        seznam.plneni()
        had.smer = 0
        had.souradnice = [(0,0), (zakladni_ctverec[0],0), (zakladni_ctverec[0]*2, 0), (zakladni_ctverec[0]*3, 0), (zakladni_ctverec[0]*4, 0), (zakladni_ctverec[0]*5, 0), (zakladni_ctverec[0]*6, 0)]
        nova_napln.novy_vyber()
        stav[0] = 0
        spoustim[0] = 0
    if stav[0] == 3 and spoustim[0] == "od začátku":
        seznam.plneni()
        had.smer = 0
        had.souradnice = [(0,0), (zakladni_ctverec[0],0), (zakladni_ctverec[0]*2, 0), (zakladni_ctverec[0]*3, 0), (zakladni_ctverec[0]*4, 0), (zakladni_ctverec[0]*5, 0), (zakladni_ctverec[0]*6, 0)]
        nova_napln.novy_vyber()
        stav[0] = 0
        spoustim[0] = 0
    if stav[0] == 4 and spoustim[0] == "od začátku":
        seznam.plneni()
        had.smer = 0
        had.souradnice = [(0,0), (zakladni_ctverec[0],0), (zakladni_ctverec[0]*2, 0), (zakladni_ctverec[0]*3, 0), (zakladni_ctverec[0]*4, 0), (zakladni_ctverec[0]*5, 0), (zakladni_ctverec[0]*6, 0)]
        nova_napln.novy_vyber()
        stav[0] = 0
        spoustim[0] = 0

    if stav[0] == 0:   
        x = had.souradnice[-1][0]
        y = had.souradnice[-1][1]

        if had.smer == "nahoru" and had.souradnice[-1][1] < window.height - (120 + 2*obrazek_had.height):
            y = y + zakladni_ctverec[0]  
            del had.souradnice[0]
            had.souradnice.append((x,y))      
        elif had.smer == "dolů" and had.souradnice[-1][1] > 0:
            y = y - zakladni_ctverec[0]         
            del had.souradnice[0]
            had.souradnice.append((x,y))   
        elif had.smer == "vpravo" and had.souradnice[-1][0] < window.width - obrazek_had.width:
            x = x + zakladni_ctverec[0]  
            del had.souradnice[0]
            had.souradnice.append((x,y))   
        elif had.smer == "vlevo" and had.souradnice[-1][0] > 0:
            x = x - zakladni_ctverec[0]  
            del had.souradnice[0]
            had.souradnice.append((x,y))   
        
        ### pokud je spravna odpoved ulozena v A
        if odpoved_spravna_lokace[0] == 0:
            # sezere spravnou odpoved:
            if x == odpoved_a_souradnice[0] and y == odpoved_a_souradnice[1] and nova_napln.odpoved_a in nova_napln.seznam_obrazky:
                had.souradnice.append((x,y))
                nova_napln.seznam_obrazky.remove(nova_napln.odpoved_a)
                skore[0] = skore[0] + 1
                stav[0] = 1

            # sezere spatnou odpoved:
            elif x == odpoved_b_souradnice[0] and y == odpoved_b_souradnice[1] and nova_napln.odpoved_b in nova_napln.seznam_obrazky:
                del had.souradnice[0]
                del had.souradnice[1]
                had.souradnice.append((x,y))
                nova_napln.seznam_obrazky.remove(nova_napln.odpoved_b)

                
            # sezere spatnou odpoved:
            elif x == odpoved_c_souradnice[0] and y == odpoved_c_souradnice[1] and nova_napln.odpoved_c in nova_napln.seznam_obrazky:
                del had.souradnice[0]
                del had.souradnice[1]
                had.souradnice.append((x,y))    
                nova_napln.seznam_obrazky.remove(nova_napln.odpoved_c)
            
            if nova_napln.odpoved_b not in nova_napln.seznam_obrazky and nova_napln.odpoved_c not in nova_napln.seznam_obrazky:
                stav[0] = 1

        ### pokud je spravna odpoved ulozena v B
        elif odpoved_spravna_lokace[0] == 1:
            # sezere spravnou odpoved:
            if x == odpoved_b_souradnice[0] and y == odpoved_b_souradnice[1] and nova_napln.odpoved_b in nova_napln.seznam_obrazky:
                had.souradnice.append((x,y))
                nova_napln.seznam_obrazky.remove(nova_napln.odpoved_b)
                skore[0] = skore[0] + 1
                stav[0] = 1

            # sezere spatnou odpoved:
            elif x == odpoved_a_souradnice[0] and y == odpoved_a_souradnice[1] and nova_napln.odpoved_a in nova_napln.seznam_obrazky:
                del had.souradnice[0]
                del had.souradnice[1]
                had.souradnice.append((x,y))
                nova_napln.seznam_obrazky.remove(nova_napln.odpoved_a)
            # sezere spatnou odpoved:
            elif x == odpoved_c_souradnice[0] and y == odpoved_c_souradnice[1] and nova_napln.odpoved_c in nova_napln.seznam_obrazky:
                del had.souradnice[0]
                del had.souradnice[1]
                had.souradnice.append((x,y))
                nova_napln.seznam_obrazky.remove(nova_napln.odpoved_c)

            if nova_napln.odpoved_a not in nova_napln.seznam_obrazky and nova_napln.odpoved_c not in nova_napln.seznam_obrazky:
                stav[0] = 1

        ### pokud je spravna odpoved ulozena v C
        elif odpoved_spravna_lokace[0] == 2:
            # sezere spravnou odpoved:
            if x == odpoved_c_souradnice[0] and y == odpoved_c_souradnice[1] and nova_napln.odpoved_c in nova_napln.seznam_obrazky:
                had.souradnice.append((x,y))
                nova_napln.seznam_obrazky.remove(nova_napln.odpoved_c)
                skore[0] = skore[0] + 1
                stav[0] = 1

            # sezere spatnou odpoved:
            elif x == odpoved_a_souradnice[0] and y == odpoved_a_souradnice[1] and nova_napln.odpoved_a in nova_napln.seznam_obrazky:
                del had.souradnice[0]
                del had.souradnice[1]
                had.souradnice.append((x,y))
                nova_napln.seznam_obrazky.remove(nova_napln.odpoved_a)
            # sezere spatnou odpoved:
            elif x == odpoved_b_souradnice[0] and y == odpoved_b_souradnice[1] and nova_napln.odpoved_b in nova_napln.seznam_obrazky:
                del had.souradnice[0]
                del had.souradnice[1]
                had.souradnice.append((x,y))
                nova_napln.seznam_obrazky.remove(nova_napln.odpoved_b)

            if nova_napln.odpoved_a not in nova_napln.seznam_obrazky and nova_napln.odpoved_b not in nova_napln.seznam_obrazky:
                stav[0] = 1

def hra():
    aktualni, aktualni_slovo, spravna, spatna_1, spatna_2 = vybirani()

    odpoved_spravna = Odpoved(spravna)
    # odpoved_spatna_1 = Odpoved(spatna_1) 
    # odpoved_spatna_2 = Odpoved(spatna_2)
    
    # lokace znamena ve ktere moznosti (A/B/C) bude spravna odpoved
    odpoved_spravna_lokace[0] = odpoved_spravna.lokace() 

    def souradnice_odpovedi():
        vybirani_souradnic_a = [randrange(0, window.width - obrazek_had.width, 64),randrange(0, window.height - (110 + 2*obrazek_had.height), 64)]
        vybirani_souradnic_b = [randrange(0, window.width - obrazek_had.width, 64),randrange(0, window.height - (110 + 2*obrazek_had.height), 64)]
        vybirani_souradnic_c = [randrange(0, window.width - obrazek_had.width, 64),randrange(0, window.height - (110 + 2*obrazek_had.height), 64)]

        while tuple(vybirani_souradnic_a) in had.souradnice:
            vybirani_souradnic_a = [randrange(0, window.width - obrazek_had.width, 64),randrange(0, window.height - (110 + 2*obrazek_had.height), 64)]
        while tuple(vybirani_souradnic_b) in had.souradnice:
            vybirani_souradnic_b = [randrange(0, window.width - obrazek_had.width, 64),randrange(0, window.height - (110 + 2*obrazek_had.height), 64)]
        while tuple(vybirani_souradnic_c) in had.souradnice:
            vybirani_souradnic_c = [randrange(0, window.width - obrazek_had.width, 64),randrange(0, window.height - (110 + 2*obrazek_had.height), 64)]

        while vybirani_souradnic_b == vybirani_souradnic_a:
            vybirani_souradnic_b = [randrange(0, window.width - obrazek_had.width, 64),randrange(0, window.height - (110 + 2*obrazek_had.height), 64)]
        while vybirani_souradnic_c == vybirani_souradnic_a or vybirani_souradnic_c == vybirani_souradnic_b:
            vybirani_souradnic_c = [randrange(0, window.width - obrazek_had.width, 64),randrange(0, window.height - (110 + 2*obrazek_had.height), 64)]

        if odpoved_spravna_lokace[0] == 0:
            odpoved_a_souradnice[0] = vybirani_souradnic_a[0]
            odpoved_a_souradnice[1] = vybirani_souradnic_a[1]
            odpoved_b_souradnice[0] = vybirani_souradnic_b[0]
            odpoved_b_souradnice[1] = vybirani_souradnic_b[1]
            odpoved_c_souradnice[0] = vybirani_souradnic_c[0]
            odpoved_c_souradnice[1] = vybirani_souradnic_c[1]

        elif odpoved_spravna_lokace[0] == 1:
            odpoved_b_souradnice[0] = vybirani_souradnic_b[0]
            odpoved_b_souradnice[1] = vybirani_souradnic_b[1]
            odpoved_a_souradnice[0] = vybirani_souradnic_a[0]
            odpoved_a_souradnice[1] = vybirani_souradnic_a[1]
            odpoved_c_souradnice[0] = vybirani_souradnic_c[0]
            odpoved_c_souradnice[1] = vybirani_souradnic_c[1]

        elif odpoved_spravna_lokace[0] == 2:
            odpoved_c_souradnice[0] = vybirani_souradnic_c[0]
            odpoved_c_souradnice[1] = vybirani_souradnic_c[1]
            odpoved_b_souradnice[0] = vybirani_souradnic_b[0]
            odpoved_b_souradnice[1] = vybirani_souradnic_b[1]
            odpoved_a_souradnice[0] = vybirani_souradnic_a[0]
            odpoved_a_souradnice[1] = vybirani_souradnic_a[1]

    souradnice_odpovedi()

    # vypsani otazky
    otazka = pyglet.text.Label(f'Slovo {aktualni_slovo} je původu ... :', font_name='Times New Roman', font_size=24, x=window.width//2, y=window.height-40, anchor_x='center', anchor_y='center')

    # vypisovani odpovedi
    if odpoved_spravna_lokace[0] == 0:
        text_odpoved_a = pyglet.text.Label(f'a) {spravna}', font_name='Times New Roman', font_size=24, x=window.width//4, y=window.height-90, anchor_x='center', anchor_y='center')
        text_odpoved_b = pyglet.text.Label(f'b) {spatna_1}', font_name='Times New Roman', font_size=24, x=(window.width//4)*2, y=window.height-90, anchor_x='center', anchor_y='center')
        text_odpoved_c = pyglet.text.Label(f'c) {spatna_2}', font_name='Times New Roman', font_size=24, x=(window.width//4)*3, y=window.height-90, anchor_x='center', anchor_y='center')
    elif odpoved_spravna_lokace[0] == 1:
        text_odpoved_a = pyglet.text.Label(f'a) {spatna_1}', font_name='Times New Roman', font_size=24, x=window.width//4, y=window.height-90, anchor_x='center', anchor_y='center')
        text_odpoved_b = pyglet.text.Label(f'b) {spravna}', font_name='Times New Roman', font_size=24, x=(window.width//4)*2, y=window.height-90, anchor_x='center', anchor_y='center')
        text_odpoved_c = pyglet.text.Label(f'c) {spatna_2}', font_name='Times New Roman', font_size=24, x=(window.width//4)*3, y=window.height-90, anchor_x='center', anchor_y='center')
    elif odpoved_spravna_lokace[0] == 2:
        text_odpoved_a = pyglet.text.Label(f'a) {spatna_1}', font_name='Times New Roman', font_size=24, x=window.width//4, y=window.height-90, anchor_x='center', anchor_y='center')
        text_odpoved_b = pyglet.text.Label(f'b) {spatna_2}', font_name='Times New Roman', font_size=24, x=(window.width//4)*2, y=window.height-90, anchor_x='center', anchor_y='center')
        text_odpoved_c = pyglet.text.Label(f'c) {spravna}', font_name='Times New Roman', font_size=24, x=(window.width//4)*3, y=window.height-90, anchor_x='center', anchor_y='center')



    etymologie = pyglet.text.Label(aktualni["etymologie"], font_name='Times New Roman', font_size=24, x=window.width//2, y=window.height//2+30, anchor_x='center', anchor_y='center', multiline=True, width=600)
    spatne = pyglet.text.Label(f'Chyba lávky! Slovo {aktualni_slovo} je původu {spravna}!', font_name='Times New Roman', font_size=24, x=window.width//2, y=window.height//2, anchor_x='center', anchor_y='center')
    
    odpoved_a = pyglet.sprite.Sprite(obrazek_a,x=odpoved_a_souradnice[0], y=odpoved_a_souradnice[1])
    odpoved_b = pyglet.sprite.Sprite(obrazek_b,x=odpoved_b_souradnice[0], y=odpoved_b_souradnice[1])
    odpoved_c = pyglet.sprite.Sprite(obrazek_c,x=odpoved_c_souradnice[0], y=odpoved_c_souradnice[1])
    seznam_obrazky = [odpoved_a, odpoved_b, odpoved_c]

    return otazka, text_odpoved_a, text_odpoved_b, text_odpoved_c, etymologie, spatne, odpoved_a, odpoved_b, odpoved_c, seznam_obrazky

def vykresli_hada():
    window.clear()
    nova_napln.otazka.draw()

    # for i in range(20):
    #     nakresli_obdelnik(0, window.height-108, window.width, window.height-106)
    for i in range(20):
        nakresli_obdelnik(0, window.height-132, window.width, window.height-130)
    for polozka in nova_napln.seznam_obrazky:    
        polozka.draw()

    for i in had.souradnice:
        cast = pyglet.sprite.Sprite(obrazek_had, x=i[0],y=i[1])
        cast.draw()

    hlava = pyglet.sprite.Sprite(obrazek_had_hlava_vpravo, x=had.souradnice[len(had.souradnice)-1][0], y=had.souradnice[len(had.souradnice)-1][1])
    if had.smer == "dolů":
        hlava = pyglet.sprite.Sprite(obrazek_had_hlava_dolu, x=had.souradnice[len(had.souradnice)-1][0], y=had.souradnice[len(had.souradnice)-1][1])
    elif had.smer == "vlevo":
        hlava = pyglet.sprite.Sprite(obrazek_had_hlava_vlevo, x=had.souradnice[len(had.souradnice)-1][0], y=had.souradnice[len(had.souradnice)-1][1])
    elif had.smer == "vpravo":
        hlava = pyglet.sprite.Sprite(obrazek_had_hlava_vpravo, x=had.souradnice[len(had.souradnice)-1][0], y=had.souradnice[len(had.souradnice)-1][1])
    elif had.smer == "nahoru":
        hlava = pyglet.sprite.Sprite(obrazek_had_hlava_nahoru, x=had.souradnice[len(had.souradnice)-1][0], y=had.souradnice[len(had.souradnice)-1][1])
    hlava.draw()


    skore_hodnota = pyglet.text.Label(f"skóre = {skore[0]}", font_name='Times New Roman', font_size=18, x=55, y=window.height-45, anchor_x='center', anchor_y='center')
    skore_hodnota.draw()
    delka_hada = pyglet.text.Label(f"délka hada = {len(had.souradnice)}", font_name='Times New Roman', font_size=18, x=81, y=window.height-20, anchor_x='center', anchor_y='center')
    delka_hada.draw()

    if nova_napln.odpoved_a not in nova_napln.seznam_obrazky:
        nova_napln.text_odpoved_b.draw()
        nova_napln.text_odpoved_c.draw()
    elif nova_napln.odpoved_b not in nova_napln.seznam_obrazky:
        nova_napln.text_odpoved_a.draw()
        nova_napln.text_odpoved_c.draw()
    elif nova_napln.odpoved_c not in nova_napln.seznam_obrazky:
        nova_napln.text_odpoved_b.draw()
        nova_napln.text_odpoved_a.draw()
    else:
        nova_napln.text_odpoved_a.draw()
        nova_napln.text_odpoved_b.draw()
        nova_napln.text_odpoved_c.draw()


def vykresli_vysledek():
    pokracovani = pyglet.text.Label("pro pokračování stiskni ENTER", font_name='Times New Roman', font_size=20, x=window.width//2, y=window.height//2-180, anchor_x='center', anchor_y='center')

    if odpoved_spravna_lokace[0] == 0 and nova_napln.odpoved_a not in nova_napln.seznam_obrazky:
        window.clear()
        etym_okenko = pyglet.sprite.Sprite(ramecek_zeleny, x=210, y=90)
        etym_okenko.draw()
        nova_napln.etymologie.draw()
        pokracovani.draw()
    elif odpoved_spravna_lokace[0] == 1 and nova_napln.odpoved_b not in nova_napln.seznam_obrazky:        
        window.clear()
        etym_okenko = pyglet.sprite.Sprite(ramecek_zeleny, x=210, y=90)
        etym_okenko.draw()
        nova_napln.etymologie.draw()
        pokracovani.draw()
    elif odpoved_spravna_lokace[0] == 2 and nova_napln.odpoved_c not in nova_napln.seznam_obrazky:
        window.clear()
        etym_okenko = pyglet.sprite.Sprite(ramecek_zeleny, x=210, y=90)
        etym_okenko.draw()
        nova_napln.etymologie.draw()
        pokracovani.draw()
    elif odpoved_a not in nova_napln.seznam_obrazky and nova_napln.odpoved_c not in nova_napln.seznam_obrazky:
        text_odpoved_b.draw()
        window.clear()
        etym_okenko = pyglet.sprite.Sprite(ramecek_cerveny, x=210, y=90)
        nova_napln.spatne.draw()
        pokracovani.draw()
    elif odpoved_b not in nova_napln.seznam_obrazky and nova_napln.odpoved_c not in nova_napln.seznam_obrazky:
        text_odpoved_a.draw()
        window.clear()
        etym_okenko = pyglet.sprite.Sprite(ramecek_cerveny, x=210, y=90)
        nova_napln.spatne.draw()
        pokracovani.draw()
    elif odpoved_a not in nova_napln.seznam_obrazky and nova_napln.odpoved_b not in nova_napln.seznam_obrazky:
        text_odpoved_c.draw()
        window.clear()
        etym_okenko = pyglet.sprite.Sprite(ramecek_cerveny, x=210, y=90)
        nova_napln.spatne.draw()
        pokracovani.draw()

def vykresli_konec_kratky():
        window.clear()
        konec = pyglet.text.Label("Konec hry. Zabil jsi hada vlastní hloupostí...", font_name='Times New Roman', font_size=24, x=window.width//2, y=window.height//2, anchor_x='center', anchor_y='center')
        skore_hodnota = pyglet.text.Label(f"skóre = {skore[0]}/30", font_name='Times New Roman', font_size=22, x=window.width//2, y=window.height//2-80, anchor_x='center', anchor_y='center')
        ukonceni_hry = pyglet.text.Label("ESC: ukončení hry     mezerník: nová hra", font_name='Times New Roman', font_size=20, x=window.width//2, y=window.height//2-180, anchor_x='center', anchor_y='center')
        etym_okenko = pyglet.sprite.Sprite(ramecek_cerveny, x=210, y=90)
        etym_okenko.draw()
        skore_hodnota.draw()
        konec.draw()
        ukonceni_hry.draw()

def vykresli_konec_dlouhy():
        window.clear()
        pseudovyhra_1 = pyglet.text.Label("Gratuluji!", font_name='Times New Roman', font_size=24, x=window.width//2, y=window.height//2+40, anchor_x='center', anchor_y='center')
        pseudovyhra_2 = pyglet.text.Label("Had se překrmil vědomostmi a praskla mu hlava!", font_name='Times New Roman', font_size=24, x=window.width//2, y=window.height//2, anchor_x='center', anchor_y='center')
        skore_hodnota = pyglet.text.Label(f"skóre = {skore[0]}/30", font_name='Times New Roman', font_size=22, x=window.width//2, y=window.height//2-80, anchor_x='center', anchor_y='center')
        ukonceni_hry = pyglet.text.Label("ESC: ukončení hry     mezerník: nová hra", font_name='Times New Roman', font_size=20, x=window.width//2, y=window.height//2-180, anchor_x='center', anchor_y='center')
        etym_okenko = pyglet.sprite.Sprite(ramecek_zeleny, x=210, y=90)
        etym_okenko.draw()
        pseudovyhra_1.draw()
        pseudovyhra_2.draw()
        skore_hodnota.draw()
        ukonceni_hry.draw()

def vykresli_konec_slovniku():
        window.clear()
        prohra_1 = pyglet.text.Label("Hadovi došla potrava a skóre vědomostí je příliš nízké!", font_name='Times New Roman', font_size=24, x=window.width//2, y=window.height//2+40, anchor_x='center', anchor_y='center')
        prohra_2 = pyglet.text.Label("Zkus to znova!", font_name='Times New Roman', font_size=24, x=window.width//2, y=window.height//2, anchor_x='center', anchor_y='center')
        skore_hodnota = pyglet.text.Label(f"skóre = {skore[0]}/30", font_name='Times New Roman', font_size=22, x=window.width//2, y=window.height//2-80, anchor_x='center', anchor_y='center')
        ukonceni_hry = pyglet.text.Label("ESC: ukončení hry     mezerník: nová hra", font_name='Times New Roman', font_size=20, x=window.width//2, y=window.height//2-180, anchor_x='center', anchor_y='center')
        etym_okenko = pyglet.sprite.Sprite(ramecek_cerveny, x=210, y=90)
        etym_okenko.draw()
        skore_hodnota.draw()
        prohra_1.draw()
        prohra_2.draw()
        skore_hodnota.draw()
        ukonceni_hry.draw()

def vykresli_uvod():
    window.clear()
    nadpis = pyglet.text.Label(f'ETYMOLOGICKÝ HAD', font_name='Times New Roman', font_size=34, x=window.width//2, y=500, anchor_x='center', anchor_y='center')
    navod_1 = pyglet.text.Label(f'Zkus uhádnout nejstarší doložený původ slova!', font_name='Times New Roman', font_size=24, x=window.width//2, y=400, anchor_x='center', anchor_y='center')
    navod_2 = pyglet.text.Label(f'Sněz správnou odpověď!', font_name='Times New Roman', font_size=24, x=window.width//2, y=350, anchor_x='center', anchor_y='center')
    navod_3 = pyglet.text.Label(f'Hlídej si délku hada!', font_name='Times New Roman', font_size=24, x=window.width//2, y=300, anchor_x='center', anchor_y='center')
    navod_4 = pyglet.text.Label(f'START HRY: zmáčni S', font_name='Times New Roman', font_size=24, x=window.width//2, y=150, anchor_x='center', anchor_y='center')

    nadpis.draw()
    navod_1.draw()
    navod_2.draw()
    navod_3.draw()
    navod_4.draw()

def prepinani():
    if stav[0] == 0:
        vykresli_hada()
    elif stav[0] == 1:
        vykresli_vysledek()
    elif stav[0] == 2:
        vykresli_konec_kratky()
    elif stav[0] == 3:
        vykresli_konec_slovniku()
    elif stav[0] == 4:
        vykresli_konec_dlouhy()
    elif stav[0] == -1:
        vykresli_uvod()


otazka, text_odpoved_a, text_odpoved_b, text_odpoved_c, etymologie, spatne, odpoved_a, odpoved_b, odpoved_c, seznam_obrazky  = hra()

nova_napln = Vyber()
nova_napln.novy_vyber()


pyglet.clock.schedule_interval(pohyb,1/4)
window.push_handlers(on_draw=prepinani, on_key_press=klavesa)


pyglet.app.run()
