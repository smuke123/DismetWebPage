from pydantic import BaseModel, EmailStr
from typing import ClassVar, Dict, Any, Optional

class UsuarioBase(BaseModel):
    nombre : str
    correo : EmailStr

class UsuarioCreate(UsuarioBase):
    contrasena: str
    username : str
    direccion : str
    telefono : str

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    correo: Optional[EmailStr] = None
    username: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None   

class CambiarPasswordRequest(BaseModel):
    current_password: str
    new_password: str

class UsuarioResponse(UsuarioBase):
    id: int
    username : str
    direccion : Optional[str] = None
    telefono : Optional[str] = None

    model_config:  ClassVar[Dict[str, Any]] = {
        "from_attributes": True
    }