#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 7/02/2015

@author: Antonio Hermosilla Rodrigo.
@contact: anherro285@gmail.com
@organization: Antonio Hermosilla Rodrigo.
@copyright: (C) 2015 by Antonio Hermosilla Rodrigo
@version: 1.0.0
'''
from math import acos,sqrt
import sys
sys.path.append('..')
import Geometrias.Punto3D as pt3
import Geometrias.Linea3D as l3


class AnguloElevacion(object):

    __lin=None
    '''!
    Clase destinada al cálculo del angulo de elevación entre dos puntos.
    '''

    def __init__(self, *args):
        '''!
        Constructor de la clase ÁnguloElevacion.
        *args: La clase admite el constructor con uno o dos argumetos.\n
        Un argumento:\n
        arg1: Linea3D Linea3D: Linea3D sobre la cual se calculará el ángulo de elevación.\n
        Dos argumentos:\n
        arg1: PuntoInicial Punto3D: Punto inicial de cálculo del ángulo de elevación.\n
        arg2: PuntoFinal Punto3D: Punto final de cálculo del ángulo de elevación.\n
        '''
        #Constructor vaico.
        if len(args)==0:
            pass
        #Constructor con linea3d.
        if len(args)==1:
            self.__checkLinea(args[0])
            self.setLinea3D(args[0])
        #Constructor con 2 puntos3d.
        if len(args)==2:
            self.__checkPunto(args[0])
            self.__checkPunto(args[1])

            self.setFromPuntos(args[0],args[1])  
        else:
            raise Exception("La clase sólo admite dos argumentos")
        
    def setFromPuntos(self,PuntoInicial,PuntoFinal):
        '''!
        @brief: Establece el cálculo del ángulo de elevación a partir de dos puntos.
        @param PuntoInicial Punto3D: Punto inicial de cálculo del ángulo de elevación.
        @param PuntoFinal Punto3D: Punto final de cálculo del ángulo de elevación.
        '''
        self.__lin=l3.Linea3D(PuntoInicial,PuntoFinal)
        
        
    def setLinea3D(self,Linea3D):
        '''!
        @brief: Establece el cálculo del ángulo de elevación a partir de una línea.
        @param Linea3D Linea3D: Linea3D sobre la cual se calculará el ángulo de elevación.
        '''
        self.__checkLinea(Linea3D)
        
        
    def __checkPunto(self,Punto3D):
        '''!
        @brief: Método para comprobar si el objeto introducido es una instancia a la clase Punto3D.
        '''
        if not isinstance(Punto3D,pt3.Punto3D):
            raise Exception("El Punto introduccido no es una instancia de la clase Punto3D")
        
    def __checkLinea(self,Linea3D):
        '''!
        @brief: Método para comprobar si el objeto introduciso es una instancia a la clase Linea3D.
        '''
        if not isinstance(Linea3D, l3.Linea3D):
            raise Exception("La línea introducida no es una instancia de la clase Linea3D.")
        self.__lin=Linea3D
        
        
    def getAnguloElevacion(self):
        '''!
        @brief: Método que calcula y devuleve el ángulo de elevación.
        @return float: Ángulo de elevación.
        @note: Devuleve el ángulo de elevación en radianes.
        '''
#         print(self.__lin.getAZ())
#         print(self.__lin.getDistancia())
        return acos(self.__lin.getAZ()/self.__lin.getDistancia())
        
def main():
    ele=AnguloElevacion(pt3.Punto3D(0,0,0),pt3.Punto3D(1,1,sqrt(2)))
    print(ele.getAnguloElevacion())
    ele=AnguloElevacion(pt3.Punto3D(10,10,10),pt3.Punto3D(20,30,40))
    print(ele.getAnguloElevacion())
    
    
if __name__=="__main__":
    main()
    
        