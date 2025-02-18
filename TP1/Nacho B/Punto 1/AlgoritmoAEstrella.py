import pygame
import random
class Nodo:
    def __init__(self, x, y):
        self.posicion = (x, y)
        self.g = 0
        self.h = 0
        self.f = 0
        self.padre = None
        self.obs = False
        
    def __repr__(self):
        return str(self.posicion)
    
    
        
def Aestrella(nodo_inicial, nodo_objetivo, obstaculos, screen):
    lista_abierta = []
    lista_cerrada = []
    camino = []
    lista_abierta.append(nodo_inicial)
    nodo_actual = lista_abierta[0]
    nodo_actual.h=abs(nodo_objetivo.posicion[0] - nodo_actual.posicion[0]) + abs(nodo_objetivo.posicion[1] - nodo_actual.posicion[1])
    
    while len(lista_abierta) > 0:  
        #print(nodo_actual)
        #print('Lista abierta:',lista_abierta)
        #print('Lista cerrada:',lista_cerrada)
        
        # Vemos si el nodo actual es el nodo final
        if nodo_actual.posicion == nodo_objetivo.posicion or nodo_actual.h <= 1:
            lista_cerrada.append(nodo_actual)
            while nodo_actual is not None:
                    camino.append(nodo_actual)
                    nodo_actual = nodo_actual.padre
            break
        
        # Bucamos los hijos del nodo actual
        hijos = []
        direcciones = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for direccion in direcciones:
            x = nodo_actual.posicion[0] + direccion[0]
            y = nodo_actual.posicion[1] + direccion[1]
            # Creamos el nodo hijo con la posicion x, y
            hijo = Nodo(x, y)
            # Creamos los nodos hijo
            hijos.append(hijo)
            # Calculamos el valor de g, h y f de los nodos hijo
            hijo.g = nodo_actual.g + 1
            hijo.h = abs(nodo_objetivo.posicion[0] - x) + abs(nodo_objetivo.posicion[1] - y)
            hijo.f = hijo.g + hijo.h
            hijo.padre = nodo_actual
            # Comprobamos si el nodo esta dentro de los limites
            for hijo in hijos.copy():  # Crea una copia de la lista hijos para iterar
                # Verifica si la posición del hijo es un obstáculo o está en la lista cerrada
                if hijo.posicion in obstaculos or any(hijo.posicion == nodo.posicion for nodo in lista_cerrada):
                    hijos.remove(hijo)  # Si es así, lo elimina de la lista hijos
            #if (hijo.posicion) in obstaculos:
            #    hijos.remove(hijo)
            #for nodo in lista_cerrada:
            #    if hijo.posicion == nodo.posicion:
            #        hijos.remove(hijo)
            if hijo.posicion[0] < 0 or hijo.posicion[0] > 6 or hijo.posicion[1] < 0 or hijo.posicion[1] > 10:
                hijos.remove(hijo)
        
        # Añadir los hijos a la lista abierta
        for hijo in hijos:        
            lista_abierta.append(hijo)
                
        # Buscar el nodo con el menor valor f
        set_abierta = set(lista_abierta)
        nodo_actual = lista_abierta[random.randint(0, len(lista_abierta) - 1)]
        for nodo in set_abierta:
            if nodo.f < nodo_actual.f:
                nodo_actual = nodo
        
        # Eliminar el nodo actual de la lista abierta y añadirlo a la lista cerrada
        lista_abierta.remove(nodo_actual)
        lista_cerrada.append(nodo_actual)
        for nodo in lista_cerrada:
            pygame.draw.rect(screen, (0, 0, 255), (nodo_actual.posicion[0]*50, nodo_actual.posicion[1]*50, 50, 50))
        pygame.display.update()  # Actualiza la pantalla
    return camino[::-1]
            