#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 7/5/2015

@author: Antonio Hermosilla Rodrigo.
@contact: anherro285@gmail.com
@organization: Antonio Hermosilla Rodrigo.
@copyright: (C) 2015 by Antonio Hermosilla Rodrigo
@version: 1.0.0
'''
import Geodesia.RadiosDeCurvatura as rcur
import Proyecciones.UTM2Geo as utm2geo
import Geometrias.Angulo as ang
import Geodesia.Elipsoides as elipsoides
from math import cos

def RAC(puntoUTM1,puntoUTM2,NombreElipsoide):
    '''!
    '''
    radcur=rcur.RadiosDeCurvatura(NombreElipsoide)
    elip=elipsoides.Elipsoides(NombreElipsoide)
    #punto1
    angaux=ang.Angulo()
    geo1=utm2geo.UTM2Geo(puntoUTM1, NombreElipsoide)
    angaux.setAngulo(geo1.getLatitud())
    angaux.setFormato('pseudosexagesimal')
    angaux.Convertir('raidian')
    nhu1=radcur.getRadioPrimerVertical(angaux.getAngulo())
    ro1=radcur.getRadioElipseMeridiana(angaux.getAngulo())
    x1=(puntoUTM1.getX()-500000)/(0.9996)
    y1=puntoUTM1.getY()/0.9996
    n21=((elip.getSegundaExcentricidad()**2))*((cos(angaux.getAngulo())**2))
    #punto2
    angaux=ang.Angulo()
    geo2=utm2geo.UTM2Geo(puntoUTM2, NombreElipsoide)
    angaux.setAngulo(geo2.getLatitud())
    angaux.setFormato('pseudosexagesimal')
    angaux.Convertir('raidian')
    nhu2=radcur.getRadioPrimerVertical(angaux.getAngulo())
    ro2=radcur.getRadioElipseMeridiana(angaux.getAngulo())
    x2=(puntoUTM2.getX()-500000)/(0.9996)
    y2=puntoUTM2.getY()/0.9996
    n22=((elip.getSegundaExcentricidad()**2))*((cos(angaux.getAngulo())**2))
    #calculoRAC
    nhum=(nhu1+nhu2)/2.0
    rom=(ro1+ro2)/2.0
    nm=(n21+n22)/2.0
    RAC12=((y2-y1)*(2.0*x1+x2)*(1+nm))/(6.0*nhum*rom)
    RAC21=((y2-y1)*(2.0*x2+x1)*(1+nm))/(6.0*nhum*rom)
    
    return RAC12,RAC21
    
    
    