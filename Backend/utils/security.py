from datetime import datetime, timedelta
from jose import jwt # type: ignore
from passlib.context import CryptContext

#Funciones para verificar la contraseña de forma segura
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password (password: str)->str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str)->bool:
    return pwd_context.verify(plain_password, hashed_password)

# Clave secreta (no la compartas con nadie)
SECRET_KEY = "3kNpuIybwh-KdLHV-V0AVYO7mLhZsNGFl5eTxqAjAL0"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
