#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 4/2/2015

@author: Antonio Hermosilla Rodrigo.
@contact: anherro285@gmail.com
@organization: Antonio Hermosilla Rodrigo.
@copyright: (C) 2015 by Antonio Hermosilla Rodrigo
@version: 1.0.0
'''

import sys
sys.path.append('../..')
import os
import sqlite3

class SQLiteManager(object):
    '''!
    Establece una conexión a una base de datos SQLite.
    '''
    __pathdb=None
    __con=None
    __cursor=None


    def __init__(self, *args):
        '''!
        Constructor de la clase Conexion.
        __init__(path)
        @param path str: Ruta a la base de datos a la que se quiere conectar.
        @note path: Si la ruta a la base de datos o la base de datos no existe, esta se creara automáticamente.
        '''
        self.setPathDB(args[0])
        self.__Conectar()
        
    def __del__(self):
        '''!
        '''
        
    def setPathDB(self,path):
        '''!
        @brief: Método que establece el path de la base de datos.
        @param path str: Ruta a la base de datos.
        @note: Si no existe el path a la base de datos se creara automaticamente.
        '''
        
        if not os.path.exists(path):
            path=os.path.normpath(path)
            aux=path.split("/")
            aux.pop()
            path1=""
            path1+="/"
            for i in aux:
                path1+=i
                if os.path.exists(path1):
                    path1+="/"
                    continue
                else:
                    os.mkdir(path1)
                    path1+="/"
            self.__pathdb=path
        else:
            self.__pathdb=path
            
    def __Conectar(self):
        '''!
        '''
        self.__con=sqlite3.connect(self.__pathdb)
        self.__cursor=self.__con.cursor()
    
    def CrearTabla(self,*args):
        '''!
        @brief: Método para crear una tabla en la base de datos, a la que se ha establecido la conexión.
        
        @param nombre_tb str : Nombre de la talba a crear.
        @note nombre_tb: ejemplo: Tabla
        
        @param nombre_campos [str]: Nombre de los campos que se van a crear en la tabla.
        @note nombre_campos: ejemplo: [campo_1,campo_2,campo_3,...,campo_n]
        
        @param tipo_campos [str]: Tipo de formato de los campos que se crearan en la tabla.
        @note tipo_campos: ejemplo: [real,integer,text,...,blob]
        @note tipo_campos: Tiene que haber tantos tipos como capos creados en la tabla.
        
        @param restricciones [str]: Restricciones de los campos creados en la tabla.
        @note restricciones: ejemplo: [not null,,primery key,..,]
        @note restricciones: Tiene que haber tantas restricciones como campos creados en la tabla.
        @note restricciones: si un campo no tiene restricción introducir un str vacío.
        
        Ejemplo:\n
        CrearTabla(nombre_tb,nombre_campos,tipo_campos,restricciones)\n
        CrearTabla('Tabla',['campo1','campo2'],['text','real'],['primary key',''])
        '''
        if len(args)>=3:
            nombre=args[0]
            nombrecampos=args[1]
            tipo=args[2]
            if len(nombrecampos)!=len(tipo):
                raise Exception("El tamaño de los del nombre de los campos y su tipo debe ser coincidente")
            try:
                restriccion=args[3]
                if len(restriccion)!=len(tipo):
                    raise Exception("Introduzca algun tipo de restrccion en todos los campos o "" si no quiere ninguna")
            except:
                restriccion=[""]*len(tipo)
        else:
            raise Exception("El nombre de la tabla, nombre de los campos y el formato de estos, son obligatorios.")
        
        linea1=""
        for i,j,k in zip(nombrecampos,tipo,restriccion):
            linea1+=str(i).lower()+" "+str(j).lower()+" "+str(k).lower()+","
        linea1 = linea1[:-1]
        sentence='''CREATE TABLE '''+nombre +"("+linea1+")"
        self.__cursor.execute(sentence)
        self.__con.commit()
        
    def Consulta(self,consulta):
        '''!
        @brief: Método que ejecuta una consulta SQL sobre la base de datos.
        @param consulta str: Consulta a realizar
        @return: Resultado de la consulta.
        '''
        self.__cursor.execute(consulta)
        return self.__cursor.fetchall()
        pass
        
    def AddRow(self,*args):
        '''!
        @brief: Método que añade una nueva fila (registro) a una tabla de la base de datos.
        @param nombre_tabla str: Nombre de la tabla a la que se quiere añadir la fila (registro).
        @param valores [str]: Valores que se quieren insertar en la nueva fila (registro).
        
        Ejemplo:\n
        AddRow('Tabla',['Bombilla','110','null'])
        '''
        nombre=args[0]
        linea1=",".join(args[1])
        sentence='''INSERT INTO '''+nombre+" values ("+linea1+")"
        print(sentence)
        self.__cursor.execute(sentence)
        self.__con.commit()
        
        
    def AddColumn(self,*args):
        '''!
        @brief: Método que añade una nueva columna (campo) a la base de datos.
        @param nombre_tabla str: Nombre tabla a la que se quiere añadir la columna (campo).
        @param nombre_columna: Nombre de columna (campo) a añadir.
        @param tipo_dato: Tipo de datos de la columna.
        
        Ejemplo:\n
        AddColum('Tabla','Potencia','real')
        '''
        tabla=args[0]
        nombre=args[1]
        tipo=args[2]
        sentence='''ALTER TABLE '''+tabla+" add column "+nombre+" "+tipo
        self.__cursor.execute(sentence)
        self.__con.commit()
    
    def ModifyValue(self,*args):
        '''!
        @brief: Método que modifica un valor de un registro de la base de datos.
        @param nombre_tabla str: Nombre tabla.
        @param nombre_columna str: Nombre columna.
        @param numero_registro str: id del elemento.
        @param nuevo_valor str: Nuevo valor
        Ejemplo:\n
        ModifyValue('Tabla','Columna','25','Coche')
        '''
        tabla=args[0]
        nombre=args[1]
        iden=args[2]
        value=args[3]
        sentence='''UPDATE '''+tabla+" set "+nombre+"="+value+" where rowid="+iden
        print(sentence)
        self.__cursor.execute(sentence)
        self.__con.commit()
        
        
        
        
    def ObtenerTodo(self,tabla):
        '''!
        @brief: Método que devuelve toda la información de una tabla de la base de datos.
        @param tabla str: Nombre de la tabla de la que se quiere obtener la información.
        @return: Todos los registros de la tabla.
        '''
        sentence='''SELECT * FROM  ''' + tabla
        self.__cursor.execute(sentence)
        return self.__cursor.fetchall()
        pass
    
    def ObtenerFila(self,tabla,idfila):
        '''!
        '''
        sentence='''SELECT * FROM '''+tabla+" WHERE rowid="+idfila
        self.__cursor.execute(sentence)
        return self.__cursor.fetchall()
        pass
    
    def ObtenerColumna(self,tabla,columna):
        '''!
        @brief: Método que devuleve todos los valores de una columna (campo).
        @param tabla str: Nombre de la tabla de la que se quere obtener la columna.
        @param columna str: Nombre de la columna a obtener.
        Ejemplo:\n
        ObtenerColumna('Tabla','Columna')
        '''
        sentence='''SELECT ''' + columna +" FROM "+tabla
        self.__cursor.execute(sentence)
        return self.__cursor.fetchall()
        pass
        
    def BorrarDB(self):
        '''!
        @brief: Método que borra la base de datos a la que se está conectado.
        '''
        self.__cursor=None
        self.__con.close()
        self.__con=None
        os.remove(self.path)
        pass
        
    def BorrarTabla(self,tabla):
        '''!
        @brief: Método que borra una tabla de la base de datos.
        @param tabla str: Nombre de la tabla a borrar.
        '''
        sentence='''DROP TABLE IF EXISTS ''' +tabla
        self.__cursor.execute(sentence)
        self.__con.commit()
        pass

        
            
            
            
            
def main():
    #### Parametros Cambio de marco. ####
    db=SQLiteManager("/home/toni/Dropbox/pyGeo/Geodesia/CambiosMarco.db")
#     db.CrearTabla('Parametros',\
#                   ["Origen","Destino","Tx","Ty","Tz","d","Rx","Ry","Rz","t0","rTx","rTy","rTz","rd","rRx","rRy","rRz"],\
#                   ["text","text","real","real","real","real","real","real","real","real","real","real","real","real","real","real","real"])
    db.AddRow("Parametros",\
              ["'ITRF93'","'ITRF89'",\
               "1.9","4.1","-5.3","0.39E-8","1.8907733563272E-9","-3.8785094488763E-9","4.6542113386515E-9","1988.0",\
               "0.29","-0.04","-0.08","0.0","5.3329504922049E-10","9.2114599410812E-10","-2.4240684055477E-10"])


    #### Base de datos valores EMG Peninsula y baleares. ####
#     db=SQLiteManager("/home/toni/Dropbox/pyGeo/Geodesia/EGM/EGM_Peninsula.db")
#     db.CrearTabla('Cabecera',\
#                   ["TLLatitude","TRLongitud","IncrementoLatitud","IncrementoLongitud","Filas","Columnas"],\
#                   ["real","real","real","real","real","real"])
#     f=open('/home/toni/Dropbox/pyGeo/Geodesia/EGM/EGM08_REDNAP.txt','r')
#     lin=f.readline()
#     lin=lin.split()
#     print(lin)
#     ilat=float(lin[2])/60
#     ilon=float(lin[3])/60
#     db.AddRow("Cabecera",[str(lin[0]),str(lin[1]),str(ilat),str(ilon),str(lin[4]),str(lin[5])])
#     vals=[]
#     for i in range(int(lin[5])):
#         name='ond_'+str(i+1)
#         vals.append(name)
#          
#     vals1=["real"]*len(vals)
#  
#     db.CrearTabla('Ondulaciones',\
#                   vals,\
#                   vals1)
#     const=85
#     seguir=True
#     while seguir:
#         try:
#             onds=[]
#             lins=[f.readline() for _ in range(const)]
#             for i in lins:
#                 i=i.split()
#                 for j in i:
#                     onds.append(j)
#             db.AddRow('Ondulaciones',\
#                       onds)
#              
#         except:
#             seguir=False




#### Base de datos valores EMG Canarias. ####
#     db=SQLiteManager("/home/toni/Dropbox/pyGeo/Geodesia/EGM/EGM_Canarias.db")
#     db.CrearTabla('Cabecera',\
#                   ["TLLatitude","TRLongitud","IncrementoLatitud","IncrementoLongitud","Filas","Columnas"],\
#                   ["real","real","real","real","real","real"])
#     f=open('/home/toni/Dropbox/pyGeo/Geodesia/EGM/EGM08_REDNAP_Canarias.txt','r')
#     lin=f.readline()
#     lin=lin.split()
#     print(lin)
#     ilat=float(lin[2])/60
#     ilon=float(lin[3])/60
#     db.AddRow("Cabecera",[str(lin[0]),str(lin[1]),str(ilat),str(ilon),str(lin[4]),str(lin[5])])
#     vals=[]
#     for i in range(int(lin[5])):
#         name='ond_'+str(i+1)
#         vals.append(name)
#           
#     vals1=["real"]*len(vals)
#   
#     db.CrearTabla('Ondulaciones',\
#                   vals,\
#                   vals1)
#     const=34
#     seguir=True
#     while seguir:
#         try:
#             onds=[]
#             lins=[f.readline() for _ in range(const)]
#             for i in lins:
#                 i=i.split()
#                 for j in i:
#                     onds.append(j)
#             db.AddRow('Ondulaciones',\
#                       onds)
#               
#         except:
#             seguir=False




    
    
    #####Base de datos Elipsoides ####
#     db=SQLiteManager("/home/toni/Dropbox/pyGeo/Geodesia/Elipsoides/Elipsoides.db")
#     db.AddRow("Elipsoides",["'Hayford 1950'","6378388.0","NULL","297.0","NULL","NULL","NULL"])
#     db.AddRow("Elipsoides",["'PZ-90'","6378136.0","NULL","298.257839303","3.9860044E14","7.292115E-5","-1.08262575E-3"])
    
#     db.AddColumn("Elipsoides","GM","real")
#     db.AddColumn("Elipsoides","we","real")
#     db.AddColumn("Elipsoides","J2","real")

#     db.ModifyValue("Elipsoides","GM","18","3986005E8")
#     db.ModifyValue("Elipsoides","we","18","7292115E-11")
#     db.ModifyValue("Elipsoides","J2","18","-108263E-8")
#   
#     db.ModifyValue("Elipsoides","GM","27","3.986004418E14")
#     db.ModifyValue("Elipsoides","we","27","7.292115E-5")
#     db.ModifyValue("Elipsoides","J2","27","-1.081874E-3")
    
    #print(db.ObtenerColumna("Nombre", "Elipsoides"))
#     db.BorrarTabla("Elipsoides")
#     db.CrearTabla("Elipsoides "\
#                   ,["Nombre","a","b","f"]\
#                   ,["text","real","real","real"])
# 
#     fi=open('/home/toni/table.csv')
#     fi.readline()
#     for i in fi:
#         i=i.split(";")
#         
#         try:
#             a=i[2].replace(",",".")
#             a=float(a)
#             a=str(a)
#         except Exception:
#             a="NULL"
#             
#         try:
#             b=i[5].replace(",",".")
#             b=float(b)
#             b=str(b)
#         except Exception:
#             b="NULL"
#             
#         try:
#             f=i[4].replace(",",".")
#             f=float(f)
#             f=str(f)
#         except Exception:
#             f="NULL"
#         
#         db.AddRow("Elipsoides",[i[1],a,b,f])
#     fi.close()

    #db.AddRow("Lineas2D",["20","30","20","50"])
    #print(db.ObtenerColumna("X1", "Lineas2D"))
    
    #print(db.ObtenerTodo("Elipsoides"))
    #db.BorrarTabla("Lineas2D")
if __name__ == "__main__":
    main()