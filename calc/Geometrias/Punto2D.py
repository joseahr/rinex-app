#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''!
Created on 29/1/2015

@author: Antonio Hermosilla Rodrigo.
@contact: anherro285@gmail.com
@organization: Antonio Hermosilla Rodrigo.
@copyright: (C) 2015 by Antonio Hermosilla Rodrigo.
@version: 1.0.0
'''

class Punto2D(object):
    '''!
    \brief Clase destinada al almacenamiento de la información espacial de un punto bidimensional.
    '''
#     \example Ejemplos de declaración del un objeto de la clase:
#     \example p=Punto2D()-->Constructor vacío
#     \example p=Punto2D(10,10)
#     \example p=Punto2D(10,10,negativos=True)
#     \example p=Punto2D(10,10,negativos=False)
#     \example p=Punto2D(-10,-10,negativos=False)-->Error
    __X = None
    __Y = None
    __neg = True
    __tolerance=None

    def __init__(self, *args, **kwargs):
        '''!
        \brief Constructor de la clase Punto2D.
        \brief Punto2D class constructor.
        
        \arg \c X float: Valor de la coordenada X.
        \arg \c X float: X coordinate value.
        \arg \c Y float: Valor de la coordenada Y.
        \arg \c Y float: Y coordinate value.
        \arg \c kwarg: negativos (bool): Estado de la propiedad negativos.
        \arg \c kwarg: negativos (bool): Negative property status.
    
        \exception ArgumentError: Se producira una excepción si se introducen más o menos argumentos de los admitidos por la clase.
        \exception ArgumentError: A exception is throwed if number of arguments are more or less than admited by class constructor.
        \exception KeyWordError: Se producira una excepción si no se reconoce el kwarg introducido.
        \exception KeyWordError: A exception is throwed if constructor don't recognized the keyword arguments.
        '''
        # Parsear los kwargs.
        if len(kwargs) > 0:
            for key in kwargs:
                if key.lower() == 'negativos':
                    aux = kwargs[key]
                    self.setNegativos(aux)
                else:
                    raise Exception("KeyWordError: El keyword: " + key + " no se reconoce.")
            
        # Parsear args.
        if len(args) == 0:
            pass
        elif len(args) == 2:
            self.setX(args[0])
            self.setY(args[1])
        else:
            raise  Exception("ArgumentError: La clase Punto2D recibe 2 parametros como argumentos.\nSe han introducido: " + str(len(args)) + " parametros.")
            
        
    def setX(self, X):
        '''!
        \brief Método para introducir el valor de la coordenada X de un punto.
        \brief Method set X coordinate value of point.
        
        \param X float: Valor de la coordenada X.
        \param X float: X coordinate value.
        
        \exception ValueError: Se producira una excepción si el valor introducido no se puede convertir a un número.
        \exception ValueError: A exception is throwed if the value can't be covert to number.
        \exception NegativeStatus: Se producira una excepción si se introduce un valor negativo con la propiedad negativos=False.
        \exception NegativeStatus: A exception is throwed if set a negative value when negative property status is False.
        '''
        if isinstance(X, str) or isinstance(X, int) or isinstance(X, float):
            # Se comprueba el tipo de dato introducido y se intenta convertir a float.
            try:
                self.__X = float(X)
            except Exception as e:
                raise Exception(e)
        else:
            raise ValueError()
        
        if self.__neg == False and self.__X < 0:
            # En el caso de que el valor sea negativo y no se puedan introducir números negativos saltara la excepción.
            raise Exception("NegativeStatus: La coordenada X no puede ser negativa.\nNegativos=" + str(self.__neg))
        
        
    def setY(self, Y):
        '''!
        \brief Método para introducir el valor de la coordenada Y de un punto.
        \param Y float: Valor de la coordenada Y.\n Y coordinate value.
        \exception ValueError: Se producira una excepción si el valor introducido no se puede convertir a un número.
        \exception NegativeStatus: Se producira una excepción si se introduce un valor negativo con la propiedad negativos=False.
        '''
        if isinstance(Y, str) or isinstance(Y, int) or isinstance(Y, float):
            # Se comprueba el tipo de dato introducido y se intenta convertir a float.
            try:
                self.__Y = float(Y)
            except Exception as e:
                raise Exception(e)
        else:
            raise ValueError()
        
        if self.__neg == False and self.__Y < 0:
            # En el caso de que el valor sea negativo y no se puedan introducir números negativos saltara la excepción.
            raise Exception("NegativeStatus: La coordenada Y no puede ser negativa.\nNegativos=" + str(self.__neg))
        
    def setTolerance(self,tolerance):
        '''!
        \brief Método que establece la tolerancia del punto.
        \param tolerance float|int|str: Valor de la tolerancia.
        '''
        if tolerance==None:
            self.__tolerance=None
            return
        if isinstance(tolerance, str) or isinstance(tolerance, int) or isinstance(tolerance, float):
            # Se comprueba el tipo de dato introducido y se intenta convertir a float.
            try:
                self.__tolerance = float(tolerance)
            except Exception as e:
                raise Exception(e)
        else:
            raise ValueError()
        
    
    def setFromWKT(self, wkt):
        '''!
        \brief Método que establece los valores de la clase a partir de un wkt
        \param wkt str: Un string en formato wkt.
        '''
        
        tipo=''
        for i in list(wkt):
            if i=='(':
                break
            else:
                tipo+=i
                
        if tipo=='POINT M ':
            coor = wkt.split('POINT M')[1]
            coor = coor.replace('(', '')
            coor = coor.replace(')', '')
            coor = coor.split()
            self.setX(coor[0])
            self.setY(coor[1])
            self.setTolerance(coor[2])
        elif tipo=='POINT ':
            coor = wkt.split('POINT')[1]
            coor = coor.replace('(', '')
            coor = coor.replace(')', '')
            coor = coor.split()
            self.setX(coor[0])
            self.setY(coor[1])
        else:
            raise Exception('No WKT.')
        
    def setFromGeoJSON(self, geojson):
        '''!
        @brief Añade un punto a partir de un string en formato geojson.
        @param geojson str: Un string en formato geojson.
        '''
        from json import loads
        coors = loads(geojson)
        if coors['type'] != 'Point':
            raise Exception("El GeoJSON introducido no corresponde con un punto")
        else:
            coor = coors['coordinates']
            self.setX(coor[0])
            self.setY(coor[1])
            
    def setNegativos(self, Negativos):
        '''!
        \brief Método para introducir la propiedad Negativos.
        \param Neagativos bool|str|int: Estado de la propiedad Negativos.
        \note Neagativos True: Permite alojar números negativos.
        \note Neagativos False: No permite alojar números negativos.
        \exception Se producira una excepción si el valor introducido no se puede convertir a bool.
        \exception Se producira una excepcion si se cambia la propiedad negativos a Flase y existen coordenadas negativas en la clase.
        '''
        if isinstance(Negativos, bool) or isinstance(Negativos, str) or isinstance(Negativos, int):
            # Se comprueba el tipo de dato introducido y se intenta convertir a bool.
            try:
                self.__neg = bool(Negativos)
            except Exception as e:
                raise Exception(e)
            
        if self.__neg == False:
            # En el caso de que no se puedan introducir números negativos y la clase contenga algún valor
            # en las coordenadas X e Y, si estas son negativas saltara una excepción.
            if self.__X != None and self.__X < 0:
                raise Exception("La coordenada X de la clase es negativa.")
            if self.__Y != None and self.__Y < 0:
                raise Exception("La coordenada Y de la clase es negativa.")
            
            
    def getX(self):
        '''!
        \brief Método que devuelve el valor de la coordenada X almacenada.
        \return float: Valor de la coordenada X.\n X coordinate value.
        '''
        return self.__X
    
    def getY(self):
        '''!
        \brief Método que devuelve el valor de la coordenada Y almacenada.
        \return float: Valor de la coordenada Y.\n Y coordinate value.
        '''
        return self.__Y
    
    def getNegativos(self):
        '''!
        @brief Método que devuelve el valor actual de la propiedad negativos.
        @return bool: Estado de la propiedad Negativos.\n Negative property status.
        '''
        return self.__neg
    
    def getTolerance(self):
        '''!
        @brief Método que devuelve la tolerancia del punto.
        @return float: Valor de la tolerancia.
        '''
        return self.__tolerance
    
    def toString(self):
        '''!
        \brief Método que devuleve toda la información del punto en formato str.
        \return str: Un string con toda la información del punto.\n A string with point information.
        '''
        return "X:" + str(self.__X) + "\n"\
            "Y:" + str(self.__Y) + "\n"\
            "Negativos:" + str(self.__neg) + "\n"
            
    def toJSON(self):
        '''!
        \brief Método que devuleve toda la información del punto en formato JSON.
        \return str: Un string en formato JSON.\n A string in JSON format.
        '''
        return "{\n" + \
            '"X":' + '"' + str(self.__X) + '"' + ",\n"\
            '"Y":' + '"' + str(self.__Y) + '"' + ",\n"\
            '"Negativos":' + '"' + str(self.__neg) + '"' + "\n"\
            + "}"
            
    def toGeoJSON(self):
        '''!
        \brief Método que devuleve un GeoJSON del punto.
        \return str: Un string en formato GeoJSON.\n A string in GeoJSON format.
        '''
        
        return "{\n" + \
            '"type":"Point"' + ",\n"\
            '"coordinates":' + \
            '[' + str(self.__X) + ',' + str(self.__Y) + ']' + "\n"\
            "}"
            
    def toWKT(self):
        '''!
        @brief Método que devuleve un wkt del punto.
        \return str: Un string en formato wkt.
        \return str: wkt in string format.
        '''
        #Incluir la tolerancia M.
        if self.__tolerance!=None:
            return 'POINT M (' + str(self.__X) + ' ' + str(self.__Y) + ' ' + str(self.__tolerance) + ')'
        else:
            return 'POINT (' + str(self.__X) + ' ' + str(self.__Y) + ')'
                
def main():
    from json import loads
    p1 = Punto2D(-10, 20, NEGATIVOS=True)
#     print(p1.toString())
#     print(p1.toJSON())
#     print(json.loads(p1.toJSON())['X'])
    print(p1.toGeoJSON())
    print(loads(p1.toGeoJSON())['coordinates'])
    print(p1.toWKT())
    
    p1.setFromWKT('POINT (50 50)')
    print(p1.toWKT())
    
    p1.setFromWKT('POINT M (50 50 0.001)')
    print(p1.toWKT())
    
    geojson = '{"type":"Point","coordinates":[-10.0,20.0]}'
    p1.setFromGeoJSON(geojson)
    p1.setTolerance(None)
    print(p1.toWKT())
#     p1.setNegativos(False)
    
if __name__ == "__main__":
    main()
        
