import unidecode
import numpy as np
import pandas as pd
import unidecode

from models import engine
from models import SessionLocal

from models.tables import (
    SQL_Alk_museos_cines_bibliotecas,
    SQL_Alk_registros_categoria,
    SQL_Alk_registros_fuente,
    SQL_Alk_registros_provincia_categoria,
    SQL_Alk_cines_provincia,
)

from .logger import create_logger
log = create_logger()

def normalize_all_decorator(func_df):
    """_summary_
    
        funcion decoradora para datos globales estandarizados, es la encargada de concatenar los DataFrame, agregarles un modelo sql_alkemy
        y realizar los filtros correspondientes.
        en este decorador en concreto tenemos:
            registros de todos los dataframe con columnas:
            
                'cod_localidad', 
                'id_provincia', 
                'id_departamento', 
                'categoria', 
                'provincia',
                'localidad', 
                'nombre', 
                'direccion', 
                'codigo_postal', 
                'telefono', 
                'mail', 
                'web'
                
        a los modelos se los pruebe buscar en models.tables
        
        input: dict{
            DataFrame_name: DataFrame,
            ...,
            DataFrame_name: DataFrame,
        }
    """
    
    def normalize(*args, **qwargs):
        dfs = func_df(*args, **qwargs)
        
        log.info("runing custom decorador 'normalize_all_decorator'")
        
        df = {}
        
        try:
            
            for i in dfs.keys():
                dfs[i].columns = [unidecode.unidecode(s).lower() for s in list(dfs[i].columns)]
                if i == 'bibliotecas':
                    #este dataframe no esta estandarizado como los demas cambio de nombre de columna de comicilio a direccion
                    dfs[i].columns = ['direccion' if x=='domicilio' else x for x in dfs[i].columns]
                
                try:
                    #poner codigo de area entre parentesis al lado del telefono (sino se pierde info crucial de contacto)
                    dfs[i]['telefono'] = (dfs[i]['cod_area'].astype(str).map(lambda x: f'({x[:-2]})-') + dfs[i]['telefono'].astype(str)).map(lambda x: np.nan if x[-1] == 'n' else x)
                except:
                    pass
                dfs[i]=dfs[i][['cod_loc', 'idprovincia', 'iddepartamento', 'categoria', 'provincia', 'localidad', 'nombre', 'direccion', 'cp', 'telefono', 'mail', 'web']]
        
            df = pd.concat([dfs['museos'],pd.concat([dfs['cines'],dfs['bibliotecas']],join="inner")],join="inner")
            df = df.replace(['s/d'], np.nan)
            #renombrando clumnas de acuerdo a consigna
            df.columns = [
                'cod_localidad', 
                'id_provincia', 
                'id_departamento', 
                'categoria', 
                'provincia',
                'localidad', 
                'nombre', 
                'direccion', 
                'codigo_postal', 
                'telefono', 
                'mail', 
                'web'
                ]
            df = {
                'museos_cines_bibliotecas':{
                    'data': df,
                    'model': SQL_Alk_museos_cines_bibliotecas
                }
            }
            
            
            log.info("custom modification completed")
        except Exception as error:
            log.warning(f"Error in costum modification. Error detail : {error}")
            pass
        

        
        return df
    return normalize

def cines_decorator(func_df):
    """_summary_

        funcion decoradora para cines, es la encargada de buscar data de cines en los DataFrame, agregarles un modelo sql_alkemy
        y realizar los filtros correspondientes.
        en este decorador en concreto tenemos:
            agrupar por provincia y hacer una cuenta de la cantidad ('provincia','pantallas','butacas','espacio_incaa')
        a los modelos se los pruebe buscar en models.tables
        
        input: dict{
            DataFrame_name: DataFrame,
            ...,
            DataFrame_name: DataFrame,
        }
    """
    
    
    def cines_table(*args,**qwargs):
        cines = func_df(*args, **qwargs)['cines']
        
        log.info("runing custom decorador 'cines_decorator'")
        
        df_count_cines = {}
        
        try:
            #columnas en minuscula y agrupacion
            cines.columns = [unidecode.unidecode(s).lower() for s in list(cines.columns)]
        
            df_count_cines = pd.DataFrame(cines.groupby(['provincia']).count()).reset_index()
            df_count_cines = df_count_cines[['provincia','pantallas','butacas','espacio_incaa']]

            #cargar modelo
            df_count_cines = {
                'cines_provincia':{
                    'data': df_count_cines,
                    'model': SQL_Alk_cines_provincia
                }   
            }
            
            log.info("custom modification completed")
        except Exception as error:
            log.warning(f"Error in costum modification. Error detail : {error}")
            pass
        
        
        
        
        return df_count_cines
    return cines_table



def register_decorator(func_df):
    """_summary_
    funcion decoradora para registros, es la encargada de concatenar los DataFrame, agregarles un modelo sql_alkemy
    y realizar los filtros correspondientes.
    en este decorador en concreto tenemos:
        agrupar por categorias y hacer una cuenta de la cantidad de registros
        agrupar por fuente y hacer una cuenta de la cantidad de registros
        agrupar por rpovincia y categoria y hacer una cuenta de la cantidad de registros
    a los modelos se los pruebe buscar en models.tables
    
    input: dict{
            DataFrame_name: DataFrame,
            ...,
            DataFrame_name: DataFrame,
        }
        
    """
    def register_tables(*args,**qwargs):
        
        dfs = func_df(*args, **qwargs)
        
        df_count = {}
        
        log.info("runing custom decorador 'register_decorator'")
        
        try:
            for i in dfs.keys():
                #pasar columnas a minuscula
                dfs[i].columns = [unidecode.unidecode(s).lower() for s in list(dfs[i].columns)]
            #concatenar todo
            df_main = pd.concat([dfs['museos'],pd.concat([dfs['cines'],dfs['bibliotecas']],join="inner")],join="inner")

            #agrupaciones y cargas de modelo
            df_count_categorie = pd.DataFrame(df_main.groupby(['categoria'])['cod_loc'].count()).reset_index()
            df_count_categorie.columns = ['categoria','cantidad_registros']
            df_count['registros_categoria'] = {
                'data': df_count_categorie,
                'model': SQL_Alk_registros_categoria
            }
            

            df_count_fuente = pd.DataFrame(df_main.groupby(['fuente'])['cod_loc'].count()).reset_index()
            df_count_fuente.columns = ['fuente','cantidad_registros']
            df_count['registros_fuente'] = {
                'data': df_count_fuente,
                'model': SQL_Alk_registros_fuente
            }
            
            df_count_categoria_provincia = pd.DataFrame(df_main.groupby(['provincia','categoria'])['cod_loc'].count()).reset_index()
            df_count_categoria_provincia.columns = ['provincia','categoria','cantidad_registros']
            df_count_categoria_provincia
            df_count['registros_provincia_categoria'] = {
                'data': df_count_categoria_provincia,
                'model': SQL_Alk_registros_provincia_categoria
            }
            
            log.info("custom modification completed")
        except Exception as error:
            log.warning(f"Error in costum modification. Error detail : {error}")
            pass


        return df_count
        
    return register_tables





def to_postgres_decorator(func_df):
    """_summary_
    esta funcion es la encargada de subir los dataframe a la base de datos.
    si la tabla en base de datos ya existe entonces se respetara el modelo de la misma, manteniendo las restricciones y tipos de datos
    en caso de que no se haya creado la misma se subira con un formato estandar.
    por esta razon es importante que el nombre dado al diccionario corresponda a la tabla en POSTGRES

    Args:
        func_df (_type_:dict[data:DataFrame,model: sql_alkemy_model]): _description_
        el input debe contener in diccionario con la siguiente estructura:
        {
            nombre_de_tabla:
            {
                data: DataFrame,
                model: sql_alkemy_model
            }
            ...
            nombre_de_tabla:
            {
                data: DataFrame,
                model: sql_alkemy_model
            }
        }
    """
    def update_postgres_data(*args,**qwargs):
        
        df_dict = func_df(*args, **qwargs)
        
        for name,data_model in df_dict.items():
            db = SessionLocal()
            try:  
                #llamada a modelo generado por los decoradores previos
                data = db.query(data_model['model'])
            except:
                log.warning(f"the table does not exist {data_model['model']}")
            if data.first() == None:
                try:
                    #subida de datos
                    data_model['data'].to_sql(name, con = engine, index = False, if_exists = 'append', chunksize = 1)
                    log.info(f"uploaded data to POSTGRESQL {name}")
                except Exception as error:
                    log.warning(f"DataFrame.to_sql ERROR : Check engine  error {error}")
                    pass
                
            else:
                #si ya hay datos borrarlos todos y subirlos de vuelta
                #no se utiliza .to_sql(if_exists = 'replace') por que quita todo el formato que le damos a la tabla en los archivos .sql
                log.info("there is data in the database - deleting data to reload")
                data.delete(synchronize_session = False)
                db.commit()
                
                try:
                    #carga de datos posterior a borrado
                    data_model['data'].to_sql(name, con = engine, index = False, if_exists = 'append', chunksize = 1)
                    log.info(f"uploaded data to POSTGRESQL {name}")
                except Exception as error:
                    log.warning(f"DataFrame.to_sql ERROR : Check engine  error {error}")
                    pass
                
            db.close()
        
        return df_dict
    return update_postgres_data
