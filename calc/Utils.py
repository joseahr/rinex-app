#!/usr/bin/python
# -*- coding: utf-8 -*-

from math import pi, sin, cos, sqrt, atan2
from numpy import matrix
class Utils(object):
    @staticmethod
    def UTC2GPS(fecha):
        '''
        @UTC2GPS: Método estático para convertir un objeto de la clase datetime a tiempo GPS
        @fecha datetime: Objeto de la clase datetime con la fecha a transformar en tiempo GPS.
        '''
        ## Obtenemos el número del día
        ## En python el día 0 es el lunes
        day = fecha.weekday()
        ## Si el día es Domingo (número 6) -> día = -1
        if day == 6 : day = -1
        ## Calculamos el tiempo GPS
        return ( (day + 1) * 86400 ) + int(fecha.strftime('%H')) * 3600 + int(fecha.strftime('%M')) * 60 + int(fecha.strftime('%S'))
    
    @staticmethod
    def XYZ2ENU(lon, lat, Xij, Yij, Zij):
        '''
        #XYZ2ENU: Método estático para convertir incrementos de coordenadas geocéntricas en 
        # incrementos de coordenadas en el sistema geodésico local
        @lon, lat: Coordenadas geodésicas del punto estación
        @Xij, Yij, Zij: Incrementos de coordenadas geocéntricas
        '''
        ## Definimos matriz de rotación
        A = matrix([
            [ -sin(lon), cos(lon), 0 ],
            [ -sin(lat)*cos(lon), -sin(lat)*sin(lon), cos(lat) ],
            [ cos(lat)*cos(lon), cos(lat)*sin(lon), sin(lat) ]
        ])
        ## Definimos el vector de términos
        X = matrix([Xij, Yij, Zij]).transpose()
        ## Obtenemos los incrementos en el sistema geodésico local
        sol = (A * X).transpose()
        ## Devolvemos el resultado en una lista
        return [sol[0, 0], sol[0, 1], sol[0, 2]]

    @staticmethod
    def ENU2CLA(eij, nij, uij):
        '''
        #XYZ2ENU: Devuelve acimut, elevación y distancia 2d
        # a partir de incrementos de coordenadas en el sistema 
        @# geodésico local
        @eij, nij, uij : incrementos de coordenadas en el sistema geodésico local
        '''
        ## Calculamos el acimut
        acimut = (2*pi) + ( (pi/2) - atan2(nij, eij))
        ## Comprobamos que está entre 0 y 360
        if acimut > 2*pi : acimut -= 2*pi
        elif acimut < 0 : acimut += 2*pi
        ## Calculamos la distancia 2D
        distancia = sqrt(eij**2 + nij**2)
        ## Calculamos la elevación
        elevacion = atan2(uij, distancia)
        ## Devolvemos acimut, elevación y distancia en una lista
        return [acimut, elevacion, distancia]

##PRUEBAS##
def main():
    from datetime import datetime
    print(Utils.UTC2GPS(datetime(2014,11,2,17,0,0)))
    x1, y1 = [0, 0]
    x2, y2 = [-1, 1]
    ax = x2 - x1
    ay = y2 - y1

    azi = 360 + (90 - atan2(ay, ax)*180/pi)
    if azi > 360 : azi -= 360
    elif azi < 0 : azi += 360
    print(azi)

if __name__=="__main__":
    main()