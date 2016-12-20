#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 30/1/2015

@author: Antonio Hermosilla Rodrigo.
@contact: anherro285@gmail.com
@organization: Antonio Hermosilla Rodrigo.
@copyright: (C) 2015 by Antonio Hermosilla Rodrigo
@version: 1.0.0
'''
from math import pi
from math import modf

class Angulo(object):
    '''!
    Clase destinada al almacenamiento de la información angular.
    Ejemplos de declaración del un objeto de la clase:\n
    ang=Angulo()-->Construtor vacío.\n
    ang=Angulo(0.1)--> radianes.\n
    ang=Angulo(10,40,50.4533)-->sexagesimal.\n
    ang=Angulo(54,formato='pseudosexagesimal')\n
    ang=Angulo(54,formato='centesimal')\n
    
    '''
    __ang=None
    __g=None
    __m=None
    __s=None
    __f=None
    __negativo=True
    __girar=False
    
    __ftype=["radian","sexagesimal","pseudosexagesimal","centesimal","latitud","longitud180","longitud360"]


    def __init__(self, *args,**kwargs):
        '''!
        Constructor de la clase Angulo.
        
        '''
        if len(kwargs)>0:
            for key in kwargs:
                if key.lower()=='girar':
                    aux=kwargs[key]
                    self.setGirar(aux)
                    
                elif key.lower()=='negativos':
                    aux=kwargs[key]
                    self.setNegativos(aux)
                    
                elif key.lower()=='formato':
                    aux=kwargs[key]
                    if aux in self.__ftype:
                        self.__f=aux
                    else:
                        raise ValueError("No se reconoce el formato introducido.")
                else:
                    raise Exception("El argumento: "+key+" no se reconoce")
                
        if self.__f==None:
            self.setFormato("radian")

        if len(args)==0:
            pass
        elif len(args)==1:
            self.setAngulo(args[0])
            self.setFormato(self.__f)
        elif len(args)==3:
            self.setAngulo(args[0],args[1],args[2])
            self.setFormato("sexagesimal")
        else:
            raise Exception("La clase Angulo recibe 1 o 3 parametros como argumentos.\nSe han introducido: "+str(len(args))+" parametros.")
                
        
    def setAngulo(self,*args):
        '''!
        @brief: Método para introducir el ángulo.
        *args: El valor del ángulo se puede introducir de dos formas:\n
        Un argumento:\n
        Angulo float: Valor del ángulo.\n
        Tres argumentos:\n
        Grados float: Valor de los grados.\n
        Minutos float: Valor de los minutos.\n
        Segundos float: Valor de los segundos.\n
        
        '''
        if len(args)==1:
            try:
                angulo=float(args[0])
                self.__ang=angulo
            except Exception as e:
                raise Exception(e)
            
        elif len(args)==3:
            try:
                g=float(args[0])
                m=float(args[1])
                s=float(args[2])
                
                self.__g=g
                self.__m=m
                self.__s=s
            except Exception as e:
                raise Exception(e)
        else:
            raise Exception("El método setAngulo recibe 1 o 3 parametros como argumentos.\nSe han introducido: "+str(len(args))+" parametros.")
            
    def setFormato(self,Formato):
        '''!
        @brief: Método para introducir el formato del ángulo.
        @param Formato str: Formato del ángulo.
        @note Formato: Formatos válidos: radian,sexagesimal,pseudosexagesimal,centesimal,latitud,longitud180,longitud360
        @excepcion: Se producira una excepción si el formato no es uno de los listados.
        '''
        try:
            if Formato.lower() in self.__ftype:
                self.__f=str(Formato)
        except Exception as e:
                raise Exception(e)
            
        if self.__ang!=None:
            if self.__f=="radian":
                if self.__negativo==True and self.__girar==True:
                    while self.__ang<-2*pi:
                        self.__ang+=2*pi
                    while self.__ang>2*pi:
                        self.__ang-=2*pi
                    return
                              
                elif self.__negativo==False and self.__girar==True:
                    while self.__ang<0:
                        self.__ang+=2*pi
                    while self.__ang>2*pi:
                        self.__ang-=2*pi
                    return
                        
                elif self.__negativo==True and self.__girar==False:
                    if self.__ang<-2*pi or self.__ang>2*pi:
                        raise Exception("El ángulo está fuera del rango de definición ]-2pi,2pi[")
                    
                elif self.__negativo==False and self.__girar==False:
                    if self.__ang<0 or self.__ang>2*pi:
                        raise Exception("El ángulo está fuera del rango de definición ]0,2pi[")
                return
                    
            elif self.__f=="pseudoxesagesimal":
                if self.__negativo==True and self.__girar==True:
                    while self.__ang<-360:
                        self.__ang+=360
                    while self.__ang>360:
                        self.__ang-=360
                    return
                
                elif self.__negativo==False and self.__girar==True:
                    while self.__ang<0:
                        self.__ang+=360
                    while self.__ang>360:
                        self.__ang-=360
                    return
                        
                elif self.__negativo==True and self.__girar==False:
                    if self.__ang<-360 or self.__ang>360:
                        raise Exception("El ángulo está fuera del rango de definición ]-360,360[")
                    
                elif self.__negativo==False and self.__girar==False:
                    if self.__ang<0 or self.__ang>360:
                        raise Exception("El ángulo está fuera del rango de definición ]0,360[")
                return
                    
            elif self.__f=="centesimal":
                if self.__negativo==True and self.__girar==True:
                    while self.__ang<-400:
                        self.__ang+=400
                    while self.__ang>400:
                        self.__ang-=400
                    return
                              
                elif self.__negativo==False and self.__girar==True:
                    while self.__ang<0:
                        self.__ang+=400
                    while self.__ang>400:
                        self.__ang-=400
                    return
                        
                elif self.__negativo==True and self.__girar==False:
                    if self.__ang<-400 or self.__ang>400:
                        raise Exception("El ángulo está fuera del rango de definición ]-400,400[")
                    
                elif self.__negativo==False and self.__girar==False:
                    if self.__ang<0 or self.__ang>400:
                        raise Exception("El ángulo está fuera del rango de definición ]0,400[")
                return
            
            elif self.__f=="latitud":
                # El ángulo Latitud es un ángulo Pseudosexagesimal está definido entre [-90,90[
                if self.__girar == True:
                    while self.__ang > 90:
                        self.__ang -= 90
                    while self.__ang < -90:
                        self.__ang += 90
                    return
                else:
                    if self.__ang < -90 or self.__ang > 90:
                        raise Exception("El ángulo está fuera del rango de definición ]-90,90[")
                return
            
            elif self.__f == "longitud180":
                if self.__girar == True:
                    # El ángulo Longitud es un ángulo Pseudosexagesimal está definido entre [-180,180[
                    while self.__ang >= 180:
                        self.__ang -= 180
                    while self.__ang < -180:
                        self.__ang += 180
                    return
                else:
                    if self.__ang < -180 or self.__ang > 180:
                        raise Exception("El ángulo está fuera del rango de definición ]-180,180[")
                return
                
            elif self.__f == "longitud360":
                if self.__girar == True:
                    # El ángulo Pseudosexagesimal está definido entre [0,360[
                    while self.__ang >= 360:
                        self.__ang -= 360
                    while self.__ang < 0:
                        self.__ang += 360
                    return
                else:
                    if self.__ang < 0 or self.__ang >= 360:
                        raise Exception("El ángulo está fuera del rango de definición [0,360[")
                return
                    
        elif self.__g!=None and self.__m!=None and self.__s!=None:
            if self.__f=="sexagesimal":
                if self.__m >= 60 or self.__m < 0:
                    raise Exception("El rango de definició de los minutos es de [0,60[")
                
                if self.__s >= 60 or self.__s < 0:
                    raise Exception("El rango de definició de los segundos es de [0,60[")
                
                if self.__negativo == True and self.__girar == True:
                    # El ángulo Sexagesimal está definido entre [-360,360[
                    while self.__g >= 360:
                        self.__g -= 360
                    while self.__g < -360:
                        self.__g += 360
                    return

                elif self.__negativo == False and self.__girar == True:
                    # El ángulo Sexagesimal está definido entre [0,360[
                    while self.__g >= 360:
                        self.__g -= 360
                    while self.__g < 0:
                        self.__g += 360
                    return

                elif self.__negativo == True and self.__girar == False:
                    if self.__g < -360 or self.__g > 360:
                        raise Exception("El ángulo está fuera del rango de definición ]-360,360[")

                elif self.__negativo == False and self.__girar == False:
                    if self.__g < 0 or self.__g >= 360:
                        raise Exception("El ángulo está fuera del rango de definición ]0,360[")
                return
        
                
        
            
            
    def setNegativos(self,Negativos):
        '''!
        @brief: Método para introducir la propiedad Negativos.
        @param Neagativos bool: Estado de la propiedad Negativos.
        @note True: Permite alojar números negativos.
        @note False: No permite alojar números negativos.
        @excepcion: Se producira una excepción si el valor no es de tipo bool.
        '''
        if isinstance(Negativos, bool):
            self.__negativo=Negativos
        else:
            raise Exception("Se esperaba un valor de tipo bool como entrada del método.\n Se ha introducido un valor de tipo: "+type(Negativos))
            
            
    def setGirar(self,Girar):
        '''!
        @brief: Método para introducir la propiedad Girar.
        @param Girar bool: Estado de la propiedad Girar.
        @note True: Permite agirar el ángulo hasta el rango.
        @note False: No permite girar el ángulo hasta el rango.
        @excepcion: Se producira una excepción si el valor no es de tipo bool.
        '''
        if isinstance(Girar, bool):
            self.__girar=Girar
        else:
            raise Exception("Se esperaba un valor de tipo bool como entrada del método.\n Se ha introducido un valor de tipo: "+type(Girar))
            
            
    def getFormato(self):
        '''!
        @brief: Método que devuelve el valor actual del formato angular de la clase.
        @return str: Formato del ángulo.
        '''
        return self.__f
    
    def getAngulo(self):
        '''!
        @brief: Método que decuelve el valor del ángulo introducido.
        @return float|[]: Angulo introducido.
        '''
        if self.__ang!=None:
            return self.__ang
        elif self.__g!=None and self.__m!=None and self.__s!=None:
            return [self.__g,self.__m,self.__s]
        else:
            return [self.__ang,self.__g,self.__m,self.__s]
        
    def getNegativos(self):
        '''!
        @brief: Método que devuleve el estado actual de la propiedad negativos.
        @return bool: Estado de la propiedad negativos.
        '''
        return self.__negativo
    
    def getGirar(self):
        '''!
        @brief: Método que devuleve el estado actual de la propiedad girar.
        @return bool: Estado de la propiedad girar.
        '''
        return self.__girar
    
    def Convertir(self,Formato):
        '''!
        @brief: Convierte el ángulo a otro formato disponible.
        @para Formato str: Formato al que se quiere convertir el ángulo.
        @note: Formatos a los que se puede convertir un ángulo:\nradian\npseudosexagesimal\nsexagesimal\ncentesimal.
        '''
        if self.__f==Formato:
            raise Exception("El formato a convertir es el mismo que el formato actual del ángulo")
        #Casos.
        if self.__f=='radian' and Formato=="pseudosexagesimal":
            self.__ang*=(180/pi)
            self.setFormato('pseudosexagesimal')
            return
        elif self.__f=='radian' and Formato=="centesimal":
            self.__ang*=(200/pi)
            self.setFormato('centesimal')
            return
        elif self.__f=='radian' and Formato=="sexagesimal":
            aux=self.__ang
            aux*=(180/pi)
            dec,ent=modf(aux)
            self.__g=ent
            dec*=(60)
            dec,ent=modf(dec)
            self.__m=abs(ent)
            dec*=(60)
            self.__s=abs(dec)
            self.__ang=None
            #print(self.__g,self.__m,self.__s)
            self.setFormato('sexagesimal')
            return
        elif self.__f=='radian' and Formato=="latitud":
            self.__ang*=(180/pi)
            self.setFormato('latitud')
            return
        elif self.__f=='radian' and Formato=="longitud180":
            self.__ang*=(180/pi)
            self.setFormato('longitud180')
            return
        elif self.__f=='radian' and Formato=="longitud360":
            self.__ang*=(180/pi)
            self.setFormato('longitud360')
            return
        elif (self.__f=='pseudosexagesimal' or self.__f=="latitud" or self.__f=="longitud180" or self.__f=="longitud360") and Formato=="radian":
            self.__ang*=(pi/180)
            self.setFormato('radian')
            return
        elif (self.__f=='pseudosexagesimal' or self.__f=="latitud" or self.__f=="longitud180" or self.__f=="longitud360") and Formato=="centesimal":
            self.__ang*=(200/180)
            self.setFormato('centesimal')
            return
        elif (self.__f=='pseudosexagesimal' or self.__f=="latitud" or self.__f=="longitud180" or self.__f=="longitud360") and Formato=="sexagesimal":
            aux=self.__ang
            dec,ent=modf(aux)
            self.__g=ent
            dec*=(60)
            dec,ent=modf(dec)
            self.__m=ent
            dec*=(60)
            self.__s=dec
            self.__ang=None
            self.setFormato('sexagesimal')
            return
        elif self.__f=='centesimal' and Formato=="radian":
            self.__ang*=(pi/200)
            self.setFormato('radian')
            return
        elif self.__f=='centesimal' and Formato=="pseudosexagesimal":
            self.__ang*=(180/200)
            self.setFormato('pseudosexagesimal')
            return
        elif self.__f=='centesimal' and Formato=="sexagesimal":
            aux=self.__ang
            aux*=(200/pi)
            dec,ent=modf(aux)
            self.__g=ent
            dec*=(60)
            dec,ent=modf(dec)
            self.__m=ent
            dec*=(60)
            self.__s=dec
            self.__ang=None
            self.setFormato('sexagesimal')
            return
        elif self.__f=='centesimal' and Formato=="latitud":
            self.__ang*=(180/200)
            self.setFormato('latitud')
            return
        elif self.__f=='centesimal' and Formato=="longitud180":
            self.__ang*=(180/200)
            self.setFormato('longitud180')
            return
        elif self.__f=='centesimal' and Formato=="longitud360":
            self.__ang*=(180/200)
            self.setFormato('longitud360')
            return
        elif self.__f=='sexagesimal' and Formato=="radian":
            ang=self.__g+(self.__m/60)+(self.__s/3600)
            self.__ang=ang*pi/180
            self.__g=None
            self.__m=None
            self.__s=None
            self.setFormato('radian')
            return
        elif self.__f=='sexagesimal' and Formato=="pseudosexagesimal":
            self.__ang=self.__g+(self.__m/60)+(self.__s/3600)
            self.__g=None
            self.__m=None
            self.__s=None
            self.setFormato('pseudosexagesimal')
            return
        elif self.__f=='sexagesimal' and Formato=="centesimal":
            self.__ang=self.__g+(self.__m/60)+(self.__s/3600)
            self.__ang*=(200/180)
            self.__g=None
            self.__m=None
            self.__s=None
            self.setFormato('centesimal')
            return
        elif self.__f=='sexagesimal' and Formato=="latitud":
            self.__ang=self.__g+(self.__m/60)+(self.__s/3600)
            self.__g=None
            self.__m=None
            self.__s=None
            self.setFormato('latitud')
            return
        elif self.__f=='sexagesimal' and Formato=="longitud180":
            self.__ang=self.__g+(self.__m/60)+(self.__s/3600)
            self.__g=None
            self.__m=None
            self.__s=None
            self.setFormato('longitud180')
            return
        elif self.__f=='sexagesimal' and Formato=="longitud360":
            self.__ang=self.__g+(self.__m/60)+(self.__s/3600)
            self.__g=None
            self.__m=None
            self.__s=None
            self.setFormato('longitud360')
            return
        elif self.__f=='longitud180' and Formato=="longitud360":
            if self.__ang<0:
                self.__ang+=360
            self.setFormato('longitud360')
            return
        elif self.__f=='longitud360' and Formato=="longitud180":
            if self.__ang>180:
                self.__ang-=360
            self.setFormato('longitud180')
            return
            
            
    def Convert2Min(self):
        '''
        @brief: Método que convierte el ángulo almacenado a minutos
        @return float: ángulo convertido a minutos.
        @excepcion: Se producira una excepción si se intenta convertir a minutos un ángulo en formato radian.
        '''
        if self.__f == "sexagesimal":
            return self.__g * 60 + self.__m + self.__s / 60
        elif self.__f == "pseudosexagesimal":
            dec, ent = modf(self.__ang)
            return ent * 60 + dec * 60
        elif self.__f == "centesimal":
            dec, ent = modf(self.__ang)
            return ent * 100 + dec * 100
        elif self.__f == "latitud":
            dec, ent = modf(self.__ang)
            return ent * 60 + dec * 60
        elif self.__f == "longitud180":
            dec, ent = modf(self.__ang)
            return ent * 60 + dec * 60
        elif self.__f == "longitud360":
            dec, ent = modf(self.__ang)
            return ent * 60 + dec * 60
        else:
            raise Exception("El Formato de ángulo que se quiere convertir a minutos no es válido")
        
    
    def Convert2Seconds(self):
        '''
        @brief: Método que convierte el ángulo almacenado a segundos.Para ello el ángulo debe ser de formato Sexagesimal, PseudoSexagesimal o Centesimal.
        @return float: Ángulo convertido a segundos.
        @excepcion: Se producira una excepción si se intenta convertir a segundos un ángulo en formato radian.
        '''
        if self.__f == "sexagesimal":
            return self.__g * 3600 + self.__m * 60 + self.__s
        elif self.__f == "pseudosexagesimal":
            dec, ent = modf(self.__ang)
            return ent * 3600 + dec * 3600
        elif self.__f == "centesimal":
            dec, ent = modf(self.__ang)
            return ent * 10000 + dec * 10000
        elif self.__f == "latitud":
            dec, ent = modf(self.__ang)
            return ent * 3600 + dec * 3600
        elif self.__f == "longitud180":
            dec, ent = modf(self.__ang)
            return ent * 3600 + dec * 3600
        elif self.__f == "longitud360":
            dec, ent = modf(self.__ang)
            return ent * 3600 + dec * 3600
        else:
            raise Exception("El Formato de ángulo que se quiere convertir a segundos no es válido")
        
    def getFormatosDisponibles(self):
        '''!
        @brief: Método que devuelve los formatos de ángulos disponibles.
        @return []: Lista con los formatos disponibles.
        '''
        return self.__ftype
        
    def toString(self):
        '''!
        @brief: Método que devuelve toda la información del ángulo en un str.
        @return str: Un string con la información del ángulo.
        '''
        try:
            anm=self.Convert2Min()
            ans=self.Convert2Seconds()
        except:
            anm=None
            ans=None
        
        return "angulo:"+str(self.__ang)+"\n"\
            "grados:"+str(self.__g)+"\n"\
            "minutos:"+str(self.__m)+"\n"\
            "segundos:"+str(self.__s)+"\n"\
            "formato:"+str(self.__f)+"\n"\
            "negativos:"+str(self.__negativo)+"\n"\
            "girar:"+str(self.__girar)+"\n"\
            "angulo minutos:"+str(anm)+"\n"\
            "angulo segundos:"+str(ans)+"\n"\
            
    def toJSON(self):
        '''!
        @brief: Método que devuelve toda la información del ángulo en un JSON.
        @return str: Un string en formato JSON con la información del ángulo.
        '''
        try:
            anm=self.Convert2Min()
            ans=self.Convert2Seconds()
        except:
            anm=None
            ans=None
        
        return "{"+\
            '"Angulo":'+'"'+str(self.__ang)+'"'+",\n"\
            '"grados":'+'"'+str(self.__g)+'"'+",\n"\
            '"minutos":'+'"'+str(self.__m)+'"'+"\n"\
            '"segundos":'+'"'+str(self.__s)+'"'+"\n"\
            '"formato":'+'"'+str(self.__f)+'"'+"\n"\
            '"negativos":'+'"'+str(self.__negativo)+'"'+"\n"\
            '"girar":'+'"'+str(self.__girar)+'"'+"\n"\
            '"angulo minutos":'+'"'+str(anm)+'"'+"\n"\
            '"angulo segundos":'+'"'+str(ans)+'"'+"\n"\
            +"}"
        
                
            
        
def main():
    #a1=Angulo(0.4,formato='pseudosexagesimal')
    a1=Angulo(0,20,0)
    print(a1.toString())
    a1.Convertir('pseudosexagesimal')
#     print(a1.getAngulo())
    print(a1.toJSON())
#     print(a1.getFormato())
#     print(a1.getNegativos())
#     print(a1.getGirar())
#     a1.Convertir('sexagesimal')
#     print(a1.getAngulo())
#     a1.Convertir('centesimal')
#     print(a1.getAngulo())
#     a1.Convertir('pseudosexagesimal')
#     print(a1.getAngulo())
#     a1.Convertir('radian')
#     print(a1.getAngulo())
#     a2=Angulo(10,20,30,formato='sexagesimal')
#     print(a2.getAngulo())
#     print(a2.getFormato())
    
if __name__=="__main__":
    main()    
        
        
        