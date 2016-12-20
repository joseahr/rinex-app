#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 27/2/2015

@author: Antonio Hermosilla Rodrigo.
@contact: anherro285@gmail.com
@organization: Antonio Hermosilla Rodrigo.
@copyright: (C) 2015 by Antonio Hermosilla Rodrigo
@version: 1.0.0
'''
import Geometrias.PuntoGeodesico as pgeo
import Geometrias.Angulo as ang
from math import sin,cos,tan,pi
import Geodesia.Elipsoides as elip
import Geodesia.RadiosDeCurvatura as radcur

class PDGeodesia(object):
    '''
    classdocs
    '''
    __pgeo=None
    __d=None
    __az=None
    __lat=None
    __lon=None


    def __init__(self, PuntoGeodesico,Distancia,Azimut):
        '''
        Constructor de la clase PDGeodesia.
        
        @param PuntoGeodesico PuntoGeodesico: Punto Geodésico inicial.
        @param Distancia float|int|str: Distancia observada al siguiente punto.
        @param Azimut float|int|str: Azimut de la línea observada.
        '''
        self.setPuntoGeodesico(PuntoGeodesico)
        self.setDistancia(Distancia)
        self.setAzimut(Azimut)
        
    
    def setPuntoGeodesico(self,PuntoGeodesico):
        '''!
        @brief: Método que establece y asigna el Punto geodesico.
        @param PuntoGeodesico PuntoGeodesico: PuntoGeodesico inicial.
        '''
        if not isinstance(PuntoGeodesico, pgeo.PuntoGeodesico):
            raise Exception("El punto introducido no es una instancia de la clase PuntoGeodesico.")
        self.__pgeo=PuntoGeodesico
        self.__lat=ang.Angulo(PuntoGeodesico.getLatitud(),formato='pseudosexagesimal')
        self.__lon=ang.Angulo(PuntoGeodesico.getLongitud(),formato='pseudosexagesimal')
        self.__lat.Convertir('radian')
        self.__lon.Convertir('radian')
        
    def setDistancia(self,Distancia):
        '''!
        @brief: Método que establece y comprueba la distancia.
        @param Distancia float|int|str: Distancia del punto incial al final.
        '''
        if isinstance(Distancia, float) or isinstance(Distancia, int) or isinstance(Distancia, str):
            self.__d=float(Distancia)
        else:
            raise Exception("Se esperaba un objeto float o convertible como entrada de la distancia.")
        
    def setAzimut(self,Azimut):
        '''!
        @brief: Método que establece y asigna el azimut:
        @param Azimut float|int|str: Azimut de la línea entre el punto inicila y final en grados pseudoxesagesimales.
        '''
        if isinstance(Azimut, float) or isinstance(Azimut, int) or isinstance(Azimut, str):
            self.__az=ang.Angulo(float(Azimut),formato='pseudosexagesimal')
            self.__az.Convertir('radian')
        elif isinstance(Azimut, ang.Angulo):
            self.__az=Azimut
            self.__az.Convertir('radian')
        else:
            raise Exception("")
        
        
    def CalcularLegendre(self,NombreElipsoide):
        '''!
        @brief: Método que cálcula el punto geodesico final.
        @param NombreElipsoide str: Elipsoide de calculo.
        '''
        az=self.__az.getAngulo()
        lat=self.__lat.getAngulo()
        lon=self.__lon.getAngulo()
        s=self.__d
        elipsoide=elip.Elipsoides(NombreElipsoide)
        a=elipsoide.getSemiEjeMayor()
        e1=elipsoide.getPrimeraExcentricidad()
        radios=radcur.RadiosDeCurvatura(NombreElipsoide)
        nhu=radios.getRadioPrimerVertical(lat)
        ro=radios.getRadioElipseMeridiana(lat)
        latsal=lat+\
        ((cos(az)*s)/(ro))-\
        ((s**2/2)*(((3*e1**2*nhu**2*sin(2*lat)*cos(az)**2)/(2*a**2*ro**2))+\
                   ((tan(lat)*sin(az)**2)/(ro*nhu))))+\
        ((s**3/6)*(((3*e1**4*nhu**4*sin(2*lat)**2*cos(az)**3)/(a**4*ro**3))-\
                   ((3*e1**2*nhu**2+cos(2*lat)*cos(az)**3)/(a**2*ro**3))-\
                   ((sin(az)**2*cos(az))/(ro**2*nhu*cos(lat)**2))+\
                   ((5*e1**2*nhu*sin(2*lat)*tan(lat)*sin(az)**2*cos(az))/(a**2*ro**2))-\
                   ((2*tan(lat)**2*cos(az)*sin(az)**2)/(ro*nhu**2))))
#         print(lat)
#         print(latsal)
        
        lonsal=lon+\
        ((s*sin(az))/(ro))+\
        ((s**2/2)*\
         (-((e1**2*nhu*sin(lat))/(a**2*ro))+\
          ((sin(lat))/(nhu*ro*cos(lat)**2))+\
          ((tan(lat))/(nhu**2*cos(lat))))*\
         (sin(az)*cos(az)*s**2))+\
        ((s**3/6)*\
         (((sin(az)*cos(az)**2)/(ro))*\
          (((e1**4*nhu**3*sin(2*lat)*sin(lat))/(a**4*ro))-\
           ((e1**2*nhu*cos(lat))/(a**2*ro))-\
           ((2*e1**2*nhu*sin(2*lat)*sin(lat))/(a**2*ro*cos(lat)**2))+\
           ((2*tan(lat)**2)/(nhu*ro*cos(lat)))+\
           ((1)/(nhu*ro*cos(lat)))-\
           ((e1**2*tan(lat)*sin(2*lat))/(a**2*cos(lat)))+\
           ((1)/(nhu**2*cos(lat)**3))+\
           ((tan(lat)**2)/(nhu**2)))-\
          ((e1**2*nhu*sin(lat)*cos(2*az)*tan(lat)*sin(az))/(a**2*nhu*ro))+\
          ((tan(lat)**2*sin(az)*cos(2*az))/(nhu**2*ro*cos(lat)))+\
          ((tan(lat)**2*sin(az)*cos(2*az))/(nhu**3*cos(lat)))))
        
        #print(lon)
        #print(lonsal)
        
        azsal=az+\
        ((s*tan(lat)*sin(az))/(nhu))+\
        (((nhu**2*sin(az)*cos(az))/(2))*\
         (-((e1**2*nhu*tan(lat)*sin(2*lat))/(2*a**2*ro))+\
          ((1)/(nhu*ro*cos(lat)**2))+\
          ((tan(lat)**2)/(nhu**2))))+\
        (((s**3*cos(2*az)*tan(lat)*sin(az))/(6*nhu))*\
         (-((e1**2*nhu*tan(lat)*sin(2*lat))/(2*a**2*ro))+\
          ((1)/(nhu*ro*cos(lat)**2))+\
          ((tan(lat)**2)/(nhu**2))))+\
        (((s**3*sin(az)*cos(az)**2)/(6*ro))*\
         (((e1**4*nhu**3*tan(lat)*sin(2*lat)**2)/(2*a**4*ro))-\
          ((e1**2*nhu*sin(2*lat))/(2*a**2*ro*cos(lat)**2))-\
          ((2*e1**2*nhu*tan(lat)*cos(2*lat))/(2*a**2*ro))-\
          ((2*e1**2*nhu*sin(2*lat))/(a**2*ro*cos(lat)**2))+\
          ((2*sin(lat))/(nhu*ro*cos(lat)**3))-\
          ((e1**2*sin(2*lat)*tan(lat)**2)/(2*a**2))+\
          ((1)/(nhu**2*cos(lat)**2))))
        
        #print(az)
        #print(azsal)
        
        return latsal,lonsal,azsal
    
    
    def Rk4o(self,NombreElipsoide,pasos=None):
        '''!
        '''
        az=self.__az.getAngulo()
        lat=self.__lat.getAngulo()
        lon=self.__lon.getAngulo()
        s=self.__d
        radios=radcur.RadiosDeCurvatura(NombreElipsoide)
        if pasos==None:
            if s<=1000:
                pasos=100
            elif s>1000 or s<=10000:
                pasos=1000
            elif s>10000 or s<=100000:
                pasos=10000
            elif s>100000 or s<=1000000:
                pasos=100000
            else:
                pasos=750000
        
        h=s/pasos
        latact=lat
        lonact=lon
        azact=az
        for i in range(pasos):
            nhu=radios.getRadioPrimerVertical(latact)
            ro=radios.getRadioElipseMeridiana(latact)
            k1=h*(cos(azact)/ro)
            m1=h*(sin(azact)/(nhu*cos(latact)))
            n1=h*((tan(latact)*sin(azact))/(nhu))
            
            nhu=radios.getRadioPrimerVertical(latact+(k1/2))
            ro=radios.getRadioElipseMeridiana(latact+(k1/2))
            k2=h*(cos(azact+(n1/2))/ro)
            m2=h*(sin(azact+(n1/2))/(nhu*cos(latact+(k1/2))))
            n2=h*((tan(latact+(k1/2))*sin(azact+(n1/2)))/(nhu))
            
            nhu=radios.getRadioPrimerVertical(latact+(k2/2))
            ro=radios.getRadioElipseMeridiana(latact+(k2/2))
            k3=h*(cos(azact+(n2/2))/ro)
            m3=h*(sin(azact+(n2/2))/(nhu*cos(latact+(k2/2))))
            n3=h*((tan(latact+(k2/2))*sin(azact+(n2/2)))/(nhu))
            
            nhu=radios.getRadioPrimerVertical(latact+(k3))
            ro=radios.getRadioElipseMeridiana(latact+(k3))
            k4=h*(cos(azact+(n3))/ro)
            m4=h*(sin(azact+(n3))/(nhu*cos(latact+(k3))))
            n4=h*((tan(latact+(k3))*sin(azact+(n3)))/(nhu))
            
        
            latact+=((1/6)*(k1+2*k2+2*k3+k4))
            lonact+=((1/6)*(m1+2*m2+2*m3+m4))
            azact+=((1/6)*(n1+2*n2+2*n3+n4))
        #print(latact,lonact,azact)
        if azact<pi:
            azact+=pi
        elif azact>=pi:
            azact-=pi
        return latact,lonact,azact
        
        
def main():
    PD=PDGeodesia(pgeo.PuntoGeodesico(50,10),1500000,140)
    lat,lon,az=PD.Rk4o('Hayford 1950')
    #lat,lon,az=PD.Rk4o('WGS 84')
    #lat,lon,az=PD.CalcularLegendre('WGS 84')
    lat=ang.Angulo(lat)
    lat.Convertir('sexagesimal')
    print(lat.getAngulo())
    lon=ang.Angulo(lon)
    lon.Convertir('sexagesimal')
    print(lon.getAngulo())
    az=ang.Angulo(az)
    az.Convertir('sexagesimal')
    print(az.getAngulo())
    pass

    #Resultados IGN: lat:39º 2' 52,6087'' lon:21º 6' 17,9256''az:327º 50' 6,24"

if __name__=="__main__":
    main()