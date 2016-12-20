#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 30/3/2015

@author: Antonio Hermosilla Rodrigo.
@contact: anherro285@gmail.com
@organization: Antonio Hermosilla Rodrigo.
@copyright: (C) 2015 by Antonio Hermosilla Rodrigo
@version: 1.0.0
'''
import Geometrias.PoliLinea2D as poli2d



from Geometrias.Punto2D import Punto2D

from numpy import mean
import Geometrias


class Poligono2D(object):
    '''
    classdocs
    '''
    __poli=None #Un poligono puede está formado por una polilínea cerrada.
    __Huecos=[] #Los huecos son polilineas cerradas dentro del poligono.
    __auxlin=poli2d.PoliLinea2D()


    def __init__(self, *args,**kwargs):
        '''
        Constructor de la clase Poligono2D.
        '''
        if len(args)==0:
            pass
        elif len(args)==1:
            self.setFromPolilinea(args[0])
            pass
        else:
            raise Exception("La clase Poligono2D recibe 1 parametros como argumentos.\nSe han introducido: "+str(len(args))+" parametros.")
    
        # Parsear los kwargs.
        if len(kwargs) > 0:
            for key in kwargs:
                if key.lower() == 'huecos':
                    aux = kwargs[key]
                    self.setHuecos(aux)
                else:
                    raise Exception("El argumento: " + key + " no se reconoce")
        
        
    #Como definir un poligono.
    #Polilinea Cerrada.
    def  setFromPolilinea(self,Polilinea):
        '''!
        '''
        if not isinstance(Polilinea, poli2d.PoliLinea2D):
            raise Exception("La Polilinea introducida no es de la clase Polilinea2D.")
        if Polilinea.isClose()==False:
            raise Exception("La Polilinea introducida no es cerrada.")
        self.__poli=Polilinea
        #print(self.toGeoJSON())
            
    def setHuecos(self,Huecos):
        '''!
        '''
        import Topologia.PointInPolygon as PIP
        if self.__poli==None:
            raise Exception("Debe definir un poligono antes de introducir un hueco.")
        
        if isinstance(Huecos, poli2d.PoliLinea2D):
            if Huecos.isClose()==False:
                raise Exception("La polilinea debe de ser cerrada.")
            else:
                topo=PIP.PointInPolygon()
                topo.setPoligono(self.__poli)
                for i in Huecos.getPuntos():
                    #print(i)
                    topo.setPunto(i)
                    if topo.Dentro()==False:
                        print(i.getX(),i.getY())
                        raise Exception("Uno de los elementos del hueco no se encuentra dentro del poligono.")
                self.__Huecos.append(Huecos)
        
        
        
        
        elif isinstance(Huecos, list):
            topo=PIP.PointInPolygon()
            topo.setPoligono(self.__poli)
            for i in Huecos:
                if not isinstance(i, poli2d.PoliLinea2D):
                    raise Exception("Uno de los elementos de la lista no es una instancia a la p¡calse polilinea.")
                if i.isClose()==False:
                    raise Exception("La polilinea debe de ser cerrada.")
                for j in i.getPuntos():
                    topo.setPunto(j)
                    if topo.Dentro()==False:
                        raise Exception("Uno de los elementos del hueco no se encuentra dentro del poligono.")
                self.__Huecos.append(i)
                    
                
            pass
            
        else:
            raise Exception("Se esperaba un polilinea o una lista como valores de entrada.")
        
        
        
#     def setHuecos(self,PoliLinea):
#         '''!
#         '''
#         import Topologia.PointInPolygon as PIP
#         if self.__poli==None:
#             raise Exception("Debe definir un poligono antes de introducir un hueco.")
#         
#         
#         if isinstance(PoliLinea, PoliLinea2D):
#             #Comprobar que todos los puntos que forman la polilinea del Hueco están dentro del poligono.
#             ptos=PoliLinea.getPuntos()
#             topo=PIP.PointInPolygon()
#             print(self.__poli.toWKT())
#             auxpol=Geometrias.Poligono2D.Poligono2D(self.__poli)
#             topo.setPoligono(auxpol)
#             for i in ptos:
#                 topo.setPunto(i)
#                 print(topo.Dentro())
#                 if topo.Dentro()==False:
#                     raise Exception("El hueco introducido no se encuentra dentro del poligono.")
#             self.__Huecos.append(PoliLinea)
#             
#             
#         elif isinstance(PoliLinea,str):
#             polilin=PoliLinea2D()
#             polilin.setWKT(PoliLinea)
#             ptos=polilin.getPuntos()
#             topo=PIP.PointInPolygon()
#             print(self.__poli.toWKT())
#             auxpol=Geometrias.Poligono2D.Poligono2D(self.__poli)
#             topo.setPoligono(auxpol)
#             for i in ptos:
#                 topo.setPunto(i)
#                 print(topo.Dentro())
#                 if topo.Dentro()==False:
#                     raise Exception("El hueco introducido no se encuentra dentro del poligono.")
#             self.__Huecos.append(PoliLinea)
#             
#             
#                 
#         else:
#             raise Exception("Se esperaba  unapolilinea como valor de entrada del método.")
            
            
            
    #WKT.
    def setFromWKT(self,wkt):
        '''!
        '''
        self.__poli=None
        self.__Huecos=[]
        coor=wkt.split('POLYGON')[1]
        coor=coor.split(')')
        for indi1,i in enumerate(coor):
            puntos=[]
            print(i)
            if indi1==0:
                i=i.replace('(','')
                i=i.split(',')
                for j in i:
                    j=j.rstrip()
                    j=j.split()
                    puntos.append(Punto2D(j[0],j[1]))
                pol=poli2d.PoliLinea2D()
                pol.setPoliLineaFromPuntos(puntos)
                self.__poli=pol
            else:
                if i=='':
                    continue
                i=i[1:]
                i+=')'
                i='LINESTRING '+i
                #print(i)
                pol=poli2d.PoliLinea2D()
                pol.setWKT(i)
                self.setHuecos(pol)
    #Geojson.
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    def setPoligono(self,Polilinea):
        '''!
        '''
        self.__poli=None
        self.__Huecos=[]
        if isinstance(Polilinea, poli2d.PoliLinea2D):
            if not Polilinea.isClose()==True:
                raise Exception("La Polilinea que forma el poligono no es cerrada.")
            else:
                self.__poli=Polilinea
                print(self.__poli.toWKT())
        
    def setPoligonoFromLineas(self,Lineas):
        '''!
        '''
        self.__poli=None
        self.__Huecos=[]
        #Podria traducirse en set poligono from lineas
        if isinstance(Lineas, list):
            pl=poli2d.PoliLinea2D()
            pl.setPoliLineaFromLineas(Lineas)
            if not pl.isClose()==True:
                raise Exception("La Polilinea que forma el poligono no es cerrada.")
            else:
                self.__poli=pl
                print(self.__poli.toWKT())
        else:
            raise Exception("Se esperaba un onbjeto de la clase Polilinea2D como parámetro de entrada.")
    
    
        
    
    def setPoligonoFromPuntos(self,Puntos):
        '''!
        '''
        self.__poli=None
        self.__Huecos=[]
        if isinstance(Puntos, list):
            for i in Puntos:
                if not isinstance(i, Punto2D):
                    raise Exception("Un elemento de la lista no es de la clase Putno2D")
            #Comprobar si el primer y el último punto son el mismo.
            if Puntos[0].getX()==Puntos[-1].getX() and Puntos[0].getY()==Puntos[-1].getY():
                pass
            else:
                Puntos.append(Puntos[0])
            #Crear la polilinea que define el poligono.
            self.__auxlin.setPoliLineaFromPuntos(Puntos)
            self.setPoligono(self.__auxlin)
            
        else:
            raise Exception("Se esperaba una lista como argumento de entrada.")
    
#     def setWKT(self,wkt):
#         '''!
#         '''
#         self.__poli=None
#         self.__Huecos=[]
#         coor=wkt.split('POLYGON')[1]
#         coor=coor.split(')')
#         for indi1,i in enumerate(coor):
#             puntos=[]
#             print(i)
#             if indi1==0:
#                 i=i.replace('(','')
#                 i=i.split(',')
#                 for j in i:
#                     j=j.rstrip()
#                     j=j.split()
#                     puntos.append(Punto2D(j[0],j[1]))
#                 pol=poli2d.PoliLinea2D()
#                 pol.setPoliLineaFromPuntos(puntos)
#                 self.__poli=pol
#             else:
#                 if i=='':
#                     continue
#                 i=i[1:]
#                 i+=')'
#                 i='LINESTRING '+i
#                 self.setHuecos(i)
                
#                 i=i.replace('(',' ')
#                 i=i.split(',')
#                 puntos=[]
#                 lin=pl2.PoliLinea2D()
#                 for j in i:
#                     j=j.rstrip()
#                     j=j.split()
#                     puntos.append(pt2d.Punto2D(j[0],j[1]))
#                 lin.setPoliLineaFromPuntos(puntos)
#                 #self.setHuecos(pol)
#                 del puntos[:]
                    

    
    
    
    def getCentroide(self):
        '''!
        '''
        ptos=self.__poli.getPuntos()[0:-1]
        X=[i.getX() for i in ptos]
        Y=[i.getY() for i in ptos]
        X=mean(X)
        Y=mean(Y)
        return Punto2D(X,Y)
        
    
    def getArea(self):
        '''!
        '''
        ptos=self.__poli.getPuntos()
        x=0
        y=0
        for i in range(len(ptos)-1):
            pt1=ptos[i]
            pt2=ptos[i+1]
            x+=pt1.getX()*pt2.getY()
            y+=pt1.getY()*pt2.getX()
        
        if self.__Huecos==[]:
            return abs(y-x)/2
        else:
            nx=0
            ny=0
            for i in self.__Huecos:
                ptos=i.getPuntos()
                for j in range(len(ptos)-1):
                    pt1=ptos[j]
                    pt2=ptos[j+1]
                    nx+=pt1.getX()*pt2.getY()
                    ny+=pt1.getY()*pt2.getX()
            return((abs(y-x)/2)-(abs(ny-nx)/2))
    
    def getBbox(self):
        '''!
        '''
        ptos=self.__poli.getPuntos()
        x=[i.getX() for i in ptos]
        y=[i.getY() for i in ptos]
        return [Punto2D(min(x),max(y)),Punto2D(max(x),min(y))]
    
    def getPolilinea2D(self):
        '''!
        '''
        return self.__poli
        
    def toGeoJSON(self):
        '''!
        '''
        ptos=self.__poli.getPuntos()
        vals=""
        vals+="[ "
        for indi1,i in enumerate(ptos):
            vals+="["
            x1=i.getX()
            y1=i.getY()
            
            vals+=str(x1)
            vals+=", "
            vals+=str(y1)
            vals+="]"


            if indi1==len(ptos)-1:
                pass
            else:
                vals+=", "
                
        vals+=" ]"
 
        return "{\n"+\
            '"type":"Polygon"'+",\n"\
            '"coordinates": [\n'+\
            vals+'\n'+\
            ']\n'+\
            "}"
        
        
        
        
        
def main():
    import Geometrias.Linea2D as l2d
#     polilin=poli2d.PoliLinea2D()
#     polilin.setWKT('LINESTRING (35 10, 45 45, 15 40, 10 20, 35 10)')
#  
#     polilinHueco=poli2d.PoliLinea2D()
#     polilinHueco.setWKT('LINESTRING (20 30, 35 35, 30 20, 20 30)')
#      
#     print(polilin.toWKT())
#     print(polilinHueco.toWKT())
#      
#     pol=Poligono2D(polilin,huecos=polilinHueco)
#     print(pol.getArea())
#     
#     
#     pol1=Poligono2D()
#     pol1.setFromWKT('POLYGON ((11.9 21.5, 11 22.5, 10 23.7, 9.3 24.5, 8.6 25.5, 8 26.6, 7.5 27.6, 7.2 28.7, 7.2 29.9, 7 31.2, 7 32.3, 7.1 33.6, 7.5 34.7, 8.2 35.9, 8.9 36.7, 9.8 37.5, 11 38.3, 12.3 39.1, 13.9 39.7, 14.9 40, 16.7 40.4, 18.5 40.7, 19.6 40.8, 20.6 40.9, 21.6 41, 22.6 41, 23.7 41, 24.8 41, 26 41, 27.1 40.9, 28.4 40.8, 29.7 40.6, 31.1 40.3, 32.4 40.1, 33.7 39.9, 35.1 39.5, 36.3 39.2, 37.4 38.8, 38.6 38.4, 39.7 38, 40.7 37.6, 42.6 36.7, 44.1 35.6, 45.6 34.4, 46.8 32.7, 47.4 31.9, 48.4 30.2, 49.2 28.4, 50.1 26.7, 50.6 25, 50.9 23.4, 51.3 21.7, 51.4 20.2, 51.4 18.8, 51.3 17.6, 50.8 16.4, 50.6 15.3, 50.3 14.3, 49.8 13, 49.1 12, 48.2 11.1, 47.3 10.2, 46.6 9.3, 45.4 8.8, 44.2 8.4, 43.1 8.1, 41.7 7.8, 40.1 7.6, 38.6 7.3, 37.3 7.1, 36.1 6.9, 34.9 6.8, 33.9 6.8, 32.9 6.9, 31.8 7.1, 30.4 7.4, 29.2 7.5, 27.8 7.6, 26.5 7.8, 24.9 8, 23.4 8.3, 22.1 8.6, 21 8.9, 19.8 9.4, 18.8 10.1, 17.7 10.8, 16.6 11.4, 15.7 12.2, 14.8 12.7, 13.9 13.2, 13.1 13.8, 9 17, 11.9 21.5), (29 18, 28 18.1, 26.7 18.4, 25.2 19.1, 24.3 19.8, 23.3 20.6, 22.5 21.6, 21.9 22.7, 21.3 23.8, 20.9 25.1, 20.7 26.1, 20.5 27.1, 20.4 28.3, 20.5 29.3, 21 30.2, 21.9 31, 23 31.4, 24.1 31.8, 25.2 32, 26.4 32.1, 27.6 32.1, 28.7 32, 29.8 31.7, 30.8 31.3, 32.1 30.7, 33.6 30.1, 34.7 29.3, 35.9 28.6, 37.1 27.8, 38.1 27.1, 38.9 26.3, 39.6 25.4, 40.1 24, 40.4 22.8, 40.6 21.6, 40.6 20.5, 40.1 19.3, 39.6 18.1, 39.1 16.9, 38.3 15.8, 37.6 15, 36.7 14.5, 35.6 14.1, 34.6 14.1, 33.4 14, 32.1 13.9, 30.8 13.9, 29.8 13.9, 29 14, 29 18))')
#     print(pol1.getArea())
    
    
    
    
    pol2=Poligono2D()
    pol2.setFromWKT('POLYGON ((3.4 39.6, 40 39.6, 40 14, 3.4 14, 3.4 39.6), (18 37, 8 26, 26 15, 37.5 23.5, 18 37))')
    print(pol2.getArea())
    
    
    
    
#     pol.setPoligono([l2d.Linea2D(pt2.Punto2D(0.0,0.0),pt2.Punto2D(10,0)),
#                                l2d.Linea2D(pt2.Punto2D(10.0,0),pt2.Punto2D(10,10)),
#                                l2d.Linea2D(pt2.Punto2D(10,10.0),pt2.Punto2D(0,10)),
#                                l2d.Linea2D(pt2.Punto2D(0,10),pt2.Punto2D(0,0))])
#     
#     print(pol.getArea())
#     print(pol.toGeoJSON())
#     print(pol.getCentroide().getX(),pol.getCentroide().getY()) 
#     pol.setFromWKT('POLYGON ((35 10, 45 45, 15 40, 10 20, 35 10),(20 30, 35 35, 30 20, 20 30))')
#     print(pol.toGeoJSON())
#     pass

if __name__=='__main__':
    main()