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
    Clase destinada a lamacenar la información de un punto geodésico.
    Ejemplos de declaración del un objeto de la clase:\n
    p=PuntoGeodesico(40,-1)
    p=PuntoGeodesico(40,-1,10)
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
        else:
            raise Exception("La clase PuntoGeodesico recibe 2 o 3 parametros como argumentos.\nSe han introducido: "+str(len(args))+" parametros.")
         
        
    def setLatitud(self,Latitud):
        '''!
        @brief: Método para introducir la latitud del punto geodésico.
        @param Latitud Angulo|float|int|str: Valor de la latitud.
        @note Latitud: Si se introduce la latitud como un objeto de la clase Angulo, asegurarse de que el ángulo es de formato latitud.
        @exception: Se producira una excepcion si el valor introducido no es de la clase de Angulo, o el valor introducido no es un número convertible a la clase Angulo.
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
        @brief: Método para introducir la longitud del punto geodésico.
        @param Longitud Angulo|float|int|str: Valor de la longitud.
        @note Longitud: Si se introduce la longitud como un objeto de la clase Angulo, asegurarse de que el ángulo es de formato longitud180 o longitud360.
        @exception: Se producira una excepcion si el valor introducido no es de la clase de Angulo, o el valor introducido no es un número convertible a la clase Angulo.
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
        @brief: Método para introducir la altura elipsoidal del punto geodésico.
        @param AlturaElipsoidal float|int|str: Valor de la altura elipsoidal.
        @exception: Se producira una excepción si no se puede convertir el valor introdicidoa un número.
        '''
        if AlturaElipsoidal==None:
            return
        if isinstance(AlturaElipsoidal,float) or isinstance(AlturaElipsoidal,int) or isinstance(AlturaElipsoidal,str):
            try:
                aux=float(AlturaElipsoidal)
            except Exception as e:
                raise Exception(e)
            finally:
                self.__h=aux
                
            
    def getLatitud(self):
        '''!
        @brief: Método que devuleve la Latitud del punto.
        @return float: Latitud del punto.
        '''
        return self.__lat.getAngulo()
    
    def getLongitud(self):
        '''!
        @brief: Método que devuleve la Longitud del punto.
        @return float: Longitud del punto.
        '''
        return self.__lon.getAngulo()
    
    def getAlturaElipsoidal(self):
        '''!
        @brief: Método que devuleve la altura elipsoidal del punto.
        @return float: Altura elipsoidal del punto.
        '''
        return self.__h
    
    def toString(self):
        '''!
        @brief: Método que devuleve toda la información del punto en formato str.
        @return str: Un string con toda la información del punto.
        '''
        
        return "Latitud:"+str(self.getLatitud())+"\n"\
            "Longitud:"+str(self.getLongitud())+"\n"\
            "Altura Elipsoidal:"+str(self.getAlturaElipsoidal())+"\n"\
    
    def toJSON(self):
        '''!
        @brief: Método que devuleve toda la información del punto en formato JSON.
        @return str: Un string en formato JSON.
        '''
        
        return "{\n"+\
            '"latitud":'+'"'+str(self.getLatitud())+'"'+",\n"\
            '"longitud":'+'"'+str(self.getLongitud())+'"'+",\n"\
            '"altura elispoidal":'+'"'+str(self.getAlturaElipsoidal())+'"'+"\n"\
            +"}"
    
    
    def toGeoJSON(self):
        '''!
        @brief: Método que devuleve un GeoJSON del punto.
        @return str: Un string en formato JSON.
        '''
        
        return "{\n"+\
               '"type":"Point"'+",\n"\
               '"coordinates":'+\
               '['+str(self.getLongitud())+','+str(self.getLatitud())+']'+"\n"\
               "}"
    
    
                
                
def main():
    p=PuntoGeodesico('10','180',50)
    print(p.toString())
    print(p.toJSON())
    print(p.toGeoJSON())
    import json
    print(json.loads(p.toGeoJSON())['coordinates'])
        
                
if __name__=="__main__":
    main()
        