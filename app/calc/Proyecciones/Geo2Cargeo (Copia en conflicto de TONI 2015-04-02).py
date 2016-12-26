# -*- coding: utf-8 -*-
'''!
Created on 6/2/2015

@author: Antonio Hermosilla Rodrigo.
@contact: anherro285@gmail.com
@organization: Antonio Hermosilla Rodrigo.
@copyright: (C) 2011 by Antonio Hermosilla Rodrigo
@version: 1.0.0
'''
from math import cos,sin

import Geometrias.Angulo as ang
import Geodesia.Elipsoides as Elip
import Geodesia.RadiosDeCurvatura as Rad
import Geometrias.Punto3D as pt3
import Geometrias.PuntoGeodesico as pgeo



def Geo2Cargeo(PuntoGeodesico,NombreElipsoide):
    '''
    @brief: Funcion que transforma de Coordenadas geodesicas a coordenadas Cartesianaes Geocentricas.
    
    @param PuntoGeodesico PuntoGeodesico: Punto Geodesico con las coordenadas del punto.
    @param NombreElipsoide str: Nombre del elipsoide de calculo.
    
    @raise Valor Punto Geodesico: Se produce una excepción en el caso de que el punto introducido
                                  no sea de tipo puntoGeodesico.
    @raise Valor Nombre Elipsoide: Se produce una excepción en el caso que el el Nombre del elipsoide
                                   no sea de tipo String.
                                   
    @return Punto3D: Valor del punto calculado.
    '''
    if not isinstance(PuntoGeodesico,pgeo.PuntoGeodesico):
        raise Exception("Valor Punto Geodesico")
    
    try:
        NombreElipsoide=str(NombreElipsoide)
    except:
        raise Exception("Valor Nombre Elipsoide")
    
    Latitud=ang.Angulo(PuntoGeodesico.getLatitud(),formato='latitud')
    Longitud=ang.Angulo(PuntoGeodesico.getLongitud(),formato='longitud180')
    AlturaElipsoidal=PuntoGeodesico.getAlturaElipsoidal()
    
    #Conversion a radian.
    Latitud.Convertir('radian')
    Longitud.Convertir('radian')
    #Calculo de parámetros.
    Elipsoide= Elip.Elipsoides(NombreElipsoide)
    e=Elipsoide.getPrimeraExcentricidad()
    nhu=Rad.RadiosDeCurvatura(NombreElipsoide).getRadioPrimerVertical(Latitud.getAngulo())
    #Cálculo de Coordenadas.            
    X=(nhu+AlturaElipsoidal)*(cos(Latitud.getAngulo()))*(cos(Longitud.getAngulo()))
    Y=(nhu+AlturaElipsoidal)*(cos(Latitud.getAngulo()))*(sin(Longitud.getAngulo()))
    Z=(nhu*(1.0-(e**2))+AlturaElipsoidal)*(sin(Latitud.getAngulo()))
    
    return pt3.Punto3D(X, Y, Z, negativos=True)


def main():
    print("Prueba de la conversión de coordenadas.")
    print("Elipsoide de pruebas:\tGRS80")
    print("Coordenadas geodesicas de prueba:")
    print("\tLatitud:\t45")
    print("\tLongitud:\t-1")
    print("\th elipsoidal:\t50")
    print("\n")
    print("Resultados:")
    p1=Geo2Cargeo(pgeo.PuntoGeodesico(45,-1,50),"GRS 1980")
    print("X: %.3f"%p1.getX())
    print("Y: %.3f"%p1.getY())
    print("Z: %.3f"%p1.getZ())
    print("\n")






if __name__=="__main__":
    main()
