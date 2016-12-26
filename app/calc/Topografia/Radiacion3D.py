#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 9/3/2015

@author: Antonio Hermosilla Rodrigo.
@contact: anherro285@gmail.com
@organization: Antonio Hermosilla Rodrigo.
@copyright: (C) 2011 by Antonio Hermosilla Rodrigo
@version: 1.0.0
'''
import Geometrias.Punto3D as pt3
import Geometrias.Angulo as ang
from math import tan,cos,sin

class Radiacion3D(object):
    '''!
    classdocs
    '''
    __x=None
    __y=None
    __z=None
    __d=None
    __az=None
    __v=None
    __i=None
    __m=None


    def __init__(self, PuntoEstacion,Distancia,Azimut,AnguloVertical,i=0,m=0):
        '''!
        Constructor
        '''
        self.setPuntoEstacion(PuntoEstacion)
        self.setDistancia(Distancia)
        self.setAzimut(Azimut)
        self.setAnguloVertical(AnguloVertical)
        self.setAlturaInstrumento(i)
        self.setAlturaMira(m)
        
    def setPuntoEstacion(self,PuntoEstacion):
        '''!
        @brief: Método que establece el Punto estación.
        @param PuntoEstacion Punto3D: Punto estación con las coordenadas.
        '''
        if isinstance(PuntoEstacion, pt3.Punto3D):
            self.__x=PuntoEstacion.getX()
            self.__y=PuntoEstacion.getY()
            self.__z=PuntoEstacion.getZ()
        else:
            raise Exception("Se esperaba un objeto de la clase Punto2D o Punto3D como valor de entrada.")
        
    def setDistancia(self,Distancia):
        '''!
        @brief: Método que asigna y comprueba la distancia introducida.
        @param Distancia float|int|str: Distancia de cálculo.
        '''
        if isinstance(Distancia, float) or isinstance(Distancia, int) or isinstance(Distancia, str):
            try:
                float(Distancia)
            except Exception as e:
                raise Exception(e)
            finally:
                self.__d=float(Distancia)
        else:
            raise Exception("Valor de distancia no válido.")
        
    def setAzimut(self,Azimut):
        '''!
        @brief: Método que asigna y comprueba el azimut introducido.
        @param Distancia float|int|str|Angulo: Distancia de cálculo.
        '''
        if isinstance(Azimut, float) or isinstance(Azimut, int) or isinstance(Azimut, str):
            try:
                float(Azimut)
                ang.Angulo(Azimut,formato='centesimal')
            except Exception as e:
                raise Exception(e)
            finally:
                a1=ang.Angulo(Azimut,formato='centesimal')
                a1.Convertir('radian')
                self.__az=float(a1.getAngulo())
        elif isinstance(Azimut, ang.Angulo):
            if Azimut.getFormato()=='centesimal':
                Azimut.Convertir('radian')
                self.__az=Azimut.getAngulo()
            else:
                raise Exception("Se esperaba un ángulo de entrada de tipo centesimal.")
        else:
            raise Exception("Valor de azimut no válido.")
        
    def setAnguloVertical(self,AnguloVertical):
        '''!
        @brief: Método que asigna y comprueba el ángulo vertical introducido.
        @param Distancia float|int|str|Angulo: Distancia de cálculo.
        '''
        if isinstance(AnguloVertical, float) or isinstance(AnguloVertical, int) or isinstance(AnguloVertical, str):
            try:
                float(AnguloVertical)
                ang.Angulo(AnguloVertical,formato='centesimal')
            except Exception as e:
                raise Exception(e)
            finally:
                a1=ang.Angulo(AnguloVertical,formato='centesimal')
                a1.Convertir('radian')
                self.__v=float(a1.getAngulo())
        elif isinstance(AnguloVertical, ang.Angulo):
            if AnguloVertical.getFormato()=='centesimal':
                AnguloVertical.Convertir('radian')
                self.__v=AnguloVertical.getAngulo()
            else:
                raise Exception("Se esperaba un ángulo de entrada de tipo centesimal.")
        else:
            raise Exception("Valor de dángulo vertical no válido.")
        
    def setAlturaInstrumento(self,i):
        '''!
        @brief: Método que asigna la altura del instrumento.
        @param i float|int|str: Altura del intrumento.
        '''
        if isinstance(i, float) or isinstance(i, int) or isinstance(i, str):
            try:
                float(i)
            except Exception as e:
                raise Exception(e)
            finally:
                self.__i=float(i)
        else:
            raise Exception("Valor de la altura del instrumento no válido.")
        
    def setAlturaMira(self,m):
        '''!
        @brief: Método que asigna la altura del instrumento.
        @param i float|int|str: Altura del intrumento.
        '''
        if isinstance(m, float) or isinstance(m, int) or isinstance(m, str):
            try:
                float(m)
            except Exception as e:
                raise Exception(e)
            finally:
                self.__m=float(m)
        else:
            raise Exception("Valor de la altura del instrumento no válido.")
        
    def Radiacion3D(self):
        '''!
        @brief: Método que cálculo la radiación con los parametros introducidos.
        @return Punto3D: Devuelve un Punto3D con las coordenadas del punto radiado.
        '''
        xs=self.__x+(self.__d*sin(self.__az))
        ys=self.__y+(self.__d*cos(self.__az))
        zs=self.__z+(self.__d/tan(self.__v))+self.__i-self.__m
        return pt3.Punto3D(xs,ys,zs)
        
        
def main():
    rad=Radiacion3D(pt3.Punto3D(10,20,10),
                    40,
                    ang.Angulo(100,formato='centesimal'),
                    ang.Angulo(98,formato='centesimal'),
                    i=0,m=0)
    sal=rad.Radiacion3D()
    print(sal.getX(),sal.getY(),sal.getZ())  
        
if __name__=="__main__":
    main()