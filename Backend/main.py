from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from jose import jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Security
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Security(oauth2_scheme)):
    return {"message": f"Bienvenido, {token}"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_CALLBACK_URL = os.getenv("GOOGLE_CALLBACK_URL")
SECRET_KEY = os.getenv("SECRET_KEY", "secretazo123")
ALGORITHM = "HS256"
@app.get("/", response_class=HTMLResponse)
async def root():
    return '<a href="/auth/google">Iniciar sesión con Google</a>'

@app.get("/auth/google")
async def auth_google():
    # Redireccionar a Google para autenticación
    google_auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth"
        f"?response_type=code"
        f"&client_id={GOOGLE_CLIENT_ID}"
        f"&redirect_uri={GOOGLE_CALLBACK_URL}"
        f"&scope=openid email profile"
        f"&access_type=offline"
    )
    return RedirectResponse(url=google_auth_url)

@app.get("/auth/google/callback")
async def google_callback(code: str):
    # Recibimos el código de autorización y pedimos tokens a Google
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

    # Decodificamos y validamos el id_token
    try:
        payload = jwt.decode(id_token, options={"verify_signature": False})
        if payload.get("aud") != GOOGLE_CLIENT_ID:
            raise HTTPException(status_code=400, detail="Token inválido")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al validar token: {e}")

    #Funcion pendiente para conectar a la BD

    # Generamos un JWT propio para la app
    user_email = payload.get("email")
    user_name = payload.get("name")

    # JWT simplificado
    user_token = jwt.encode({"sub": user_email}, SECRET_KEY, algorithm=ALGORITHM)

    # En vez de redirect a perfil, mandamos un JSON con token y usuario
    return {"access_token": user_token, "email": user_email, "name": user_name}

@app.get("/profile")
async def profile(token: str = Depends(get_current_user)):
    # Aquí validarías tu JWT para proteger la ruta
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email = payload.get("sub")
        return {"message": f"Bienvenido, {user_email}"}
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido")