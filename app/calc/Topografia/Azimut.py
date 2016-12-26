#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''!
Created on 2/2/2015

@author: Antonio Hermosilla Rodrigo.
@contact: anherro285@gmail.com
@organization: Antonio Hermosilla Rodrigo.
@copyright: (C) 2011 by Antonio Hermosilla Rodrigo
@version: 1.0.0
'''
import sys
sys.path.append('..')
from math import atan,pi
import Geometrias.Punto2D as pt2
import Geometrias.Punto3D as pt3
import Geometrias.Linea2D as l2
import Geometrias.Linea3D as l3
import Geometrias.PuntoUTM as putm


class Azimut(object):
    '''!
    classdocs
    '''
    __x1=None
    __y1=None
    __x2=None
    __y2=None
    __azimut=None


    def __init__(self, *args):
        '''!
        Constructor de la clase Azimut.
        '''
        if len(args)==0:
            pass
        #Constructor con dos argumentos
        elif len(args)==1:
            #Linea 2D o Linea3D
            self.__checkLinea(args[0])
            self.setLinea(args[0])
        #Constructor con dos argumentos.
        elif len(args)==2:
            #Puntos2D o Puntos3D, o posibles convinaciones.
            self.__checkPunto(args[0])
            self.setPuntoInicial(args[0])
            self.__checkPunto(args[1])
            self.setPuntoFinal(args[1])
        else:
            raise Exception("El número de argumentos introducidos en le costructor de la clase Azimut no es válido.")



    def __checkPunto(self,Punto):
        '''!
        @brief: Metodo para comprobar si el objeto introducido es una instancia a la clase Punto2D o Punto3D.
        '''
        if isinstance(Punto,pt3.Punto3D) or isinstance(Punto,pt2.Punto2D) or isinstance(Punto,putm.PuntoUTM):
            pass
        else:
            raise Exception("El Punto introduccido no es una instancia de la clase Punto2D o Punto3D.")
        
    def __checkLinea(self,Linea):
        '''!
        '''
        if isinstance(Linea,l3.Linea3D) or isinstance(Linea,l2.Linea2D):
            pass
        else:
            raise Exception("La línea introduccido no es una instancia de la clase Linea2D o Linea3D.")
        
    def setPuntoInicial(self,PuntoInicial):
        '''!
        @brief: Método para introducir el punto inicial de cálculo del azimut.
        @param PuntoInicial Punto2D|Punto3D: Punto inicial de cálculo.
        '''
        self.__checkPunto(PuntoInicial)
        self.__x1=PuntoInicial.getX()
        self.__y1=PuntoInicial.getY()
    
    def setPuntoFinal(self,PuntoFinal):
        '''!
        @brief: Método para introducir el punto final de cálculo del azimut.
        @param PuntoInicial Punto2D|Punto3D: Punto final de cálculo.
        '''
        self.__checkPunto(PuntoFinal)
        self.__x2=PuntoFinal.getX()
        self.__y2=PuntoFinal.getY()
        
        
    def setLinea(self,Linea):
        '''!
        @brief: Método para introducir una línea con la cual calcular el azimut.
        @param Linea Linea2D|Linea2D: Línea con la cual calcular el azimut.
        '''
        self.__checkLinea(Linea)
        self.__x1=Linea.getPuntoInicial().getX()
        self.__y1=Linea.getPuntoInicial().getY()
        self.__x2=Linea.getPuntoFinal().getX()
        self.__y2=Linea.getPuntoFinal().getY()


    def __getAX(self):
        '''!
        @brief: Método que devuelve el incremento de coordenadas en el eje X.
        @return float: Incremento X.
        '''
        return self.__x2-self.__x1

    def __getAY(self):
        '''!
        @brief: Método que devuelve el incremento de coordenadas en el eje Y.
        @return: float
        '''
        return self.__y2-self.__y1


    def getAzimut(self):
        '''!
        @brief: Método que devuleve el azimut de la direccion, en radianes.
        @return float: Azimut de la dirección.
        '''
        #print(self.__getAX(),self.__getAY())
        if self.__getAX()==0 and self.__getAY()>0:
            self.__azimut=0
            return self.__azimut
        elif self.__getAX()==0 and self.__getAY()<0:
            self.__azimut=pi
            return self.__azimut
            
        if self.__getAY()==0 and self.__getAX()>0:
            self.__azimut=pi/2
            return self.__azimut
        elif self.__getAY()==0 and self.__getAX()<0:
            self.__azimut=3*pi/2
            return self.__azimut
        #Primer cuadrante
        if self.__getAX()>0 and self.__getAY()>0:
            self.__azimut=atan(self.__getAX()/self.__getAY())
            return self.__azimut
        #Segundo cuadrante
        if self.__getAX()>0 and self.__getAY()<0:
            self.__azimut=(pi/2)+abs(atan(self.__getAX()/self.__getAY()))
            return self.__azimut
        #Tercer cuadrante
        if self.__getAX()<0 and self.__getAY()<0:
            self.__azimut=(pi)+atan(self.__getAX()/self.__getAY())
            return self.__azimut
        #Cuarto cuadrante
        if self.__getAX()<0 and self.__getAY()>0:
            self.__azimut=2*pi+atan(self.__getAY()/self.__getAX())
            return self.__azimut
    