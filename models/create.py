from models import cursor
from .logger import create_logger

log = create_logger()

def mk_sql():
    """_summary_
    esta funcion se encarga de ejecutar cada archivo .sql (tablas) y generarlas automaticamente para la posterior carga de datos
    """
    try:
        with open(r'sql_files\tabla_museos_cines_bibliotecas.sql', 'r') as myfile:
            data = myfile.read()
            cursor.execute(data)
            log.info("table 'tabla_museos_cines_bibliotecas.sql' created")
    except:
        log.warning("SyntaxError: invalid syntax for 'tabla_museos_cines_bibliotecas.sql'")
        pass
    try:
        with open(r'sql_files\tabla_cines_provincia.sql', 'r') as myfile:
            data = myfile.read()
            cursor.execute(data)
            
            log.info("table 'tabla_cines_provincia.sql' created")
    except:
        log.warning("SyntaxError: invalid syntax for 'tabla_cines_provincia.sql'")
        pass
    try:
        with open(r'sql_files\tabla_registros_categoria.sql', 'r') as myfile:
            data = myfile.read()
            cursor.execute(data)
            
            log.info("table 'tabla_registros_categoria.sql' created")
    except:
        log.warning("SyntaxError: invalid syntax for 'tabla_registros_categoria.sql'")
        pass
    try:
        with open(r'sql_files\tabla_registros_fuente.sql', 'r') as myfile:
            data = myfile.read()
            cursor.execute(data)
            
            log.info("table 'tabla_registros_fuente.sql' created")
    except:
        log.warning("SyntaxError: invalid syntax for 'tabla_registros_fuente.sql'")
        pass
    try:
        with open(r'sql_files\tabla_registros_provincia_categoria.sql', 'r') as myfile:
            data = myfile.read()
            cursor.execute(data)
            
            log.info("table 'tabla_registros_provincia_categoria.sql' created")
    except:
        log.warning("SyntaxError: invalid syntax for 'tabla_registros_provincia_categoria.sql'")
        pass
    
    cursor.close()
        
    