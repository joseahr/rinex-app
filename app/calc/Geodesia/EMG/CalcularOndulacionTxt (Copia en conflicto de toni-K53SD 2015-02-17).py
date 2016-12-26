#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''!
Created on 10/2/2015

@author: Antonio Hermosilla Rodrigo.
@contact: anherro285@gmail.com
@organization: Antonio Hermosilla Rodrigo.
@copyright: (C) 2015 by Antonio Hermosilla Rodrigo
@version: 1.0.0
'''

from os.path import split,realpath
from os import  listdir
import sys
import Geometrias.PuntoGeodesico as pgeo


sys.path.append('../..')

def CalcularOndulacion(PuntoGeodesico):
    '''
    Función para realizar la interpolación de la ondulación del geoide a traves de la rejilla en formato txt.
    '''
    Latitud=PuntoGeodesico.getLatitud()
    Longitud=PuntoGeodesico.getLongitud()
    path,arch=split(realpath(__file__)) #Hace referencia al directorio donde se encuentra el archivo de código.
    # En función del rango de longitud y laitud se debera abrir el archivo de la peninsula o el de canarias.
    
    arch=None
    validos=[i for i in listdir(path) if i.endswith("txt")]
    Lat_rejilla=None
    Lon_rejilla=None
    nfil_rejilla=None
    ncol_rejilla=None
    NO_DATA=-999
    ancho_fil=None
    ancho_col=None
    Rango_Lat=None
    Rango_Lon=None
    val=None
    for i in validos:
        rut=path+"/"+i
        f=open(rut,'r')
        lin1=f.readline().split()
        Lat_rejilla=float(lin1[0])
        Lon_rejilla=float(lin1[1])-360
        ancho_fil=float(lin1[2])/60
        ancho_col=float(lin1[3])/60
        nfil_rejilla=int(lin1[4])
        ncol_rejilla=int(lin1[5])
        Rango_Lat=[Lat_rejilla-i*ancho_fil for i in range(nfil_rejilla)]
        Rango_Lon=[Lon_rejilla+i*ancho_col for i in range(ncol_rejilla)]

        if Latitud>Rango_Lat[-1] and Latitud<Rango_Lat[0] and Longitud>Rango_Lon[0] and Longitud<Rango_Lon[-1]:
            val=rut
            break
        else:
            Lat_rejilla=None
            Lon_rejilla=None
            nfil_rejilla=None
            ncol_rejilla=None
            NO_DATA=-999
            ancho_fil=None
            ancho_col=None
            Rango_Lat=None
            Rango_Lon=None
            continue

    if val==None:
        raise Exception("El punto introducido no se encuentra en ninguna rejilla.")
##    print(val)
    const=85 #Numero de lineas de fichero en las que hay datos para una latitud
    Alat=Lat_rejilla-Latitud
    Alon=Lon_rejilla-Longitud
##    print(Alat,Alon)
    fila=round(abs(Alat)/ancho_fil)
    columna=round(abs(Alon)/ancho_col)
##    print(fila,columna)
##    print(Rango_Lat[fila])
##    print(Rango_Lon[columna])

    Alat=Rango_Lat[fila]-Latitud
    Alon=Rango_Lon[columna]-Longitud
    #print(Alat,Alon)
    lin_fila=(fila*const)+1
##    print(lin_fila)
##    input()

    if Alat==0 and Alon==0:
        #Valor exacto de la celda.
        f=open(rut,'r')
        val=[]
        seccion=f.readlines()[lin_fila:lin_fila+const]
        f.close()
        for i in seccion:
            i=i.split()
            for j in i:
                val.append(j)
                
        #print(val[columna-1])
        return float(val[columna])
    elif Alat!=0 and Alon==0:
        #Intepolacion lineal en latitud.
        #print(Alat)
        lin_fila2=None
        if Alat>0:
            lin_fila2=((fila+1)*const)+1
        else:
            lin_fila2=((fila-1)*const)+1

        f=open(rut,'r')
        seccion1=f.readlines()[lin_fila:lin_fila+85]
        f.seek(0)
        seccion2=f.readlines()[lin_fila2:lin_fila2+85]
        f.close()

        val1=[]
        val2=[]
        for i1,i2 in zip(seccion1,seccion2):
            j1=i1.split()
            j2=i2.split()
            for k1,k2 in zip(j1,j2):
                val1.append(k1)
                val2.append(k2)
        val1=float(val1[columna-1])
        val2=float(val2[columna-1])
        #print(val1,val2)
        #Interpolacion.
        fact=(val2-val1)/(1/60)
        val=None
        if Alat>0:
            val=val1+(Alat*fact)
        else:
            #print("negativo")
            Alat=(1/60)-Alat
            val=val1+(Alat*fact)
        return val
        pass
    elif Alat==0 and Alon!=0:
        #Interpolacion lineal en longitud.
        #print(Alon)
        #Coger la linea de la latitud.
        f=open(rut,'r')
        seccion=f.readlines()[lin_fila:lin_fila+85]
        f.close()
        val=[]
        for i1 in seccion:
            j1=i1.split()
            for k1 in j1:
                val.append(k1)
        #De esta seccion coger los dos valores validos.
        val1=None
        val2=None
        if Alon>0:
            val1=float(val[columna])
            val2=float(val[columna+1])
        else:
            val1=float(val[columna])
            val2=float(val[columna-1])
            
        fact=(val2-val1)/(1/60)
        val=None
        if Alon>0:
            val=val1+(Alon*fact)
        else:
            val=val1+(Alon*fact)
        return val
        pass
    
    
    
    
    
    elif Alat!=0 and Alon!=0:
        #Interpolacion bilineal.
        #En función de la latitud se necesitan las dos secciones.
        lin_fila2=None
        if Alat>0:
            lin_fila2=((fila+1)*const)+1
        else:
            lin_fila2=((fila-1)*const)+1

        f=open(rut,'r')
        seccion1=f.readlines()[lin_fila:lin_fila+85]
        f.seek(0)
        seccion2=f.readlines()[lin_fila2:lin_fila2+85]
        f.close()

        val1=[]
        val2=[]
        for i1,i2 in zip(seccion1,seccion2):
            j1=i1.split()
            j2=i2.split()
            for k1,k2 in zip(j1,j2):
                val1.append(k1)
                val2.append(k2)
        #de estas secciones, en función de la longitud se gogen los valores,
        vala=None
        valb=None
        valc=None
        vald=None
        
        if Alon>0:
            vala=float(val1[columna])
            valb=float(val1[columna+1])
            valc=float(val2[columna])
            vald=float(val2[columna+1])
        else:
            vala=float(val1[columna])
            valb=float(val1[columna-1])
            valc=float(val2[columna])
            vald=float(val2[columna-1])
            
        #print(vala,valb,valc,vald) 
        v1=valc*(Alon*Alat)
        v2=vald*((1-Alon)*Alat)
        v3=vala*Alon*(1-Alat)
        v4=valb*(1-Alon)*(1-Alat)
        #print(v1,v2,v3,v4)
        return(v1+v2+v3+v4)
            
                
                
                
        pass
        






    


##    print(fila,columna)
##    lin_fila=(fila*const)+1
##    print(lin_fila)
##    #Que fila esta mas prxima a la elegida la anterior o la siguiente.
##    Lpost=Rango_Lat[fila-1]
##    Lant=Rango_Lat[fila+1]
##    d1L=abs(Lant-Latitud)
##    d2L=abs(Lpost-Latitud)
##    Escogida=None
##    Lat_inter=None
##    linea_fichero_b=None
##    if d1L<d2L:
##        Lat_inter=Lant
##        linea_fichero_b=1+(fila-1)*const
##        Escogido="Anteior"
##    else:
##        Lat_inter=Lpost
##        linea_fichero_b=1+(fila+1)*const
##        Escogido="Posteior"
##
##    print(Lat_inter,Escogido,linea_fichero_b)
##
##    #[......**.....]-1
##    #[......**.....]
##    #[......**.....]+1
##    #Hay que analizar que linea conviene coger, la anterior o la siguiente para realizar la interpolacion
##    f=open(ruta_b,'r')
##    seccion1=f.readlines()[linea_fichero:linea_fichero+85]
##    f.seek(0)
##    seccion2=f.readlines()[linea_fichero_b:linea_fichero_b+85]
##    f.close()
##    #Se arreglan los datos y se convierten en una única fila.
##    sal1=[]
##    sal2=[]
##    for i1,i2 in zip(seccion1,seccion2):
##        j1=i1.split()
##        j2=i2.split()
####        print(j1)
##        for k1,k2 in zip(j1,j2):
####            print(k1)
##            sal1.append(k1)
##            sal2.append(k2)
##    
    



    
        
    


##    input()





        
def main():
    p=pgeo.PuntoGeodesico(40,-1)
    print(CalcularOndulacion(p))
    p=pgeo.PuntoGeodesico(40,-1.1)
    print(CalcularOndulacion(p))
    p=pgeo.PuntoGeodesico(40,-0.9)
    print(CalcularOndulacion(p))
    p=pgeo.PuntoGeodesico(40.1,-1)
    print(CalcularOndulacion(p))
    p=pgeo.PuntoGeodesico(39.9,-1)
    print(CalcularOndulacion(p))
    p=pgeo.PuntoGeodesico(40,-1.111)
    print(CalcularOndulacion(p))
    p=pgeo.PuntoGeodesico(40,-0.999)
    print(CalcularOndulacion(p))
    p=pgeo.PuntoGeodesico(40.111,-1)
    print(CalcularOndulacion(p))
    p=pgeo.PuntoGeodesico(39.999,-1)
    print(CalcularOndulacion(p))
    p=pgeo.PuntoGeodesico(39.999,-1.111)
    print(CalcularOndulacion(p))
    p=pgeo.PuntoGeodesico(39.999,-0.999)
    print(CalcularOndulacion(p))
    
    
    
#     p=pgeo.PuntoGeodesico(35.11,-1)
#     CalcularOndulacion(p)
#     p=pgeo.PuntoGeodesico(40,-3)
#     CalcularOndulacion(p)
#     p=pgeo.PuntoGeodesico(42,-5)
#     CalcularOndulacion(p)
#     p=pgeo.PuntoGeodesico(43,-7)
#     CalcularOndulacion(p)
    

if __name__=="__main__":
    main()
    
    
