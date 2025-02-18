import heapq  # Importamos el módulo heapq para usar montículos (heap)
import matplotlib.pyplot as plt
import pygame

ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 255, 0)
AMARILLO = (255, 255, 0)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
NARANJA = (255, 165 ,0)
TURQUESA = (64, 224, 208)

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
                return camino[::-1]  # Devolvemos el camino en orden inverso

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
            pygame.time.delay(300)
            pygame.draw.circle(ventana, color, (nodo[1] * 60 + 30, nodo[0] * 60 + 30), 20)
    
filas = 14
columnas = 14
obstaculos = [(2,2),(2,3),(2,6),(2,7),(2,10),(2,11),(3,2),(3,3),(3,6),(3,7),(3,10),(3,11),(4,2),(4,3),(4,6),(4,7),(4,10),(4,11),(5,2),(5,3),(5,6),(5,7),(5,10),(5,11),(8,2),(8,3),(8,6),(8,7),(8,10),(8,11),(9,2),(9,3),(9,6),(9,7),(9,10),(9,11),(10,2),(10,3),(10,6),(10,7),(10,10),(10,11),(11,2),(11,3),(11,6),(11,7),(11,10),(11,11)]  # Posiciones de obstáculos

tablero = Tablero(filas, columnas, obstaculos)  # Creamos el tablero
inicio1 = Nodo(2, 2)  # Nodo de inicio  ---> colocar (fila,columna) de obstaculo
objetivo1 = Nodo(8, 11)  # Nodo objetivo
inicio2 = Nodo(8, 11)
objetivo2 = Nodo(2, 2)


##======== Modificacion de inicio y final de recorridos =========
if (inicio1.x,inicio1.y) in obstaculos:
    if (inicio1.x,inicio1.y + 1) in obstaculos:
        inicio1 = Nodo(inicio1.x, inicio1.y - 1)
    else:
        inicio1 = Nodo(inicio1.x, inicio1.y + 1)
else:
    print("Reingrese la posicion inicial del primer agente")
    while(True):
        pass

print(inicio1.x,inicio1.y)

if (objetivo1.x,objetivo1.y) in obstaculos:
    if (objetivo1.x,objetivo1.y + 1) in obstaculos:
        objetivo1 = Nodo(objetivo1.x , objetivo1.y - 1)
    else:
        objetivo1 = Nodo(objetivo1.x, objetivo1.y + 1)
else:
    print("Reingrese la posicion final del primer agente")
    while(True):
        pass
##===================================================================

# Encontramos el camino desde el nodo de inicio hasta el nodo objetivo
camino = tablero.encontrar_camino(inicio1, objetivo1)
print(camino)  # Imprimimos el camino encontrado

pygame.init()
ANCHO = tablero.columnas * 60
ALTO = tablero.filas * 60
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Caminos")

# Dibujar el tablero
for fila in range(tablero.filas):
    for columna in range(tablero.columnas):
        color = BLANCO if (fila, columna) not in tablero.obstaculos else NEGRO
        pygame.draw.rect(ventana, color, (columna * 60, fila * 60, 60, 60))

tablero.plotear_camino(camino,ROJO)