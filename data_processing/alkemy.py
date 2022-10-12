import requests
import os
from datetime import datetime
import pandas as pd

from .decorators import (
    normalize_all_decorator,
    cines_decorator,
    register_decorator,
    to_postgres_decorator,
)
from .logger import create_logger
log = create_logger()


class Alkemy:
    """
    _summary_
    La clase Alkemy provee un conjunto de dataframes y la creacion de directorios para almacenar csv's a partir de id de links provistos.
    contiene un conjunto de metodos decorados que estan programados de acuerdo a las necesitades especificas del desafio.
    
    
    Input: links class dict
        key: nombre de csv
        value: id de GOOGLE spreadsheets (hoja tipo excel)
            ejemplo:
            Del siguiente link
            https://docs.google.com/spreadsheets/d/1PS2_yAvNVEuSY0gI8Nky73TQMcx_G1i18lm--jOGfAA/edit#gid=514147473
            El id correspondiente es:
                1PS2_yAvNVEuSY0gI8Nky73TQMcx_G1i18lm--jOGfAA
    
    """
    def __init__(self, links:dict) -> None:
        
         self.links = links
         self.df = self.create_files()
         
         log.info("Alkemy class instance Dataframe Available from json_files")
         
         
    def create_files(self, xlsx:bool = False):
        #para respetar la condigna y poner los meses en español se crea el siguiente diccionario
        meses = {
            1:'enero',
            2:'febrero',
            3:'marzo',
            4:'abril',
            5:'mayo',
            6:'junio',
            7:'julio',
            8:'agosto',
            9:'septiembre',
            10:'octubre',
            11:'noviembre',
            12:'diciembre' 
        }
        dfs = {}
        for k,v in self.links.items():
            correct_requests = False
            #traer data de links provistos
            try:
                data = requests.get(f'https://docs.google.com/spreadsheets/d/{v}/export/format=xlsx',allow_redirects = True)
                log.info(f"Correct requests {k}")
                correct_requests = True
            except Exception as error:
                log.warning(f"incorrect id in spreadsheet-Google : {k} : {v}. CHECK JSON_FILES, Error: {error}")
                pass
            
            #generacion de path
            date = datetime.today()
            path_mkdir = f'csv_files/{k}/{date.strftime("%Y")}-{meses[date.month]}'
            
            try:
                os.makedirs(path_mkdir)
                log.info(f"mkdir success {path_mkdir}")
            except:
                log.info(f"existing address {path_mkdir}")
                pass
            if correct_requests:
                #carga de datos csv y Dataframe
                path = f'{path_mkdir}/{k}-{date.strftime("%d")}-{date.strftime("%m")}-{date.year}.xlsx'
                open(path,'wb').write(data.content)
                df=pd.read_excel(path)
                df.to_csv(f'{path[:-4]}csv')
                dfs[k]=df
                
                log.info(F"CSV file available {path}")
                if not xlsx:
                    os.remove(path=path)
            
        return dfs
    
    @to_postgres_decorator
    @normalize_all_decorator
    def normalize_df_table(self):
        return self.df.copy()
    
    @to_postgres_decorator
    @cines_decorator
    def cines_df_table(self):
        return self.df.copy()
    
    @to_postgres_decorator
    @register_decorator
    def register_df_tables(self):
        return self.df.copy()
