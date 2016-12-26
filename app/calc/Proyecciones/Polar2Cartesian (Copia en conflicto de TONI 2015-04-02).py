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
@summary: Conversión de coordenadas polares a cartesianas.
"""
__docformat__ = "epytext"

import math
import sys

import Geometrias.Punto3D as pt3


sys.path.append('..')

def Polar2Cartesian(*args):
    if len(args)!=3:
        raise Exception("Se esperaban tres argumentos en la función.")
    try:
        float(args[0])
        float(args[1])
        float(args[2])
    except Exception as e:
        raise Exception(e)
    finally:
        azi=float(args[0])
        ele=float(args[1])
        dis=float(args[2])
        
        x=dis*math.sin(ele)*math.sin(azi)
        y=dis*math.sin(ele)*math.cos(azi)
        z=dis*math.cos(ele)
        
    return pt3.Punto3D(x,y,z)

def main():
    sal=Polar2Cartesian(math.pi,math.pi/4,100)
    
    print(sal.get_Coordenada_X(),sal.get_Coordenada_Y(),sal.get_Coordenada_Z())
    
if __name__=="__main__":
    main()
        