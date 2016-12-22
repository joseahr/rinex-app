#!/usr/bin/python
# -*- coding: utf-8 -*-


from ObsParser import *
from NavParser import *
from Utils import Utils
from math import sqrt, sin, atan2, cos, pi, atan,acos, tan
from Geometrias.Punto3D import Punto3D
from Proyecciones.Cargeo2Geo import Cargeo2Geo
from numpy import exp, matrix, linalg, diag, shape, dot
import cli.app
import os

class Solver(object) :

    def __init__(self, navParser, obsParser) :
        if not isinstance(navParser, NavigationParser) : raise Exception('navParser debe ser del tipo NavigationParser')
        if not isinstance(obsParser, ObservationParser) : raise Exception('obsParser debe ser del tipo ObservationParser')

        self.navigation = navParser
        self.observation = obsParser

        self.epocas = []
        self.resultados = []

        ## Velocidad de la luz
        self.C = 2.99792458e8
        ## Constante Gravitatoria * Masa de la tierra
        self.GM = 3.986005e14

        self.__calcSatelitesPosition()
        self.__calcReceptorPositions()

    def getB(self, h):
        datos = [[0.0, 1.156], [500.0, 1.079], [1000.0, 1.006], [1500.0, 0.938], [2000.0, 0.874], [2500.0, 0.813], [3000.0, 0.757], [4000.0, 0.654], [5000.0, 0.563]]
        b = 0
        try :
            for indx, el in enumerate(datos):
                d0 = el
                d1 = datos[indx + 1]
                if h >= d0[0] and h <= d1[0] :
                    distancia = d1[0] - d0[0]
                    distancia2 = h - d0[0]
                    dif= d1[1] - d0[1]
                    b = d0[1] + (distancia2*dif/distancia)
                    return b
        except IndexError as e:
            return b

    def __calcSatelitesPosition(self):
        for obs in self.observation.getObservations():
            ## De la observación de una época
            ## Para cada satélite
            if obs['OK_FLAG'] != 0: continue
            ## Tobservación
            tobs = obs['EPOCA']
            epocObj = {'EPOCA': tobs, 'OBSERVACIONES' : {} }
            for sat in obs['OBSERVACIONES'].keys():
                ## Si el satélite es GPS
                if 'G' in sat :
                    ## Cogemos los observables del satélite
                    observation = obs['OBSERVACIONES'][sat]
                    ## Efeméride más próxima a nuestra época
                    efem = self.navigation.getParams(tobs, sat)

                    ## Si no hay observable P2 no seguimos
                    ## IMPORTANTE!! Si no hay P2 no podemos
                    ## calcular NADA!!
                    if not efem or not 'P2' in observation: continue

                    ## TOE
                    toe = efem['toe']
                    ## Parámetros para el cálculo de la falta de sincronización de los relojes
                    a0, a1, a2 = [ efem['sv_clock_bias'], efem['sv_clock_drift'], efem['sv_clock_drift_rate'] ]
                    ## Semieje mayor de la órbita
                    a = efem['sqrt_a']**2
                    ## Diferencia del movimiento medio respecto al valor calculado
                    delta_n = efem['delta_n']
                    ## Mo = Anomalía media en el tiempo de referencia
                    Mo = efem['mo']
                    ## Excentricidad de la órbita del satélite
                    e = efem['eccentricity']
                    ## Argumento del perigeo
                    w = efem['omega']
                    ## Parámetros para correcciones orbitales Cus, Crs, Cis
                    cus, crs, cis = [ efem['cus'], efem['crs'], efem['cis'] ]
                    cuc, crc, cic = [ efem['cuc'], efem['crc'], efem['cic'] ]
                    ## Inclinación de la órbita en el momento de referencia
                    io = efem['io']
                    ## Variación del ángulo de inclinación de la órbita
                    idot = efem['idot']
                    ## Longitud del nodo ascendente de la órbita
                    ## en la época de la semana de referencia
                    omega_0 = efem['OMEGA']
                    ## Variación de la ascensión recta
                    omega_var = efem['omega_dot']
                    ## Valor de la rotación terrestre
                    omega_e = 7.2921151467e-5

                    ## Cálculo del tiempo de emisión
                    temis = Utils.UTC2GPS(tobs) - (observation['P2']['VALUE']/self.C) - toe

                    tcorr = a0 + a1*temis + a2*temis**2

                    temis = Utils.UTC2GPS(tobs) - (observation['P2']['VALUE']/self.C) - tcorr - toe

                    tcorr = a0 + a1*temis + a2*temis**2
                    temis = Utils.UTC2GPS(tobs) - (observation['P2']['VALUE']/self.C) - tcorr - toe


                    ## Movimiento medio
                    n = sqrt( self.GM / (a**3) ) + delta_n
                    ## M = Anomalía media
                    M = Mo + (n * temis)
                    ## E = Anomalía excéntrica
                    E = Eant = M
                    Eant = 0 ## Variable auxiliar para el proceso iterativo
                    while(abs(E - Eant) > 0.0000000001):
                        Eant = E
                        E = M + ( e * sin(Eant) )

                    ## Anomalía verdadera
                    v = atan2( (sqrt(1 - (e**2) )*sin(E)), (cos(E) - e) )
                    ## Argumento de la latitud
                    arg_lat = v + w

                    ## Términos correctivos de los parámetros orbitales
                    du = cus * sin(2 * arg_lat) + cuc * cos(2 * arg_lat)
                    dr = crs * sin(2 * arg_lat) + crc * cos(2 * arg_lat)
                    di = cis * sin(2 * arg_lat) + cic * cos(2 * arg_lat)

                    ## Argumento de la latitud corregido
                    arg_lat += du
                    ## Radio de la órbita corregido
                    r = a * (1 - e * cos(E)) + dr
                    ## Inclinación de la órbita corregida
                    i = io + di + idot * temis

                    ## Posición del satélite en el plano orbital
                    Xop = r * cos(arg_lat)
                    Yop = r * sin(arg_lat)

                    ## Longitud corregida del nodo ascendente
                    omega = omega_0 + ( (omega_var - omega_e) * temis ) - ( omega_e * toe )

                    ## Coordenadas finales del satélite
                    Xsat = Xop * cos(omega) - Yop * cos(i)*sin(omega)
                    Ysat = Xop * sin(omega) + Yop * cos(i)*cos(omega)
                    Zsat = Yop * sin(i)

                    ## Efecto relativista debido a la elipticidad de la órbita del satélite
                    trel = -2 * sqrt( self.GM * a ) / (self.C ** 2) * e * sin(E)

                    ## TGD (Total Group Delay) o constante instrumental del satélite
                    ttgd_l1 = efem['tgd']
                    ttgd_l2 = 1.65 * ttgd_l1

                    ## Finalmente el tiempo corregido será :
                    tcorr += trel - ttgd_l2
                    ## Generamos un diccionario con los datos necesarios de la observación
                    epocObj['OBSERVACIONES'].update({sat : {
                          'ECEF' : [Xsat, Ysat, Zsat]
                        , 'TCORR': tcorr
                        ##, 'EPOCA': tobs
                        ##, 'SAT'  : sat
                        , 'OBSERVACION' : obs['OBSERVACIONES'][sat]
                    }})
                    '''
                    printSats = ['G02', 'G04', 'G23']
                    if sat in printSats and Utils.UTC2GPS(obs['EPOCA']) == 135110 :
                        print ('sat', sat)
                        print ('obs epoca gps_secs', Utils.UTC2GPS(obs['EPOCA']))
                        print ('epoca nav', efem['epoca'])
                        print ('epoca obs', obs['EPOCA'])
                        print ('tnav - tobs', efem['epoca'] - tobs)
                        print ('toe', toe)
                        print ('Temis', temis)
                        print ('TcorrF', tcorr)
                        print ('Mov. medio', n)
                        print ('Anomalía media', M)
                        print ('du', du)
                        print ('dr', dr)
                        print ('di', di)
                        print ('u', arg_lat)
                        print ('r', r)
                        print ('i', i)
                        print ('Xop, Yop', Xop, Yop)
                        print ('omega', omega)
                        print ('Anomalía Excentr.', E)
                        print ('Anomalía verdadera', v)
                        print ('PosSat', Xsat, Ysat, Zsat)
                        print ('trel', trel)
                        print ('tcorr', tcorr)
                        print ('\n')
                    '''
            ## Lo añadimos a la lista de épocas
            self.epocas.append(epocObj)

    def __calcReceptorPositions(self):
        w = 7.2921151467e-5
        ## Coordenadas aproximadas del observador
        apx_pos = self.observation.getHeader()['APX_COORDS']
        ## Recorremos las épocas
        Xest, Yest, Zest = apx_pos
        corr_reloj = 0
        for epoc in self.epocas :
            ## Coordenadas aproximadas del observador que se actualizarán
            ## Hora de la observación
            tobs = epoc['EPOCA']
            #print(tobs, sat)
            ## Hora de la observación en segundos GPS
            tsec_week = Utils.UTC2GPS(tobs)

            A = []
            K = []
            P = []

            cont = 0
            corr_reloj_ant = 1            
            #for i in range(0, 6):
            while(abs(corr_reloj_ant - corr_reloj)> 1e-07):
                ##print(tobs, corr_reloj_ant, corr_reloj, corr_reloj_ant - corr_reloj, Xest, Yest, Zest)
                cont += 1
                ##print(cont)
                ##if cont > 10 : break
                corr_reloj_ant = corr_reloj
                ## Recorremos las observaciones a cada satélite
                for sat in epoc['OBSERVACIONES'].keys():
                    ## Coordenadas ECEF del satélite
                    Xsat, Ysat, Zsat = epoc['OBSERVACIONES'][sat]['ECEF']
                    ## TravelTime
                    traveltime = sqrt( (Xsat - Xest)**2 + (Ysat - Yest)**2 + (Zsat - Zest)**2 ) / self.C
                    ## OmegaTau
                    wt = w * traveltime
                    ##Coordenadas del satélite rotadas
                    Xsat, Ysat, Zsat = [ cos(wt)*Xsat + sin(wt) * Ysat, - sin(wt) * Xsat + cos(wt) * Ysat, Zsat ]
                    ## Incremento de coordenadas ECEF
                    incX, incY, incZ = [ Xsat - Xest, Ysat - Yest, Zsat - Zest ]
                    #print(incX, incY, incZ)
                    ## Coordenadas de la estación en lat, lon, h (Elipsoide WGS 84)
                    pgeo = Cargeo2Geo(Punto3D(*apx_pos), 'WGS 84')
                    lon_est = pgeo.getLongitud()
                    lat_est = pgeo.getLatitud()
                    h_est   = pgeo.getAlturaElipsoidal()
                    ## Incrementos de coordenadas en el Sistema Geodésico Local
                    eij, nij, uij = Utils.XYZ2ENU(lon_est*pi/180, lat_est*pi/180, incX, incY, incZ)
                    azi, ele, dist = Utils.ENU2CLA(eij, nij, uij)

                    ## Si la elvación es menor que 10º descartamos la observación
                    #if ele < 10 : continue

                    ## Cálculo de la presión
                    pres = 1013.25 * ((1 - 0.000065*h_est)**5.225)
                    ## Cálculo de la temperatura
                    temp = 291.15 - (0.0065*h_est)
                    ## Humedad en la que se aproxima la altura Hortométrica 
                    ## por la altura elipsoidal
                    H    = 50*exp(-0.0006396*h_est)
                    ## Vapor de agua
                    e_wp = (H*0.01)*exp(-37.2465 + 0.213166*temp - (0.000256908*temp*temp) )
                    b    = self.getB(h_est)

                    dtropo = (0.002277 / cos( (pi/2) - ele))*(pres + ((1255/temp) + 0.05)*e_wp - (b*(tan( (pi/2) - ele)**2)) )

                    e_semicirculos = (ele*180/pi)/180

                    psi = (0.0137/(e_semicirculos + 0.11)) - 0.022

                    lat_semicirculos =  lat_est/180
                    lat_i = (lat_semicirculos + (psi * cos(azi)))
                    if lat_i > 0.416 : lat_i = 0.416
                    if lat_i < -0.416: lat_i = -0.416
                    
                    lon_semicirculos = lon_est/180
                    lon_i = lon_semicirculos + ( (psi * sin(azi))/cos(lat_i*pi) )

                    lat_geomagnetica = lat_i + (0.064 * cos( (lon_i - 1.617) * pi ))
                
                    tiempo_local = (43200 * lon_i) + tsec_week
                    if tiempo_local >= 86400 : tiempo_local -= 86400
                    elif tiempo_local < 0 : tiempo_local += 86400

                    ## Cálculo de la amplitud del retraso ionosférico
                    ion_alpha = self.navigation.getHeader()['ION_ALPHA']
                    ion_beta = self.navigation.getHeader()['ION_BETA']
                    Ai = 0
                    Pi = 0
                    for i in range(0, 4):
                        Ai += ion_alpha[i]*(lat_geomagnetica**i)
                        Pi += ion_beta[i]*(lat_geomagnetica**i)

                    if Ai < 0 : Ai = 0
                    if Pi < 72000 : Pi = 72000

                    ## Cálculo de la fase del retraso ionosférico
                    Xi = (2*pi*(tiempo_local - 50400)/Pi)

                    ## Cálculo del factor de inclinación
                    F = 1.0 + (16.0*(0.53 - e_semicirculos)**3)

                    ## Cálculo del retraso ionosférico (en segundos)
                    if Xi <= 1.57 :
                        Il1 = (5e-9 + (Ai*( 1 - ((Xi**2)/2) + ((Xi**4)/24) )))*F
                    else :
                        Il1 = 5e-9*F

                    ## Transformación a metros del retraso ionosférico
                    Il1m = Il1 * self.C

                    ## Cálculo del retraso ionosférico para la frecuencia L2 (en metros)
                    Il2 = 1.65 * Il1m

                    dist = sqrt( (Xsat-Xest)**2 + (Ysat-Yest)**2 + (Zsat-Zest)**2 )
                    p2   = epoc['OBSERVACIONES'][sat]['OBSERVACION']['P2']['VALUE']
                    tcorr= epoc['OBSERVACIONES'][sat]['TCORR']
                    A.append([-(Xsat-Xest)/dist, -(Ysat-Yest)/dist, -(Zsat-Zest)/dist, 1])
                    K.append([p2 - dist - corr_reloj + (self.C*tcorr) - dtropo - Il2])
                    P.append((sin(ele)**2)/((1.5*0.3)**2))
                    '''
                    if sat == 'G04' and cont < 2:
                        print (traveltime)
                        print (wt)
                        print (Xsat, Ysat, Zsat)
                        print (azi*180/pi, ele*180/pi)
                        print (lon_est*pi/180, lat_est*pi/180)
                        print(eij, nij, uij)
                        print('helip', h_est)
                        print('pres', pres, 'temp', temp, 'H', H, 'e_wp', e_wp, 'e_semicirculos', e_semicirculos, 'b', b, 'dtropo', dtropo, 'psi', psi)
                        print('lon_i', lon_i, 'lat_i', lat_i)
                        print('lat_geomag', lat_geomagnetica)
                        print('tsec', tsec_week)
                        print('tiempo_local', tiempo_local)
                        print('Ai', Ai, 'Pi', Pi, 'Il1', Il1m, 'Il2', Il2)
                        print('-----------------')
                '''
                matrizA = matrix(A)
                matrizK = matrix(K)
                matrizP = matrix(diag(P))

                ## Calculamos la solución
                matrizX = [dx, dy, dz, corr_reloj] = linalg.inv(matrizA.transpose() * matrizP * matrizA) * (matrizA.transpose() * matrizP * matrizK)
                Xest += dx[0, 0]
                Yest += dy[0, 0]
                Zest += dz[0, 0]
                corr_reloj = corr_reloj[0, 0]/self.C
            
            pgeo_ = Cargeo2Geo(Punto3D(Xest, Yest, Zest), 'WGS 84')
            matrizR = dot( matrizA, matrizX ) - matrizK
            gdl = shape(matrizA)
            est_ = float(sqrt( dot(dot( matrizR.transpose(), matrizP), matrizR ) ) / (gdl[0] - gdl[1]))
            #print(est_, matrizA, matrizR, 'P', matrizP)
            Qxx = dot(linalg.inv( dot( dot( matrizA.transpose(), matrizP ), matrizA ) ), est_)
            dx = sqrt(Qxx[0,0])
            dy = sqrt(Qxx[1,1])
            dz = sqrt(Qxx[2,2])
            dt = sqrt(Qxx[3,3])
            #print(dx, dy, dz, dt)
            ##print(Qxx)
            self.resultados.append({
                  'tobs' : str(tobs)
                , 'lon'  : pgeo_.getLongitud()
                , 'lat'  : pgeo_.getLatitud()
                , 'err'  : [dx, dy, dx, dt]
                , 'est'  : est_
            })
            ##print(tobs, Qxx, Xest, Yest, Zest, pgeo_.getLongitud(), pgeo_.getLatitud(), pgeo_.getAlturaElipsoidal(), 'num_sats', len(epoc['OBSERVACIONES'].keys()))
        ##print('Fin')


@cli.app.CommandLineApp
def ResolvePosition(app):
    import time
    try : 
        t = time.time()
        ##print(app.params.fobs)
        ##print(app.params.fnav)
        navParser = NavigationParser(app.params.fnav)
        obsParser = ObservationParser(app.params.fobs)
        print('Lo que tarda en hacer los archivos:', time.time() - t)
        t = time.time()
        solver = Solver(navParser, obsParser)
        resultados = solver.resultados
        print('Tiempo que tarda en Resolver Posición satélite y Receptor', time.time() - t)
        t = time.time()
        ##print(resultados)
        fichPath = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(fichPath, 'results', 'solucion.json'), 'wt') as sol:
            sol.write(str(resultados))
        print('Timepo que tarda en hacer el archivo JSON', time.time() - t)
    except Exception as e:
        print(e)
ResolvePosition.add_param("fobs", help="Fichero de observación", default=1, type=str)
ResolvePosition.add_param("fnav", help="Fichero de navegación", default=1, type=str)

if __name__ == '__main__':
    ResolvePosition.run()
'''
## Función principal para probar la clase
def main():
    ## Creamos un objeto de la clase
    navParser = NavigationParser('sampledata/brdc0590-1.11n')
    obsParser = ObservationParser('sampledata/89090590-1.11o')
    solver = Solver(navParser, obsParser)
    ##print (solver.epocas)
    pass

## Si estamos ejecutando directamente
## este fichero la variable __name__ contendrá el valor "__main__"
if __name__=="__main__":
    ## Ejecutamos la función main
    main()
'''