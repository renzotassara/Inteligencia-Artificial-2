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

class Agente:
    def __init__(self, x, y):
        self.ubicacion = (x, y)
        
    def __repr__(self):
        return str(self.ubicacion)

def Aestrella(nodo_inicial1, nodo_objetivo1, nodo_inicial2, nodo_objetivo2, obstaculos, screen):
    lista_abierta1 = []
    lista_cerrada1 = []
    lista_abierta2 = []
    lista_cerrada2 = []
    camino1 = []
    camino2 = []
    lista_abierta1.append(nodo_inicial1)
    lista_abierta2.append(nodo_inicial2)
    nodo_actual1 = lista_abierta1[0]
    nodo_actual2 = lista_abierta2[0]
    nodo_actual1.h=abs(nodo_objetivo1.posicion[0] - nodo_actual1.posicion[0]) + abs(nodo_objetivo1.posicion[1] - nodo_actual1.posicion[1])
    nodo_actual2.h=abs(nodo_objetivo2.posicion[0] - nodo_actual2.posicion[0]) + abs(nodo_objetivo2.posicion[1] - nodo_actual2.posicion[1])
    direcciones = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    while len(lista_abierta1) > 0 and len(lista_abierta2):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        #Verificamos que los nodos actuales no sean los nodos objetivos
        if nodo_actual1.posicion == nodo_objetivo1.posicion or nodo_actual1.h <= 1:
            lista_cerrada1.append(nodo_actual1)
            while nodo_actual1 is not None:
                camino1.append(nodo_actual1)
                nodo_actual1 = nodo_actual1.padre
        
        if nodo_actual2.posicion == nodo_objetivo2.posicion or nodo_actual2.h <= 1:
            lista_cerrada2.append(nodo_actual2)
            while nodo_actual2 is not None:
                camino2.append(nodo_actual2)
                nodo_actual2 = nodo_actual2.padre
        
        if nodo_actual1 is None or nodo_actual2 is None:
            #Si uno de los dos nodos ya encontro el camino el otro sigue buscando
            if nodo_actual1 is None:
                while nodo_actual2 is not None:
                    #verificamos que el nodo actual no sea el objetivo
                    if nodo_actual2.posicion == nodo_objetivo2.posicion:
                        break
                    if nodo_actual2.h <= 1:
                        lista_cerrada2.append(nodo_actual2)
                        while nodo_actual2 is not None:
                            camino2.append(nodo_actual2)
                            nodo_actual2 = nodo_actual2.padre
                        break
                    #Buscamos los hijos del nodo actual
                    hijos2 = []
                    for direccion in direcciones:
                        x = nodo_actual2.posicion[0] + direccion[0]
                        y = nodo_actual2.posicion[1] + direccion[1]
                        hijo = Nodo(x, y)
                        hijos2.append(hijo)
                        hijo.g = nodo_actual2.g + 1
                        hijo.h = abs(nodo_objetivo2.posicion[0] - x) + abs(nodo_objetivo2.posicion[1] - y)
                        hijo.f = hijo.g + hijo.h
                        hijo.padre = nodo_actual2
                        for hijo in hijos2.copy():
                            if any(hijo.posicion == obstaculo.posicion for obstaculo in obstaculos) or any(hijo.posicion == nodo.posicion for nodo in lista_cerrada2):
                                hijos2.remove(hijo)
                        if hijo.posicion[0] < 0 or hijo.posicion[0] > 13 or hijo.posicion[1] < 0 or hijo.posicion[1] > 21:
                            if hijo in hijos2:
                                hijos2.remove(hijo)
                    # Añadir los hijos a la lista abierta
                    for hijo in hijos2:
                        if hijo not in lista_abierta2:
                            lista_abierta2.append(hijo)
                    # Buscar el nodo con el menor valor f
                    set_abierta2 = set(lista_abierta2)
                    nodo_actual2 = lista_abierta2[random.randint(0, len(lista_abierta2) - 1)]
                    for nodo in set_abierta2:
                        if nodo.f < nodo_actual2.f:
                            nodo_actual2 = nodo
                    # Eliminar el nodo actual de la lista abierta y añadirlo a la lista cerrada
                    lista_abierta2.remove(nodo_actual2)
                    lista_cerrada2.append(nodo_actual2)
                    pygame.draw.rect(screen, (0, 0, 100), (nodo_actual2.posicion[0]*25, nodo_actual2.posicion[1]*25, 25, 25))
                    pygame.display.update()
                    pygame.time.delay(50)  # Agrega un retraso de 500 milisegundos (0.5 segundos)
                    pygame.display.flip()
                return camino1[::-1], camino2[::-1]
            if nodo_actual2 is None:
                while nodo_actual1 is not None:
                    #verificamos que el nodo actual no sea el objetivo
                    if nodo_actual1.posicion == nodo_objetivo1.posicion:
                        break
                    if nodo_actual1.h <= 1:
                        lista_cerrada1.append(nodo_actual1)
                        while nodo_actual1 is not None:
                            camino1.append(nodo_actual1)
                            if nodo_actual1.padre is not None and nodo_actual1.padre.obs == True:
                                # Si el padre del nodo actual es un obstáculo, buscamos otro camino
                                 nodo_actual1 = lista_abierta1[random.randint(0, len(lista_abierta1) - 1)]
                            nodo_actual1 = nodo_actual1.padre
                        break
                    #Buscamos los hijos del nodo actual
                    hijos1 = []
                    for direccion in direcciones:
                        x = nodo_actual1.posicion[0] + direccion[0]
                        y = nodo_actual1.posicion[1] + direccion[1]
                        hijo = Nodo(x, y)
                        hijos1.append(hijo)
                        hijo.g = nodo_actual1.g + 1
                        hijo.h = abs(nodo_objetivo1.posicion[0] - x) + abs(nodo_objetivo1.posicion[1] - y)
                        hijo.f = hijo.g + hijo.h
                        hijo.padre = nodo_actual1
                        for hijo in hijos1.copy():
                            if any(hijo.posicion == obstaculo.posicion for obstaculo in obstaculos) or any(hijo.posicion == nodo.posicion for nodo in lista_cerrada1):
                                hijos1.remove(hijo)
                        if hijo.posicion[0] < 0 or hijo.posicion[0] > 13 or hijo.posicion[1] < 0 or hijo.posicion[1] > 21:
                            hijos1.remove(hijo)
                    # Añadir los hijos a la lista abierta
                    for hijo in hijos1:
                        if hijo not in lista_abierta1:
                            lista_abierta1.append(hijo)
                    # Buscar el nodo con el menor valor f
                    set_abierta1 = set(lista_abierta1)
                    nodo_actual1 = lista_abierta1[random.randint(0, len(lista_abierta1) - 1)]
                    for nodo in set_abierta1:
                        if nodo.f < nodo_actual1.f:
                            nodo_actual1 = nodo
                    # Eliminar el nodo actual de la lista abierta y añadirlo a la lista cerrada
                    lista_abierta1.remove(nodo_actual1)
                    lista_cerrada1.append(nodo_actual1)
                    pygame.draw.rect(screen, (0, 0, 255), (nodo_actual1.posicion[0]*25, nodo_actual1.posicion[1]*25, 25, 25))
                    pygame.display.update()
                    pygame.time.delay(50)
                    pygame.display.flip() # Agrega un retraso de 500 milisegundos (0.5 segundos)
                return camino1[::-1], camino2[::-1]
        
        if nodo_actual1.posicion == nodo_objetivo1.posicion and nodo_actual2.posicion == nodo_objetivo2.posicion:
            break
            
        #Buscamos los hijos de los nodos actuales
        hijos1 = []
        hijos2 = []
        for direccion in direcciones:
            x = nodo_actual1.posicion[0] + direccion[0]
            y = nodo_actual1.posicion[1] + direccion[1]
            hijo = Nodo(x, y)
            hijos1.append(hijo)
            hijo.g = nodo_actual1.g + 1
            hijo.h = abs(nodo_objetivo1.posicion[0] - x) + abs(nodo_objetivo1.posicion[1] - y)
            hijo.f = hijo.g + hijo.h
            hijo.padre = nodo_actual1
            for hijo in hijos1.copy():
                if any(hijo.posicion == obstaculo.posicion for obstaculo in obstaculos) or any(hijo.posicion == nodo.posicion for nodo in lista_cerrada1):
                    hijos1.remove(hijo)
            if hijo.posicion[0] < 0 or hijo.posicion[0] > 13 or hijo.posicion[1] < 0 or hijo.posicion[1] > 21:
                if hijo in hijos1:
                    hijos1.remove(hijo)
        for direccion in direcciones:
            x = nodo_actual2.posicion[0] + direccion[0]
            y = nodo_actual2.posicion[1] + direccion[1]
            hijo = Nodo(x, y)
            hijos2.append(hijo)
            hijo.g = nodo_actual2.g + 1
            hijo.h = abs(nodo_objetivo2.posicion[0] - x) + abs(nodo_objetivo2.posicion[1] - y)
            hijo.f = hijo.g + hijo.h
            hijo.padre = nodo_actual2
            for hijo in hijos2.copy():
                if any(hijo.posicion == obstaculo.posicion for obstaculo in obstaculos) or any(hijo.posicion == nodo.posicion for nodo in lista_cerrada2):
                    hijos2.remove(hijo)
                if hijo.posicion == nodo_actual1.posicion and nodo_actual1.obs == True:
                    if hijo in hijos2:
                        hijos2.remove(hijo)
            if hijo.posicion[0] < 0 or hijo.posicion[0] > 13 or hijo.posicion[1] < 0 or hijo.posicion[1] > 21:
                if hijo in hijos1:
                    hijos2.remove(hijo)
        # Añadir los hijos a la lista abierta
        for hijo in hijos1:
            if hijo not in lista_abierta1:
                lista_abierta1.append(hijo)
        for hijo in hijos2:
            if hijo not in lista_abierta2:
                lista_abierta2.append(hijo)
        
        # Buscar el nodo con el menor valor f
        set_abierta1 = set(lista_abierta1)
        set_abierta2 = set(lista_abierta2)
        nodo_actual1 = lista_abierta1[random.randint(0, len(lista_abierta1) - 1)]
        nodo_actual2 = lista_abierta2[random.randint(0, len(lista_abierta2) - 1)]
        for nodo in set_abierta1:
            if nodo.f < nodo_actual1.f:
                nodo_actual1 = nodo
        for nodo in set_abierta2:
            if nodo.f < nodo_actual2.f:
                nodo_actual2 = nodo
        
        #Verificamos si los agentes estan cerca
        if abs(nodo_actual1.posicion[0] - nodo_actual2.posicion[0]) + abs(nodo_actual1.posicion[1] - nodo_actual2.posicion[1]) <= 1:
            nodo_actual1.obs = True
            set_abierta1.remove(nodo_actual1)
            lista_abierta1.remove(nodo_actual1)
            for nodo in set_abierta1:
                if nodo.f < nodo_actual1.f:
                    nodo_actual1 = nodo
        
        # Eliminar el nodo actual de la lista abierta y añadirlo a la lista cerrada
        if nodo_actual1 in lista_abierta1:
            lista_abierta1.remove(nodo_actual1)
        lista_cerrada1.append(nodo_actual1)
        pygame.draw.rect(screen, (0, 0, 255), (nodo_actual1.posicion[0]*25, nodo_actual1.posicion[1]*25, 25, 25))
        pygame.display.update()
        pygame.time.delay(50)  # Agrega un retraso de 500 milisegundos (0.5 segundos)
        pygame.display.flip()
        lista_abierta2.remove(nodo_actual2)
        lista_cerrada2.append(nodo_actual2)
        pygame.draw.rect(screen, (0, 0, 100), (nodo_actual2.posicion[0]*25, nodo_actual2.posicion[1]*25, 25, 25))
        pygame.time.delay(50)  # Agrega un retraso de 500 milisegundos (0.5 segundos)
        pygame.display.update()
        pygame.display.flip()
    return camino1[::-1], camino2[::-1]
         
        
        