#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''!
Created on 4/3/2015

@author: Antonio Hermosilla Rodrigo.
@contact: anherro285@gmail.com
@organization: Antonio Hermosilla Rodrigo.
@copyright: (C) 2015 by Antonio Hermosilla Rodrigo
@version: 1.0.0
'''
import Geometrias.PuntoGeodesico as pgeo
import Geometrias.Angulo as ang
import Geodesia.Elipsoides as elip
from numpy import matrix,dot

from math import tan,cos,sin,asin,atan2,pi,atan

class PIGeodesia(object):
    '''!
    classdocs
    '''
    __pgeo1=None
    __pgeo2=None


    def __init__(self, PGInicial,PGFinal):
        '''!
        Constructor
        @param PGInicial PuntoGeodesico: Punto Geodésico inicial de la línea.
        @param PGFinal PuntoGeodesico: Punto Geodésico final de la línea.
        '''
        self.setPGInicial(PGInicial)
        self.setPGFinal(PGFinal)
        
        
    def setPGInicial(self,PGInicial):
        '''!
        @brief: Método que establece y comprueba el punto geodésio inicial.
        @param PGInicial PuntoGeodesico: Punto Geodésico inicial de la línea.
        '''
        if not isinstance(PGInicial, pgeo.PuntoGeodesico):
            raise Exception("Se esperaba un objeto de la clase PuntoGeodesico como parametro de entrada para el punto inicial.")
        self.__pgeo1=PGInicial
        
    def setPGFinal(self,PGFinal):
        '''!
        @brief: Método que establece y comprueba el punto geodésio final.
        @param PGFinal PuntoGeodesico: Punto Geodésico final de la línea.
        '''
        if not isinstance(PGFinal, pgeo.PuntoGeodesico):
            raise Exception("Se esperaba un objeto de la clase PuntoGeodesico como parametro de entrada para el punto final.")
        self.__pgeo2=PGFinal
        
        
#     def CalcularEsfera(self):
#         '''!
#         @brief: Método que resuelve el problema inverso de la geodesia sobre la esfera.
#         '''
#         lat1=ang.Angulo(self.__pgeo1.getLatitud(),formato='pseudosexagesimal')
#         lat1.Convertir('radian')
#         lat1=lat1.getAngulo()
#         
#         lon1=ang.Angulo(self.__pgeo1.getLongitud(),formato='pseudosexagesimal')
#         lon1.Convertir('radian')
#         lon1=lon1.getAngulo()
#         
#         lat2=ang.Angulo(self.__pgeo2.getLatitud(),formato='pseudosexagesimal')
#         lat2.Convertir('radian')
#         lat2=lat2.getAngulo()
#         
#         lon2=ang.Angulo(self.__pgeo2.getLongitud(),formato='pseudosexagesimal')
#         lon2.Convertir('radian')
#         lon2=lon2.getAngulo()
#         
#         #Solución PI Esfera:
#         s2=matrix([[(cos(latesf2)*cos(lonesf2))],
#                   [(cos(latesf2)*sin(lonesf2))],
#                   [(sin(latesf2))]])
#         m1=matrix([[(-sin(latesf1)*cos(lonesf1)),(-sin(latesf1)*sin(lonesf1)),(cos(latesf1))],
#                   [(sin(lonesf1)),(-cos(lonesf1)),(0)],
#                   [(cos(latesf1)*cos(lonesf1)),(cos(latesf1)*sin(lonesf1)),(sin(latesf1))]])
#         
#         sol=dot(m1,s2)
# 
#         lonsal=atan2(float(sol[1]),float(sol[0]))
#         latsal=asin(float(sol[2]))
#         
#         azsal=0 #Ya es el bueno.
#         s=(pi/2)-latsal #Distancia sobre la esfera
#         if lonsal==0:
#             azsal=0
#         elif lonsal<0:
#             azsal=abs(lonsal)
#         elif lonsal>0:
#             azsal=2*pi-lonsal
                
                
        
        
    def CalcularBessel(self,NombreElipsoide):
        '''!
        @brief: Método que calcula el problema inverso de la geodesia.
        @param NombreElipsoide str: Elipsoide de calculo.
        @return 
        '''
        lat1=ang.Angulo(self.__pgeo1.getLatitud(),formato='pseudosexagesimal')
        lat1.Convertir('radian')
        lat1=lat1.getAngulo()
        
        lon1=ang.Angulo(self.__pgeo1.getLongitud(),formato='pseudosexagesimal')
        lon1.Convertir('radian')
        lon1=lon1.getAngulo()
        
        lat2=ang.Angulo(self.__pgeo2.getLatitud(),formato='pseudosexagesimal')
        lat2.Convertir('radian')
        lat2=lat2.getAngulo()
        
        lon2=ang.Angulo(self.__pgeo2.getLongitud(),formato='pseudosexagesimal')
        lon2.Convertir('radian')
        lon2=lon2.getAngulo()
        
        Alon=lon2-lon1
        
        elipsoide=elip.Elipsoides(NombreElipsoide)
        a=elipsoide.getSemiEjeMayor()
        b=elipsoide.getSemiEjeMenor()
        e1=elipsoide.getPrimeraExcentricidad()
        
        latesf1=atan((b/a)*tan(lat1))
        latesf2=atan((b/a)*tan(lat2))
        
        lonesf1=lon1
        
        correccion=0
        
        correccion1=Alon
        
        while abs(correccion-correccion1)>0.0000000001:
            correccion1=correccion
            lonesf2=lonesf1+Alon+correccion
            #Solución PI Esfera:
            s2=matrix([[(cos(latesf2)*cos(lonesf2))],
                      [(cos(latesf2)*sin(lonesf2))],
                      [(sin(latesf2))]])
            m1=matrix([[(-sin(latesf1)*cos(lonesf1)),(-sin(latesf1)*sin(lonesf1)),(cos(latesf1))],
                      [(sin(lonesf1)),(-cos(lonesf1)),(0)],
                      [(cos(latesf1)*cos(lonesf1)),(cos(latesf1)*sin(lonesf1)),(sin(latesf1))]])
            
            sol=dot(m1,s2)

            lonsal=atan2(float(sol[1]),float(sol[0]))
            latsal=asin(float(sol[2]))
            
            azsal=0 #Ya es el bueno.
            s=(pi/2)-latsal #Distancia sobre la esfera
            if lonsal==0:
                azsal=0
            elif lonsal<0:
                azsal=abs(lonsal)
            elif lonsal>0:
                azsal=2*pi-lonsal
            
            #Problema inverso en el elipsoide
            M=atan2(tan(latesf1),cos(azsal))
            m=asin(sin(azsal)*cos(latesf1))
            
            #Calculo de las integrales.
            cMs=cos(M+s)
            sMs=sin(M+s)
            sMs3=sMs**3
            sMs5=sMs**5
            cm=cos(m)
            cm2=cm**2
            cm4=cm**4
            cm6=cm**6
            cM=cos(M)
            sm=sin(m)
            sM=sin(M)
            sM3=sM**3
            sM5=sM**5
             
            I1=(s)+\
            ((1/2)*cm2*cMs*sMs)-\
            ((1/2)*s*cm2)-\
            ((1/2)*cm2*cM*sM)
             
            I2=(s)+\
            (cm2*cMs*sMs)-\
            (s*cm2)-\
            ((1/4)*cm4*cMs*sMs3)-\
            ((3/8)*cm4*cMs*sMs)-\
            ((3/8)*s*cm4)-\
            (cm2*cM*sM)+\
            ((1/4)*cm4*cM*sM3)+\
            ((3/8)*cm4*cM*sM)
             
            I3=(s)+\
            ((3/2)*cm2*cMs*sMs)-\
            ((3/2)*s*cm2)-\
            ((3/4)*cm4*cMs*sMs3)-\
            ((9/8)*cm4*cMs*sMs)+\
            ((9/8)*s*cm4)+\
            ((1/6)*cm6*cMs*sMs5)+\
            ((5/24)*cm6*cMs*sMs3)+\
            ((5/16)*cm6*cMs*sMs)-\
            ((5/16)*s*cm6)+\
            ((3/2)*cm2*cMs*sMs)+\
            ((3/4)*cm4*cM*sM3)-\
            ((9/8)*cm4*cM*sM)-\
            ((1/6)*cm6*cM*sM5)-\
            ((5/24)*cm6*cM*sM3)-\
            ((5/16)*cm6*cM*sM)
            
            correccion=((e1**2*sm)/2)*\
            ((s)+(((e1**2)/4)*(I1))+(((e1**4)/8)*(I2))+(((5*e1**6)/64)*(I3)))
            
            #print(azsal,s*(a+b)/2,correccion,correccion1)
            #input()
        return azsal,s
        
        
        
        
def main():
    PI=PIGeodesia(pgeo.PuntoGeodesico(50,10),pgeo.PuntoGeodesico(40,9))
    az,s=PI.CalcularBessel('WGS 84')
    az=ang.Angulo(az)
    az.Convertir('sexagesimal')
    print(az.getAngulo(),s)
    #Solucion PAG: AZ:184º 25' 5,72''  s: 1114083,080 m


if __name__=="__main__":
    main()