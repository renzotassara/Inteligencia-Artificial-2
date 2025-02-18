"""
Dada una orden de pedido, que incluye una lista de productos del almacén anterior que 
deben ser despachados en su totalidad, determinar el orden óptimo para la operación de 
picking mediante Temple Simulado. ¿Qué otros algoritmos pueden utilizarse para esta 
tarea? 
"""
import math
import random
import pygame
import heapq

e = math.e

ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 255, 0)
AMARILLO = (255, 255, 0)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
NARANJA = (255, 165 ,0)
TURQUESA = (64, 224, 208)

colores = [BLANCO,NEGRO,ROJO,VERDE,AZUL,AMARILLO,NARANJA,TURQUESA]

import itertools
import heapq  # Importamos el módulo heapq para usar montículos (heap)
import pygame

class Nodo:
    def __init__(self, x, y, costo_g=0, costo_h=0, padre=None):
        # Constructor de la clase Nodo.
        self.x = x  # Posición x del nodo en el tablero
        self.y = y  # Posición y del nodo en el tablero
        self.costo_g = costo_g  # Costo del camino desde el nodo inicial hasta este nodo
        self.costo_h = costo_h  # Heurística: costo estimado desde este nodo hasta el objetivo
        self.padre = padre  # Nodo padre de este nodo en el camino

    def costo_total(self):
        # Función que devuelve el costo total de este nodo, suma del costo de camino y la heurística
        return self.costo_g + self.costo_h

        # Definir el método especial __lt__ para comparación de nodos
    def __lt__(self, otro):
        return self.costo_total() < otro.costo_total()
    
class Tablero:
    def __init__(self, filas, columnas, obstaculos):
        # Constructor de la clase Tablero.
        self.filas = filas  # Número de filas del tablero
        self.columnas = columnas  # Número de columnas del tablero
        self.obstaculos = obstaculos  # Lista de posiciones de obstáculos en el tablero

    def es_valido(self, x, y):
        # Verifica si una posición (x, y) es válida en el tablero y no está ocupada por un obstáculo
        return 0 <= x < self.filas and 0 <= y < self.columnas and (x, y) not in self.obstaculos

    def obtener_vecinos(self, nodo):
        # Obtiene los nodos vecinos válidos ortogonalmente (movimientos arriba, abajo, izquierda, derecha) al nodo dado
        vecinos = []
        movimientos = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Movimientos ortogonales

        for dx, dy in movimientos:
            nuevo_x, nuevo_y = nodo.x + dx, nodo.y + dy
            if self.es_valido(nuevo_x, nuevo_y):
                vecinos.append(Nodo(nuevo_x, nuevo_y))  # Agregamos el nodo vecino válido a la lista
        
        return vecinos

    def calcular_heuristica(self, nodo, objetivo):
        # Calcula y devuelve la heurística para el nodo dado utilizando la distancia Manhattan
        return abs(nodo.x - objetivo.x) + abs(nodo.y - objetivo.y)

    def encontrar_camino(self, inicio, objetivo):
        # Encuentra y devuelve un camino desde el nodo de inicio hasta el nodo objetivo utilizando el algoritmo A*
        abiertos = []  # Lista de nodos a explorar
        cerrados = set()  # Conjunto de nodos ya explorados

        heapq.heappush(abiertos, (inicio.costo_total(), inicio))  # Agregamos el nodo de inicio al montículo

        while abiertos:
            _, nodo_actual = heapq.heappop(abiertos)  # Obtenemos el nodo con menor costo total de la lista abiertos

            if (nodo_actual.x, nodo_actual.y) == (objetivo.x, objetivo.y):
                # Si llegamos al nodo objetivo, reconstruimos el camino desde el nodo objetivo hasta el inicio
                camino = []
                while nodo_actual:
                    camino.append((nodo_actual.x, nodo_actual.y))  # Agregamos la posición del nodo al camino
                    nodo_actual = nodo_actual.padre  # Movemos al nodo siguiente en el camino
                return camino[::-1],nuevo_costo_g # Devolvemos el camino en orden inverso

            cerrados.add((nodo_actual.x, nodo_actual.y))  # Agregamos la posición del nodo actual al conjunto cerrados

            for vecino in self.obtener_vecinos(nodo_actual):
                if (vecino.x, vecino.y) in cerrados:
                    continue

                nuevo_costo_g = nodo_actual.costo_g + 1  # Se asume que todos los movimientos tienen un costo de 1

                if (vecino.costo_g == 0) or (nuevo_costo_g < vecino.costo_g):
                    vecino.costo_g = nuevo_costo_g
                    vecino.costo_h = self.calcular_heuristica(vecino, objetivo)
                    vecino.padre = nodo_actual  # Establecemos el nodo actual como padre del vecino

                    heapq.heappush(abiertos, (vecino.costo_total(), vecino))  # Agregamos el vecino al montículo

        return None  # Si no se encuentra un camino, devolvemos None

    def plotear_camino(self,camino,color):
        
        # Dibujar el camino
        for nodo in camino:
            pygame.draw.circle(ventana, color, (nodo[1] * 60 + 30, nodo[0] * 60 + 30), 20)
            pygame.draw.circle(ventana, NEGRO, (nodo[1] * 60+60 // 2, nodo[0] * 60+60 // 2), 20, 5)  # Contorno negro de 2 píxeles de ancho
            pygame.display.flip()
            pygame.time.delay(velocidad)
            pygame.draw.circle(ventana, color, (nodo[1] * 60 + 30, nodo[0] * 60 + 30), 20)
    

#=========== Variables ============
#Dimensiones del tablero
filas = 14
columnas = 14
obstaculos = [(2,2),(2,3),(2,6),(2,7),(2,10),(2,11),(3,2),(3,3),(3,6),(3,7),(3,10),(3,11),(4,2),(4,3),(4,6),(4,7),(4,10),(4,11),(5,2),(5,3),(5,6),(5,7),(5,10),(5,11),(8,2),(8,3),(8,6),(8,7),(8,10),(8,11),(9,2),(9,3),(9,6),(9,7),(9,10),(9,11),(10,2),(10,3),(10,6),(10,7),(10,10),(10,11),(11,2),(11,3),(11,6),(11,7),(11,10),(11,11)]  # Posiciones de obstáculos
tablero = Tablero(filas, columnas, obstaculos)  # Creamos el tablero

#Recorrido (siendo la primer tupla el inicio)
recorrido = [(6,0),(2, 2),(8, 11),(4, 7),(5,11),(11,3)]
velocidad = 100 #Velocidad del agente

#Valores para funcion de temple
decremento_T = 0.9
probabilidad = 0.95
valor_limite_T = 3 #Con 3 funciona todo el tiempo, con 4 funciona la mayoria de las veces

##======== Modificacion de inicio y final de recorridos =========
#Es seccion es para modificar las posiciones de los nodos objetivos y desplazarlo a un pasillo, que no quede sobre el obstaculo
recorrido_nuevo = []
for posicion in recorrido:
    x,y = posicion
    if (x,y) in obstaculos:
        if (x,y + 1) in obstaculos:
            recorrido_nuevo.append((x, y-1))
        else:
            recorrido_nuevo.append((x, y+1))
    else:
        recorrido_nuevo.append((x, y))

##====================== Permutaciones entre posicion de almacenes ================================
# Generar todas las posibles combinaciones de las tuplas en recorrido
combinaciones = list(itertools.permutations(recorrido_nuevo[1:]))
combinaciones = [(recorrido_nuevo[0],) + permutacion for permutacion in combinaciones]  #Agrego la posicion inicial como si fuera la entrada del mercado (siempre entro por el mismo lugar)
combinaciones = [list(perm) for perm in combinaciones]  #Genero una lista de listas (matriz tridimensional) para luego poder elegir mas facil el orden del recorrido
#for combinacion in combinaciones:
#    print(combinacion)

#===================Calculo de energia y camino nuevo a comparar==============
def camino_sucesor():
    combinacion_actual = random.choice(combinaciones)
    combinaciones.pop(combinaciones.index(combinacion_actual))
    energia_total_actual = 0
    camino_total_actual = []

    for i in range(len(combinacion_actual[:])-1):
        nodo1 = combinacion_actual[i]
        nodo2 = combinacion_actual[i+1]
        camino,energia = tablero.encontrar_camino(Nodo(nodo1[0],nodo1[1]), Nodo(nodo2[0],nodo2[1]))
        for nodo in camino:
            camino_total_actual.append(nodo)
        energia_total_actual = energia_total_actual + energia

    return camino_total_actual,energia_total_actual

#===================== Temple ============================
def Temple():
    camino_total_actual,energia_total_actual = camino_sucesor() #Camino y energia de una secuencia aleatoria

    T = len(combinaciones)  #Temperatura igual a la cantidad de combinaciones logradas

    while T > valor_limite_T:
        T *= decremento_T
        camino_total_sucesor,energia_total_sucesor = camino_sucesor()
        deltaE = -(energia_total_sucesor - energia_total_actual)    #Esta negativo ya que cuando mayor en la energia, peor es el camino
        if (deltaE > 0):
            energia_total_actual = energia_total_sucesor
            camino_total_actual = camino_total_sucesor
        elif (deltaE < 0 and e**(deltaE/T) > probabilidad):
            energia_total_actual = energia_total_sucesor
            camino_total_actual = camino_total_sucesor
    return camino_total_actual,energia_total_actual

# ==========Dibujar el tablero y recorrido==========

camino,costo = Temple()

pygame.init()
ANCHO = tablero.columnas * 60
ALTO = tablero.filas * 60
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Caminos")

for fila in range(tablero.filas):
    for columna in range(tablero.columnas):
        if (fila,columna) not in (tablero.obstaculos or recorrido): 
            pygame.draw.rect(ventana, colores[0], (columna * 60, fila * 60, 60, 60))
        else:
            if (fila,columna) in recorrido:
                pygame.draw.rect(ventana, colores[7], (columna * 60, fila * 60, 60, 60))
                pygame.draw.rect(ventana, NEGRO, (columna * 60 + 60 // 2- 30, fila * 60 + 60 // 2 - 30, 60, 60), 5)
            else:
                pygame.draw.rect(ventana, colores[1], (columna * 60, fila * 60, 60, 60))

tablero.plotear_camino(camino,colores[2])

