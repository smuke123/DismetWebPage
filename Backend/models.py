from sqlalchemy import Column, Integer, String, DECIMAL, Text
from Backend.database import Base

class Usuario(Base):
    __tablename__ = "Usuario"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(100), nullable=False, unique= True)
    username = Column(String(50), unique=True, nullable=False)
    direccion = Column(String(200))
    telefono = Column(String(20))
    contrasena = Column(String(100), nullable=False)

class Producto(Base):
    __tablename__ = "Producto"

    id = Column(Integer, primary_key=True, index=True)
    img = Column(String(255))
    categoria = Column(String(100))
    marca = Column(String(100))
    titulo = Column(String(150), nullable=False)
    descripcion_corta = Column(String(255))
    precio = Column(DECIMAL(10, 2), nullable=False)
    descripcion = Column(Text)