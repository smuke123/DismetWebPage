from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
import bcrypt
from Backend.utils.security import hash_password, verify_password
from Backend.models import Usuario
from Backend import schemas, models
from Backend.database import get_db

router = APIRouter()

# Crear usuario 
@router.post("/", response_model=schemas.UsuarioResponse)
def crear_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
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
        contrasena = hashed_password
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

# Obtener todos los usuarios
@router.get("/", response_model=List[schemas.UsuarioResponse])
def obtener_usuarios(db: Session = Depends(get_db)):
    return db.query(Usuario).all()

# Obtener usuario por ID
@router.get("/{usuario_id}", response_model=schemas.UsuarioResponse)
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

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
@router.put("/{usuario_id}")
def actualizar_usuario(usuario_id: int, usuario_update: schemas.UsuarioUpdate, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado, compa")

    for attr, value in usuario_update.dict(exclude_unset=True).items():
        setattr(usuario, attr, value)

    db.commit()
    db.refresh(usuario)
    return usuario

#cambiar password
@router.put("/{usuario_id}/password")
def cambiar_password(usuario_id: int, datos: schemas.CambiarPasswordRequest, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if not verify_password(datos.current_password, usuario.contrasena):
        raise HTTPException(status_code=400, detail="Contraseña actual incorrecta")

    usuario.contrasena = hash_password(datos.new_password)
    db.commit()
    return {"msg": "Contraseña actualizada con éxito"}