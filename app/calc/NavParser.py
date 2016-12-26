#!/usr/bin/python
# -*- coding: utf8 -*-

import os
import re
import datetime as dt
import itertools

'''
@@ Clase NavigationParser
@@ ^^^^^^^^^^^^^^^^^^^^^^^
@@ Recibe el path hacia un archivo RINEX de Navegación
'''
class NavigationParser(object):

    def __init__(self, path):
        '''
        @@ Constructor de la clase NavigationParser
        @path : Path al archivo de observación
        '''
        ## Comprobamos que el fichero existe
        if not isinstance(path, str) : raise Exception('Path debe ser de tipo str')
        if not os.path.isfile(path)  : raise Exception('La ruta hacia el fichero introducida no es válida')
        ## Comprobamos que la extensión es .XXn .XXN
        if not re.match(r".\d{2,}[nN]", os.path.splitext(path)[1]) : raise Exception('La extensión del fichero no es la de un archivo RINEX de observación')

        self.header = {}

        self.body = []

        self.REGEX_EXTRACT_FLOAT_E = r"[+-]?\d+\.\d+E[+-]\d+"
        self.REGEX_PARSE_LINEA_NAV = r"[+-]?\d+\.\d+E[+-]\d+|\d+\.\d+|\d+"

        self.__parse(path)

    '''
    @@ getHeader()
    @@ Devuelve la cabecera parseada
    @@ del fichero RINEX de Navegación
    '''
    def getHeader(self):
        return self.header

    '''
    @@ getBody()
    @@ Devuelve el cuerpo parseado
    @@ del fichero RINEX de Navegación
    '''
    def getBody(self):
        return self.body
    
    '''
    @@ getParams(epoca, satelite)
    '''
    def getParams(self, epoca, satelite):
        try :
            if re.match(r"[RG]\d+", satelite):
                satelite = re.sub('G','',satelite)
                satelite = re.sub('R','',satelite)
            satelite = float(satelite)
            res = [ [x, abs(x['epoca'] - epoca) ] for x in self.body if x['sat_prn'] == satelite ]
            res = sorted(res, key = lambda x : x[1])
            return res[0][0] if len(res) else None
        except Exception as e:
            print (e)
            return


    def __parse(self, file):
        ## Abrimos el fichero
        with open(file) as n :
            ## Guardamos todas las lineas del fichero en
            ## el array @obs
            nav = n.readlines()
        ## Recorremos las líneas del fichero
        for index, line in enumerate(nav) :
            if 'ION ALPHA' in line :
                line = re.sub('D', 'E', line)
                ion_alfa = list(map(float, re.findall( self.REGEX_EXTRACT_FLOAT_E, line) ))
                self.header.update({ 'ION_ALPHA' : ion_alfa })
                continue
            if 'ION BETA' in line :
                line = re.sub('D', 'E', line)
                ion_beta = list(map(float, re.findall( self.REGEX_EXTRACT_FLOAT_E, line)))
                self.header.update({ 'ION_BETA' : ion_beta })
                continue
            if 'LEAP SECONDS' in line :
                leap_seconds = int(re.findall(r"\d+", line)[0])
                self.header.update({ 'LEAP_SECONDS' : leap_seconds })
                continue

            ## LLegamos al final de la cabecera
            if 'END OF HEADER' in line :

                def parseNav(idx = index + 1):

                    navArray = nav[idx : idx + 8]
                    keys = [
                        'sat_prn', 'epoca', 'sv_clock_bias', 'sv_clock_drift', 'sv_clock_drift_rate', 'iode', 'crs'\
                        , 'delta_n', 'mo', 'cuc', 'eccentricity', 'cus', 'sqrt_a', 'toe', 'cic', 'OMEGA', 'cis', 'io', 'crc', 'omega', 'omega_dot'\
                        , 'idot', 'l2_codes_channel', 'gps_week', 'l2_p_data_flag', 'sv_accuraccy', 'sv_health', 'tgd', 'iodc', 'transmission_time'\
                        , 'fit_interval'
                    ]

                    values = list(map(float, re.findall(self.REGEX_PARSE_LINEA_NAV, re.sub('D', 'E', ''.join(navArray)) )))[:-2]
                    values[1] += 2000
                    epoca = dt.datetime( *map(int,  values[1:7]) )
                    values[1:7] = [epoca]

                    navObj = dict( zip(keys, values) )
                    self.body.append(navObj)

                    try :
                        ## Llamamos a la función parseObs
                        ## con el nuevo índice
                        parseNav(idx + 8)
                    except IndexError as e :
                        print (idx)
                        ## Hemos llegado al final del archivo
                        pass
                parseNav()
                return

## Función principal para probar la clase
def main():
    ## Creamos un objeto de la clase
    navParser = NavigationParser('brdc0590-1.11n')
    print (navParser.getHeader())
    print (navParser.getBody()[0])
    print (navParser.getParams(dt.datetime(2011,2, 28), 'G01'))


## Si estamos ejecutando directamente
## este fichero la variable __name__ contendrá el valor "__main__"
if __name__=="__main__":
    ## Ejecutamos la función main
	main()