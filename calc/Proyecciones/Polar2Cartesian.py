#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''!
Created on 6/2/2015

@author: Antonio Hermosilla Rodrigo.
@contact: anherro285@gmail.com
@organization: Antonio Hermosilla Rodrigo.
@copyright: (C) 2015 by Antonio Hermosilla Rodrigo
@version: 1.0.0
'''

from math import sin,cos,pi
import sys

import Geometrias.Punto3D as pt3


sys.path.append('..')

def Polar2Cartesian(Azimut,AnguloElevacion,Distancia):
    '''!
    @brief: Método que convierte de coordenadas polares a cartesianas.
    @param: Azimut float|int|str: Valor del azimut de cálculo.
    @param: AnguloElevacion float|int|str: Valor del ángulo de elevación de cálculo.
    @param: Distancia float|int|str: Valor dela distancia de cálculo.
    @return Punto3D: Punto3D con las coordenadas transformadas.
    '''
    try:
        float(Azimut)
        float(AnguloElevacion)
        float(Distancia)
    except Exception as e:
        raise Exception(e)
    finally:
        Azimut=float(Azimut)
        AnguloElevacion=float(AnguloElevacion)
        Distancia=float(Distancia)
        
        x=Distancia*sin(AnguloElevacion)*sin(Azimut)
        y=Distancia*sin(AnguloElevacion)*cos(Azimut)
        z=Distancia*cos(AnguloElevacion)
        
    return pt3.Punto3D(x,y,z)

def main():
    sal=Polar2Cartesian(pi,pi/4,100)
    
    print(sal.getX(),sal.getY(),sal.getZ())
    
if __name__=="__main__":
    main()
        