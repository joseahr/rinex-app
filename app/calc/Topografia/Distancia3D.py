#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2/2/2015

@author: Antonio Hermosilla Rodrigo.
@contact: anherro285@gmail.com
@organization: Antonio Hermosilla Rodrigo.
@copyright: (C) 2015 by Antonio Hermosilla Rodrigo
@version: 1.0.0
'''
import Geometrias.Punto3D
import Geometrias.Linea3D
from math import sqrt

class Distancia3D(object):
    '''
    classdocs
    '''
    __dis=None


    def __init__(self, *args):
        '''!
        Constructor de la clase Distancia3D.
        '''
        if len(args)==1:
            self.__DistanciaLinea(args[0])
        elif len(args)==2:
            self.__DistanciaPuntos(args[0], args[1])
        else:
            raise Exception("La clase Distancia3D recibe 1 o 2 parametros como argumentos.\nSe han introducido: "+str(len(args))+" parametros.")
        
    def __DistanciaLinea(self,Linea):
        '''!
        @brief: Método para cácular la distancia a partir de una Linea3D.
        @params Linea Linea3D: Línea3D con la que cálcular la distancia.
        '''
        if isinstance(Linea, Geometrias.Linea3D.Linea3D):
            AX=Linea.getAX()
            AY=Linea.getAY()
            AZ=Linea.getAZ()
            self.__dis=sqrt(AX**2+AY**2+AZ**2)
        else:
            raise Exception("Se esperaba un objeto de la clase Linea2D")
        
    def __DistanciaPuntos(self,PuntoInicial,PuntoFinal):
        '''!
        @brief: Método para cácular la distancia a partir de dos puntos.
        @param PuntoInicial Punto3D: Primer punto con el que cálcular la distancia.
        @param PuntoFinal Punto3D: Segundo punto con el que cálcular la distancia.
        '''
        if isinstance(PuntoInicial, Geometrias.Punto3D.Punto3D) and isinstance(PuntoFinal, Geometrias.Punto3D.Punto3D):
            AX=PuntoFinal.getX()-PuntoInicial.getX()
            AY=PuntoFinal.getY()-PuntoInicial.getY()
            AZ=PuntoFinal.getY()-PuntoInicial.getZ()
            self.__dis=sqrt(AX**2+AY**2+AZ**2)
        else:
            raise Exception("Se esperaba un objeto de la clase Punto3D.")
    
        
    def getDistancia3D(self):
        '''!
        @brief: Método que devuelve la distancia a calcular.
        @return float: Valor de la distancia.
        '''
        return self.__dis
    
def main():
    d=Distancia3D(Geometrias.Linea3D.Linea3D(Geometrias.Punto3D.Punto3D(10,-20,60),Geometrias.Punto3D.Punto3D(30,40,50)))
    print(d.getDistancia3D()) 
        
        
if __name__=="__main__":
    main()