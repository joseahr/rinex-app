#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''!
Created on 29/1/2015

@author: Antonio Hermosilla Rodrigo.
@contact: anherro285@gmail.com
@organization: Antonio Hermosilla Rodrigo.
@copyright: (C) 2015 by Antonio Hermosilla Rodrigo
@version: 1.0.0
'''
from Geometrias.Punto2D import Punto2D

class Punto3D(Punto2D):
    '''!
    Clase destinada al almacenamiento de la información espacial de un punto tridimensional.
    Ejemplos de declaración del un objeto de la clase:\n
    p=Punto3D()-->Constructor vacío.\n
    p=Punto3D(10,20,30)\n
    p=Punto3D(10,20,30,negativos=True)\n
    p=Punto3D(10,20,30,negativos=False)\n
    p=Punto3D(Punto2D(10,20),30)\n
    p=Punto3D(Punto2D(10,20),30,negativos=True)-->negativos sobreescribe a negativos de la clase Punto2D.\n
    p=Punto3D(Punto2D(10,20),30,negativos=False)-->negativos sobreescribe a negativos de la clase Punto2D.\n
    p=Punto3D(Punto2D(10,20,negativos=False),30,negativos=True)-->negativos sobreescribe a negativos de la clase Punto2D.\n
    '''
    __Z=None


    def __init__(self, *args,**kwargs):
        '''!
        Constructor de la clase Punto2D.
        *args: La clase admite en el constructor dos o tres argumentos.\n
        Dos argumentos:\n
        args1: Punto Punto2D: Punto2D con el valor de las coordenadas X e Y.
        args2: Z float|int|str: Valor de la coordenada Z.\n
        Tres argumentos:\n
        args1 X float: Valor de la coordenada X.\n
        args2 Y float: Valor de la coordenada Y.\n
        args3 Z float: Valor de la coordenada Z.\n
        Parametros de tipo kwargs(para todos los constructores):\n
        kwargs negativos bool: Estado de la propiedad negativos.
        @exception: Se producira una excepción si se introducen más o menos argumentos de los admitidos por la clase.
        @exception: Se producira una excepción si no se reconoce el kwarg introducido.
        '''
        Negativos=None
        if len(kwargs)>0:
            for key in kwargs:
                if key.lower()=='negativos':
                    aux=kwargs[key]
                    self.setNegativos(aux)
                else:
                    raise Exception("El argumento: "+key+" no se reconoce")
        
        
        
        if len(args)==2:    #Punto2D,Z
            if isinstance(args[0], Punto2D):
                CoordenadaX = args[0].getX()
                CoordenadaY = args[0].getY()
                CoordenadaZ = args[1]
                if Negativos==None:
                    Negativos = args[0].getNegativos()
                    self.setNegativos(Negativos)
                # Inicializar la clase padre.
                Punto2D.__init__(self, CoordenadaX, CoordenadaY, negativos=Negativos)
                self.setZ(CoordenadaZ)
            else:
                raise Exception("Se esperaba un objeto de la clase Punto2D como primer argumento del constructor")
        elif len(args)==3:
            CoordenadaX = args[0]
            CoordenadaY = args[1]
            CoordenadaZ = args[2]
            if Negativos==None:
                Negativos = True  # Valor por defecto.
                self.setNegativos(Negativos)
            # Inicializar la clase padre.
            Punto2D.__init__(self, CoordenadaX, CoordenadaY, negativos=Negativos)
            self.setZ(CoordenadaZ)
        elif len(args)==0:
            Punto2D.__init__(self)
            #Constructor vacio.
            pass

        else:
            raise Exception("La clase Punto3D recibe 2 o 3 parametros como argumentos.\nSe han introducido: "+str(len(args))+" parametros.")
        
    
    def setZ(self,Z):
        '''!
        @brief: Método para introducir el valor de la coordenada Z de un punto.
        @param Z float: Valor de la coordenada
        '''
        if isinstance(Z, str) or isinstance(Z, int) or isinstance(Z, float):
            try:
                self.__Z=float(Z)
            except Exception as e:
                raise Exception(e)
        else:
            raise ValueError()
        
        if self.getNegativos()==False and self.__Z<0:
            raise Exception("La coordenada Z no puede ser negativa.\nNegativos="+str(self.getNegativos()))
        
    def getZ(self):
        '''!
        @brief: Método que devuelve el valor de la coordenada Z.
        @return float: Valor de la coordenada Z.
        '''
        return self.__Z
    
    def toPunto2D(self):
        '''!
        @brief: Método que devuelve un objeto de la clase Punto2D, equivalente al Punto3D de la clase.
        @return Punto2D: Punto2D equivalente
        '''
        return Punto2D(self.getX(),self.getY(),negativos=self.getNegativos())
    
    def getNegativos(self):
        '''!
        @brief: Método que devuelve el valor actual de la propiedad negativos.
        @return bool: Estado de la propiedad Negativos.
        '''
        return Punto2D.getNegativos(self)
    
    def setNegativos(self, Negativos):
        '''!
        @brief: Método para introducir la propiedad Negativos.
        @param Neagativos bool|str|int: Estado de la propiedad Negativos.
        @note Neagativos True: Permite alojar números negativos.
        @note Neagativos False: No permite alojar números negativos.
        @exception: Se producira una excepción si el valor introducido no se puede convertir a bool.
        @exception: Se producira una excepcion si se cambia la propiedad negativos a Flase y existen coordenadas negativas en la clase.
        '''
        Punto2D.setNegativos(self, Negativos)
        if self.getNegativos()==False:
            if self.__Z!=None and self.__Z<0:
                raise Exception("La coordenada Z de la clase es negativa.")
            
            
    def toString(self):
        '''!
        @brief: Método que devuleve toda la información del punto en formato str.
        @return str: Un string con toda la información del punto.
        '''
        val=Punto2D.toString(self).split('\n')
        val.insert(2,"Z:"+str(self.__Z))
        return '\n'.join(val)
    
    def toJSON(self):
        '''!
        @brief: Método que devuleve toda la información del punto en formato JSON.
        @return str: Un string en formato JSON.
        '''
        val=Punto2D.toJSON(self).split('\n')
        val.insert(3,'"Z":'+'"'+str(self.__Z)+'"'+",")
        return '\n'.join(val)
    
    def toGeoJSON(self):
        '''!
        '''
        val=Punto2D.toGeoJSON(self).split('\n')
        val[2]='"coordinates":'+'['+str(self.getX())+','+str(self.getY())+','+str(self.__Z)+']'
        return '\n'.join(val)
    
    def toWKT(self):
        '''!
        '''
        return 'POINT Z ('+str(self.getX())+' '+str(self.getY())+' '+str(self.__Z)+')'
    
    
        
        
def main():
    import json
    p1 =Punto3D(10,20,-30,NEGATIVOS=True)
#     print(p1.toString())
#     print(p1.toJSON())
#     print(json.loads(p1.toJSON())['X'])
    print(p1.toGeoJSON())
    print(json.loads(p1.toGeoJSON())['coordinates'])
    print(p1.toWKT())
#     p1.setNegativos(False)

    
if __name__=="__main__":
    main()