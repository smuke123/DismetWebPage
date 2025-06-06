from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
import bcrypt
from Backend.utils.security import hash_password, verify_password
from Backend.models import Usuario
from Backend import models, schemas
from Backend.database import get_db
from Backend.schemas import SCHusuario
from Backend.routers.oauth import obtener_usuario_actual


router = APIRouter()

# Crear usuario 
@router.post("/", response_model=SCHusuario.UsuarioResponse)
def crear_usuario(usuario: SCHusuario.UsuarioCreate, db: Session = Depends(get_db)):
    usuario_existente = db.query(Usuario).filter(Usuario.correo == usuario.correo).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    hashed_password = bcrypt.hashpw(usuario.contrasena.encode('utf-8'), bcrypt.gensalt()) 

    db_usuario = models.Usuario(
        nombre = usuario.nombre,
        correo = usuario.correo,
        username=usuario.username,
        direccion=usuario.direccion,
        telefono=usuario.telefono,
        contrasena = hashed_password,
        rol = usuario.rol
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

# Obtener todos los usuarios
@router.get("/", response_model=List[SCHusuario.UsuarioResponse])
def obtener_usuarios(db: Session = Depends(get_db)):
    return db.query(Usuario).all()


#eliminar un Usuario
@router.delete("/{usuario_id}")
def eliminar_usuario(usuario_id: int, db: Session=Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    db.delete(usuario)
    db.commit()
    return {"mensaje": f"Usuario con ID {usuario_id} eliminado exitosamente"}

#Editar un Usuario
@router.put("/{usuario_id}", response_model=SCHusuario.UsuarioResponse)
def actualizar_usuario(usuario_id: int, usuario_update: SCHusuario.UsuarioUpdate, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    for attr, value in usuario_update.dict(exclude_unset=True).items():
        setattr(usuario, attr, value)

    db.commit()
    db.refresh(usuario)
    return usuario

#cambiar password
@router.put("/{usuario_id}/password")
def cambiar_password(usuario_id: int, datos: SCHusuario.CambiarPasswordRequest, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if not verify_password(datos.current_password, usuario.contrasena):
        raise HTTPException(status_code=400, detail="Contraseña actual incorrecta")

    usuario.contrasena = hash_password(datos.new_password)
    db.commit()
    return {"msg": "Contraseña actualizada con éxito"}


#Obtener Usuario Actual
@router.get("/me", response_model=SCHusuario.UsuarioResponse)
def get_current_user_info(db: Session = Depends(get_db), current_user: models.Usuario = Depends(obtener_usuario_actual)):
    return current_user