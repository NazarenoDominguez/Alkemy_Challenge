from data_processing.alkemy import Alkemy
from models.create import mk_sql
import json

if __name__ == '__main__':
    
    with open(r'json_files\links.json') as js:
        links = json.load(js)
    
    mk_sql()
    alkemy = Alkemy(links=links)
    
    tabla_modelo_global_normalizada = alkemy.normalize_df_table()
    tabla_modelo_cines = alkemy.cines_df_table()
    tabla_modelo_registros = alkemy.register_df_tables()
    