#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
################################################################################

""" 
    This program is free software; you can redistribute it and/or modify  
    it under the terms of the GNU General Public License as published by  
    the Free Software Foundation; either version 2 of the License, or     
    (at your option) any later version.
    
@author: Antonio Hermosilla Rodrigo
@version: 1.0.0
@since: 13-10-2014.
@contact: anherro285@gmail.com
@copyright: (C) 2014 by Antonio Hermosilla Rodrigo.
@summary: Conversión de coordenadas cartesianas a polares.
"""

__docformat__ = "epytext"

import sys

import Geometrias.Punto3D as pt3
import Topografia.AnguloElevacion as ele
import Topografia.Azimut as az
import Topografia.Distancia3D as d3


sys.path.append('..')


def Cartesian2Polar(*args):
    if len(args)!=1:
        raise Exception("El constructor de la clase sólo admite un argumento.")
    elif not isinstance(args[0], pt3.Punto3D):
        raise Exception("Se esperaba un objeto de la clase Punto3D en el constructor.")
    else:
        d=d3.Distancia3D(pt3.Punto3D(0,0,0),args[0]).get_Distancia3D()
        azi=az.Azimut(pt3.Punto3D(0,0,0),args[0]).get_Azimut()
        eleva=ele.AnguloElevacion(pt3.Punto3D(0,0,0),args[0]).get_Angulo_Elevacion();
        
    return [d,azi,eleva]

def main():

    p1=Cartesian2Polar(pt3.Punto3D(1,-10,50))
    print(p1[0],p1[1],p1[2])

if __name__=="__main__":
    main()

        
            
        
    
        
    