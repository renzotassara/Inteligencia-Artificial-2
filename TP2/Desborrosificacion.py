import numpy as np
def Desfuzzyficacion(Domain, Fuzzy):
    """Calcula el valor nitido a partir de un conjunto difuso
    
    Domain = [limite inferior, limite superior]
    Fuzzy = [NG,NP,Z,PP,PG]
    """

    #Fuzzy = [NG,NP,Z,PP,PG]

    # Calcula el valor nitido por media de centros
    P = (Domain[1]-Domain[0])/4
    center = [Domain[0], Domain[0]+P, Domain[0]+2*P, Domain[1]-P, Domain[1]]
    crisp = 0
    for i in range(5):
        crisp += center[i]*Fuzzy[i]
    crisp = crisp/np.sum(Fuzzy)
    return crisp

