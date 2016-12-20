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

from math import sqrt,atan,cos
import Geometrias.Angulo as ang
import Geodesia.Elipsoides as Elip
import Geodesia.RadiosDeCurvatura as Rad
import Geometrias.Punto3D as pt3
import Geometrias.PuntoGeodesico as pgeo

def Cargeo2Geo(Punto,NombreElipsoide):
    '''!
    @brief: Funcion que transforma de Coordenadas Cartesianas Geocentricas a Geodesicas Elipsoidales.
    
    @param Punto Punto3D: Punto3D con las coordenadas Cartesianas Geocentricas.
    @param NombreElipsoide str: Nombre del elipsoide de calculo.
    
    @raise Valor Punto3D: Se produce una excepción en el caso de que el punto introducido no sea de tipo punto3D.
    @raise Valor Nombre Elipsoide: Se produce una excepción en el caso que el el Nombre del elipsoide no sea de tipo String.
                                   
    @return PuntoGeodesico: Punto Geodesico con el resultado.
    '''
    if not isinstance(Punto,pt3.Punto3D):
        raise Exception("Se esperaba un objeto de la clase Punto3D como primer valor de entrada del constructor.")
    
    try:
        NombreElipsoide=str(NombreElipsoide)
    except:
        raise Exception("Se esperaba un str como segundo valor entrada de la función.")
    
    x=Punto.getX()
    y=Punto.getY()
    z=Punto.getZ()
    #Calculo de parámetros.
    Elipsoide= Elip.Elipsoides(NombreElipsoide)
    e=Elipsoide.getPrimeraExcentricidad()
    #Calculos auxiliares
    r=sqrt((x**2)+(y**2))
    latact=atan((z/r)/(1.0-(e**2)))
    latiter=0.0
    helip=0.0
    cont=0
    aux=Rad.RadiosDeCurvatura(NombreElipsoide)
    while abs(latact-latiter) > 0.000000000001 :
        if cont !=0:
            latact=latiter
        nhu=aux.getRadioPrimerVertical(latact)
        helip=(r/cos(latact))-nhu
        latiter=atan((z/r)/(1.0-((e**2)*(nhu/(nhu+helip)))))
        cont+=1
    '''
    Casos del arcotangente CUADRANTES
    '''
        
    Lat=ang.Angulo(latiter,formato='radian')
    Lon=ang.Angulo(atan(y/x),formato='radian')
    Lat.Convertir('latitud')
    Lon.Convertir('longitud180')

    return pgeo.PuntoGeodesico(Lat, Lon, helip)

def Cargeo2GeoFromFile(File,NombreElipsoide):
    from os.path import exists,isfile
    from PyQt4 import QtGui
    '''!
    '''
    #ID,X,Y,Z
    if not type(File)==str:
        raise Exception("Not str")
    if not exists(File):
        raise Exception("Not Exists")
    if not isfile(File):
        raise Exception("Not File")
    IDS=[]
    Xs=[]
    Ys=[]
    Zs=[]
    f=open(File,'r')
    for i in f:
        QtGui.QApplication.processEvents()
        i=i.split(",")
        IDS.append(i[0])
        Xs.append(i[1])
        Ys.append(i[2])
        Zs.append(i[3])
    f.close()
        
    Sal=[]
    for ids,i,j,k in zip(IDS,Xs,Ys,Zs):
        QtGui.QApplication.processEvents()
        p=pt3.Punto3D(i,j,k)
        p1=Cargeo2Geo(p, NombreElipsoide)
        Sal.append([ids,p,p1])
    
    return Sal
        



def main():
    print("Prueba de la conversión de coordenadas.")
    print("Elipsoide de pruebas:\tGRS80")
    print("Coordenadas geodesicas de prueba:")
    print("\tX:\t4516938.178")
    print("\tY:\t-78843.449")
    print("\tZ:\t4487383.764")
    print("\n")


    p1=pt3.Punto3D(6350095.806,587201.017,112526.845)
    p2=Cargeo2Geo(p1,"WGS 84")
    print("Resultados:")
    print("Latitud:\t%.8f"%p2.getLatitud())
    print("Longitud:\t%.8f"%p2.getLongitud())
    print("h Elipsoidal:\t%.3f"%p2.getAlturaElipsoidal())
    print("\n")

if __name__=="__main__":
    main()
