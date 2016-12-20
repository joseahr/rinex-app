#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 25/3/2015

@author: Antonio Hermosilla Rodrigo.
@contact: anherro285@gmail.com
@organization: Antonio Hermosilla Rodrigo.
@copyright: (C) 2015 by Antonio Hermosilla Rodrigo.
@version: 1.0.0
'''

from os.path import split,realpath
import Geometrias.PuntoGeodesico as pgeo
import BasesDeDatos.SQLite.SQLiteManager as DB


def CalcularOndulacion(PuntoGeodesico,tipo='bilineal'):
    '''!
    \brief Función para calcular la ondulación del geoide con el modelo EGM08 del IGN.
    \param PuntoGeodesico PuntoGeodesico: Punto geodesico de cálculo:
    \param tipo str: Tipo de interpolación que realizara. bilineal distancia.
    '''
    if tipo!='bilineal' and tipo!='bicubica' and tipo!='distancia':
        raise Exception("La interpolación de la ondulación ha de ser de tipo bilineal o bicubica.")
    # Conexión a las bases de datos existentes.
    rutafil, file=split(realpath(__file__))
    #print(rutafil)
    db1 = DB.SQLiteManager(rutafil+'/EGM_Peninsula.db')
    db2 = DB.SQLiteManager(rutafil+'/EGM_Canarias.db')
    # comprobar si el punto introducido puede ser calculado.
    lat = PuntoGeodesico.getLatitud()
    lon = PuntoGeodesico.getLongitud()
    
    vals1 = db1.ObtenerTodo('Cabecera')
    #print(vals1)
    lat1=vals1[0][0]
    lon1=vals1[0][1]
    ilat1=vals1[0][2]
    ilon1=vals1[0][3]
    fil1=vals1[0][4]
    col1=vals1[0][5]
    Alat=ilat1*fil1
    Alon=ilon1*col1
    lat1f=lat1-Alat
    lon1f=lon1+Alon
    if lon1f>=360:
        lon1f-=360
    #print(Alat,Alon,lat1f,lon1f)
    
    
    
    vals2 = db2.ObtenerTodo('Cabecera')
    #print(vals2)
    lat2=vals2[0][0]
    lon2=vals2[0][1]
    ilat2=vals2[0][2]
    ilon2=vals2[0][3]
    fil2=vals2[0][4]
    col2=vals2[0][5]
    Alat=ilat2*fil2
    Alon=ilon2*col2
    lat2f=lat2-Alat
    lon2f=lon2+Alon
    if lon2f>=360:
        lon2f-=360
    #print(Alat,Alon,lat2f,lon2f)
    
    
    
    lonaux=lon
    if lon<0:
        lonaux=lon+360
        
#     print(lonaux)
    
    incfil=0
    inccol=0
    onds1=None
    onds2=None
    onds3=None
    onds4=None
    lat_calc=0
    lon_calc=0
    
    if (lat<lat1 and lat>lat1f):
        # Si el punto de cálculo está en la peninsula y al oeste de greenwhich
        if lonaux<360 and lonaux>lon1:
            #print('Peninsula')
            diflat=lat1-lat
            diflon=lonaux-lon1
            incfil=int(diflat/ilat1)
            inccol=int(diflon/ilon1)
            
            if tipo == 'bilineal' or 'distancia':
                onds1=db1.ObtenerFila('Ondulaciones', str(incfil))
                onds2=db1.ObtenerFila('Ondulaciones', str(incfil+1))
            elif tipo == 'bicubica':
                onds1=db1.ObtenerFila('Ondulaciones', str(incfil-1))
                onds2=db1.ObtenerFila('Ondulaciones', str(incfil))
                onds3=db1.ObtenerFila('Ondulaciones', str(incfil+1))
                onds4=db1.ObtenerFila('Ondulaciones', str(incfil+2))
            lat_calc=lat1-ilat1*incfil
            lon_calc=lon1+ilon1*inccol
            if lon_calc>=360:
                lon_calc-=360
        elif lonaux>=0 and lonaux<lon1f:
            # Si el punto de cálculo está en la peninsula y al este de greenwhich
            #print('Peninsula')
            diflat=lat1-lat
            diflon=(360-lon1)+lonaux
            incfil=int(diflat/ilat1)
            inccol=int(diflon/ilon1)
            
            if tipo == 'bilineal' or 'distancia':
                onds1=db1.ObtenerFila('Ondulaciones', str(incfil))
                onds2=db1.ObtenerFila('Ondulaciones', str(incfil+1))
            elif tipo == 'bicubica':
                onds1=db1.ObtenerFila('Ondulaciones', str(incfil-1))
                onds2=db1.ObtenerFila('Ondulaciones', str(incfil))
                onds3=db1.ObtenerFila('Ondulaciones', str(incfil+1))
                onds4=db1.ObtenerFila('Ondulaciones', str(incfil+2))
            lat_calc=lat1-ilat1*incfil
            lon_calc=lon1+ilon1*inccol
            if lon_calc>=360:
                lon_calc-=360
    elif (lat<lat2 and lat>lat2f) and (lonaux>lon2 and lonaux<lon2f):
        #Si el punto está en las canarias.
        #print('Canarias')
        diflat=lat2-lat
        diflon=lonaux-lon2
        incfil=int(diflat/ilat2)
        inccol=int(diflon/ilon2)
        
        if tipo == 'bilineal':
            onds1=db1.ObtenerFila('Ondulaciones', str(incfil))
            onds2=db1.ObtenerFila('Ondulaciones', str(incfil+1))
        elif tipo == 'bicubica':
            onds1=db1.ObtenerFila('Ondulaciones', str(incfil-1))
            onds2=db1.ObtenerFila('Ondulaciones', str(incfil))
            onds3=db1.ObtenerFila('Ondulaciones', str(incfil+1))
            onds4=db1.ObtenerFila('Ondulaciones', str(incfil+2))
        lat_calc=lat2-ilat2*incfil
        lon_calc=lon2+ilon2*inccol
        if lon_calc>=360:
            lon_calc-=360
    else:
        #Se devuelve None ya que no se pyede calcular con estas bases de datos.
        #Se puede añadir un elipsoide global para estos casos.
        #print('No valido')
        return None
    
#     print(onds1)
#     print(onds2)
    if tipo == 'bilineal':
        ond0=onds1[0][inccol+1]
        ond1=onds1[0][inccol]
        ond2=onds2[0][inccol+1]
        ond3=onds2[0][inccol]

        Alat=abs(lat_calc-lat)
        Alon=abs(lon_calc-lonaux)

        v1=ond0*Alon*Alat
        v2=ond1*(ilon1-Alon)*Alat
        v3=ond2*Alon*(ilat1-Alat)
        v4=ond3*(ilon1-Alon)*(ilat1-Alat)
        #print(v1,v2,v3,v4)
        return(v1+v2+v3+v4)/(ilon1*ilat1)
    
    elif tipo == 'distancia':
        ond0=onds1[0][inccol+1]
        ond1=onds1[0][inccol]
        ond2=onds2[0][inccol+1]
        ond3=onds2[0][inccol]
        import Geodesia.PIGeodesia as pigeo
        #print(PuntoGeodesico.getLongitud(),lon_calc)
        
        p=pigeo.PIGeodesia(pgeo.PuntoGeodesico(PuntoGeodesico.getLatitud(),lonaux),pgeo.PuntoGeodesico(lat_calc,lon_calc))
        az,dr1=p.CalcularBessel('GRS 1980')
        
        p=pigeo.PIGeodesia(pgeo.PuntoGeodesico(PuntoGeodesico.getLatitud(),lonaux),pgeo.PuntoGeodesico(lat_calc,lon_calc+ilon1))
        az,dr2=p.CalcularBessel('GRS 1980')
        
        p=pigeo.PIGeodesia(pgeo.PuntoGeodesico(PuntoGeodesico.getLatitud(),lonaux),pgeo.PuntoGeodesico(lat_calc+ilat1,lon_calc))
        az,dr3=p.CalcularBessel('GRS 1980')
        
        p=pigeo.PIGeodesia(pgeo.PuntoGeodesico(PuntoGeodesico.getLatitud(),lonaux),pgeo.PuntoGeodesico(lat_calc+ilat1,lon_calc+ilon1))
        az,dr4=p.CalcularBessel('GRS 1980')
        
        az=None
        print((dr1*ond1+dr2*ond0+dr3*ond3+dr4*ond2)/(dr1+dr2+dr3+dr4))
        print(dr1,dr2,dr3,dr4)
        pass





def main():
    p = pgeo.PuntoGeodesico(39.205324, -0.524532)  # Valor PAG: 50.256
    print(CalcularOndulacion(p))
    
    p = pgeo.PuntoGeodesico(39.205324, -0.495632)  # Valor PAG: 50.202
    print(CalcularOndulacion(p)) 
    
    p = pgeo.PuntoGeodesico(39.205324, 0.495632)  # Valor PAG: 48.127
    print(CalcularOndulacion(p))
    
    p = pgeo.PuntoGeodesico(40.505324, 0.495632)  # Valor PAG: 49.689
    print(CalcularOndulacion(p))
    
    p = pgeo.PuntoGeodesico(28.505324, 345.495632)  # Valor PAG:
    print(CalcularOndulacion(p))
    
    p = pgeo.PuntoGeodesico(58.505324, 345.495632)  # Valor PAG:
    print(CalcularOndulacion(p))
    
if __name__ == '__main__':
    main()
