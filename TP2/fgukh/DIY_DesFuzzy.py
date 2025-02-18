import numpy as np
def Desfuzzyficacion(Dominio, fuzzy):
    #dominio =[limite inferior, limite superior]
    #fuzzy = [NG,NP,Z,PP,PG]

    #calcula el valor nitido por media de centros
    L0 = (Dominio[1] - Dominio[0]) / 4  # Longitud de cada subintervalo
    centros = [Dominio[0], Dominio[0] + L0, Dominio[0] + 2 * L0, Dominio[1] - L0, Dominio[1]]  # Centros de los subintervalos
    valor_nitido = 0  # Inicializa el valor nítido
    for i in range(5):
        valor_nitido += centros[i] * fuzzy[i]  # Suma ponderada de los centros
    valor_nitido = valor_nitido / np.sum(fuzzy)  # Divide por la suma de los valores difusos
    return valor_nitido  # Devuelve el valor nítido calculado

