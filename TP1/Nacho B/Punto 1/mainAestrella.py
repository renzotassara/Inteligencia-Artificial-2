from AlgoritmoAEstrella import Nodo, Aestrella
import pygame

Nodo_inicial = Nodo(6, 0)
Nodo_objetivo = Nodo(0, 10)
obstaculos = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 6), (1, 7), (1, 8), (1, 9), (2,1), (2, 2), (2, 3), (2, 4), (2, 6), (2, 7), (2, 8), (2, 9), (4, 1), (4, 2), (4, 3), (4, 4), (4, 6), (4, 7), (4, 8), (4, 9), (5, 1), (5, 2), (5, 3), (5, 4), (5, 6), (5, 7), (5, 8), (5, 9)]
for obstaculo in obstaculos:
    obstaculo = Nodo(obstaculo[0], obstaculo[1])
    obstaculo.obs = True
#Dibujamos el tablero
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("A*")
screen.fill((255, 255, 255))
#Dibujamos los nodos
for i in range(7):
    for j in range(11):
        pygame.draw.rect(screen, (0, 0, 0), (i*50, j*50, 50, 50), 1)
#Dibujamos los obstaculos
for obstaculo in obstaculos:
    pygame.draw.rect(screen, (0, 0, 0), (obstaculo[0]*50, obstaculo[1]*50, 50, 50))

#Calculamos el camino
camino = Aestrella(Nodo_inicial, Nodo_objetivo, obstaculos, screen)
print(camino)
# Dibujamos el camino en verde
for nodo in camino:
    pygame.draw.rect(screen, (0, 255, 0), (nodo.posicion[0]*50, nodo.posicion[1]*50, 50, 50))

# Dibujamos el nodo inicial y el objetivo en rojo
pygame.draw.rect(screen, (255, 0, 0), (Nodo_inicial.posicion[0]*50, Nodo_inicial.posicion[1]*50, 50, 50))
pygame.draw.rect(screen, (255, 0, 0), (Nodo_objetivo.posicion[0]*50, Nodo_objetivo.posicion[1]*50, 50, 50))

pygame.display.flip()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()