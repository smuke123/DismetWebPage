from pydantic import BaseModel, EmailStr
from typing import ClassVar, Dict, Any

class UsuarioBase(BaseModel):
    nombre : str
    correo : EmailStr

class UsuarioCreate(UsuarioBase):
    contrasena: str
    username : str
    direccion : str
    telefono : str

class UsuarioResponse(UsuarioBase):
    id: int

    cmodel_config:  ClassVar[Dict[str, Any]] = {
        "from_attributes": True
    }