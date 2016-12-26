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

from math import cos,sin,tan,sqrt

import Geometrias.Angulo as ang
import Geodesia.Elipsoides as Elip
import Geodesia.RadiosDeCurvatura as Rad
import Geometrias.PuntoGeodesico as pgeo
import Geometrias.PuntoUTM as putm


##import Geometrias.puntoGeodesicoUTM as pgeoUTM

def UTM2Geo(PuntoUTM,NombreElipsoide):
    '''
    Funcion que transforma de Coordenadas UTM a Geodesicas Elipsoidales.
    
    @param PuntoUTM: Punto con las Coordenadas UTM.
    @type PuntoUTM: puntoUTM.
    
    @param Nombre_Elipsoide: Nombre del elipsoide de calculo.
    @type Nombre_Elipsoide: String.
    
    @raise Valor Punto UTM: Se produce una excepción en el caso de que el punto introducido
                                  no sea de tipo puntoUTM.
    @raise Valor Nombre Elipsoide: Se produce una excepción en el caso que el el Nombre del elipsoide
                                   no sea de tipo String.
                                   
    @return: puntoGeodesicoUTM
    '''
#     print(type(PuntoUTM))
#     print(putm.PuntoUTM.__class__)
    if not isinstance(PuntoUTM.__class__,putm.PuntoUTM.__class__):
        raise Exception("Valor Punto UTM.")
    
    try:
        NombreElipsoide=str(NombreElipsoide)
    except:
        raise Exception("Valor Nombre Elipsoide")
    
    x= PuntoUTM.getX()
    y= PuntoUTM.getY()
    helip= PuntoUTM.getAlturaElipsoidal()
    posY= PuntoUTM.getHemisferioY()
    Huso = PuntoUTM.getHuso()
    
    Elipsoide= Elip.Elipsoides(NombreElipsoide)
    a= Elipsoide.getSemiEjeMayor()
    e= Elipsoide.getPrimeraExcentricidad()
    e2= Elipsoide.getSegundaExcentricidad()
    #Calculos auxiliares.
    if posY is "S":
        y = 10000000.0 - y
    
    x=(x-500000.0)/0.9996
    y=y/0.9996
    
    #Calculo iterativo de la latitud auxiliar.
    Lat=(y)/(a*(1-(e**2)))
    Latsig=0.0
    cont=0
    while abs(Lat-Latsig) > 0.000000000001:
        if cont !=0:
            Lat=Latsig
        
        s1=sin(Lat)
        s3=(s1**3)
        s5=(s1**5)
        s7=(s1**7)
        s9=(s1**9)
        c1=cos(Lat)
        g2=1.5*(e**2)*((-0.5*s1*c1)+0.5*Lat)
        g3=(15.0/8.0)*(e**4)*((-0.25*s3*c1)-((3.0/8.0)*s1*c1)+((3.0/8.0)*Lat))
        g4=(35.0/16.0)*(e**6)*((-(1.0/6.0)*s5*c1)-((5.0/24.0)*s3*c1)-((5.0/16.0)*s1*c1)+((5.0/16.0)*Lat))
        g5=(315.0/128.0)*(e**8)*((-(1.0/8.0)*s7*c1)-((7.0/48.0)*s5*c1)-((35.0/192.0)*s3*c1)-((35.0/128.0)*s1*c1)+((35.0/128.0)*Lat))
        g6=(693.0/256.0)*(e**10)*((-(1.0/10.0)*s9*c1)-((9.0/80.0)*s7*c1)-((21.0/160.0)*s5*c1)-((21.0/128.0)*s3*c1)-((63.0/256.0)*s1*c1)+((63.0/256.0)*Lat))
        Latsig=(y)/(a*(1-(e**2)))-(g2+g3+g4+g5+g6)
        cont +=1
        
    #Valores Auxiliares
    t=tan(Latsig)
    t2=(t**2)
    t4=(t**4)
    t6=(t**6)
    t8=(t**8)
    n2=((e2**2))*((cos(Latsig)**2))
    n4=(n2**2)
    n6=(n2**3)
    n8=(n2**4)
    n10=(n2**5)
    n12=(n2**6)
    n14=(n2**7)
    #Claculo de las series de terminos.
    #Calculo del incremento de longitud.
    #x cubo.
    x3=(1.0+2.0*t2+n2)
    #x quinta.
    x5=(5.0+28.0*t2+24.0*t4+6.0*n2+8.0*n2*t2-3.0*n4+4.0*n4*t2-4.0*n6+24.0*n6*t2)
    #x septima.
    x7=(61.0+662.0*t2+1320.0*t4+720.0*t6+107.0*n2+440.0*n2*t2+336.0*n2*t4+43.0*n4-234.0*n4*t2-192.0*n4*t4+97.0*n6-772.0*n6*t2+408.0*n6*t4+188.0*n8-2392.0*n8*t2+1536.0*n8*t4+88.0*n10-1632.0*n10*t2+1920.0*n10*t4)
    #x novena. 
    x9=(1385.0+24568.0*t2+83664.0*t4+100800.0*t6+40320.0*t8+3116.0*n2+26736.0*n2*t2+47808.0*n2*t4+24192.0*n2*t6+1158.0*n4-4884.0*n4*t2-20736.0*n4*t4-13824.0*n4*t6-3500.0*n6+27104.0*n6*t2+576.0*n6*t4+12192.0*n6*t6-11735.0*n8+44788.0*n8*t2-195984.0*n8*t4+9788.0*n8*t6-20280.0*n10+459312.0*n12*t2-1239552.0*n12*t4+437760.0*n12*t6-4672.0*n14+175680.0*n14*t2-603648.0*n14*t4+322560.0*n14*t6)
    nhu=Rad.RadiosDeCurvatura(NombreElipsoide).getRadioPrimerVertical(Latsig)
    c1=cos(Latsig)
    Alon=(x/(nhu*c1))-(((x**3)/(6.0*(nhu**3)*c1))*x3)+(((x**5)/(120.0*(nhu**5)*c1))*x5)-(((x**7)/(5040.0*(nhu**7)*c1))*x7)+(((x**9)/(362880.0*(nhu**9)*c1))*x9)
    
    lon0=ang.Angulo((Huso*6)-183,formato='longitud180')
    lon0.Convertir('radian')
    Lon=lon0.getAngulo()+Alon
    #Calculo de la Latitud.
    #x cuadrado.
    x2=(1.0+n2)
    #x cuarta.
    x4=(5.0+3.0*t2+6.0*n2-6.0*n2*t2-3.0*n4-9.0*n4*t2-4.0*n6)
    #x sexta.
    x6=(61.0+90.0*t2+45.0*t4+107.0*n2-162.0*n2*t2-45.0*n2*t4+43.0*n4-318.0*n4*t2+135.0*n4*t4+97.0*n6+18.0*n6*t2+225.0*n6*t4)
    #x octava.
    x8=(1385.0+3633.0*t2+4515.0*t4+2310.0*t4+3116.0*n2-5748.0*n2*t2+4704.0*n2*t4-525.0*n2*t6+1158.0*n4-17826.0*n4*t2+37734.0*n4*t4-9450.0*n4*t6-3500.0*n6+1164.0*n6*t2+14006.0*n6*t4-20790.0*n6*t6-11735.0*n8+29001.0*n8*t2+13389.0*n8*t4-45.0*n8*t6-20280.0*n10+64272.0*n10*t2-15864.0*n10*t4-16144.0*n12+75408.0*n12*t2-31872.0*n12*t4-4672.0*n14+30528.0*n14*t2-23040.0*n14*t4)
    
    Lats=Latsig +(((-(x**2)/(2.0*(nhu**2)))*t*x2)+((((x**4)/(24.0*(nhu**4)))*t*x4))-((((x**6)/(720.0*(nhu**6)))*t*x6))+((((-x**8)/(40320.0*(nhu**8)))*t*x8)))
    
    #Cálculo de la convergencia de meridianos.
    #coeficientes.
    c2=(c1**2)
    c4=(c1**4)
    c6=(c1**6)
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
    
    Lats=ang.Angulo(Lats,formato='radian')
    Lats.Convertir('latitud')
    Lats=Lats.getAngulo()
    
    Lon=ang.Angulo(Lon,formato='radian')
    Lon.Convertir('longitud180')
    Lon=Lon.getAngulo()
    
    p1=pgeo.PuntoGeodesico(Lats, Lon, helip)
    PuntoUTM.setConvergenciaMeridianos(convmed)
    PuntoUTM.setEscalaLocalPunto(kp)
    
    return p1

def UTM2GeoFromFile(File,NombreElipsoide):
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

    #ID,Lat,Lon,helip.....
    f=open(File,'r')
    Xs=[i.split(",")[1] for i in f]
    f.seek(0)
    Ys=[i.split(",")[2] for i in f]
    f.close()
    Elips=[NombreElipsoide]*len(Xs)
    Puntos=[putm.PuntoUTM(i,j) for i,j in zip(Xs,Ys)]
    sal=map(UTM2Geo,Puntos,Elips)
    return sal


def main():
    import os
    print("Conversor de Coordenadas UTM a Geodesicas.")
    opt=None
    while opt!=0:
        print()
        print("Seleccione una opción:\n\t1-Convertir un punto.\n\t2-Convertir un fichero.\n\t0-Salir.")
        opt=int(input("Opción: "))
        if opt>2:
            print("Opción Invalida")
            continue
        else:
            if opt==1:
                print()
                try:
                    X=float(input("X(UTM): "))
                    Y=float(input("Y(UTM): "))
                    Huso=int(input("Huso: "))
                    Nombre_Elipsoide=input("Elipsoide: ")
                    p=putm.PuntoUTM(X,Y,Huso=Huso)
                    sal=UTM2Geo(p,Nombre_Elipsoide)
                    print()
                    print("Resultados:")
                    print("Latitud: "+str(sal.get_Latitud()))
                    print("Longitud: "+str(sal.get_Longitud()))
                    print("h Elipsoidal: "+str(sal.get_Altura_Elipsoidal()))
                    print("kp: %.5f"%p.get_Escala_Local_Punto())
                    print("conv_med: %.6f"%p.get_Convergencia_Meridianos())
                except Exception as e:
                    print(e)
                    continue
            elif opt==2:
                print()
                try:
                    r_ent=input("Ruta fichero Entrada: ")
                    r_sal=input("Ruta fichero Salida: ")
                    if r_ent==r_sal:
                        print()
                        print("Error: El archivo de entrada no puede conincidir con el de salida.")
                        continue
                    Nombre_Elipsoide=input("Elipsoide: ")
                    sal=UTM2GeoFromFile(r_ent,Nombre_Elipsoide)
                    pr=open(r_sal,'wb',1024)
                    for i in sal:
                        a=bytes((""+str(i.get_Latitud())+";"+str(i.get_Longitud())+"\n").encode(encoding='UTF-8',errors='strict'))
                        pr.write(a)
                except Exception as e:
                    print(e)
                    continue
                
            else:
                os.system('pause')
                


    
##    sal=UTM2Geo_From_File('fichero_UTM.txt','GRS80')
##    pr=open('sal_pr','wb',1024)
##    for i in sal:
##        a=bytes((""+str(i.get_Latitud())+";"+str(i.get_Longitud())+"\n").encode(encoding='UTF-8',errors='strict'))
####        a=a.encode()
####        a=bytes(a)
####        
####        a=bytes(str(i.get_Latitud()).encode(encoding='UTF-8',errors='strict'))
##        pr.write(a)
##    pr.close()
##    input("Y")
##    print("Prueba de la conversión de coordenadas.")
##    print("Elipsoide de pruebas:\tGRS80")
##    print("Coordenadas UTM de prueba:")
##    print("\tX:\t657630.641")
##    print("\tY:\t4984896.171")
##    print("\th:\t50")
##    print("\tHuso:\t30")
##    print("\n")
##    p1=putm.PuntoUTM(657630.641,4984896.171,Altura_Elipsoidal=50,Huso=30)
##    p2=UTM2Geo(p1,"GRS80")
##    print("Latitud:\t%.8f"%p2.get_Latitud())
##    print("Longitud:\t%.8f"%p2.get_Longitud())
##    print("h Elipsoidal:\t%.3f"%p2.get_Altura_Elipsoidal())
##    print("kp:\t%.5f"%p1.get_Escala_Local_Punto())
##    print("conv_med:\t%.6f"%p1.get_Convergencia_Meridianos())
##    print("\n")



if __name__=="__main__":
    main()
