from pydantic import BaseModel
from typing import ClassVar, Dict, Any, Optional

class ProductoBase(BaseModel):
    titulo: str
    descripcion :str
    precio: float

class ProductoCreate(ProductoBase):
    img: str
    categoria: str
    marca: str
    descripcion_corta: str



class ProductoResponse(ProductoBase):
    id: int

    model_config:  ClassVar[Dict[str, Any]] = {
        "from_attributes": True
    }
