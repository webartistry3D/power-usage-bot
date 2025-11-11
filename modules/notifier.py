# Twilio SMS/WhatsApp alerts

from twilio.rest import Client
from config.settings import TWILIO_SID, TWILIO_TOKEN, TWILIO_WHATSAPP, USER_WHATSAPP

def send_report(summary, prediction):
    client = Client(TWILIO_SID, TWILIO_TOKEN)

    message = (
        f"⚡ PowerPal Report ⚡\n"
        f"Balance: {summary['balance']} units\n"
        f"Avg Daily Usage: {summary['average_usage']} units\n"
        f"Predicted Tomorrow: {prediction} units\n"
        f"Days Left: {summary['days_left']}"
    )

    client.messages.create(
        from_=TWILIO_WHATSAPP,
        body=message,
        to=USER_WHATSAPP
    )
    print("✅ WhatsApp report sent successfully.")
