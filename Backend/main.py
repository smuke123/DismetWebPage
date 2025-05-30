from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Backend.database import Base, engine
from Backend import models
from Backend.routers import usuario, producto, oauth, stripe
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Base de datos
models.Base.metadata.create_all(bind=engine)

app.include_router(usuario.router, prefix="/usuarios")
app.include_router(producto.router, prefix="/productos")
app.include_router(oauth.router)
app.include_router(stripe.router)