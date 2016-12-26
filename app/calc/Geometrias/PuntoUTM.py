#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''!
Created on 6/2/2015

@author: Antonio Hermosilla Rodrigo.
@contact: anherro285@gmail.com
@organization: Antonio Hermosilla Rodrigo.
@copyright: (C) 2015 by Antonio Hermosilla Rodrigo
@version: 1.0.0
'''

class PuntoUTM(object):
    '''
    Clase destinada a lamacenar la información espacial de un punto en proyección UTM
    '''
    __X=None
    __Y=None
    __Hemis=None
    __H=None
    __h_elip=0
    __conmed=None
    __kpunto=None


    def __init__(self, *args,**kwargs):
        '''!
        Constructor de la clase PuntoUTM.
        @param args1 X float|int|str: Valor de la coordenada X UTM.
        @param args2 Y float|int|str: Valor de la coordenada Y UTM.
        @param kwargs huso int: Huso geográfico de las coordenadas del punto UTM.
        @note kwargs huso: Valor por defecto 30.
        @param kwargs hemisferioY str: Posición geográfica de la coordenada Y.
        @note kwargs hemisferioY: Valor por defecto N.
        @param kwargs helip float|int|str: Valor de la altura elipsoidal.
        @note kwargs helip: Valor por defecto 0.
        
        '''
        try:
            HemisferioY=kwargs['hemisferioY']
        except:
            HemisferioY='N'
        self.setHemisferioY(HemisferioY)
        #Huso geográfico.
        try:
            Huso=kwargs['huso']
        except:
            Huso=30
        self.setHuso(Huso)
        #Altura elipsoidal.
        try:
            Helip=kwargs['helip']
        except:
            Helip=0
        self.setAlturaElipsoidal(Helip) 
        
        
        if len(args)==0:
            pass
        elif len(args)==2:
            self.setX(args[0])
            self.setY(args[1])
        else:
            raise Exception("La clase PuntoUTM recibe 2 parametros como argumentos.\nSe han introducido: "+str(len(args))+" parametros.")
         
        
    def setX(self,X):
        '''!
        @brief: Método para introducir y comprobar el valor de la Coordenada X UTM introducida.
        @param X float: Valor de la coordenada X UTM en metros.
        @raise
        @raise
        '''
        try:
            float(X)
        except Exception as e:
            raise Exception(e)
        finally:
            self.__X=float(X)
        if self.__X<0:
            raise Exception("La coordenada X UTM no puede ser negativa")

    def setY(self,Y):
        '''!
        @brief: Método para introducir y comprobar el valor de la Coordenada Y UTM introducida.
        @param Y float: Valor de la coordenada Y UTM en metros.
        @raise
        @raise
        '''
        try:
            float(Y)
        except Exception as e:
            raise Exception(e)
        finally:
            self.__Y=float(Y)
        if self.__Y<0:
            raise Exception("La coordenada Y UTM no puede ser negativa")

    def setHemisferioY(self,HemisferioY):
        '''!
        Método para introducir y comprobar el valor del Hemisferio donde está situada la coordenada Y.
        @param HemisferioY str: Situación del hemisferio de la coordenada Y.
        @note HemisferioY: Los posibles valores para HemisferioY son N o S.
        @note HemisferioY: Vaor por defecto N.
        @exception: Se pruducira una excepción si el valor introducido no es de tipo str.
        @exception: Se pruducira una excepción si el valor no es N o S.
        '''
        if not type(HemisferioY)==str:
            raise Exception("El valor de Hemisferio_Y no es de tipo string.")
        elif HemisferioY!="S" and HemisferioY!="N":
            raise Exception("El valor de Hemisferio_Y solo puede ser N o S.")
        else:
            self.__Hemis=HemisferioY

    def setAlturaElipsoidal(self,AlturaElipsoidal):
        '''!
        @brief: Método para introducir y comprobar la Altura Elipsoidal.
        @param AlturaElipsoidal float|int|str: Valor de la altura elipsoidal.
        @note AlturaElipsoidal: El rango de definición de la longitud es de altura elipsoidal>=0.
        @exception
        @exception
        '''
        if AlturaElipsoidal==None:
            return
        try:
            float(AlturaElipsoidal)
        except Exception as e:
            raise Exception(e)
        finally:
            self.__h=float(AlturaElipsoidal)

        if self.__h<0:
            raise Exception("El rango de la altura elipsoidal no es válido")

        

    def setHuso(self,Huso):
        '''!
        @brief: Método para introducir el Huso geografico de la coordenada UTM.
        @param Huso int|str: Huso geográfico de la coordenada UTM.
        @note Huso: El Huso debe de estar comprendido entre los valores 0-60.
        '''
        try:
            int(Huso)
        except Exception as e:
            raise Exception(e)
        finally:
            self.__H=int(Huso)
        if self.__H < 1 or self.__H > 60:
            raise Exception("El Huso UTM debe ser un valor entre 1 y 60")


    def setConvergenciaMeridianos(self,ConvergenciaMeridianos):
        '''!
        @brief: Método para asignar la convergencia de meridianos del punto.
        @param ConvergenciaMeridianos float|int|str: Valor de la Convergencia de meridianos.
        '''
        if ConvergenciaMeridianos==None:
            return
        
        try:
            float(ConvergenciaMeridianos)
        except Exception as e:
            raise Exception(e)
        finally:
            self.__conmed=float(ConvergenciaMeridianos)
        
    def setEscalaLocalPunto(self,EscalaLocalPunto):
        '''!
        @brief: Método para asignar la escala local del punto.
        @param EscalaLocalPunto float|int|str: Valor de la escala local.
        '''
        if EscalaLocalPunto==None:
            return
        
        try:
            float(EscalaLocalPunto)
        except Exception as e:
            raise Exception(e)
        finally:
            self.__kpunto=float(EscalaLocalPunto)
            
    def getX(self):
        '''!
        @brief: Método que devuelve el valor de la coordenada X UTM.
        @return float: Valor de la coordenada X UTM.
        '''
        return self.__X

    def getY(self):
        '''!
        @brief: Método que devuelve el valor de la coordenada Y UTM.
        @return float: Valor de la coordenada Y UTM.
        '''
        return self.__Y

    def getHemisferioY(self):
        '''!
        @brief: Método que devuelve el valor de la posición del Hemisferio de la coordenada Y.
        @return str: Hemisferio de la coordenada Y.
        '''
        return self.__Hemis

    def getAlturaElipsoidal(self):
        '''!
        @brief: Método que devuelve el valor de la altura elipsoidal.
        @return float: Altura elipsoidal.
        '''
        return self.__h_elip
                            

    def getHuso(self):
        '''!
        @brief: Método que devuelve el valor del Huso geográfico de las coordenadas.
        @return int: Huso geográfico.
        '''
        return self.__H

    def getConvergenciaMeridianos(self):
        '''!
        @brief: Método que devuelve el valor de la convergencia de meridianos.
        @return float: convergencia de meridianos.
        '''
        return self.__conmed

    def getEscalaLocalPunto(self):
        '''!
        @brief: Método que devuelve el valor de la escala local del punto.
        @return float: Escala local del punto.
        '''
        return self.__kpunto

    def getZonaUTM(self):
        '''!
        @brief: Método que cálcula la zona UTM a la que pertenece el Punto.
        @return str: Letra a correspondiente a la zona UTM del punto.
        '''
        #Se puede mejorar convirtiendo antes las coordenadas a geograficas.
        #De este modo solo habra que dividir por 8.
        import Proyecciones.UTM2Geo as u2g
        sal=u2g.UTM2Geo(self, 'GRS 1980')
        if self.__Hemis=="N":
            Zona=["N","P","Q","R","S","T","U","V","W","X"]
            ancho_zona=self.__Y/(8*111111.111)
            ancho_zona1=sal.getLatitud()/8.0
#             print(ancho_zona,ancho_zona1)
#             print(round(ancho_zona),round(ancho_zona1))
            return Zona[round(ancho_zona)]
            

        else:
            Zona=["C","D","E","F","G","H","J","K","L","M"]
            ancho_zona=abs((10000000-self.__Y)/(8*111111.111))
            ancho_zona1=sal.getLatitud()/8.0
#             print(ancho_zona,ancho_zona1)
#             print(round(ancho_zona),round(ancho_zona1))
            return Zona[round(ancho_zona)]
        
        
    
    def toString(self):
        '''!
        @brief: Método que devuleve toda la información del punto en formato str.
        @return str: Un string con toda la información del punto.
        '''
        
        return "X:"+str(self.getX())+"\n"\
            "Y:"+str(self.getY())+"\n"\
            "Hemisferio Y:"+str(self.getHemisferioY())+"\n"\
            "Huso:"+str(self.getHuso())+"\n"\
            "Altura Elipsoidal:"+str(self.getAlturaElipsoidal())+"\n"\
            "Convergencia meridianos:"+str(self.getConvergenciaMeridianos())+"\n"\
            "Escala local del punto:"+str(self.getEscalaLocalPunto())+"\n"\
            "Zona UTM:"+str(self.getZonaUTM())+"\n"\
    
    def toJSON(self):
        '''!
        @brief: Método que devuleve toda la información del punto en formato JSON.
        @return str: Un string en formato JSON.
        '''
        return "{\n"+\
            '"X":'+'"'+str(self.getX())+'"'+",\n"\
            '"Y":'+'"'+str(self.getY())+'"'+",\n"\
            '"hemisferioY":'+'"'+str(self.getHemisferioY())+'"'+",\n"\
            '"huso":'+'"'+str(self.getHuso())+'"'+",\n"\
            '"alturaElipsidal":'+'"'+str(self.getAlturaElipsoidal())+'"'+",\n"\
            '"w":'+'"'+str(self.getConvergenciaMeridianos())+'"'+",\n"\
            '"kp":'+'"'+str(self.getEscalaLocalPunto())+'"'+",\n"\
            '"ZonaUTM":'+'"'+str(self.getZonaUTM())+'"'+"\n"\
            +"}"
    
    def toGeoJSON(self):
        '''!
        @brief: Método que devuleve un GeoJSON del punto.
        @return str: Un string en formato JSON.
        '''
        
        return "{\n"+\
            '"type":"Point"'+",\n"\
            '"coordinates":'+\
            '['+str(self.__X)+','+str(self.__Y)+']'+"\n"\
            "}"
            
def main():
    p=PuntoUTM(670725.49,'4429672.97')
#     print(p.getX(),p.getY(),p.getHemisferioY(),p.getHuso())
#     print(p.getZonaUTM())
    print(p.toString())
    print(p.toJSON())
    print(p.toGeoJSON())
    import json
    print(json.loads(p.toGeoJSON())['coordinates'])
    
    p=PuntoUTM(670725.49,'5570327.03',hemisferioY='S',huso=34.0)
#     print(p.getX(),p.getY(),p.getHemisferioY(),p.getHuso())
#     print(p.getZonaUTM())

if __name__=="__main__":
    main()
        
        
        