#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 6/2/2015

@author: Antonio Hermosilla Rodrigo.
@contact: anherro285@gmail.com
@organization: Antonio Hermosilla Rodrigo.
@copyright: (C) 2011 by Antonio Hermosilla Rodrigo
@version: 1.0.0
"""

from math import cos,sin,tan,floor,sqrt

import Geometrias.Angulo as ang

import Geodesia.Elipsoides as Elip
import Geodesia.RadiosDeCurvatura as Rad
import Geometrias.PuntoGeodesico as pgeo
import Geometrias.PuntoUTM as putm




def Geo2UTM(PuntoGeodesico,NombreElipsoide,Huso=None):
    '''
    Funcion que transforma de Coordenadas geodesicas a coordenadas Cartesianaes Geocentricas.
    
    @param PuntoGeodesico: Punto Geodesico con las coordenadas del punto.
    @type PuntoGeodesico: puntoGeodesico.
    
    @param Nombre_Elipsoide: Nombre del elipsoide de calculo.
    @type Nombre_Elipsoide: String.
    
    @param Huso: Valor del Huso en el caso de que se quieran forzar las coordenadas a ese Huso.
    @type Huso: int.
    
    @raise Valor Punto Geodesico: Se produce una excepción en el caso de que el punto introducido
                                  no sea de tipo puntoGeodesico.
    @raise Valor Nombre Elipsoide: Se produce una excepción en el caso que el el Nombre del elipsoide
                                   no sea de tipo String.
                                   
    @return: puntoUTM
    '''
    if not isinstance(PuntoGeodesico,pgeo.PuntoGeodesico):
        raise Exception("Valor Punto Geodesico")
    
    try:
        NombreElipsoide=str(NombreElipsoide)
    except:
        raise Exception("Valor Nombre Elipsoide")
    
    #Conversion a radian.
    Latitud=ang.Angulo(PuntoGeodesico.getLatitud(),formato='latitud')
    Latitud.Convertir('radian')
    Lat=Latitud.getAngulo()
    Longitud=ang.Angulo(PuntoGeodesico.getLongitud(),formato='longitud180')
    Longitud.Convertir('radian')
    Lon=Longitud.getAngulo()
    AlturaElipsoidal=PuntoGeodesico.getAlturaElipsoidal()

    #Calculo de parámetros del elipsoide.
    Elipsoide= Elip.Elipsoides(NombreElipsoide)
    nhu=Rad.RadiosDeCurvatura(NombreElipsoide).getRadioPrimerVertical(Lat)
    e=Elipsoide.getPrimeraExcentricidad()
    e2=Elipsoide.getSegundaExcentricidad()
    #Valores Auxiliares
    t=tan(Lat)
    t2=(t**2)
    t4=(t**4)
    t6=(t**6)
    t8=(t**8)
    n2=((e2**2))*((cos(Lat)**2))
    n4=(n2**2)
    n6=(n2**3)
    n8=(n2**4)
    n10=(n2**5)
    n12=(n2**6)
    n14=(n2**7)
    #Claculo de las series de terminos.
    #x cubo.
    x3=(1.0-t2+n2)
    #x quinta.
    x5=(5.0-18.0*t2+t4+14.0*n2-58.0*n2*t2+13.0*n4-64.0*n4*t2+4.0*n6-24.0*n6*t2)
    #x septima.
    x7=(61.0-479.0*t2+179.0*t4-t6+331.0*n2-3298.0*n2*t2+177.0*n2*t4+715.0*n4-8655.0*n4*t2+6080.0*n4*t4+769.0*n6-10964.0*n6*t2+9480.0*n6*t4+412.0*n8-5176.0*n8*t2+6912.0*n8*t4+88.0*n10-1632.0*n10*t2+1920.0*n10*t4)
    #x novena.
    x9=(1385.0-20480.0*t2+20690.0*t4-1636.0*t6+t8+12284.0*n2-173088.0*n2*t2+201468.0*n2*t4-54979.0*n2*t6-21.0*n2*t8+45318.0*n4-883449.0*n4*t2+14499197.0*n4*t4-390607.0*n4*t6-14.0*n4*t8+90804.0*n6-2195193.0*n6*t2+549800.0*n6*t4-1394064.0*n6*t6+104073.0*n8-2875680.0*n8*t2+7041648.0*n8*t4-2644992.0*n8*t6+68568.0*n10-2115840.0*n10*t2+5968512.0*n10*t4-2741760.0*n10*t6+25552.0*n12-880192.0*n12*t2+2811456.0*n12*t4-1474560.0*n12*t6+4672.0*n14-175680.0*n14*t2+603648.0*n14*t4-322560.0*n14*t6)
    #y cuarta.
    y4=(5.0-t2+9.0*n2+4.0*n4)
    #y sexta.
    y6=(61.0-58.0*t2+t4+270.0*n2-330.0*n2*t2+445.0*n4-680.0*n4*t2+324.0*n6-600.0*n6*t2+88.0*n8-192.0*n8*t2)
    #y octava.
    y8=(1385.0-3595.0*t2+543.0*t4-t6+10899.0*n2-18634.0*n2*t2+10787.0*n2*t4+7.0*n2*t6+34419.0*n4-120582.0*n4*t2+49644.0*n4*t4+56385.0*n6-252084.0*n6*t2+121800.0*n6*t4+47688.0*n8-242496.0*n8*t2+151872.0*n8*t4+20880.0*n10-121920.0*n10*t2+94080.0*n10*t4+4672.0*n12-30528.0*n12*t2+23040.0*n12*t4)
    
    #Calculo de lam.
    s1=sin(Lat)
    s3=(s1**3)
    s5=(s1**5)
    s7=(s1**7)
    s9=(s1**9)
    c1=cos(Lat)
    g1=Lat
    g2=1.5*(e**2)*((-0.5*s1*c1)+0.5*Lat)
    g3=(15.0/8.0)*(e**4)*((-0.25*s3*c1)-((3.0/8.0)*s1*c1)+((3.0/8.0)*Lat))
    g4=(35.0/16.0)*(e**6)*((-(1.0/6.0)*s5*c1)-((5.0/24.0)*s3*c1)-((5.0/16.0)*s1*c1)+((5.0/16.0)*Lat))
    g5=(315/128)*(e**8)*((-(1/8)*s7*c1)-((7/48)*s5*c1)-((35/192)*s3*c1)-((35/128)*s1*c1)+((35/128)*Lat))
    g6=(693/256)*(e**10)*((-(1/10)*s9*c1)-((9/80)*s7*c1)-((21/160)*s5*c1)-((21/128)*s3*c1)-((63/256)*s1*c1)+((63/256)*Lat))
    lam=Elipsoide.getSemiEjeMayor()*(1-(e**2))*(g1+g2+g3+g4+g5+g6)
    
    #Calculo del Huso.
    if Huso==None:
        Huso=floor(((180.0+Longitud)/6)+1)
        lon0=ang.Angulo((Huso*6)-183,formato='pseudosexagesimal')
        lon0.Convertir('radian')
        lon0=lon0.getAngulo()
    else:
        Huso=int(Huso)
        #Meridiano central.
        lon0=ang.Angulo((Huso*6)-183,formato='pseudosexagesimal')
        lon0.Convertir('radian')
        lon0=lon0.getAngulo()
        lon0d=lon0+0.05817764173314432 #3º20'
        lon0i=lon0-0.05817764173314432
        print(lon0d,lon0i,Lon)
        if Lon<lon0i or Lon>lon0d:
            raise Exception("Solo se pueden forzar las coordenadas a los Husos adyacentes un máximo de 20'")
        
    #Incremento de longitud.
    Alon=Lon-lon0
    #Calculo de X.
    c3=(c1**3)
    c5=(c1**5)
    c7=(c1**7)
    c9=(c1**9)
    X=500000.0+(0.9996*((Alon*nhu*c1)+(((Alon**3)/6.0)*nhu*c3*x3)+(((Alon**5)/120.0)*nhu*c5*x5)+(((Alon**7)/5040.0)*nhu*c7*x7)+(((Alon**9)/362880.0)*nhu*c9*x9)))
    #Calculo de Y.
    c2=(cos(Lat)**2)
    c4=(cos(Lat)**4)
    c6=(cos(Lat)**6)
    c8=(cos(Lat)**8)
    Y=0.9996*(lam+(((Alon**2)/2.0)*nhu*t*c2)+(((Alon**4)/24.0)*nhu*t*c4*y4)+(((Alon**6)/720.0)*nhu*t*c6*y6)+(((Alon**8)/40320.0)*nhu*t*c8*y8))
    
    # Si la latiud está en el Hemisferio Sur:
    if Latitud.getAngulo()<0:
        Y=10000000.0-Y
        
    #Cálculo de la convergencia de meridianos.
    #coeficientes.
    m3=(1.0+3.0*n2+2*n4)
    m5=(2.0-t2+15.0*n2*t2+35.0*n4-50.0*n4*t2+33.0*n6-60.0*n6*t2+11.0*n8-24.0*n8*t2)
    m7=(-148.0-3427.0*t2+18.0*t4-1387.0*t6+2023.0*n2-46116.0*n2*t2+5166.0*n2*t4+18984.0*n4-100212.0*n4*t4+34783*n6-219968.0*n6*t2+144900.0*n6*t4+36180.0*n8-261508.0*n8*t2+155904.0*n8*t4+18472.0*n10-114528.0*n10*t2+94080.0*n10*t4+4672.0*n12-30528.0*n12*t2+23040.0*n12*t4)
    convmed=(Alon*s1)+(((Alon**3)/3.0)*s1*c2*m3)+(((Alon**5)/15.0)*s1*c4*m5)+(((Alon**7)/5040.0)*s1*c6*m7)
    convmed=ang.Angulo(convmed,formato='radian')
    convmed.Convertir('pseudosexagesimal')
    convmed=convmed.getAngulo()
    #Calculo de la escala local del punto.
    #coeficientes.
    k2=(1+n2)
    k4=(8.0-24.0*t2+4.0*t4+20.0*n2-28.0*n2*t2+16.0*n4-48.0*n4*t2+4.0*n6-24.0*n6*t2)
    k6=(136.0+10576.0*t2-9136.0*t4+224.0*t6+616.0*n2+43952.0*n2*t2-50058.0*n2*t4-1120.0*n4+66960.0*n4*t2-95680.0*n4*t4+1024.0*n6+42736.0*n6*t2-80160.0*n6*t4+472.0*n8+9184.0*n8*t2-21888.0*n8*t4+88.0*n10-1632.0*n10*t2+1920.0*n10*t4)
    kp=(0.9996**2)*(1+((Alon**2)*c2*k2)+(((Alon**4)/12.0)*c4*k4)+(((Alon**6)/360.0)*c6*k6))
    kp=sqrt(kp)
    
    posY=None
    if Latitud.getAngulo() > 0:
        posY ="N"
    else:
        posY="S"
    
    sal=putm.PuntoUTM(X, Y, hemisferioY=str(posY), helip=AlturaElipsoidal, huso=int(Huso) )
    sal.setConvergenciaMeridianos(convmed)
    sal.setEscalaLocalPunto(kp)
    
    return sal

def Geo2UTM_From_File(File,NombreElipsoide):
    import os
    '''
Función que realiza la conversión de geodesicas a UTM desde un fichero.
    @param File:
    @type File: str.
'''
    if not type(File)==str:
        raise Exception("Not str")
    if not os.path.exists(File):
        raise Exception("Not Exists")
    if not os.path.isfile(File):
        raise Exception("Not File")

    #ID,Lat,Lon,.....
    f=open(File,'r')
    Lats=[i.split(",")[1] for i in f]
    f.seek(0)
    Lons=[i.split(",")[2] for i in f]
    f.close()
    Elips=[NombreElipsoide for number in range(len(Lats))]
    Puntos=[pgeo.PuntoGeodesico(i,j) for i,j in zip(Lats,Lons)]
    sal=map(Geo2UTM,Puntos,Elips)
    return sal
    

def main():
#     import os
#     print("Conversor de Coordenadas Geodesicas a UTM.")
#     opt=None
#     while opt!=0:
#         print()
#         print("Seleccione una opción:\n\t1-Convertir un punto.\n\t2-Convertir un fichero.\n\t0-Salir.")
#         opt=int(input("Opción: "))
#         if opt>2:
#             print("Opción Invalida")
#             continue
#         else:
#             if opt==1:
#                 print()
#                 Lat=float(input("Latitud: "))
#                 Lon=float(input("Longitud: "))
#                 Nombre_Elipsoide=input("Elipsoide: ").upper()
#                 Force=""
#                 while True:
#                     Force=input("Forzar Coordenadas a un Huso? (S/N):")
#                     Force=Force.upper()
#                     if Force=="S":
#                         break
#                     elif Force=="N":
#                         try:
#                             p=pgeo.PuntoGeodesico(Lat,Lon)
#                             sal=Geo2UTM(p,Nombre_Elipsoide)
#                             print()
#                             print("Resultados:")
#                             print("X:\t%.3f"%sal.get_X_UTM())
#                             print("Y:\t%.3f"%sal.get_Y_UTM())
#                             print("Z:\t"+str(sal.get_Altura_Elipsoidal()))
#                             print("Huso:\t"+str(sal.get_Huso()))
#                             print("W:\t%.8f"%sal.get_Convergencia_Meridianos())
#                             print("fesca:\t%.9f"%sal.get_Escala_Local_Punto())
#                         except Exception as e:
#                             print(e)
#                             break
#                         break
#             elif opt==2:
#                 print()
#                 try:
#                     r_ent=input("Ruta fichero Entrada: ")
#                     r_sal=input("Ruta fichero Salida: ")
#                     if r_ent==r_sal:
#                         print()
#                         print("Error: El archivo de entrada no puede conincidir con el de salida.")
#                         continue
#                     Nombre_Elipsoide=input("Elipsoide: ").upper()
#                     sal=Geo2UTM_From_File(r_ent,Nombre_Elipsoide)
#                     pr=open(r_sal,'wb',1024)
#                     for i in sal:
#                         a=bytes((""+str(i.get_X_UTM())+";"+str(i.get_Y_UTM())+"\n").encode(encoding='UTF-8',errors='strict'))
#                         pr.write(a)
#                 except Exception as e:
#                     print(e)
#                     break
#                 break
# 
#             else:
#                 os.system('pause')
            









        
#     sal=Geo2UTM_From_File('GeodesicasElipsoidales.txt','GRS80')
#     input("Y")
#     for i in sal:
#         print(i.get_X_UTM(),i.get_Y_UTM())
#     print("Prueba de la conversión de coordenadas.")
#     print("Elipsoide de pruebas:\tGRS80")
#     print("Coordenadas geodesicas de prueba:")
#     print("\tLatitud:\t45")
#     print("\tLongitud:\t-1")
#     print("\th elipsoidal:\t50")
#     print("\n")
    p1=pgeo.PuntoGeodesico(ang.Angulo(45,formato='latitud'),ang.Angulo(0.03,formato='longitud180'),50)
    p2=Geo2UTM(p1,"GRS 1980",30)
    print("Resultados:")
    print("X:\t%.3f"%p2.getX())
    print("Y:\t%.3f"%p2.getY())
    print("Z:\t%.3f"%p2.getAlturaElipsoidal())
    print("Huso:\t"+str(p2.getHuso()))
    print("W:\t%.8f"%p2.getConvergenciaMeridianos())
    print("fesca:\t%.9f"%p2.getEscalaLocalPunto())


    
if __name__=="__main__":
    main()
