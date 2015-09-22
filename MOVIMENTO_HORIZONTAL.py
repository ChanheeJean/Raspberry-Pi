#!/usr/bin/python
# coding: utf-8


#----------------------------------------------------------------
# Autor: Saymon C. A. Oliveira
# Email: saymowan@gmail.com
# Descrição: este algoritmo descreve a sétima implementação de OpenCV
# Funções: Imagem digital -> Transformação HSV -> Imagem binária -> Erosão binária -> Encontrar área -> Encontrar coordenadas
# Funções 2: desenhar circulo no centroide (x,y) -> declaração de pinos -> declaração de funções de movimento do motor -> declaração Função Z
# Funções 3: realizar movimento do robô  de profundidade (area)
# Tecnologias: OpenCV, Python, GPIO e NumPy
#---------------------------------------------------------------

import cv2.cv as cv
import cv2 as cv2
import time
import numpy as np
import RPi.GPIO as gpio


gpio.setmode(gpio.BOARD)
# Desliga alertas
gpio.setwarnings(False)
#---------------------------------------
#Declara pinos como saida GPIO - Motor A
 
#pino de ativação do motor A via Rasp 1
gpio.setup(7, gpio.OUT)
 
#pino de ativação do motor A via Rasp 2 
gpio.setup(11, gpio.OUT)
 
# Iniciar Pino 13 como saida - Motor A
gpio.setup(13, gpio.OUT)
 
#Iniciar Pino 15 como saida - Motor A
gpio.setup(15, gpio.OUT)
 
#---------------------------------------
#Declara pinos como saida GPIO - Motor B
 
#pino de ativação do motor B via Rasp 1
gpio.setup(26, gpio.OUT)
 
#pino de ativação do motor B via Rasp 2 
gpio.setup(16, gpio.OUT)
 
# Iniciar Pino 5 como saida - Motor B
gpio.setup(18, gpio.OUT)
 
#Iniciar Pino 22 como saida - Motor B
gpio.setup(22, gpio.OUT)
 


#-----------------------------------------
# Permitir que o L298N seja controlado pelo GPIO:
#---------------------------------------
#Valores iniciais - True - Motor A ativado
gpio.output(7, True) #Motor A - Rasp 1
gpio.output(11, True) #Motor A - Rasp 2
#---------------------------------------
#Valores iniciais - True - Motor B ativado
gpio.output(26, True) #Motor B - Rasp 1
gpio.output(16, True) #Motor B - Rasp 2
#---------------------------------------



# Motor da Esquerda
# Padr񥳊# 13 e 15
# F e V -> Tr�? V e F -> Frente
# F e F -> Parar

# Motor da Direita
# 5 e 22
# F e V -> Frente
# V e F -> Tr�? F e F -> Parar



def Frente():
# Motor 1
 gpio.output(13, True)
 gpio.output(15, False)
# Motor 2
 gpio.output(18, False)
 gpio.output(22, True)
	
def Tras():
# Motor 1
 gpio.output(13, False)
 gpio.output(15, True)
# Motor 2
 gpio.output(18, True)
 gpio.output(22, False)
 
 
def Parar():
# Motor 1
 gpio.output(18, False)
 gpio.output(22, False)
# Motor 2
 gpio.output(13, False)
 gpio.output(15, False)


def Direita():
# Motor 1
 gpio.output(13, True)
 gpio.output(15, False)
# Motor 2
 gpio.output(18, True)
 gpio.output(22, False)


def Esquerda():
# Motor 1
 gpio.output(13, False)
 gpio.output(15, True)
# Motor 2
 gpio.output(18, False)
 gpio.output(22, True)

 
 def ajusteZ(area):
  if(area<=120):
      Frente()
  elif(area>=600):
      Tras()
  else:
      Parar()
	  
	  
#----------------------------------------------------------------
#    P R O C E S S A M E N T O   D E   I M A G E N S
#------------------------------------------------------------------
# ETAPA 1: OK
# USAR FUNÇÃO INRANGE PARA MUDAR DE RGB-HSV
# PARA ISSO TEMOS QUE DEFINIR OS LIMITES DE VALORES DE H,S E VALORES

# Faixa de HSV que usamos para detectar o objeto colorido
# Neste exemplo, pré definidos para uma bola verde
Hmin = 42
Hmax = 92
Smin = 62
Smax = 255
Vmin = 63
Vmax = 235


#Padrão RED
#Hmin = 0
#Hmax = 179 
#Smin = 131
#Smax = 255
#Vmin = 126
#Vmax = 255


 # Cria-se um array de valores HSV(mínimo e máximo)
rangeMin = np.array([Hmin, Smin, Vmin], np.uint8)
rangeMax = np.array([Hmax, Smax, Vmax], np.uint8)

# Área mínima á ser detectada
minArea = 50


#cv.NamedWindow("Entrada")
#cv.NamedWindow("HSV")
#cv.NamedWindow("Thre")
cv.NamedWindow("Erosao")


# Parametros do tamannho da imagem de captura
width = 160
height = 120
 

 
with picamera.PiCamera() as camera:
    with picamera.array.PiRGBArray(camera) as stream:
        camera.resolution = (320, 240)

        while True:
           entrada = stream.array
	     imgHSV = cv2.cvtColor(entrada,cv2.cv.CV_BGR2HSV)	
	     imgThresh = cv2.inRange(imgHSV, rangeMin, rangeMax)
 	     imgErode = cv2.erode(imgThresh, None, iterations = 3)
 	     moments = cv2.moments(imgErode, True)
	     area = moments['m00']
	     if moments['m00'] >= minArea:
 	  	   print(area)
 	  	   ajusteZ(area)    
 	     else:
 	 	    Parar()
    
   	     #cv2.imshow("Entrada",entrada)
  	     #cv2.imshow("HSV", imgHSV)
  	     #cv2.imshow("Thre", imgThresh)
   	cv2.imshow("Erosao", imgErode)

  	 if cv.WaitKey(10) == 27:
       	 break
        stream.seek(0)
        stream.truncate()
        cv.DestroyAllWindows()	
	   gpio.cleanup()	
	

	