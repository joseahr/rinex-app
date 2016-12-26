#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 9/3/2015

@author: Antonio Hermosilla Rodrigo.
@contact: anherro285@gmail.com
@organization: Antonio Hermosilla Rodrigo.
@copyright: (C) 2014 by Antonio Hermosilla Rodrigo
@version: 1.0.1
'''
import Geometrias.Punto2D as pt2
import Geometrias.Punto3D as pt3
import Geometrias.Angulo as ang
from math import sin,cos
import Topografia.Azimut as azi
from numpy import mean, std


class Radiacion2D(object):
    '''!
    classdocs
    '''
    __pEst=None
    __d=None
    __az=None
    __referencias=[]
    __lecturasRef=[]


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
        \param Referencias [Punto2D]: Lista con los puntos que hacen de referencia.
        \note Referencias Si no se expecifica ninguna refrencia, se supondrá que la lectura horizontal es un acimut.
        \note Referencias Se debe itroducir el mismo número de Referencias que de lecturas.
        
        '''
        if isinstance(Referencias, list):
            if Referencias==[]:
                return
            else:
                for i in Referencias:
                    if not isinstance(i, pt2.Punto2D):
                        raise Exception("No es de la clase Punto2D")
                self.__referencias=Referencias
        else:
            raise Exception("Se esperaba una lista")
        
        
    def setPuntoEstacion(self,PuntoEstacion):
        '''!
        @brief Método que establece el Punto estación.
        @param PuntoEstacion Punto2D|Punto3D: Punto estación con las coordenadas.
        '''
        if isinstance(PuntoEstacion, pt2.Punto2D):
            self.__pEst=PuntoEstacion
        elif isinstance(PuntoEstacion, pt3.Punto3D):
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
        if not isinstance(self.getReferencias(), list):
            return
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
        
    
        
    def Radiacion2D(self,Distancia,LecturaHorizontal):
        '''!
        @brief: Método que cálculo la radiación con los parametros introducidos.
        @return Punto2D: Devuelve un Punto2D con las coordenadas del punto radiado.
        '''
        #Comprobaciones.
        self.__checkDistancia(Distancia)
        self.__checkLecturaHorizontal(LecturaHorizontal)
        #Claculo de la raidiación.
        desmean=0
        angaux=ang.Angulo()
        angaux.setGirar(True)
        angaux.setNegativos(False)
        
        if self.__referencias!=[] and self.__lecturasRef!=[]:
            #Cálculo azimuts referencia.
            azRef=[]
            azimuts=azi.Azimut()
            azimuts.setPuntoInicial(self.__pEst)
            for i in self.__referencias:
                azimuts.setPuntoFinal(i)
                azRef.append(azimuts.getAzimut())
            #print(azRef)
            #Cálculo desorientaciones.
            des=[]
            for i,j in zip(azRef,self.__lecturasRef):
                j.Convertir('radian')
                deso=i-j.getAngulo()
                angaux.setAngulo(deso)
                angaux.setFormato('radian')
                des.append(angaux.getAngulo())
            #print(des)
            desmean=mean(des)
            #print(mean(des),std(des))
        #Cálculo de la radiación
        if self.__checkLecDis(Distancia, LecturaHorizontal)==True:
            Sal=[]
            #Radiación por bucle.
            for i,j in zip(Distancia,LecturaHorizontal):
                j.Convertir('radian')
                az=j.getAngulo()+desmean
                angaux.setAngulo(az)
                angaux.setFormato('radian')
                xs=self.__pEst.getX()+(i*sin(angaux.getAngulo()))
                ys=self.__pEst.getY()+(i*cos(angaux.getAngulo()))
                Sal.append(pt2.Punto2D(xs,ys))
            return Sal
        else:
            #Radiación simle
            LecturaHorizontal.Convertir('radian')
            az=LecturaHorizontal.getAngulo()+desmean
            angaux.setAngulo(az)
            angaux.setFormato('radian')
            
            xs=self.__pEst.getX()+(Distancia*sin(angaux.getAngulo()))
            ys=self.__pEst.getY()+(Distancia*cos(angaux.getAngulo()))
            return pt2.Punto2D(xs,ys)
    
    
    def Radiacion2DFromFile(self,fEstaciones,fReferencias,fLecturasReferencias,fLecturas):
        '''!
        \param fEstaciones Fichero con las coordenadas de las estaciones desde las que se quiere radiar.
        \note fEstaciones Fomato: id_Estacion,X,Y,Z
        
        \param fReferencias Fichero con las coordenadas con los puntos usados como referencias.
        \note fReferencias Formato: id_Referencia,X,Y,Z
        
        \param fLecturasReferencias Fichero con las lecturas realizadas a las referencias.
        \note fLecturasReferencias Formato: id_Estacion,id_Referencia,LH,LV
        
        \param fLecturas Fichero con las lecturas de los puntos radiados.
        \param fLecturas Formato: id_Estacion,id_Punto,LH,LV,Distancia
        '''
        #TO-DO:
        
        
        
def main():
    pest=pt2.Punto2D(0,0)
    pref=[pt2.Punto2D(10,0),pt2.Punto2D(0,10),pt2.Punto2D(-10,-10),pt2.Punto2D(10,10)]
    lecs=[ang.Angulo(0,formato='centesimal'),ang.Angulo(301,formato='centesimal'),ang.Angulo(149,formato='centesimal'),ang.Angulo(351,formato='centesimal')]
    rad2d=Radiacion2D(pest,pref,lecs)
#     rad2d=Radiacion2D(pest)
    dis=[100,200,300]
    angs=[ang.Angulo(150,formato='centesimal'),ang.Angulo(250,formato='centesimal'),ang.Angulo(350,formato='centesimal')]
    sal=rad2d.Radiacion2D(dis, angs)
    for i in sal:
        print(i.getX(),i.getY())
        
    rad2d=Radiacion2D(pest)
    sal=rad2d.Radiacion2D(100, ang.Angulo(100,formato='centesimal'))
    print(sal.getX(),sal.getY())
        
        
        
        
if __name__=="__main__":
    main()
