def fuzzyfication(Domain, alpha, x):
    """Devuelve el valor de la funcion de pertenencia a cada particion en la posicion x.

        Domain = dominio de las entradas [limite inferior, limite superior]
        alpha = porcentaje de solapamiento entre particiones
        x = valor nitido de entrada

        Particiones (NG, NP, Z, PP, PG):
        Utiliza la funcion de pertenencia tipo hombro para NG y PG
        y la funcion de pertenencia tipo triangulo para NP, Z y PP"""

    # Calculamos el ancho de las particiones
    P = (Domain[1]-Domain[0])/4
    width = P/(1-alpha)

    # Determino los centros de las particiones
    center = [Domain[0],
              Domain[0]+P,
              Domain[0]+2*P,
              Domain[0]+3*P,
              Domain[1]]

    # Calculo la funcion de pertenencia para cada particion
    NG = particion_hombro(center[0], width, -1, x)
    NP = particion(center[1] , width, x)
    Z = particion(center[2], width, x)
    PP = particion(center[3], width, x)
    PG = particion_hombro(center[4], width, 1, x)

    return [NG, NP, Z, PP, PG]

def particion(center, width, x):
    """Devuelve el valor de la particion en la posicion

        center = centro de la particion
        width = ancho de la particion
        x = valor nitido de entrada"""

    width = width/2
    if x <= center-width:
        return 0
    elif x > center-width and x <= center:
        return (x-center+width)/width
    elif x > center and x <= center+width:
        return (center+width-x)/width
    else:
        return 0
    
def particion_hombro(center,width,side,x):
    """Devuelve el valor de la particion en la posicion

        center = centro de la particion
        width = ancho de la particion
        side = lado de la particion (-1 izquierda, 1 derecha)
        x = valor nitido de entrada"""

    width = width/2
    if side == -1:
        if x <= center:
            return 1
        elif x > center and x <= center+width:
            return (center+width-x)/width
        else:
            return 0
    elif side == 1:
        if x <= center-width:
            return 0
        elif x > center-width and x <= center:
            return (x-center+width)/width
        else:
            return 1
    else:
        return 0