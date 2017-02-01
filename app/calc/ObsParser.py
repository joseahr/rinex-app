#!/usr/bin/python
# -*- coding: utf8 -*-

import os
import re
import datetime as dt
import itertools

'''
@@ Clase ObservationParser
@@ ^^^^^^^^^^^^^^^^^^^^^^^
@@ Recibe el path hacia un archivo RINEX de Observación
@@ Válido para la versión 2.11
'''
class ObservationParser(object):

    def __init__(self, path):
        '''
        @@ Constructor de la clase ObservationParser
        @path : Path al archivo de observación
        '''
        ## Comprobamos que el fichero existe
        if not isinstance(path, str) : raise Exception('Path debe ser de tipo str')
        if not os.path.isfile(path)  : raise Exception('La ruta hacia el fichero introducida no es válida')
        ## Comprobamos que la extensión es .XXo .XXO
        if not re.match(r".\d{2,}[oO]", os.path.splitext(path)[1]) : raise Exception('La extensión del fichero no es la de un archivo RINEX de observación')

        ## @header:
        ## Cabecera del fichero RINEX de Observación
        self.header = {}

        ## @observations :
        ## Observaciones encontradas en el fichero
        ## cada época se introduce como un diccionario
        ## dentro de esta lista
        self.observations = []

        ## @REGEX_VALUE : Extrae de un string
        ## cadenas de números como +-XXXX.YYYY
        self.REGEX_FLOATS = r"[-+]?\d*\.\d+|\d+"

        ## @REGEX_OBS_TYPES : Extrae de un string
        ## caracteres del tipo : L1 L2 P1 P2 L3
        self.REGEX_OBS_TYPES = r"[CPL]+[1-3]"

        ## @REGEX_SATS : Extrae de un string
        ## caracteres del tipo G02 G17 R02
        self.REGEX_SATS = r"[RG]+\d+"

        ## @REGEX_PARSE_LINEA_INICIO_EPOCA : Extrae de un string
        ## como 11  2 28 13 31 50.0000000  0 16G02G04G07G08G10G13G17G20G23R01R02R11
        ## Extraería |11|  |2| |28| |13| |31| |50.0000000|  |0| |16|
        ## y excluiría G02G04G07G08G10G13G17G20G23R01R02R11
        self.REGEX_PARSE_LINEA_INICIO_EPOCA = r"[-+]?\d*\.\d+|(?<![RG0-9])\d+"

        ## @REGEX_PARSE_LINEA_INICIO_OBS : Extrae de un string
        ## como   22527689.086 7                   -578290.975 7   -410051.96348  22527682.94948
        ## Extraería |22527689.086| |7|                   |-578290.975| |7|   |-410051.963|4|8|  |22527682.949|4|8|
        ## Los huecos de mayor tamaño son observaciones vacías
        self.REGEX_PARSE_LINEA_OBS = r"([-+ \d]{9}[. ][ \d]{3})([\d ])([\d ])"

        ## @MAX_OBSERVABLES_PER_LINE :
        ## Número máximo de observables que caben en una línea
        ## del fichero RINEX 2.11
        self.MAX_OBSERVABLES_PER_LINE = 5

        ## @MAX_SATS_PER_LINE :
        ## Número máximo de satélite que caben en una
        ## línea de inicio de época del fichero RINEX 2.11
        self.MAX_SATS_PER_LINE = 12

        ## llamamos al método parse para que
        ## parsee el archivo y obtener el resultado
        ## en las variables de clase header y observations
        self.__parse(path)

    '''
    @@ getHeader()
    @@ Devuelve la cabecera parseada
    @@ del fichero RINEX
    '''
    def getHeader(self):
        return self.header

    '''
    @@ getObservations()
    @@ Devuelve las observaciones
    @@ del fichero RINEX
    '''
    def getObservations(self):
        return self.observations

    '''
    @@ getObservation(época, [satelite, [observación)
    @@ Dada una época com mínimo edvuelve todas las observaciones
    @@ @@ date : Eṕoca de la observación datetime.datetime(y, m, d, hh, mm, ss)
    @@ @@ sat  : (Opcional) -> Nombre del satélite
    @@ @@ obs  : (Opcional) -> Tipo de Observable
    '''
    def getObservation(self, date, sat='', obs='') :
        ## date debe ser de tipo datime.datetime
        if not isinstance(date, dt.datetime) : raise Exception('date debe ser de tipo datime.datetime')
        if not isinstance(sat, str) : raise Exception('Sat debe ser de tipo str')
        if not isinstance(obs, str) : raise Exception('Obs debe ser de tipo str')

        try :
            ## Si no se ha pasado sat como parámetro
            if not sat :
                return [x for x in self.observations if x['EPOCA'] == date ][0]['OBSERVACIONES']

            ## Si no se ha pasado obs como parámetro
            if not obs :
                return [x for x in self.observations if x['EPOCA'] == date ][0]['OBSERVACIONES'][sat]

            ## Se han pasado sat y obs como parámetro
            return [x for x in self.observations if x['EPOCA'] == date ][0]['OBSERVACIONES'][sat][obs]
        except :
            return

    '''
    @@ __parse()
    @@ función privada
    @@ parsea el fichero RINEX, primero la cabecera
    @@ luego las observaciones
    '''
    def __parse(self, file):

        ## Abrimos el fichero
        with open(file) as o :
            ## Guardamos todas las lineas del fichero en
            ## el array @obs
            obs = o.readlines()

        ## Recorremos las líneas del fichero
        for index, line in enumerate(obs) :

            ## Guardamos la versión del fichero RINEX
            if 'RINEX VERSION' in line:
                ## Regex ->> X.YY
                version = re.findall(r"\d{1}.\d{2}", line)[0]
                ## Lanzamos un error si no es la versión 2.11
                if not version == '2.11' : raise Exception('Este parser solo es válido para la versión 2.11')
                ## Añadimos la clave valor al diccionario header
                self.header.update({ 'RINEX_VERSION' : version })
                ## no sigas comprobando los demás ifs para esta iteración
                continue

            ## Guardamos la posición aproximada
            if 'APPROX POSITION XYZ' in line :
                ## Coordenadas Aproximadas
                coords = re.findall(self.REGEX_FLOATS, line)
                ## Las pasamos a float
                Xapx, Yapx, Zapx = map(float, coords)
                ## Añadimos la clave valor al diccionario header
                self.header.update({ 'APX_COORDS' : [Xapx, Yapx, Zapx] })
                ## no sigas comprobando los demás ifs para esta iteración
                continue

            ## Guardamos los offsets de la antena
            if 'ANTENNA: DELTA H/E/N' in line :
                antena_deltas = re.findall(self.REGEX_FLOATS, line)
                ## Pasamos a float los valores
                h, e, n = map(float, antena_deltas)
                ## Añadimos la clave valor al diccionario header
                self.header.update({ 'ANTENA_DELTA' : [h, e, n] })
                ## no sigas comprobando los demás ifs para esta iteración
                continue

            ## Guardamos los tipos de observables
            if '# / TYPES OF OBSERV' in line :
                # Tipos de observables
                types_obs = re.findall(self.REGEX_OBS_TYPES, line)
                ## Añadimos la clave valor al diccionario header
                self.header.update({ 'OBSERV_TYPES' : types_obs })
                ## no sigas comprobando los demás ifs para esta iteración
                continue

            ## Guardamos la fecha de la primera observación
            if 'TIME OF FIRST OBS' in line :
                # Fecha de la primera observación
                date = re.findall(self.REGEX_FLOATS, line)
                # Pasamos a float luego a int
                dateList = map(int, map(float, date))
                # creamos un objeto datetime
                date = dt.datetime(*dateList)
                ## Añadimos la clave valor al diccionario header
                self.header.update({ 'FIRST_OBS_TIME' : date })
                ## no sigas comprobando los demás ifs para esta iteración
                continue

            ## LLegamos al final de la cabecera
            if 'END OF HEADER' in line :

                ## Definimos una función que entrará en bucle hasta
                ## que llegue al final del archivo
                ## @ Recibe un índice, el cual debe coincidir con una línea de inicio de época
                def parseObs(idx = index + 1):

                    ## Array temporal, coge los valores
                    ## desde idx hasta el final de la lista
                    obsArray = obs[idx:]

                    ## Obtenemos la fecha de la época de observación y, m, d, hh, mm, ss
                    ## El OK_FLAG y el número de satélites observados
                    y, m, d, hh, mm, ss, ok_flag, num_sats = map( int, map( float, re.findall(self.REGEX_PARSE_LINEA_INICIO_EPOCA, obsArray[0]) ) )

                    ## El año lo cogermos de la cabecera ya que en la época aparece 11 en vez de 2011
                    y += 2000

                    ## Creamos un objeto datetime
                    date = dt.datetime( y, m, d, hh, mm, ss )

                    ## Satélites de la observación
                    sats = re.findall(self.REGEX_SATS, obsArray[0])

                    ## Índice por el que debe empezar el loop de sobre obsArray
                    start = 1

                    ## Si el número de satélites es mayor que el número
                    ## máximo de satélites por línea
                    if num_sats > self.MAX_SATS_PER_LINE :
                        ## El índice para empezar será dos
                        start = 2
                        ## Los satélites están en dos líneas
                        sats = re.findall(self.REGEX_SATS, ''.join(obsArray[:2]) )

                    ## Obeto que almacenará las observaciones para esta época
                    obsObj = { 'EPOCA' : date, 'SATELITES_OBSERVADOS' : sats, 'OBSERVACIONES' : {}, 'OK_FLAG' : ok_flag, 'NUM_SATS' : num_sats }

                    ## step indica cada cuantas files la observación pertenece
                    ## a otro satélite
                    step = 1

                    ## end será la posición en la que debemos dejar de
                    ## recorrer obsArray ya que cambiará la época
                    ## Lo calculamos como número de satélites + la posición de inicio
                    end = start + num_sats

                    ## Si el número de observables es mayor a 5
                    ## habrá que buscarlo en dos líneas
                    if (len(self.header['OBSERV_TYPES']) > 5) :
                        ## end será entonces (inicio + (número de satélites * 2) )
                        end = start + (num_sats * 2)
                        ## step será por tanto 2
                        step = 2

                    ## Recorremos según el start, end y step el obsArray
                    for obsindex in range(start, end, step):
                        ## Función que dado un string le quita los espacios
                        def strip_(el): return el.strip()

                        ##Obtenemos la observación
                        the_obs = re.findall(self.REGEX_PARSE_LINEA_OBS, ''.join(obsArray[obsindex : obsindex + step]) )
                        
                        ## quitamos los espacios de la lista
                        ## El regex devuelve un array de tuplas
                        ## con chain.from_iterable() las tuplas desaparecen
                        ## y pasan dentro de la lista como strings
                        the_obs = list(map(strip_, list(itertools.chain.from_iterable(the_obs))))

                        ## El regex nos puede dejar huecos al final si no hay observaciones
                        ## con esto rellenamos los huecos
                        if(len(the_obs) < len(self.header['OBSERV_TYPES'] * 3)) :
                            ## Cuantos huecos faltan por rellenar ?
                            size = (len(self.header['OBSERV_TYPES'] * 3)) - len(the_obs)
                            ## rellenamos los huecos DEL FINAL!!!
                            the_obs[len(the_obs):] = ['' for x in range(size)]

                        ## Nombre del satélite
                        sat = sats[ int( (obsindex - start) / step) ]
                        #print (sat, obsindex, start, step)
                        #print sat

                        ## Creamos un objeto dentro del objeto observaciones
                        ## para cada satélite
                        obsObj['OBSERVACIONES'][sat] = {}

                        ## Recorremos los observables
                        for ii, observable in enumerate(self.header['OBSERV_TYPES']):
                            try :
                                ## Intentamos convertir a float el valor del observable
                                value = float(the_obs[ii * 3])
                                ## Creamos dentro de ['OBSERVACIONES'][sat]
                                ## un objeto para cada observable
                                obsObj['OBSERVACIONES'][sat][observable] = {}
                                ## Introducimos el valor del observable
                                obsObj['OBSERVACIONES'][sat][observable]['VALUE'] = value

                                try :
                                    ## Intentamos convertir a float el valor del LLI
                                    obsObj['OBSERVACIONES'][sat][observable]['LLI'] = float(the_obs[(ii * 3) + 1])
                                except :
                                    ## Si no se puede no tiene valor
                                    obsObj['OBSERVACIONES'][sat][observable]['LLI'] = None
                                ## Añadimos el SSI (Siempre va a aparecer)
                                obsObj['OBSERVACIONES'][sat][observable]['SSI'] = float(the_obs[(ii * 3) + 2])
                            except ValueError as e :
                                ## El valor del observable no existe
                                ## Pasamos a la siguiente iter
                                continue
                    ## Añadimos la época de observación
                    ## a la lista de observaciones
                    self.observations.append(obsObj)

                    try :
                        ## Llamamos a la función parseObs
                        ## con el nuevo índice
                        parseObs(idx + end)
                    except IndexError as e:
                        ## Si recibimos un IndexError
                        ## hemos llegado al final del archivo
                        ##print (e)
                        #print 'Final de archivo'
                        '''
                        with open('resultados', 'w') as file:
                            file.write(str(self.getObservations()))
                        '''
                        pass
                ## Empezamos el bucle llamando a parseObs
                parseObs()
                ## Salimos del bucle principal
                return
## Función principal para probar la clase
def main():
    ## Creamos un objeto de la clase
    obsParser = ObservationParser('89090590-1.11o')
    ## Imprimimos la cabecera
    print (obsParser.getHeader())
    ## Imprimimos para la época tal, las obaservaciones del satélite G02
    print (obsParser.getObservation(dt.datetime(2011, 2, 28, 13, 45, 35), 'G02'))
    ## Imprimimos para la época tal, el observable P2 del satélite G02
    print (obsParser.getObservation(dt.datetime(2011, 2, 28, 13, 45, 35)))
    ## No existe
    ##rr = obsParser.getObservation(dt.datetime(2015, 2, 28, 13, 45, 35), 'G02', 'P2') or 'a'
    ##print rr

## Si estamos ejecutando directamente
## este fichero la variable __name__ contendrá el valor "__main__"
if __name__=="__main__":
    ## Ejecutamos la función main
	main()