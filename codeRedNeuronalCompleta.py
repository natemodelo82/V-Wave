##########################################################################################################
#               __                                                                      __               #
#       (      /  \                         +++++++++++++++++                          /  \      )       #
#       ( (   /    \_______________________|                 |_______________________ /    \   ) )       #
#     (    (  ( + )     _____________      | Proyecto V~Wave |      ______________     ( + )  )    )     #
#       ( (                          ------|                 |------                           ) )       #
#       (                                    +++++++++++++++++                                  )        #
#                                                                                                        #
#            Sistema de alerta de peligros ambientales para personas con discapacidad auditiva           #
#                                                                                                        #
#                   Colegio Técnico Profesional de Oreamuno, Informática Empresarial                     #
#                                                                                                        #
#                                       Red Neuronal                                                     #
#                               Integrantes:                                                             #
#                                                                                                        #
#                                  - Montenegro Araya Manfred                                            #
#                                  - Mora Torres Jazmín                                                  #
#                                  - Ramírez Guzmán Celeste                                              #
#                                  - Vega Camacho María José                                             #
#                                                                                                        #  
#                               Profesor Tutor:                                                          #
#                                    Ronald Fallas Rojas                                                 #
#                                                                                                        #
#                                        Año: 2023                                                       #
#                                      Versión: 1.0                                                      #
##########################################################################################################


from ideaboard import IdeaBoard
from time import sleep
import board
import sys
import math





datos = []

ib = IdeaBoard()

#Microfonos IO
#Calibre el umbral de detección del módulo utilizando el potenciómetro.
#Gírelo en el sentido de las agujas del reloj para aumentar la sensibilidad de detección o
#gírelo en el sentido contrario a las agujas del reloj para disminuir la sensibilidad de detección.
#Si el LED Verde del módulo está encendido, los niveles de ruido están por encima del umbral y debes disminuir la sensibilidad.

#sensores de sonido

mic = ib.AnalogIn(board.IO35)
limite = 0

#Cantidad de entradas
p = [] # Entradas, matriz 10 x 1
#Representan la cantidad de neuronas
W = [] # Pesos, Matriz, 1 x 10
b = [] # Bias, Matriz, 1x1
n = [] # Salida 1x1





#rutina para recolectar datos de los sonidos
#Se decidió tomar cada muestra por un sonido producido durante 3 segundos, tomando el muestreo cada 0.3 segundos (10 valores por sonido)
#Esto con el fin de tener datos más representativos que si fuera una sola muestra.
#Este proceso se repite 10 veces, opteniendo 10 muestras por prueba.
#Las muestras se guardan en una matriz 10x10
def recolectarDatosSonido():
    print("Recolectando Datos")
    acumVI = 0
    acumVD = 0
    veces = 10
    muestras = 10
    sleep(1)
    for i in range(veces):
        sonidoIndividual = []
        for j in range(muestras):
            muestra = mic.value
            sonidoIndividual.append(muestra)
            sleep(0.3)
        global datos
        datos.append(sonidoIndividual)
        
    print(datos)




def neurona(p, W, b, n):
    aux = 0.0 # suma neta
    # recorre las columnas de W
    for k in range(len(p[0])):
        aux += p[0][k] * W[k][0]
        print(f"{p[0][k]} * {W[k][0]}")
        
    n[0][0] = aux + b[0][0]
    return n
    

def redNeuronal(p1, W1, b1, n1):
    for i in range(len(W1[0])):
        aux = 0.0
       # recorre las columnas de W
        for j in range(len(W1)):
            aux += p1[0][j] * W1[j][i]
        n1[i][0] = aux + b1[i][0] 

    return n1



def relu(n):
    if(n>=0):
        return n
    elif (n<0):
        return 0;

def sigmoid(n):
  return 1.0/(1.0 + math.exp(-n))


def normalizarDatos(inputData, mean, desvStandar):
    valueNorm = (inputData-mean)/desvStandar
    return valueNorm




def redNeuronalMulticapaCalculada(p):
    
    #///////////////////////////////// Preprocesamiento Red Neuronal /////////////////////////////////
    mean=[[34008.35,33966.9695652174,34026.6608695652,34036.2434782609,34030.0847826087,33969.6739130435,34018.4717391304,33972.352173913,33957.7739130435,34120.2630434783]]
    dstd=[[882.18824109,1362.3971533373,911.8849864258,947.6200494447,991.3688249888,923.0300139815,1275.8240752316,1318.4733175218,1303.725153156,1043.6162496149]]
    #///////////////////////////////////////////////////////////////////////////////////////////////////////
    #///////////////////////////////// Variables Red Neuronal /////////////////////////////////
    a0 = [[normalizarDatos(p[0][0],mean[0][0],dstd[0][0]), normalizarDatos(p[0][1],mean[0][1],dstd[0][1]), normalizarDatos(p[0][2],mean[0][2],dstd[0][2]), normalizarDatos(p[0][3],mean[0][3],dstd[0][3]), normalizarDatos(p[0][4],mean[0][4],dstd[0][4]), normalizarDatos(p[0][5],mean[0][5],dstd[0][5]), normalizarDatos(p[0][6],mean[0][6],dstd[0][6]), normalizarDatos(p[0][7],mean[0][7],dstd[0][7]), normalizarDatos(p[0][8],mean[0][8],dstd[0][8]), normalizarDatos(p[0][9],mean[0][9],dstd[0][9])]];
    W1 = [[-0.1159003, 0.8178369],[0.35219643,-0.041178703],[0.5905676,0.069490455],[-0.2870028,-0.51846415],[0.011987732, -0.25196758],[-0.20487653, -1.0273029],[-0.61676157,-0.5579937],[-0.48574302,-2.7561378],[-0.061449666,-1.7380555],[-0.07331486,0.090650566]]
    a1= [[0.0],[0.0]]
    W2 = [[-2.2262938,4.2875624]]
    a2 = [[0.0]]
    b1= [[-1.2296512],[0.16868275]]
    b2= [[1.1835334]]
    aux = 0.0;
    #//////////////////////////////////////////////////////////////////



   
    #///////////////////////////////// Estructura Red Neuronal /////////////////////////////////
    for  i in range(2):
        aux=0.0
        for j in range(10):
            aux += p[0][j] * W1[j][i]
            
        a1[i][0]=relu(aux+b1[i][0])
    
    for  i in range(1):
        aux=0.0
        for j in range(2):
             aux += W2[i][j] * a1[j][0]
        a2[i][0] = sigmoid(aux + b2[i][0]) 
    
    #//////////////////////////////////////////////////////////////////////////////////////////

    return a2






def redNeuronalMulticapa(p1, W1, b1, n1, W2, b2, n2):

    
    #capa 1
    #Se esperan las matrices de la forma
    # p = [[0.51,0.59,-0.15]] *** puede variar la cantidad de entradas
    # W = [[0.57,-0.57],[-0.79,0.69],[0.75,0.43]]
    # b = [[0.8],[1.5]]
    # n = [[0.0],[0.0]]
    for i in range(len(W1[0])):
        aux = 0.0
       # recorre las columnas de W
        for j in range(len(W1)):
            aux += p1[0][j] * W1[j][i]
        n1[i][0] = aux + b1[i][0]
        
    #capa 2
    # Se esperan las matrices de la forma
    # W2 = [[-0.41,-0.34]]
    # b2 = [[-0.5]]
    # n2 = [[0.0]]
    for i in range(len(W2)):
        aux = 0.0
       # recorre las columnas de W2
        for j in range(len(W2[0])):
            aux += W2[i][j] * n1[j][0]
        n2[i][0] = aux + b2[i][0] 
    return n2


def verMatriz():
     for i in range(len(W[0])):
        aux = 0.0
       # recorre las columnas de W
        for j in range(len(W)):
            print(f"{i}-{j}")
            print(W[j][i])
            print(p[0][j])
            aux += p[0][j] * W[j][i]
        n[i][0] = aux + b[i][0] 
           




##print(redNeuronalMulticapa(p, W, b, n, W2, b2, n2))

#recolectarDatosSonido()
        
print(redNeuronalMulticapaCalculada([[100, 100, 100, 100, 100, 100, 100, 100, 100, 100]])) #gato
print(redNeuronalMulticapaCalculada([[33700, 34078, 33760, 34256, 34336, 33978 ,33919, 34018, 34137, 34058]])) #camion
