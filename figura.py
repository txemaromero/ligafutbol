import matplotlib.pyplot as plt
import math

# len(jornadas)==len(puntosObtenidos)
def mostrar(jornadas, puntosObtenidos, equipo):
    """ Muestra la figura con los valores de las últimas jornadas de equipo """
    y = [0., 0.5, 1., 1.5, 2., 2.5]
    yint = range(math.ceil(min(y)), math.ceil(max(y))+1)
    xint = range(math.ceil(min(jornadas)), math.ceil(max(jornadas))+1)
    plt.yticks(yint)
    plt.xticks(xint)
    plt.ylabel('Puntos obtenidos en jornada')
    plt.xlabel('Jornada')
    plt.title('Últimos resultados del equipo ' + equipo)
    plt.plot(jornadas, puntosObtenidos)
    plt.show()
