from fastapi import APIRouter, HTTPException, Request, Depends
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from pydantic import BaseModel
import stripe
import os

from Backend.models import Usuario, Pago
from Backend.database import get_db


load_dotenv()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
STRIPE_PUBLIC_KEY = os.getenv("STRIPE_PUBLIC_KEY")
endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

router = APIRouter(prefix="/stripe", tags=["Stripe"])

class PagoRequest(BaseModel):
   total: float #Total en COP

@router.post("/crear-pago/")
def crear_pago(data: PagoRequest):
  
    try:
        total_cop = data.total
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'cop',
                    'product_data': {
                        'name': 'Compra en Dismet',
                    },
                    'unit_amount': int(total_cop * 100),  #en centavos COP
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://localhost:3000/',
            cancel_url='http://localhost:3000/',
        )

        return {"url": checkout_session.url}
    except Exception as e:
        return {"error": str(e)}
    
@router.post("/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        # Invalid payload
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        raise HTTPException(status_code=400, detail="Invalid signature")

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        # Se obtiene toda la info del pago:
        customer_email = session.get("customer_details", {}).get("email")
        amount_total = session.get("amount_total")  # en centavos
        payment_intent = session.get("payment_intent")

        usuario = db.query(Usuario).filter(Usuario.correo == customer_email).first()

        if usuario:
            nuevo_pago = Pago(
                usuario_id=usuario.id,
                monto=amount_total,
                payment_intent_id=payment_intent
            )
            db.add(nuevo_pago)
            db.commit()
            db.refresh(nuevo_pago)
            print(f"Pago registrado para {usuario.nombre} - {amount_total} COP")
        else:
            print(f"Usuario con correo {customer_email} no encontrado")

    return {"status": "success"}

@router.get("/pagos/{usuario_id}")
def obtener_pagos(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    pagos = db.query(Pago).filter(Pago.usuario_id == usuario_id).all()
    return[
        {
            "id": pago.id,
            "monto": pago.monto / 100,  # Convertimos a pesos
            "payment_intent_id": pago.payment_intent_id
        }
        for pago in pagos
    ]

# Testeo de agregar pago 
from fastapi import Body

@router.post("/test/agregar-pago/")
def test_agregar_pago(
    usuario_id: int = Body(...),
    monto: int = Body(...),  # en centavos
    payment_intent_id: str = Body(...),
    db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    nuevo_pago = Pago(
        usuario_id=usuario.id,
        monto=monto,
        payment_intent_id=payment_intent_id
    )
    db.add(nuevo_pago)
    db.commit()
    db.refresh(nuevo_pago)

    return {
        "mensaje": "Pago de prueba guardado con éxito",
        "pago": {
            "id": nuevo_pago.id,
            "usuario_id": nuevo_pago.usuario_id,
            "monto": nuevo_pago.monto / 100,
            "payment_intent_id": nuevo_pago.payment_intent_id
        }
    }
