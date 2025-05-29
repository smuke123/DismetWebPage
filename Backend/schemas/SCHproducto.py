from pydantic import BaseModel
from typing import ClassVar, Dict, Any, Optional

class ProductoBase(BaseModel):
    titulo: str
    descripcion :str
    precio: float
    cantidad: int 


class ProductoCreate(ProductoBase):
    img: str
    categoria: str
    marca: str
    descripcion_corta: str

class ProductoUpdate(BaseModel):
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[float] = None
    img: Optional[str] = None
    categoria: Optional[str] = None
    marca: Optional[str] = None
    descripcion_corta: Optional[str] = None

class ProductoResponse(ProductoBase):
    id: int
    img: str
    categoria: str
    marca: str
    descripcion_corta: str
    
    model_config:  ClassVar[Dict[str, Any]] = {
        "from_attributes": True
    }
