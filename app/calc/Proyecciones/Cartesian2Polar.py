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

import sys

import Geometrias.Punto3D as pt3
import Topografia.AnguloElevacion as ele
import Topografia.Azimut as az
import Topografia.Distancia3D as d3


sys.path.append('..')


def Cartesian2Polar(Punto3D,Punto3DOrigen=None):
    '''!
    @brief: Método que convierte de coordenadas cartesianas a coordenadas polares.
    @param Punto3D Punto3D: Objeto de la clas Punto3D con las coordenadas a transformas.
    @param Punto3DOrigen Punto3D: Objeto de la clase Punto3D para fijar las coordenadas del origen de cálculo.
    @return float,float,float: Devuelve los valores de azimut ángulo de elevación y distancia.
    '''

    if not isinstance(Punto3D, pt3.Punto3D):
        raise Exception("Se esperaba un objeto de la clase Punto3D en el constructor.")
    else:
        if Punto3DOrigen==None:
            PO=pt3.Punto3D(0,0,0)
        else:
            if not isinstance(Punto3DOrigen, pt3.Punto3D):
                raise Exception("Se esperaba un objeto de la clase Punto3D en el constructor.")
            else:
                PO=Punto3DOrigen
        d=d3.Distancia3D(PO,Punto3D).getDistancia3D()
        azi=az.Azimut(PO,Punto3D).getAzimut()
        eleva=ele.AnguloElevacion(PO,Punto3D).getAnguloElevacion()
        
    return azi,eleva,d

def main():

    az,ele,d=Cartesian2Polar(pt3.Punto3D(1,-10,50))
    print(az,ele,d)

if __name__=="__main__":
    main()

        
            
        
    
        
    