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
from Geometrias.Angulo import Angulo

class PuntoGeodesico(object):
    '''!
    classdocs
    '''
    __lat=None
    __lon=None
    __h=None


    def __init__(self, *args):
        '''!
        Constructor de la clase PuntoGeodesico.
        '''
        if len(args)==0:
            pass
        elif len(args)==2:
            self.setLatitud(args[0])
            self.setLongitud(args[1])
        elif len(args)==3:
            self.setLatitud(args[0])
            self.setLongitud(args[1])
            self.setAlturaElipsoidal(args[2])
        
    def setLatitud(self,Latitud):
        '''!
        '''
        if isinstance(Latitud,Angulo):
            if Latitud.getFormato()=="latitud":
                self.__lat=Latitud
            else:
                raise Exception("El formato del ángulo introducido no es de tipo latitud")
        elif isinstance(Latitud,float) or isinstance(Latitud,int) or isinstance(Latitud,str):
            try:
                aux=float(Latitud)
                Angulo(aux,formato="latitud")
            except Exception as e:
                raise Exception(e)
            finally:
                self.__lat=Angulo(aux,formato="latitud")
                
    def setLongitud(self,Longitud):
        '''!
        '''
        if isinstance(Longitud,Angulo):
            if Longitud.getFormato()=="longitud180" or Longitud.getFormato()=="longitud360":
                self.__lon=Longitud
            else:
                raise Exception("El formato del ángulo introducido no es de tipo longitud180 o longitud360")
            
        elif isinstance(Longitud,float) or isinstance(Longitud,int) or isinstance(Longitud,str):
            try:
                aux=float(Longitud)
            except Exception as e:
                raise Exception(e)
            
            if aux>-180 and aux<=180:
                self.__lon=Angulo(aux,formato="longitud180")
            elif aux >0 and aux<360:
                self.__lon=Angulo(aux,formato="longitud360")
            else:
                raise Exception("La longitud no se puede asociar a ningun tipo conocido.")
            
    def setAlturaElipsoidal(self,AlturaElipsoidal):
        '''!
        '''
        if isinstance(AlturaElipsoidal,float) or isinstance(AlturaElipsoidal,int) or isinstance(AlturaElipsoidal,str):
            try:
                aux=float(AlturaElipsoidal)
            except Exception as e:
                raise Exception(e)
            finally:
                self.__h=aux
                
            
    def getLatitud(self):
        '''!
        '''
        return self.__lat.getAngulo()
    
    def getLongitud(self):
        '''!
        '''
        return self.__lon.getAngulo()
    
    def getAlturaElipsoidal(self):
        '''!
        '''
        return self.__h
    
    
                
                
def main():
    p=PuntoGeodesico(10,180,50)
    p.getLongitud()
    print(p.getAlturaElipsoidal())
        
                
if __name__=="__main__":
    main()
        