from fastapi import FastAPI, Request, Form
from fastapi.responses import JSONResponse
from twilio.rest import Client
import os

app = FastAPI()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")  # whatsapp:+14155238886

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

@app.post("/whatsapp-webhook")
async def whatsapp_webhook(
    request: Request,
    From: str = Form(...),
    Body: str = Form(...)
):
    print(f"📥 Message reçu de {From} : {Body}")
    
    # Nettoyage du message
    user_message = Body.lower().strip()

    # Réponse dynamique
    if "hôtel" in user_message or "réserver" in user_message:
        message_texte = "🛎️ Veuillez me donner le nom de la ville et les dates de votre séjour."
    elif "restaurant" in user_message:
        message_texte = "🍽️ D'accord ! Quel type de cuisine recherchez-vous et pour quelle date ?"
    elif "plat" in user_message:
        message_texte = "🥘 Quels plats voulez-vous commander ?"
    elif "artisan" in user_message:
        message_texte = "🧵 Quel type de produit artisanal cherchez-vous ?"
    elif "maison" in user_message:
        message_texte = "🏠 Indiquez-nous ce que vous souhaitez comme plat fait maison."
    elif "duty free" in user_message:
        message_texte = "🛍️ Voici les meilleures offres disponibles dans les duty free. Souhaitez-vous voir par catégorie ?"
    else:
        message_texte = (
            "👋 Bienvenue chez Askley !\n"
            "1️⃣ Réserver un hôtel\n"
            "2️⃣ Réserver un restaurant\n"
            "3️⃣ Commander un plat\n"
            "4️⃣ Produits artisanaux\n"
            "5️⃣ Plats faits maison\n"
            "6️⃣ Offres duty free"
        )

    try:
        message = client.messages.create(
            from_=TWILIO_PHONE_NUMBER,
            body=message_texte,
            to=From
        )
        print(f"📤 Réponse : {message_texte}")
    except Exception as e:
        print(f"❌ Erreur : {e}")
        return JSONResponse(content={"error": str(e)}, status_code=400)

    return {"status": "ok"}
