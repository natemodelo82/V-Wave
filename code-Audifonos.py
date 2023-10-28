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
import espnow #libreria para comunicarse con otro IdeaBoard


mac_x = b'\x08:\x8d\x8e3\xc0'
mac_z = b'\x80do\x110<'


ib = IdeaBoard()
e = espnow.ESPNow()
pulsera = espnow.Peer(mac=mac_x)
e.peers.append(pulsera)

#Microfonos IO
#Calibre el umbral de detección del módulo utilizando el potenciómetro.
#Gírelo en el sentido de las agujas del reloj para aumentar la sensibilidad de detección o
#gírelo en el sentido contrario a las agujas del reloj para disminuir la sensibilidad de detección.
#Si el LED Verde del módulo está encendido, los niveles de ruido están por encima del umbral y debes disminuir la sensibilidad.

#sensores de sonido
micIzq = ib.AnalogIn(board.IO33)
micDer = ib.AnalogIn(board.IO35)
limiteDer = 0
limiteIzq = 0

#Vibradores  valores desde 17000 hasta 20000
vibIzq = ib.AnalogOut (board.IO26)
vibDer = ib.AnalogOut (board.IO25)

    

#Envia un mensaje al otro Ideaboard usando el protocolo espnow
def enviarMensajePulsera(mensaje):
    e.send(mensaje)
    
#rutina para calibrar sensores de sonido
#como se están obteniendo distintas lecturas de los sensores
#no podemos definir un límite en común, entonces mejor calibrar cada sensor
#lo que hacemos es que durante 20 seg vamos a tomar lecturas de ambos sensores y luego vamos a sacar un promedio
#ese promedio va a representar el límite para identificar sonidos en cada sensor
def calibrarLimiteSonido():
    print("Calibrando sensores...")
    acumVI = 0
    acumVD = 0
    veces = 30
    muestraIzq = micIzq.value
    muestraDer = micDer.value
    sleep(1)
    for i in range(veces):
        muestraIzq = micIzq.value
        muestraDer = micDer.value
        #print(str(muestraIzq) + "," + str(muestraDer))
        acumVI = acumVI + muestraIzq  # acumula las lecturas de cada sensor
        acumVD = acumVD + muestraDer
        sleep(0.1)
    #print(str(acumVI) + "," + str(acumVD))
    global limiteIzq
    limiteIzq = int(acumVI / (veces))    
    global limiteDer
    limiteDer = int(acumVD / (veces))
    print("Limite derecho:")
    print(limiteDer)
    print("Limite izquierdo:")
    print(limiteIzq)

vibIzq.value = 0
vibDer.value = 0
#calibrar sensores
calibrarLimiteSonido()

while True:
    vibIzq.value = 0
    vibDer.value = 0
    sonidoIzq = micIzq.value
    sonidoDer = micDer.value
    sleep(0.2)
    #print(str(sonidoIzq) + " - " + str(limiteIzq))
    #print(str(sonidoDer) + " - " + str(limiteDer))
    
    difIzq =  sonidoIzq - limiteIzq   # se calcula la diferencia entre el límite de sonido y el sonido leido
    if (difIzq > 200):
        print("Vibrar izq " + str(difIzq))
        fuerzaVibracion = (17000 + difIzq * 10)
        if (fuerzaVibracion > 40000): #se valida si la fuerza es mayor a 40000 para que el valor no sobrepase los 40000
            fuerzaVibracion = 40000
        vibIzq.value =  fuerzaVibracion 
        enviarMensajePulsera("activar_izq")
        sleep(3)
    
    difDer =  sonidoDer - limiteDer
    if (difDer > 200):
        print("Vibrar der " + str(difDer))
        fuerzaVibracion = (17000 + difDer * 10)
        if (fuerzaVibracion > 40000): #se valida si la fuerza es mayor a 40000 para que el valor no sobrepase los 40000
            fuerzaVibracion = 40000
        vibDer.value = fuerzaVibracion
        enviarMensajePulsera("activar_der")
        sleep(3)
    print("*") 