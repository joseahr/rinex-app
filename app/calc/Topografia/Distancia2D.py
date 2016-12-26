#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''!
Created on 1/2/2015

@author: Antonio Hermosilla Rodrigo.
@contact: anherro285@gmail.com
@organization: Antonio Hermosilla Rodrigo.
@copyright: (C) 2011 by Antonio Hermosilla Rodrigo
@version: 1.0.0
'''
# import sys
# sys.path.append('..')
import Geometrias.Punto2D
import Geometrias.Linea2D
from math import sqrt

class Distancia2D(object):
    '''!
    classdocs
    '''
    __dis=None
    


    def __init__(self, *args):
        '''!
        Constructor de la clase Distancia2D.
        '''
        if len(args)==1:
            self.__DistanciaLinea(args[0])
        elif len(args)==2:
            self.__DistanciaPuntos(args[0], args[1])
        else:
            raise Exception("La clase Distancia2D recibe 1 o 2 parametros como argumentos.\nSe han introducido: "+str(len(args))+" parametros.")
        
    def __DistanciaLinea(self,Linea):
        '''!
        @brief: Método para cácular la distancia a partir de una Linea2D.
        @param Linea Linea2D: Línea2D con la que cálcular la distancia.
        '''
        if isinstance(Linea, Geometrias.Linea2D.Linea2D):
            AX=Linea.getAX()
            AY=Linea.getAY()
            self.__dis=sqrt(AX**2+AY**2)
        else:
            raise Exception("Se esperaba un objeto de la clase Linea2D")
        
    def __DistanciaPuntos(self,PuntoInicial,PuntoFinal):
        '''!
        @brief: Método para cácular la distancia a partir de dos puntos.
        @param PuntoInicial Punto2D: Primer punto con el que cálcular la distancia.
        @param PuntoFinal Punto2D: Segundo punto con el que cálcular la distancia.
        '''
        if isinstance(PuntoInicial, Geometrias.Punto2D.Punto2D) and isinstance(PuntoFinal, Geometrias.Punto2D.Punto2D):
            AX=PuntoFinal.getX()-PuntoInicial.getX()
            AY=PuntoFinal.getY()-PuntoInicial.getY()
            self.__dis=sqrt(AX**2+AY**2)
        else:
            raise Exception("Se esperaba un objeto de la clase Punto2D.")
    
        
    def getDistancia2D(self):
        '''!
        @brief: Método que devuelve la distancia a calcular.
        @return float: Valor de la distancia.
        '''
        return self.__dis
    
    
    
def main():
    d=Distancia2D(Geometrias.Linea2D.Linea2D(Geometrias.Punto2D.Punto2D(10,20),Geometrias.Punto2D.Punto2D(30,40)))
    print(d.getDistancia2D()) 
        
        
if __name__=="__main__":
    main()
        