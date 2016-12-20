#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''!
Created on 5/2/2015

@author: Antonio Hermosilla Rodrigo.
@contact: anherro285@gmail.com
@organization: Antonio Hermosilla Rodrigo.
@copyright: (C) 2015 by Antonio Hermosilla Rodrigo
@version: 1.0.0
'''

from math import sqrt,pow,sin

import Geodesia.Elipsoides as Elipsoide
import Geometrias.PuntoGeodesico as pgeo
import Geometrias.Angulo as ang


class RadiosDeCurvatura(object):
    __elip=None
    def __init__(self,NombreElipsoide):
        '''!
        Constructor de la clase RadiosDeCurvatura.
        @param NombreElipsoide str: Nombre del elipsoide.
        '''
        self.__elip=Elipsoide.Elipsoides(NombreElipsoide)

    def __CheckValor(self,Latitud):
        if isinstance(Latitud,float) or isinstance(Latitud,pgeo.PuntoGeodesico):
            pass
        else:
            raise Exception("El valor introducido no es válido")

    def getRadioPrimerVertical(self,Latitud):
        '''!
        @brief: Método que cálcula el valor del radio del primer vertical del elipsoide.
        @param Latitud float|PuntoGeodesico: Latitud del punto de cálculo en Radianes.
        @note Latitud: La latitud del punto se puede introducir como un valor float, o como un objeto de la clase PuntoGeodesico.
        @return float: Valor del radio del primer vetical en metros (nhu).
        '''
        lat=None
        self.__CheckValor(Latitud)
        if isinstance(Latitud,float):
            lat=Latitud
        elif isinstance(Latitud,pgeo.PuntoGeodesico):
            aux=ang.Angulo(Latitud.getLatitud(),formato="latitud")
            aux.Convertir('radian')
            lat=aux.getAngulo()
        Latitud=None
        numerador=self.__elip.getSemiEjeMayor()
        denominador=sqrt(1-((self.__elip.getPrimeraExcentricidad()**2)*(sin(lat)**2)))
        return numerador/denominador

    def getRadioElipseMeridiana(self,Latitud):
        '''!
        @brief: Método que cálcula el valor del radio de la elipse meridiana.
        @param Latitud float|PuntoGeodesico: Latitud del punto de cálculo en Radianes.
        @note Latitud: La latitud del punto se puede introducir como un valor float, o como un objeto de la clase PuntoGeodesico.
        @return: float: Valor del radio de la elipse meridiana en metros (ro).
        '''
        lat=None
        self.__CheckValor(Latitud)
        if isinstance(Latitud,float):
            lat=Latitud
        elif isinstance(Latitud,pgeo.PuntoGeodesico):
            aux=ang.Angulo(Latitud.getLatitud(),formato="latitud")
            aux.Convertir('radian')
            lat=aux.getAngulo()
        Latitud=None
        #Se da por supuesto que la latitud ya entra en radianes.
        numerador=self.__elip.getSemiEjeMayor()*(1-(self.__elip.getPrimeraExcentricidad()**2))
        denominador=pow(1-((self.__elip.getPrimeraExcentricidad()**2)*(sin(lat)**2)),1.5)
        return numerador/denominador
    
    
        
        



def main():
    r=RadiosDeCurvatura("WGS 84")
    print(r.getRadioPrimerVertical(0.785398163),
          r.getRadioElipseMeridiana(0.785398163))
    p=pgeo.PuntoGeodesico(ang.Angulo(45,formato="latitud"),ang.Angulo(45,formato="longitud180"))
    print(r.getRadioPrimerVertical(p),
          r.getRadioElipseMeridiana(p))
    p=pgeo.PuntoGeodesico(ang.Angulo(0,formato="latitud"),ang.Angulo(45,formato="longitud180"))
    print(r.getRadioPrimerVertical(p),
          r.getRadioElipseMeridiana(p))


if __name__=="__main__":
    main()

