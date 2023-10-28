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
import espnow
import board
from time import sleep


ib = IdeaBoard()

vibPulsera = ib.AnalogOut (board.IO25)  # pin donde se conecta el vibrador

fuerzaVibracion = 40000
vibPulsera.value =  0

ib.brightness = 0.2

AZUL = (0,0,255)
VERDE = (0,255,0)
ROJO = (255,0,0)
APAGADO = (0,0,0)

e = espnow.ESPNow()


while True:
    
    if e: #evento recibido desde los audifonos
        mensaje = e.read()
        print("Señal recibida...")
        print(mensaje)
        if ("activar_izq" in str(mensaje)):
            #color RGB
            ib.pixel = VERDE
            #activar vibrador
            vibPulsera.value =  fuerzaVibracion
            sleep(3)
            
        elif ("activar_der" in str(mensaje)):
            #color RGB
            ib.pixel = AZUL
            #activar vibrador
            vibPulsera.value =  fuerzaVibracion
            sleep(3)
                  
        #apagar led
        ib.pixel = APAGADO
        #apagar vibrador
        vibPulsera.value =  0    
        
        


