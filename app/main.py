import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import JSONResponse
from twilio.rest import Client

app = FastAPI()

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

@app.post("/whatsapp-webhook")
async def whatsapp_webhook(
    request: Request,# Lecture des variables d'environnement
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_WHATSAPP_FROM")  # ✅ bon nom

    From: str = Form(...),
    Body: str = Form(...)
):
    print(f"📥 Message reçu de {From} : {Body}")

    # Exemple de réponse
    message_texte = (
        "👋 Bienvenue chez Askley !\n"
        "1️⃣ Réserver un hôtel\n"
        "2️⃣ Réserver un restaurant\n"
        "3️⃣ Aide"
    )

    try:
        message = client.messages.create(
            from_=TWILIO_PHONE_NUMBER,  # Correctement injecté depuis l'env
            body=message_texte,
            to=From
        )
        print(f"📤 Réponse : {message_texte}")
    except Exception as e:
        print(f"❌ Erreur : {e}")
        return JSONResponse(content={"error": str(e)}, status_code=400)

    return {"status": "ok"}
