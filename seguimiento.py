import sys, time, unicodedata
import urllib.request as urllib2
from http.cookiejar import CookieJar
from bs4 import BeautifulSoup as bs
from colorama import init, Fore, Back
from figura import mostrar

def elimina_tildes(s): return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

urlMarca = ["http://www.marca.com/futbol/primera/calendario.html", "http://www.marca.com/futbol/segunda/calendario.html"]
separaGoles = "-"
numeroUltimosSeguimiento = 5 # Número de partidos a estudiar equipo

cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-agent', 'Mozilla/5.0')]

class Marcadores():
    """ Datos extraídos desde MARCA.com con los marcadores """
    def __init__(self, eql, eqv, golL, golV ):
        self.eql = " ".join(eql.lower().split())
        self.eqv =  " ".join(eqv.lower().split())
        self.golL = golL
        self.golV = golV
    def __str__(self):
        return self.eql + " - " + self.eqv + " --> " + self.golL + " - " + self.golV

def gethtml(url):
    """ Recupera código HTML a partir de URL """
    try:
        texto = opener.open(url).read()
        return texto
    except Exception as e:
        print("Error: ", str(e))
        time.sleep(2)
        return ''

def pregunta(mensaje, opciones):
    """ Recupera un valor preguntando al usuario """
    ask = input(mensaje)
    try:
        return int(ask) if int(ask) in opciones else 0
    except:
        return 0

def procesarResultadosJornada(data, jorn, equipo=''):
    """ Ejecuta la extracción de la información desde el código HTML extraído """
    soup = bs(data, "html.parser")
    tjornadas = soup.findAll("div", { "class" : "jornada calendarioInternacional" })

    try:
        tlocales = tjornadas[jorn-1].findAll("td", { "class" : "local" })
        tvisits = tjornadas[jorn-1].findAll("td", { "class" : "visitante" })
        tresults = tjornadas[jorn-1].findAll("td", { "class" : "resultado" })

        lMarcadores = []
        partidoEquipo = ''
        if equipo != '':
            for i in range(0,len(tlocales)):
                goles = tresults[i].text.split(separaGoles)
                goles = ajustaGoles(goles)
                partido = Marcadores(elimina_tildes(tlocales[i].text), elimina_tildes(tvisits[i].text), goles[0], goles[1])
                if partido.eql == equipo or partido.eqv == equipo:
                    partidoEquipo = partido
                    break
        else:
            for i in range(0,len(tlocales)):
                goles = tresults[i].text.split(separaGoles)
                goles = ajustaGoles(goles)
                partido = Marcadores(elimina_tildes(tlocales[i].text), elimina_tildes(tvisits[i].text), goles[0], goles[1])
                lMarcadores.append(partido)

        return lMarcadores, partidoEquipo
    except:
        print("¡Jornada", jorn, "no jugada!")
        return [], ''

def ajustaGoles(marca):
    """ Ajuste de goles, devolviendo gol como string """
    try:
        marca[0] = str(int(marca[0]))
        marca[1] = str(int(marca[1]))
    except:
        marca[0] = ''
        marca[1] = ''
    return marca

def puntosObtenidosEquipo(partido, equipo):
    """ Determina los puntos que ha conseguido equipo en partido """
    if partido.eql == equipo:
        if partido.golL > partido.golV:
            return 3
        elif partido.golL < partido.golV:
            return 0
        else:
            return 1
    elif partido.eqv == equipo:
        if partido.golV > partido.golL:
            return 3
        elif partido.golV < partido.golL:
            return 0
        else:
            return 1
    else:
        return -1

def borrarPantalla():
    """ Borrar pantalla y situar cursor """
    print("\033[2J\033[1;1f")

def colorConsola(texto):
    """ Escribir texto en color """
    print(Fore.WHITE+Back.BLUE+texto+Fore.RESET+Back.RESET)

def main():
    borrarPantalla()
    div = pregunta('Primera o segunda división [1 ó 2]: ', [1,2])
    if div == 0:
        print("¡Error al seleccionar division!")
        sys.exit()
    jornada = pregunta('Número de jornada: ', range(1,43))
    if jornada == 0:
        print("¡Error al seleccionar jornada!")
        sys.exit()

    data = gethtml(urlMarca[div - 1])

    marcadores, partidoEquipo = procesarResultadosJornada(data, jornada)
    print()
    init()
    colorConsola("Marcadores de la jornada " + str(jornada))
    for marc in marcadores:
        print(marc)

    print()
    equipo = input('Seguimiento equipo: ')
    print()
    colorConsola("Últimos " + str(numeroUltimosSeguimiento) + " partidos del equipo " + equipo + " desde la jornada " + str(jornada))

    i = jornada
    puntosObtenidos = []
    jornadasUltimas = []

    while (i>0 and i>jornada-numeroUltimosSeguimiento and i<jornada+1):
        marcadores, partidoEquipo = procesarResultadosJornada(data, i, equipo)
        if partidoEquipo != '':
            print("Jornada", i, ":", partidoEquipo)
            puntosObtenidos.insert(0, puntosObtenidosEquipo(partidoEquipo, equipo))
            jornadasUltimas.insert(0, i)
        else:
            print("¡Equipo", equipo, "no jugó la jornada", i, "!")
        i = i-1

    if len(puntosObtenidos) == numeroUltimosSeguimiento:
        print()
        colorConsola("Mostrando figura ...")
        print(puntosObtenidos)
        print(jornadasUltimas)
        mostrar(jornadasUltimas, puntosObtenidos, equipo)

if __name__ == '__main__':
    main()
