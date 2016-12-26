#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''!
Created on 1/2/2015

@author: Antonio Hermosilla Rodrigo.
@contact: anherro285@gmail.com
@organization: Antonio Hermosilla Rodrigo.
@copyright: (C) 2015 by Antonio Hermosilla Rodrigo
@version: 1.0.0
'''
import sys
sys.path.append('..')
from Geometrias.Punto2D import Punto2D
from Geometrias.PuntoUTM import PuntoUTM
from json import loads

class Linea2D(object):
    '''!
    Clase destinada a almacenar la información de una línea bidimensional.
    Ejemplos de declaración del un objeto de la clase:\n
    l=Linea2D()-->Constructor vacío.\n
    l=Linea2D(Punto2D(10,10),Punto2D(20,20))
    '''
    __pini=None
    __pfin=None


    def __init__(self, *args):
        '''!
        Constructor de la clase Linea2D.
        @param args1 Punto2D: Punto inicial de la linea.
        @param args2 Punto2D: Punto final de la línea.
        @exception: Se producira una excepción si se introducen más o menos argumentos de los admitidos por la clase.
        '''
        if len(args)==0:
            pass
        elif len(args)==2:
            self.setPuntoInicial(args[0])
            self.setPuntoFinal(args[1])
            self.__checkLinea()
        else:
            raise Exception("La clase Linea2D recibe 2 parametros como argumentos.\nSe han introducido: "+str(len(args))+" parametros.")
        
        
        
    def setFromWKT(self,wkt):
        '''!
        '''
        try:
            coor = wkt.split('LINESTRING')[1]
        except Exception as e:
            raise Exception(e)
        coor = coor.replace('(', '')
        coor = coor.replace(')', '')
        coor=coor.split(',')
        if len(coor)>2:
            raise Exception("La linea contiene más de dos puntos.")
        vals=coor[0].rstrip().split()
        self.setPuntoInicial(Punto2D(vals[0],vals[1]))
        vals=coor[1].rstrip().split()
        self.setPuntoFinal(Punto2D(vals[0],vals[1]))
        
    def setFromGeoJSON(self,geojson):
        '''!
        '''
        try:
            coors=loads(geojson)
        except Exception as e:
            raise Exception(e)
        
        if coors['type'] != 'LineString':
            raise Exception("El GeoJSON introducido no corresponde con una línea")
        else:
            coor = coors['coordinates']
        if len(coors)>2:
            raise Exception("")
        else:
            self.setPuntoInicial(Punto2D(coor[0][0],coor[0][1]))
            self.setPuntoFinal(Punto2D(coor[1][0],coor[1][1])) 
        
    def setPuntoInicial(self,PuntoInicial):
        '''!
        @brief: Método para introducir o modificar el punto inicial de la linea.
        @param PuntoInicial Punto2D: Punto inicial de la línea.
        @exception: Se producira una excepción si no se introduce un objeto de la clase Punto2D como valor de entrada del método.
        '''
        if isinstance(PuntoInicial, Punto2D) or isinstance(PuntoInicial, PuntoUTM):
            self.__pini=PuntoInicial
        else:
            raise Exception("Se esperaba un objeto de la clase Punto2D.")
        if self.__pini!=None and self.__pfin!=None:
            self.__checkLinea()
        
    def setPuntoFinal(self,PuntoFinal):
        '''!
        @brief: Método para introducir o modificar el punto final de la linea.
        @param PuntoFinal Punto2D: Punto final de la línea.
        @exception: Se producira una excepción si no se introduce un objeto de la clase Punto2D como valor de entrada del método.
        '''
        if isinstance(PuntoFinal, Punto2D) or isinstance(PuntoFinal, PuntoUTM):
            self.__pfin=PuntoFinal
        else:
            raise Exception("Se esperaba un objeto de la clase Punto2D.")
        if self.__pini!=None and self.__pfin!=None:
            self.__checkLinea()
        
    def __checkLinea(self):
        '''!
        @brief: Método para comprobar que el punto inicial y final de la línea son distintos.
        '''
        x1=self.__pini.getX()
        y1=self.__pini.getY()
        x2=self.__pfin.getX()
        y2=self.__pfin.getY()
        
        if x1==x2 and y1==y2:
            raise Exception("El punto inicial y final de la linea deben de ser distintos.")
        
    def getPuntoInicial(self):
        '''!
        @brief: Método que devuelve el Puno inicial de la línea.
        @return Punto2D: Punto inicial. 
        '''
        return self.__pini
    
    def getPuntoFinal(self):
        '''!
        @brief: Método que devuelve el Puno final de la línea.
        @return Punto2D: Punto final. 
        '''
        return self.__pfin
    
    def getAX(self):
        '''!
        @brief: Método que devuelve el incremento de coordenadas en el eje X de la línea.
        @return float: Incremento X. 
        '''
        x1=self.__pini.getX()
        x2=self.__pfin.getX()
        return x2-x1
    
    def getAY(self):
        '''!
        @brief: Método que devuelve el incremento de coordenadas en el eje Y de la línea.
        @return float: Incremento Y. 
        '''
        y1=self.__pini.getY()
        y2=self.__pfin.getY()
        return y2-y1
    
    def getDisnatcia(self):
        '''!
        @brief: Método que devuelve la distancia de la línea.
        @return float: Distancia. 
        '''
        import Topografia.Distancia2D
        d=Topografia.Distancia2D.Distancia2D(self.__pini,self.__pfin)
        return d.getDistancia2D()
    
    def getAzimut(self):
        '''!
        @brief: Devuleve el aximut de la linea.
        @return float: Azimut.
        '''
        import Topografia.Azimut
        az=Topografia.Azimut.Azimut(self.__pini,self.__pfin)
        return az.getAzimut()
    
    def PointIn(self,Punto2D,tolerance=0):
        #Añadir tolerancia.
        '''!
        @brief: El método comprueba si un punto se encuentra sobre la línea. The method check if point is in line.
        '''
        v1=self.getAX()
        v2=self.getAY()
        if v1==0:
            #Incremento de X es 0. Línea vertical.
            vals=[self.__pini.getY(),self.__pfin.getY()]
            vals.sort()
            vals[0]=vals[0]-tolerance
            vals[1]=vals[1]+tolerance
            if Punto2D.getY()>=vals[0] and Punto2D.getY()<=vals[1]:
                return True
            else:
                return False
        if v2==0:
            #Incremento de Y es 0. Línea horizontal.
            vals=[self.__pini.getX(),self.__pfin.getX()]
            vals.sort()
            vals[0]=vals[0]-tolerance
            vals[1]=vals[1]+tolerance
            if Punto2D.getX()>=vals[0] and Punto2D.getX()<=vals[1]:
                return True
            else:
                return False
        val=self.__pini.getY()-((self.__pini.getX()*v2)/v1)+(v2/v1)*Punto2D.getX()
        print(val,tolerance,Punto2D.getY())
        if Punto2D.getY()+tolerance<=val and Punto2D.getY()-tolerance>=val:
            return True
        else:
            return False
        
    
    def toString(self):
        '''!
        @brief: Método que devuleve toda la información del punto en formato str.
        @return str: Un string con toda la información de la linea.
        '''
        return "Punto Inicial: X: "+str(self.__pini.getX())+" Y: "+str(self.__pini.getY())+"\n"\
            "Punto Final: X: "+str(self.__pfin.getX())+" Y: "+str(self.__pfin.getY())+"\n"\
            "AX: "+str(self.getAX())+"\n"\
            "AY: " +str(self.getAX())+"\n"\
            "Dintancia: "+str(self.getDisnatcia())+"\n"\
            "Azimut: "+str(self.getAzimut())
            
    def toJSON(self):
        '''!
        @brief: Método que devuleve toda la información del punto en formato JSON.
        @return str: Un string en formato JSON.
        '''
        return "{\n"+\
            '"Punto inicial":'+"\n" +self.__pini.toJSON()+","+"\n"\
            '"Punto final":'+"\n" +self.__pfin.toJSON()+","+"\n"\
            '"AX":'+'"'+str(self.getAX())+'"'+",\n"\
            '"AY":'+'"'+str(self.getAY())+'"'+",\n"\
            '"Distancia":'+'"'+str(self.getDisnatcia())+'"'+",\n"\
            '"Azimut":'+'"'+str(self.getAzimut())+'"'+"\n"\
            +"}"
            
            
    def toGeoJSON(self):
        '''!
        @brief: Método que devuleve un GeoJSON del punto.
        @return str: Un string en formato JSON.
        '''
        
        return "{\n"+\
            '"type":"LineString"'+",\n"\
            '"coordinates":'+\
            '['+\
            '['+\
            str(self.__pini.getX())+','+str(self.__pini.getY())+'],'+\
            '['+\
            str(self.__pfin.getX())+','+str(self.__pfin.getY())+']]'+"\n"\
            "}"
            
    def toWKT(self):
        '''!
        '''
        return 'LINESTRING ('+\
            str(self.__pini.getX())+' '+str(self.__pini.getY())+', '+\
            str(self.__pfin.getX())+' '+str(self.__pfin.getY())+')'
            
def main():
    l=Linea2D(Punto2D(10,10),Punto2D(20,30))
    print(l.toString())
    print(l.toJSON())

    print(loads(l.toJSON())['Punto inicial']['X'])
    print(l.toGeoJSON())
    print(loads(l.toGeoJSON())['coordinates'])
    print(l.toWKT())
    l.setFromWKT('LINESTRING (100.0 10.0, 20.0 30.0)')
    print(l.toWKT())
    l.setFromGeoJSON('{"type":"LineString","coordinates":[[10.0,10.0],[20.0,30.0]]}')
    print(l.toWKT()) 
        
if __name__=="__main__":
    main()
        