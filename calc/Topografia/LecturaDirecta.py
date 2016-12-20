#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 4/5/2015

@author: Antonio Hermosilla Rodrigo.
@contact: anherro285@gmail.com
@organization: Antonio Hermosilla Rodrigo.
@copyright: (C) 2011 by Antonio Hermosilla Rodrigo
@version: 1.0.0
'''
import Geometrias.Angulo as ang
from math import sqrt


#Hacerlo para incluir listas donde todas la lecturas se supondran que son a un mismo punto.
class LecturaDirecta(object):
    '''
    classdocs
    '''
    __LCD=None
    __LCI=None
    __LD=None
    __Err=None


    def __init__(self, LCD,LCI):
        '''
        Constructor de la clase LecturaDirecta.
        \brief La clase recibe la lectura directa e inversa de una medición topografica y devulvela lectura directa.
        '''
        self.setLecturaCD(LCD)
        self.setLecturaCI(LCI)
        
    def setLecturaCD(self,LCD):
        '''!
        \brief Establece la lectura del circulo directo.
        \param LCD Angulo: Lectura en el circulo directo, el ángulo debe ser centesimal.
        '''
        if isinstance(LCD, ang.Angulo):
            if LCD.getFormato()=='centesimal':
                self.__LCD=LCD
            else:
                raise Exception("Se esperaba un ángulo de tipo centesimal.")
        else:
            raise Exception("Se esperaba un objeto de la clase Angulo.")
        
    def setLecturaCI(self,LCI):
        '''!
        \brief Establece la lectura del circulo inverso.
        \param LCI Angulo: Lectura en el circulo inverso, el ángulo debe ser centesimal.
        '''
        if isinstance(LCI, ang.Angulo):
            if LCI.getFormato()=='centesimal':
                self.__LCI=LCI
            else:
                raise Exception("Se esperaba un ángulo de tipo centesimal.")
        else:
            raise Exception("Se esperaba un objeto de la clase Angulo.")
        
    def getLecturaDirecta(self,lectura='azimutal'):
        '''!
        \param angulo str: ángulo sobre el que se quiere calcular la lectura directa. azimutal o cenital.
        '''
        try:
            lectura=str(lectura)
            lectura=lectura.lower()
        except Exception as e:
            raise Exception(e)
        if lectura not in ['azimutal','cenital']:
            raise Exception("El tipo de lectura debe ser azimutal o centesimal")
        
        
        if self.__LCD==None:
            raise Exception("El circulo directo debe contener algun valor.")
        if self.__LCI==None:
            raise Exception("El circulo inverso debe contener algun valor.")
        
        cd=self.__LCD.getAngulo()
        ci=self.__LCI.getAngulo()
        
        angulo=None
        if lectura=='azimutal':
            if cd>ci:
                angulo=(cd+ci+200)/2
            elif ci>cd:
                angulo=(cd+(ci-200))/2
            
        if lectura=='cenital':
                angulo=(cd+(400-ci))/2
                
        sal=ang.Angulo(angulo,formato='centesimal')
        return sal
    
    def getErrorLectura(self,lectura='azimutal',numeroObservaciones=1):
        '''!
        \param angulo str: ángulo sobre el que se quiere calcular la lectura directa. azimutal o cenital.
        '''
        try:
            lectura=str(lectura)
            lectura=lectura.lower()
        except Exception as e:
            raise Exception(e)
        if lectura not in ['azimutal','cenital']:
            raise Exception("El tipo de lectura debe ser azimutal o centesimal")
        
        
        if self.__LCD==None:
            raise Exception("El circulo directo debe contener algun valor.")
        if self.__LCI==None:
            raise Exception("El circulo inverso debe contener algun valor.")
        
        cd=self.__LCD.getAngulo()
        ci=self.__LCI.getAngulo()
        err=0
        if lectura=='azimutal':
            if cd>ci:
                err=(cd-(ci+200))/(sqrt(2*numeroObservaciones))
            elif ci>cd:
                err=(cd-(ci-200))/(sqrt(2*numeroObservaciones))
                
        if lectura=='cenital':
                err=(cd-(400-ci))/(sqrt(2*numeroObservaciones))
                 
        return err
        
        
        
def main():
    '''!
    '''
    LDirecta=LecturaDirecta(ang.Angulo(301.2365,formato='centesimal'),ang.Angulo(101.2341,formato='centesimal'))
    print(LDirecta.getLecturaDirecta(lectura='azimutal').getAngulo())
    print(LDirecta.getErrorLectura(lectura='azimutal',numeroObservaciones=1))
    
    LDirecta=LecturaDirecta(ang.Angulo(301.2365,formato='centesimal'),ang.Angulo(98.7653,formato='centesimal'))
    print(LDirecta.getLecturaDirecta(lectura='cenital').getAngulo())
    print(LDirecta.getErrorLectura(lectura='cenital',numeroObservaciones=1))
    
if __name__=='__main__':
    main()