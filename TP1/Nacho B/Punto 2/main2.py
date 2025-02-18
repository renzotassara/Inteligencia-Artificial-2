from AlgoritmoAestrella2 import Nodo, Agente, Aestrella
import pygame

Nodo_inicial1 = Nodo(6, 0)
Nodo_objetivo1 = Nodo(4, 19)
Nodo_inicial2 = Nodo(0, 0)
Nodo_objetivo2 = Nodo(13, 19)
obstaculos_nodos = []
#Tablero de 7x11
#obstaculos = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 6), (1, 7), (1, 8), (1, 9), (2,1), (2, 2), (2, 3), (2, 4), (2, 6), (2, 7), (2, 8), (2, 9), (4, 1), (4, 2), (4, 3), (4, 4), (4, 6), (4, 7), (4, 8), (4, 9), (5, 1), (5, 2), (5, 3), (5, 4), (5, 6), (5, 7), (5, 8), (5, 9)]
#Tablero de 14x22
obstaculos = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 6), (1, 7), (1, 8), (1, 9), (2,1), (2, 2), (2, 3), (2, 4), (2, 6), (2, 7), (2, 8), (2, 9), (4, 1), (4, 2), (4, 3), (4, 4), (4, 6), (4, 7), (4, 8), (4, 9), (5, 1), (5, 2), (5, 3), (5, 4), (5, 6), (5, 7), (5, 8), (5, 9), (7, 1), (7, 2), (7, 3), (7, 4), (7, 6), (7, 7), (7, 8), (7, 9), (8,1), (8, 2), (8, 3), (8, 4), (8, 6), (8, 7), (8, 8), (8, 9), (10, 1), (10, 2), (10, 3), (10, 4), (10, 6), (10, 7), (10, 8), (10, 9), (11, 1), (11, 2), (11, 3), (11, 4), (11, 6), (11, 7), (11, 8), (11, 9), (13, 1), (13, 2), (13, 3), (13, 4), (13, 6), (13, 7), (13, 8), (13, 9), (1, 11), (1, 12), (1, 13), (1, 14), (1, 16), (1, 17), (1, 18), (1, 19), (2, 11), (2, 12), (2, 13), (2, 14), (2, 16), (2, 17), (2, 18), (2, 19), (4, 11), (4, 12), (4, 13), (4, 14), (4, 16), (4, 17), (4, 18), (4, 19), (5, 11), (5, 12), (5, 13), (5, 14), (5, 16), (5, 17), (5, 18), (5, 19), (7, 11), (7, 12), (7, 13), (7, 14), (7, 16), (7, 17), (7, 18), (7, 19), (8, 11), (8, 12), (8, 13), (8, 14), (8, 16), (8, 17), (8, 18), (8, 19), (10, 11), (10, 12), (10, 13), (10, 14), (10, 16), (10, 17), (10, 18), (10, 19), (11, 11), (11, 12), (11, 13), (11, 14), (11, 16), (11, 17), (11, 18), (11, 19), (13, 11), (13, 12), (13, 13), (13, 14), (13, 16), (13, 17), (13, 18), (13, 19)]
for obst in obstaculos:
    obstaculo = Nodo(obst[0], obst[1])
    obstaculo.obs = True
    obstaculos_nodos.append(obstaculo)

#dibujamos el tablero
pygame.init()
screen = pygame.display.set_mode((500,700))
pygame.display.set_caption('A*')
screen.fill((255, 255, 255))
#dibujamos los nodos
for i in range(14):
    for j in range(22):
        pygame.draw.rect(screen, (0, 0, 0), (i*25, j*25, 25, 25), 1)
#dibujamos los obstaculos
for obstaculo in obstaculos:
    pygame.draw.rect(screen, (0, 0, 0), (obstaculo[0]*25, obstaculo[1]*25, 25, 25))  
#calculamos los caminos
camino1, camino2= Aestrella(Nodo_inicial1, Nodo_objetivo1, Nodo_inicial2, Nodo_objetivo2, obstaculos_nodos, screen)
print(camino1)
print(camino2)
#dibujamos los caminos en verde y verde oscuro
for nodo in camino1:
    pygame.draw.rect(screen, (0, 255, 0), (nodo.posicion[0]*25, nodo.posicion[1]*25, 25, 25))
    pygame.display.flip()
    pygame.time.delay(50) # Agrega un retraso de 500 milisegundos (0.5 segundos)
for nodo in camino2:
    pygame.draw.rect(screen, (0, 128, 0), (nodo.posicion[0]*25, nodo.posicion[1]*25, 25, 25))
    pygame.display.flip()
    pygame.time.delay(50)  # Agrega un retraso de 500 milisegundos (0.5 segundos)
#dibujamos los nodos iniciales y objetivos en rojo y rosado
pygame.draw.rect(screen, (255, 0, 0), (Nodo_inicial1.posicion[0]*25, Nodo_inicial1.posicion[1]*25, 25, 25))
pygame.draw.rect(screen, (255, 0, 0), (Nodo_objetivo1.posicion[0]*25, Nodo_objetivo1.posicion[1]*25, 25, 25))
pygame.draw.rect(screen, (255, 192, 203), (Nodo_inicial2.posicion[0]*25, Nodo_inicial2.posicion[1]*25, 25, 25))
pygame.draw.rect(screen, (255, 192, 203), (Nodo_objetivo2.posicion[0]*25, Nodo_objetivo2.posicion[1]*25, 25, 25))
pygame.display.flip()
pygame.time.delay(100)  # Agrega un retraso de 1000 milisegundos (0.1 segundo) 
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
            


