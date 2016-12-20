#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 4/5/2015

@author: Antonio Hermosilla Rodrigo.
@contact: anherro285@gmail.com
@organization: Antonio Hermosilla Rodrigo.
@copyright: (C) 2015 by Antonio Hermosilla Rodrigo
@version: 1.0.0
'''
import Geometrias.PuntoUTM as putm
import Geometrias.Angulo as ang
import Topografia.Azimut as azi


import Proyecciones.UTM2Geo as utm2geo
import Geodesia.RadiosDeCurvatura as radCur
import Geodesia.Elipsoides as elip
from math import cos,pi
from numpy import mean

import Geodesia.RAC as rac


class RadiacionUTM(object):
    '''
    classdocs
    '''
    __pEst=None
    __d=None
    __az=None
    __referencias=None
    __lecturasRef=None

    def __init__(self, PuntoEstacion,Referencias=[],Lecturas=[]):
        '''!
        Constructor de la clase Radiacion2D.
        '''
        self.setPuntoEstacion(PuntoEstacion)
        self.setReferencias(Referencias)
        self.setLecturasReferencias(Lecturas)
        self.__checkRefLec()
        
    def setReferencias(self,Referencias):
        '''!
        \brief Método que establece los puntos tomados como referencia para calcular la rediación.
        \param Referencias [PuntoUTM]: Lista con los puntos que hacen de referencia.
        \note Referencias Si no se expecifica ninguna refrencia, se supondrá que la lectura horizontal es un acimut.
        \note Referencias Se debe itroducir el mismo número de Referencias que de lecturas.
        
        '''
        if isinstance(Referencias, list):
            if Referencias==[]:
                return
            else:
                for i in Referencias:
                    if not isinstance(i, putm.PuntoUTM):
                        raise Exception("No es de la clase PuntoUTM")
                self.__referencias=Referencias
        else:
            raise Exception("Se esperaba una lista")
        
        
    def setPuntoEstacion(self,PuntoEstacion):
        '''!
        @brief Método que establece el Punto estación.
        @param PuntoEstacion Punto2D|Punto3D: Punto estación con las coordenadas.
        '''
        if isinstance(PuntoEstacion, putm.PuntoUTM):
            self.__pEst=PuntoEstacion
        else:
            raise Exception("Se esperaba un objeto de la clase Punto2D o Punto3D como valor de entrada.")
        
    def setLecturasReferencias(self,Lecturas):
        '''!
        \brief Método que establece las lecturas horizontales a las referencias.
        \param Lecturas [Angulo]: Lecturas a cada una de las refrencias introducidas.
        \note Lecturas Las lecturas son ángulos centesimales.
        \note Lecturas Se debe incluir el mismo número de lecturas que de referencias.
        '''
        if isinstance(Lecturas, list):
            if Lecturas==[]:
                return
            else:
                for i in Lecturas:
                    if not isinstance(i, ang.Angulo):
                        raise Exception("No es de la clase Angulo")
                    if i.getFormato()!='centesimal':
                        raise Exception('Se esperaba un ángulo centesimal')
                self.__lecturasRef=Lecturas
        else:
            raise Exception("Se esperaba una lista")
        
    def getReferencias(self):
        '''!
        '''
        return self.__referencias
    
    def getLecturasReferencias(self):
        '''!
        '''
        return self.__lecturasRef
        
    def __checkRefLec(self):
        '''!
        '''
        print(self.getReferencias())
        if len(self.getReferencias())==len(self.getLecturasReferencias()):
            return
        else:
            raise Exception('El número de lecturas no coincide con el número de referencias introducidas.')
    
    
    def __checkDistancia(self,Distancia):
        '''!
        '''
        if isinstance(Distancia,list):
            for i in Distancia:
                try:
                    float(i)
                except Exception as e:
                    raise Exception(e)
            
        elif isinstance(Distancia, float) or isinstance(Distancia, int) or isinstance(Distancia, str):
            try:
                float(Distancia)
            except Exception as e:
                raise Exception(e)
        else:
            raise Exception("No se reconoce el valor introducido como distancia.")
        
    def __checkLecturaHorizontal(self,LecturaHorizontal):
        '''!
        '''
        if isinstance(LecturaHorizontal, list):
            for i in LecturaHorizontal:
                if not isinstance(i, ang.Angulo):
                    raise Exception("No es ángulo")
                if not i.getFormato()=='centesimal':
                    raise Exception('El ángulo debe ser de tipo centesimal.')
        elif isinstance(LecturaHorizontal, ang.Angulo):
            if not LecturaHorizontal.getFormato()=='centesimal':
                raise Exception('El ángulo debe ser de tipo centesimal.')
        else:
            raise Exception("No es ángulo")
        
        
    def __checkLecDis(self,Distancia,LecturaHorizontal):
        '''!
        '''
        if isinstance(Distancia, list) and isinstance(LecturaHorizontal, list):
            if len(Distancia)==len(LecturaHorizontal):
                return True
            else:
                raise Exception("El número de distancias y lecturas horizontales debe de coincidir")
    
    def RAC(self,p1,p2):
        '''!
        '''
    
        
    def RadiacionUTM(self,NombreElipsoide,Distancia,LecturaHorizontal):
        '''!
        @brief: Método que cálculo la radiación con los parametros introducidos.
        @return PuntoUTM: Devuelve un Punto2D con las coordenadas del punto radiado.
        '''
        #Comprobaciones.
        self.__checkDistancia(Distancia)
        self.__checkLecturaHorizontal(LecturaHorizontal)
        print(rac.RAC(self.__pEst,self.__referencias[0],NombreElipsoide))
        #Claculo de la raidiación.
        desmean=0
        angaux=ang.Angulo()
        #angaux.setGirar(True)
        angaux.setNegativos(True)
        self.__checkRefLec()
        
        if self.getReferencias()!=[] and self.getLecturasReferencias()!=[]:
            #Cálculo azimuts referencia.
            azRef=[]
            azimuts=azi.Azimut()
            azimuts.setPuntoInicial(self.__pEst)
            for i in self.__referencias:
                azimuts.setPuntoFinal(i)
                azRef.append(azimuts.getAzimut())#acc
            print(azRef)
            #Cálculo desorientaciones.
            des=[]
            for i,j in zip(azRef,self.__lecturasRef):
                j.Convertir('radian')
                deso=i-j.getAngulo()
                angaux.setAngulo(deso)
                angaux.setFormato('radian')
                des.append(angaux.getAngulo())
        #print(des)
        #Cálculo de la radiación
            desmean=mean(des)
        print(desmean)
        
        
        
        
        
        
        rc=radCur.RadiosDeCurvatura(NombreElipsoide)
        EL=elip.Elipsoides(NombreElipsoide)
        #1º Radiación con RAC12 y kEst
        #Acimut aplicando RAC12
        #iteraciones con RAC13 y kmedio.
        #azimut aplicando RAC12 y RAC13    
        geoEst=utm2geo.UTM2Geo(self.__pEst,NombreElipsoide)
        convEst=self.__pEst.getConvergenciaMeridianos() #Vienen en pseudo
        convEst=ang.Angulo(convEst,formato='pseudosexagesimal')
        convEst.Convertir('sexagesimal')
        print(convEst.getAngulo())
        convEst.Convertir(Formato='radian')
        convEst=convEst.getAngulo()
        kpEst=self.__pEst.getEscalaLocalPunto()
        nhuEst=rc.getRadioPrimerVertical(geoEst.getLatitud())
        roEst=rc.getRadioElipseMeridiana(geoEst.getLatitud())

        print(kpEst,convEst)

#         Radia2d=rad2d.Radiacion2D(pt2d.Punto2D(self.__x,self.__y),self.__d*k1a,(self.__az+convA)*200/pi)
#         res=Radia2d.Radiacion2D()
#         
#         putmb=putm.PuntoUTM(res.getX(),res.getY())
#         self.__xsal=res.getX()
#         self.__ysal=res.getY()
#         print(self.__xsal,self.__ysal)
#         xant=0
#         yant=0
#         while(abs(xant-self.__xsal)>0.0001):
#             print(abs(xant-self.__xsal))
#             xant=self.__xsal
#             yant=self.__ysal
#             geo2=utm2geo.UTM2Geo(putmb,Elipsoide)
#             nhu2=rc.getRadioPrimerVertical(geo2.getLatitud())
#             ro2=rc.getRadioElipseMeridiana(geo2.getLatitud())
#             k1b=putmb.getEscalaLocalPunto()
#             convB=putmb.getConvergenciaMeridianos()
#             convB=ang.Angulo(convB,formato='pseudosexagesimal')
#             convB.Convertir(Formato='radian')
#             convB=convB.getAngulo()
#             
#             k1m=(k1a+k1b)/2
#             k1=6/((1/k1a)+(4/k1m)+(1/k1b))
#             s=k1*self.__d
#             azcg=self.__az+convA
#             lat=ang.Angulo(geo1.getLatitud(),formato='pseudosexagesimal')
#             lat.Convertir(Formato='radian')
#             lat=lat.getAngulo()     
#             e2=EL.getSegundaExcentricidad()
#             n2=((e2**2))*(cos(lat)**2) #Probar con la laitud media de ambos.
#             #Coordenada al meridiano.
#             x1=(self.__x-500000)/0.9996
#             x2=(self.__xsal-500000)/0.9996
#             
#             dtAB=(((self.__ysal/0.9996-self.__y/0.9996)*(2*x2+x1))/(6*((nhu1+nhu2)/2)*((ro1+ro2)/2)))*(1+n2)
#             azcc=azcg+dtAB
#             
#             d=s-((1/24)*(((((x1+x2)/2)*(cos(azcc)))/((0.9996**2)*((nhu1+nhu2)/2)*((ro1+ro2)/2)))**2)*s**3)
#             print(dtAB,d)
#             Radia2d.setAzimut(azcc*200/pi)
#             Radia2d.setDistancia(d)
#             res=Radia2d.Radiacion2D()
#             self.__xsal=res.getX()
#             self.__ysal=res.getY()
#             putmb=putm.PuntoUTM(res.getX(),res.getY())
#             print(self.__xsal,self.__ysal)
            
        
        
        
        
def main():
    '''!
    '''
    pest=putm.PuntoUTM(720478.006,4404082.474)
    pref=[putm.PuntoUTM(724835.704,4434215.362)]
    lecs=[ang.Angulo(304.72931,formato='centesimal')]
    rad2d=RadiacionUTM(pest,pref,lecs)
#     rad2d=Radiacion2D(pest)
#     dis=[100,200,300]
#     angs=[ang.Angulo(150,formato='centesimal'),ang.Angulo(250,formato='centesimal'),ang.Angulo(350,formato='centesimal')]
    sal=rad2d.RadiacionUTM('WGS 84',10658.332, ang.Angulo(9.7324,formato='centesimal'))
    for i in sal:
        print(i.getX(),i.getY())
    #from math import pi
#     p=putm.PuntoUTM(718763.1524,4397605.0467)
#     rutm=RadiacionUTM(p)
#     rutm.RadiacionUTM('WGS 84',100,ang.Angulo(150,formato='centesimal'))
    
if __name__=='__main__':
    main()
        
        