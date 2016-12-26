#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 14/3/2015

@author: Antonio Hermosilla Rodrigo.
@contact: anherro285@gmail.com
@organization: Antonio Hermosilla Rodrigo.
@copyright: (C) 2015 by Antonio Hermosilla Rodrigo
@version: 1.0.0
'''
from Geometrias.Punto2D import Punto2D
import Geometrias.Linea2D as l2d
import Intersecciones.Interseccion2D as inter2d
from json import loads

class PoliLinea2D(object):
    '''
    classdocs
    '''
    __ptos=[]
    __lins=[]


    def __init__(self,*args):
        '''
        Constructor
        '''
        if len(args)==0:
            pass
        
        
        
    def setPoliLineaFromPuntos(self,Puntos):
        '''!
        '''
        self.__ptos=[]
        self.__lins=[]
        if isinstance(Puntos, list):
            for i in Puntos:
                if not isinstance(i, Punto2D):
                    raise Exception("Uno de los elementos de la lista no es un objeto de la clase Punto2D.")
                else:
                    self.__ptos.append(i)
            for indi,i in enumerate(Puntos):
                if indi==len(Puntos)-1:
                    break
                else:
                    pt1=i
                    pt2=Puntos[indi+1]
                    l=l2d.Linea2D(pt1,pt2)
                    self.__lins.append(l)      
        else:
            raise Exception("Se esperaba una lista como argumento de entrada del método.")
        self.__checkPoli()
        
    
    
    def setPoliLineaFromLineas(self,Lineas):
        '''!
        '''
        self.__ptos=[]
        self.__lins=[]
        if isinstance(Lineas, list):
            for indi1,i in enumerate(Lineas):
                if not isinstance(i, l2d.Linea2D):
                    raise Exception("Uno de los elementos de la lista no es un objeto de la clase Linea2D.")
                else:
                    self.__lins.append(i)
                    if indi1==len(Lineas)-1:
                        self.__ptos.append(i.getPuntoInicial())
                        self.__ptos.append(i.getPuntoFinal())
                    else:
                        self.__ptos.append(i.getPuntoInicial())
                           
        else:
            raise Exception("Se esperaba una lista como argumento de entrada del método.")
        self.__checkPoli()
        
    def setWKT(self,wkt):
        '''!
        '''
        self.__ptos=[]
        coor=wkt.split('LINESTRING')[1]
        coor=coor.replace('(','')
        coor=coor.replace(')','')
        coor=coor.split(',')
        Puntos=[]
        for i in coor:
            i=i.rstrip()
            i=i.split()
            Puntos.append(Punto2D(i[0],i[1]))
        self.setPoliLineaFromPuntos(Puntos)
        
        
        
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
            puntos=[]
            for i in coor:
                puntos.append(Punto2D(i[0],i[1]))
            self.setPoliLineaFromPuntos(puntos)
                
        
                
    def __checkPoli(self):
        '''
        '''
        for indi,i in enumerate(self.__lins):
            if indi==len(self.__lins)-1:
                break
            else:
                l1=i
                l2=self.__lins[indi+1]
                p1=l1.getPuntoFinal()
                p2=l2.getPuntoInicial()
                if p1.getX()==p2.getX() and p1.getY()==p2.getY():
                    pass
                else:
                    raise Exception("La polilinea no es continua.")
                
    def isClose(self):
        '''
        '''
        l1=self.__lins[-1]
        l2=self.__lins[0]
        p1=l1.getPuntoFinal()
        p2=l2.getPuntoInicial()
        if p1.getX()==p2.getX() and p1.getY()==p2.getY():
            return True
        else:
            return False
        
    def selfIntersect(self):
        '''
        '''
        selfInter=[]
        for indi1,i in enumerate(self.__lins):
            for indi2,j in enumerate(self.__lins):
                if indi1==indi2 or indi1>indi2:
                    continue
                elif indi1+1==indi2:
                    continue
                elif indi1-1==indi2:
                    continue
                elif self.isClose()==True and indi1==len(self.__lins)-1 and indi2==0:
                    continue
                elif self.isClose()==True and indi2==len(self.__lins)-1 and indi1==0:
                    continue
                else:
                    inter=inter2d.Interseccion2D(i,j)
                    sal=inter.Intersectar(tipo='real')
                    if sal==None:
                        continue
                    else:
                        selfInter.append([indi1,indi2,sal.getX(),sal.getY()])
                        #print(indi1,indi2,sal.getX(),sal.getY())
        return selfInter
    
    def getPuntos(self):
        '''
        @brief: Método que devuelve los puntos de la polilinea.
        @return []:Puntos de la polilinea.
        '''
        return self.__ptos
    
    def getLineas(self):
        '''!
        '''
        return self.__lins
    
    def getLongitudParcial(self):
        import Topografia.Distancia2D as d2
        Sal=[]
        for indi1,i in enumerate(self.__lins):
            Distancia=d2.Distancia2D(i)
            dis=Distancia.getDistancia2D()
            Sal.append([indi1,dis])
        return Sal
        
    
    def getLongitud(self):
        '''!
        @brief: Devulve la longitud total de la polilinea.
        '''
        import Topografia.Distancia2D as d2
        dis=0
        for i in self.__lins:
            Distancia=d2.Distancia2D(i)
            dis+=Distancia.getDistancia2D()
        return dis
    
    
    def toGeoJSON(self):
        '''!
        @brief: Método que devuleve un GeoJSON del punto.
        @return str: Un string en formato JSON.
        '''
        #Esta mal esto es un conjunto de polilineas.
#         vals=""
#         for indi1,i in enumerate(self.__lins):
#             vals+="[ ["
#             x1=i.getPuntoInicial().getX()
#             y1=i.getPuntoInicial().getY()
#             vals+=str(x1)
#             vals+=", "
#             vals+=str(y1)
#             vals+="], ["
#             x2=i.getPuntoFinal().getX()
#             y2=i.getPuntoFinal().getY()
#             vals+=str(x2)
#             vals+=", "
#             vals+=str(y2)
#             vals+="]"
#             if indi1==len(self.__lins)-1:
#                 vals+=" ]\n"
#             else:
#                 vals+=" ],\n"
        vals=''
        for indi1,i in enumerate(self.__ptos):
            if indi1==len(self.__ptos)-1:
                vals+='['+str(i.getX())+','+str(i.getY())+']'
                break
            vals+='['+str(i.getX())+','+str(i.getY())+'],'
        
 
        return "{\n"+\
            '"type":"MultiLineString"'+",\n"\
            '"coordinates": [\n'+\
            vals+\
            ']\n'+\
            "}"
            
    def toWKT(self):
        '''!
        '''
        #Que hacer  si la línea es cerrada...
        vals="LINESTRING ("
        for indi1,i in enumerate(self.__lins):
            pto=i.getPuntoInicial()
            vals+=str(pto.getX())+' '+str(pto.getY())+', '
            if indi1==len(self.__lins)-1:
                pto=i.getPuntoFinal()
                vals+=str(pto.getX())+' '+str(pto.getY())+')'
                pass
        return vals
        
        
        
        
def main():
    pl=PoliLinea2D()
    pl.setPoliLineaFromLineas([l2d.Linea2D(Punto2D(0.0,0.0),Punto2D(10,0)),
                               l2d.Linea2D(Punto2D(10.0,0),Punto2D(-10,10)),
                               l2d.Linea2D(Punto2D(-10,10.0),Punto2D(10,10)),
                               l2d.Linea2D(Punto2D(10.0,10.0),Punto2D(-10,0)),
                               l2d.Linea2D(Punto2D(-10.0,0),Punto2D(0,0))])
    print(pl.isClose())
    print(pl.selfIntersect())
    print(pl.getLongitud())
    print(pl.getLongitudParcial())
    print(pl.toGeoJSON())
    print(pl.toWKT())
    pl.setWKT('LINESTRING (30 10, 10 30, 40 40)')
    print(pl.toWKT())
    pl.setFromGeoJSON('{"type":"LineString","coordinates": [[0.0,0.0],[10.0,0.0],[-10.0,10.0],[10.0,10.0],[-10.0,0.0],[0.0,0.0]]}')
    print(pl.toWKT())
    

if __name__=='__main__':
    main()