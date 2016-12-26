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
import BasesDeDatos.SQLite.SQLiteManager as bd
from math import sqrt
from os.path import split,realpath

class Elipsoides(object):
    '''!
    Clase destinada a almacenar información sobre un elipsoide.
    Ejemplos de declaración del un objeto de la clase:\n
    elip=Elipsoides('WGS 1984')
    '''
    __nom=None
    __a=None
    __b=None
    __f=None
    __GM=None
    __we=None
    __J2=None


    def __init__(self, NombreElipsoide):
        '''!
        Constructor de la clase Elipsoide.
        @param NombreElipsoide srt: Nombre del elipsoide a cargar.
        '''
        self.__checkNombreElipsoide(NombreElipsoide)
        rutafil, file=split(realpath(__file__))
        elips=bd.SQLiteManager(rutafil+'/Elipsoides/Elipsoides.db')
        
        try:
            parametros=elips.Consulta('''SELECT * FROM Elipsoides WHERE Nombre='''+"'"+NombreElipsoide+"'")
            self.__nom=NombreElipsoide
        except Exception as e:
            raise Exception(e)
        
        if parametros==[]:
            raise Exception("No se encuentra el elipsoide introducido.")
        
        self.__a=parametros[0][1]
        self.__b=parametros[0][2]
        self.__f=parametros[0][3]
        self.__GM=parametros[0][4]
        self.__we=parametros[0][5]
        self.__J2=parametros[0][6]
            
    def getElipsoidesDisponibles(self):
        '''!
        @brief: Método que devuelve el listado de elipsoides disponibles en la base de datos.
        @return str: Nombres de los elipsoide.
        '''
        elips=bd.SQLiteManager('../Geodesia/Elipsoides/Elipsoides.db')
        return elips.ObtenerColumna('Elipsoides', 'Nombre')
        
    def __checkNombreElipsoide(self,Nombre):
        '''!
        '''
        if not isinstance(Nombre, str):
            raise Exception("Se esperaba un str como argumento de entrada.")
        
        
    def getSemiEjeMayor(self):
        '''!
        @brief: Método que devuelve el semieje mayor del elipsoide.
        @return float: Valor del semieje mayor del elipsoide.
        '''
        return self.__a
    
    def getSemiEjeMenor(self):
        '''!
        @brief: Método que devuelve el semieje menor del elipsoide.
        @return float: Valor del semieje menor del elipsoide.
        '''
        if self.__f==None:
            return self.__a
        return self.__a-(self.__a*(1/self.__f))
    
    def getAplanamiento(self):
        '''!
        @brief: Método que devuelve el aplanamiento del elipsoide.
        @return float: Aplanamiento del elipsoide.
        '''
        if self.__f==None:
            self.__f=1/((self.__a-self.__b)/(self.__a))
            return self.__f
        return self.__f
    
    def getExcentricidadLineal(self):
        '''
        @brief: Método que devuelve la excentricidad lineal del elipsoide.
        @return: float: Valor de la excentricidad lineal (E).
        '''
        return (sqrt((self.__a**2)-(self.getSemiEjeMenor()**2)))
    
    def getPrimeraExcentricidad(self):
        '''
        @brief: Método que devuelve la primera excntricidad del elipsoide.
        @return: float: Valor de la primera excentricidad (e).
        '''
        return (self.getExcentricidadLineal()/self.__a)

    def getSegundaExcentricidad(self):
        '''
        @brief: Método que devuelve la segunda exentricidad del elipsoide.
        @return: float: Valor de la segunda excentricidad (e').
        '''
        return (self.getExcentricidadLineal()/self.getSemiEjeMenor())
    
    def getVelocidadAngular(self):
        '''
        @brief: Método que devuelve la velocidad angular del elipsoide, si esta está disponible.
        @return float, None: velocidad angular del elipsoide.
        @note: En el caso de que la velocidad angular no esté disponible para el elipsoide, se devolvera None.
        '''
        return self.__we

    def getProductoGM(self):
        '''
        @brief: Método que devuelve el producto de G*M del elipsoide, si esta está disponible.
        @return float, None: Valor del producto de G*M.
        @note: En el caso de que el producto de G*M no esté disponible para el elipsoide, se devolvera None.
        '''
        return self.__GM

    def getFactorFormaDinamico(self):
        '''
        @brief: Método que devuelve el factor de forma dinámico del elipsoide, si esta está disponible.
        @return float, None: Valor del factor de forma dinámico (J2)
        @note: En el caso de que el factor de forma dinámico no esté disponible para el elipsoide, se devolvera None.
        '''
        return self.__J2
    
    def toString(self):
        '''!
        @brief: Método que devuleve toda la información del punto en formato str.
        @return str: Un string con toda la información del punto.
        '''
        return "Nombre:"+str(self.__nom)+"\n"\
            "Semieje Mayor:"+str(self.getSemiEjeMayor())+"\n"\
            "Semieje Menor:"+str(self.getSemiEjeMenor())+"\n"\
            "Aplanamiento:"+str(self.getAplanamiento())+"\n"\
            "Excentricidad Lineal:"+str(self.getExcentricidadLineal())+"\n"\
            "Primera Excentricidad:"+str(self.getPrimeraExcentricidad())+"\n"\
            "Segunda Excentricidad:"+str(self.getSegundaExcentricidad())+"\n"\
            "Producto GM:"+str(self.getProductoGM())+"\n"\
            "Velocidad Angular:"+str(self.getVelocidadAngular())+"\n"\
            "Factor de forma dinámico:"+str(self.getFactorFormaDinamico())+"\n"
            
    def toJSON(self):
        '''!
        @brief: Método que devuleve toda la información del punto en formato JSON.
        @return str: Un string en formato JSON.
        '''
        return "{"+\
            '"Nombre":'+'"'+str(self.__nom)+'"'+",\n"\
            '"Semieje Mayor":'+'"'+str(self.getSemiEjeMayor())+'"'+",\n"\
            '"Aplanamiento":'+'"'+str(self.getSemiEjeMenor())+'"'+",\n"\
            '"Excentricidad Lineal":'+'"'+str(self.getExcentricidadLineal())+'"'+",\n"\
            '"Primera Excentricidad":'+'"'+str(self.getPrimeraExcentricidad())+'"'+",\n"\
            '"Segunda Excentricidad":'+'"'+str(self.getSegundaExcentricidad())+'"'+",\n"\
            '"Producto GM":'+'"'+str(self.getProductoGM())+'"'+",\n"\
            '"Velocidad Angular":'+'"'+str(self.getVelocidadAngular())+'"'+",\n"\
            '"Factor de forma dinámico":'+'"'+str(self.getFactorFormaDinamico())+'"'+"\n"\
            +"}"
        
        
def main():
    el=Elipsoides('GRS 1980')
#     el=Elipsoides('Clarke 1858')
    print(el.toString())
    print(el.toJSON())
    print(el.getElipsoidesDisponibles())
    
if __name__=="__main__":
    main()
        