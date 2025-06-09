
from fastapi import FastAPI, Request, Form
from fastapi.responses import JSONResponse
from twilio.rest import Client
import os

app = FastAPI()

# Initialiser le client Twilio avec les variables d'environnement
twilio_sid = os.getenv("TWILIO_ACCOUNT_SID")
twilio_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_from = os.getenv("TWILIO_PHONE_NUMBER")

client = Client(twilio_sid, twilio_token)

@app.post("/whatsapp-webhook")
async def whatsapp_webhook(
    request: Request,
    From: str = Form(...),
    Body: str = Form(...)
):
    print(f"📥 Message reçu de {From} : {Body}")

    # Logique de réponse simple
    if "bonjour" in Body.lower():
        response = (
            "👋 Bienvenue chez Askley !\n"
            "1️⃣ Réserver un hôtel\n"
            "2️⃣ Réserver un restaurant\n"
            "3️⃣ Aide"
        )
    elif Body.strip() == "1":
        response = "🏨 Super ! Envoyez-moi le nom de la ville et les dates pour réserver un hôtel."
    elif Body.strip() == "2":
        response = "🍽️ Très bien ! Envoyez-moi le type de cuisine ou le nom du restaurant."
    else:
        response = "🤖 Je n'ai pas compris. Envoyez 'Bonjour' pour démarrer."

    # Envoi de la réponse via Twilio
    try:
        client.messages.create(
            from_=f"whatsapp:{twilio_from}",
            to=From,
            body=response
        )
    except Exception as e:
        print(f"❌ Erreur : {e}")
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=400)

    print(f"📤 Réponse envoyée à {From} : {response}")
    return {"status": "success"}
