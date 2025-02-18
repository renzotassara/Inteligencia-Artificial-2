def fuzzyfication(Dominio, alfa, x):
    # devuelve el valor de la funcion de pertenencia a cada particion en la posicion x
    # Dominio es una lista con el valor minimo y maximo del dominio
    # alfa es el porcentaje de solapamiento entre particiones
    # x es el valor nitido
    #el numero de particiones es 5 (NG, NP, Z, PP, PG)

    # Cálculo del ancho de las particiones considerando la superposición alfa.
    L0 = (Dominio[1] - Dominio[0]) / 4
    L = L0 / (1 - alfa)

    # Centros de las particiones
    centro = [Dominio[0], Dominio[0] + L0, Dominio[0] + 2 * L0, Dominio[1] - L0, Dominio[1]]

    # Cálculo del valor de la función de pertenencia en cada partición utilizando la función particion
    NG = particion(centro[0],L,-1,x)
    NP = particion(centro[1],L,0,x)
    Z = particion(centro[2],L,0,x)
    PP = particion(centro[3],L,0,x)
    PG = particion(centro[4],L,1,x)

    return [NG, NP, Z, PP, PG]


   

def particion(centro,L,lado, x):
    # devuelve el valor de la particion en la posicion
    # centro es el valor del centro de la particion
    # lado es el lado de la particion (-1 izquierda, 1 derecha)
    # L es el ancho de la particion
    # x es el valor nitido

    # Calcula el ancho medio de la partición.
    L = L / 2

    # Maneja el caso en que la partición está a la izquierda del centro.
    if lado == -1:
        # Si x es menor o igual que el centro, la función de membresía es 1.
        if x <= centro:
            return 1
        # Si x está entre centro y centro + L, la función de membresía disminuye linealmente desde 1 hasta 0.
        elif x > centro and x <= centro + L:
            return (centro + L - x) / L
        # Si x está fuera del rango de la partición, la función de membresía es 0.
        else:
            return 0
    elif lado == 1:
        if x <= centro-L:
            return 0
        elif x > centro-L and x <= centro:
            return (x-centro+L)/L
        else:
            return 1
    
    else: 
        if x <= centro-L:
            return 0
        elif x > centro-L and x <= centro:
            return (x-centro+L)/L
        elif x > centro and x <= centro+L:
            return (centro+L-x)/L
        else:
            return 0