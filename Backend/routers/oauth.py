from fastapi import APIRouter, Request, HTTPException, Depends, Body
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi import Security
from jose import jwt, JWTError # type: ignore
import httpx
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from Backend.database import get_db
from Backend import models
from Backend.utils.security import verify_password, create_access_token

load_dotenv()

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_CALLBACK_URL = os.getenv("GOOGLE_CALLBACK_URL")
SECRET_KEY = os.getenv("SECRET_KEY", "secretazo123")
ALGORITHM = "HS256"

async def get_current_user(token: str = Security(oauth2_scheme)):
    return {"message": f"Bienvenido, {token}"}

@router.get("/", response_class=HTMLResponse)
async def root():
    return '<a href="/auth/google">Iniciar sesión con Google</a>'

@router.get("/auth/google")
async def auth_google():
    google_auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth"
        f"?response_type=code"
        f"&client_id={GOOGLE_CLIENT_ID}"
        f"&redirect_uri={GOOGLE_CALLBACK_URL}"
        f"&scope=openid email profile"
        f"&access_type=offline"
    )
    return RedirectResponse(url=google_auth_url)


@router.get("/auth/google/callback")
async def google_callback(code: str, db: Session = Depends(get_db)):
    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "redirect_uri": GOOGLE_CALLBACK_URL,
                "grant_type": "authorization_code",
            }
        )

    token_json = token_response.json()
    id_token = token_json.get("id_token")
    if not id_token:
        raise HTTPException(status_code=400, detail="No se recibió id_token de Google")

    try:
        payload = jwt.decode(id_token,key='', options={"verify_signature": False, "verify_at_hash": False}, audience=GOOGLE_CLIENT_ID)

        if payload.get("aud") != GOOGLE_CLIENT_ID:
            raise HTTPException(status_code=400, detail="Token inválido")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al validar token: {e}")

    user_email = payload.get("email")
    user_name = payload.get("name")
    user_username = user_email.split('@')[0]
    # Verificar si el usuario ya existe
    db_user = db.query(models.Usuario).filter(models.Usuario.correo == user_email).first()
    if not db_user:
        nuevo_usuario = models.Usuario(nombre=user_name, correo=user_email, username = user_username)
        db.add(nuevo_usuario)
        db.commit() 
        db.refresh(nuevo_usuario)

    user_token = jwt.encode({"sub": str(db_user.id)}, SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token": user_token, "email": user_email, "name": user_name}


@router.get("/profile")
async def profile(token: str = Depends(get_current_user)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email = payload.get("sub")
        return {"message": f"Bienvenido, {user_email}"}
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido")

#Autenticar usuario

def obtener_usuario_actual(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

    usuario = db.query(models.Usuario).filter(models.Usuario.correo == (email)).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

#Log in

@router.post("/login")
def login(data: dict = Body(...), db: Session = Depends(get_db)):
    email = data.get("email")
    password = data.get("password")
    usuario = db.query(models.Usuario).filter(models.Usuario.correo == email).first()
    if not usuario:
        raise HTTPException(status_code=400, detail="Correo o contraseña incorrectos")
    if not verify_password(password, usuario.contrasena):
        raise HTTPException(status_code=400, detail="Correo o contraseña incorrectos")
    
    token = create_access_token(data={"sub": usuario.correo})
    return {"access_token": token, "token_type": "bearer"}
