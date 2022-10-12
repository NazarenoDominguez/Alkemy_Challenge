from sqlalchemy import TIMESTAMP, Column, String, Integer
from sqlalchemy.sql.expression import text
from models import Base


# SCHEMAS para querys

class SQL_Alk_museos_cines_bibliotecas(Base):
    __tablename__ = 'museos_cines_bibliotecas'
    
    id_centro_recreativo = Column(Integer, primary_key = True, nullable = False)
    cod_localidad = Column(String, nullable = False)
    fecha_carga = Column(TIMESTAMP(timezone=True),nullable = False, server_default = text('now()'))
    id_provincia = Column(Integer, nullable = False)
    id_departamento = Column(Integer, nullable = False)
    categoria = Column(String, nullable = False)
    provincia = Column(String, nullable = False)
    localidad = Column(String, nullable = False)
    nombre = Column(String, nullable = False)
    direccion = Column(String)
    codigo_postal = Column(String)
    telefono = Column(String)
    mail = Column(String)
    web = Column(String)
    


class SQL_Alk_registros_categoria(Base):
    __tablename__ = 'registros_categoria'
    
    categoria = Column(String, primary_key = True, nullable = False)
    cantidad_registros = Column(Integer, nullable = False)
    fecha_carga = Column(TIMESTAMP(timezone=True),nullable = False, server_default = text('now()'))
    

class SQL_Alk_registros_fuente(Base):
    __tablename__ = 'registros_fuente'
    
    fuente = Column(String, primary_key = True, nullable = False)
    cantidad_registros = Column(Integer, nullable = False)
    fecha_carga = Column(TIMESTAMP(timezone=True),nullable = False, server_default = text('now()'))



class SQL_Alk_registros_provincia_categoria(Base):
    __tablename__ = 'registros_provincia_categoria'
    
    id_provincia_categoria = Column(Integer, primary_key = True, nullable = False)
    provincia = Column(String, nullable = False)
    categoria = Column(String, nullable = False)
    cantidad_registros = Column(Integer, nullable = False)
    fecha_carga = Column(TIMESTAMP(timezone=True),nullable = False, server_default = text('now()'))


class SQL_Alk_cines_provincia(Base):
    __tablename__ = 'cines_provincia'
    
    provincia = Column(String, primary_key = True, nullable = False)
    pantallas = Column(Integer,  nullable = False)
    butacas = Column(Integer,  nullable = False)
    espacio_incaa = Column(Integer,  nullable = False)
    fecha_carga = Column(TIMESTAMP(timezone=True),nullable = False, server_default = text('now()'))

