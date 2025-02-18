import numpy as np
import matplotlib.pyplot as plt
from scipy import constants
from Control import ControlDifuso

CONSTANTE_M = 2 # Masa del carro
CONSTANTE_m = 1 # Masa de la pertiga
CONSTANTE_l = 1 # Longitud dela pertiga

# Simula el modelo del carro-pendulo.
# Parametros:
#   t_max: tiempo maximo (inicia en 0)
#   delta_t: incremento de tiempo en cada iteracion
#   theta_0: Angulo inicial (grados)
#   v_0: Velocidad angular inicial (radianes/s)
#   a_0: Aceleracion angular inicial (radianes/s2)
def simular(t_max, delta_t, theta_0, v_0, a_0):
  # borrar el arechivo data.txt
  open('data.txt', 'w').close()

  theta = (theta_0 * np.pi) / 180
  v = v_0
  a = a_0

  # Simular
  y = []
  F=[]
  V=[]
  x = np.arange(0, t_max, delta_t)
  for t in x:
    f=ControlDifuso(theta,v)
    F.append(f)
    a = calcula_aceleracion(theta, v, f)
    v = v + a * delta_t
    theta = theta + v * delta_t + a * np.power(delta_t, 2) / 2

    if theta > np.pi:
      theta = theta - 2 * np.pi
    elif theta < -np.pi:  
      theta = theta + 2 * np.pi

    y.append(theta)
    V.append(v)

  #fig, ax = plt.subplots()
  #ax.plot(x, y)


  #ax.set(xlabel='time (s)', ylabel='theta', title='Delta t = ' + str(delta_t) + " s")
  #ax.grid()
  
  #plt.show()
  #plot F
  #fig, ax = plt.subplots()
  #ax.plot(x, F)
  #ax.set(xlabel='time (s)', ylabel='F', title='Delta t = ' + str(delta_t) + " s")
  #ax.grid()
  #plt.show()


#mostar la grafica de theta,V y la de F en una sola ventana pero distintas graficas UNA arriba de la otra

  fig, (ax1, ax2, ax3) = plt.subplots(3, 1)
  fig.suptitle('Delta t = ' + str(delta_t) + " s")
  ax1.plot(x, y)
  ax1.set(xlabel='time (s)', ylabel='theta')
  ax1.grid()
  ax2.plot(x, V)
  ax2.set(xlabel='time (s)', ylabel='V')
  ax2.grid()
  ax3.plot(x, F)
  ax3.set(xlabel='time (s)', ylabel='F')
  ax3.grid()
  plt.show()


 



# Calcula la aceleracion en el siguiente instante de tiempo dado el angulo y la velocidad angular actual, y la fuerza ejercida
def calcula_aceleracion(theta, v, f):
    numerador = constants.g * np.sin(theta) + np.cos(theta) * ((-f - CONSTANTE_m * CONSTANTE_l * np.power(v, 2) * np.sin(theta)) / (CONSTANTE_M + CONSTANTE_m))
    denominador = CONSTANTE_l * (4/3 - (CONSTANTE_m * np.power(np.cos(theta), 2) / (CONSTANTE_M + CONSTANTE_m)))
    return numerador / denominador

#print(calcula_aceleracion(0, 0, 10))
#print(calcula_aceleracion(0, 0, -10))

#simular(10, 0.1, 45, 0, 0)

#simular(10, 0.01, 45, 0, 0)

simular(10, 0.001, 80, 0.4, 0)

#simular(10, 0.0001, 45, 0, 0)