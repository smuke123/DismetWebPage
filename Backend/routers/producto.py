from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from Backend.models import Producto
from Backend.database import get_db
from Backend.schemas import SCHproducto

router = APIRouter()

#Crear producto
@router.post("/", response_model=SCHproducto.ProductoResponse)
def crear_producto(producto: SCHproducto.ProductoCreate, db: Session = Depends(get_db)):
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
def actualizar_producto(producto_id: int,producto_actualizado: SCHproducto.ProductoUpdate , db: Session=Depends(get_db)):
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
def eliminar_producto(producto_id: int, db: Session=Depends(get_db)):
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db.delete(producto)
    db.commit()
    return {"msg":"Producto eliminado exitosamente"}