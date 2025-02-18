
from Borrosificacion import fuzzyfication
from Desborrosificacion import Desfuzzyficacion
import numpy as np


def ControlDifuso(theta,vel):

    #dominos y solaopamiento
    theta_domain = [-np.pi/2,np.pi/2]
    vel_domain = [-6,6]
    Force_domain = [-80,80]
    alpha_theta = 0.5
    alpha_vel = 0.5

    theta_Fuzzy = fuzzyfication(theta_domain,alpha_theta,theta)
    vel_Fuzzy = fuzzyfication(vel_domain,alpha_vel,vel)

    # Fuzzy Abstract Machine (FAM)
    #vel:     NG   NP   Z    PP  PG
    reglas=[['NG','NG','NG','NP','Z'],  #theta: NG
            ['NG','NG','NP','Z','PP'],  #theta: NP
            ['NG','NP','Z','PP','PG'],  #theta: z
            ['NP','Z','PP','PG','PG'],  #theta: PP
            ['Z','PP','PG','PG','PG']]  #theta: PG


    # Combinaciones que implican F = __
    labels = ['NG','NP','Z','PP','PG']
    
    grouped_rules = []

    for n in range(0,5):
        grouped_rules.append([])
        for i in range(0,5):
            for j in range(0,5):
                if reglas[i][j] == labels[n]:
                    grouped_rules[n].append([i,j])

    #inferencia
    Force_Fuzzy = np.zeros(5)

    for n in range(0,5):
        for i in range(0,len(grouped_rules[n])):
            Force_Fuzzy[n] = max(Force_Fuzzy[n],min(theta_Fuzzy[grouped_rules[n][i][0]],vel_Fuzzy[grouped_rules[n][i][1]]))

    Force = Desfuzzyficacion(Force_domain,Force_Fuzzy)

    # Guardamos theta, vel, theta_Fuzzy, vel_Fuzzy, Force_Fuzzy y Force
    # en un archivo de llamado save.txt como una fila mas
    save = False
    if save:
        with open('save.txt','a') as f:
            f.write('----------------------------------------\n')
        
            #theta en gados, mins y secs
            grades = int(theta*180/np.pi)
            mins = int((theta*180/np.pi-int(theta*180/np.pi))*60)
            secs = round((((theta*180/np.pi-int(theta*180/np.pi))*60)-int((theta*180/np.pi-int(theta*180/np.pi))*60))*60,6)

            f.write('theta: '+str(grades)+'g '+str(mins)+'m '+str(secs)+'s  --> [')
            for i in range(0,5):
                f.write(str(round(theta_Fuzzy[i],4))+' ')
            f.write(']\n')

            f.write('vel:  '+str(round(vel,6))+'--> [')
            for i in range(0,5):
                f.write(str(round(vel_Fuzzy[i],4))+' ')
            f.write(']\n')
                    
            # Representamos Force_Fuzzy con 3 decimales
            f.write('Force_Fuzzy: [')
            for i in range(0,5):
                f.write(str(round(Force_Fuzzy[i],4))+' ')
            f.write('] -->'+str(Force )+'\n')

    return Force 
