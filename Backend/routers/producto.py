from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List

from Backend.models import Producto, Usuario
from Backend.database import get_db
from Backend.schemas import SCHproducto
from Backend.routers.oauth import obtener_usuario_actual

router = APIRouter()

#Crear producto
@router.post("/", response_model=SCHproducto.ProductoResponse)
def crear_producto(producto: SCHproducto.ProductoCreate, db: Session = Depends(get_db), 
                   usuario_actual : Usuario = Depends(obtener_usuario_actual)):
    if not usuario_actual.rol:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="No tienes permiso para agregar productos")

    nuevo_produco = Producto(**producto.dict())
    db.add(nuevo_produco)
    db.commit()
    db.refresh(nuevo_produco)
    return nuevo_produco

#Obtener todos los productos
@router.get("/", response_model=List[SCHproducto.ProductoResponse])
def obtener_productos(db:Session = Depends(get_db)):
    return db.query(Producto).all()

#Obtener producto por ID
@router.get("/{producto_id}", response_model=SCHproducto.ProductoResponse)
def obtener_producto(producto_id:int, db:Session=Depends(get_db)):
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

#actualizar producto
@router.put("/{producto_id}", response_model=SCHproducto.ProductoResponse)
def actualizar_producto(producto_id: int,producto_actualizado: SCHproducto.ProductoUpdate , db: Session=Depends(get_db),
                   usuario_actual: Usuario = Depends(obtener_usuario_actual)):
    if not usuario_actual.rol:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="No tienes permiso para actualizar productos")
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    for campo, valor in producto_actualizado.dict().items():
        setattr(producto, campo, valor)
    db.commit()
    db.refresh(producto)
    return(producto)

#eliminar producto
@router.delete("/{producto_id}")
def eliminar_producto(producto_id: int, db: Session=Depends(get_db),
                      usuario_actual: Usuario=Depends(obtener_usuario_actual)):
    if not usuario_actual.rol:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="No tienes permiso para eliminar productos")
    
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db.delete(producto)
    db.commit()
    return {"msg":"Producto eliminado exitosamente"}

@router.post("/{producto_id}/comprar", response_model=SCHproducto.ProductoResponse)
def comprar_producto(producto_id: int, cantidad: int, 
                     db: Session = Depends(get_db),
                     usuario_actual: Usuario = Depends(obtener_usuario_actual)):
   #Para realizar una compra, el usuario debe exisitir y estar registrador 
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    if cantidad <= 0:
        raise HTTPException(status_code=400, detail="La cantidad debe ser positiva")

    if producto.cantidad < cantidad:
        raise HTTPException(status_code=400, detail="No hay suficiente stock disponible")

    producto.cantidad -= cantidad
    db.commit()
    db.refresh(producto)

    return producto
