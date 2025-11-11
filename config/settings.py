# loads environment variables

from dotenv import load_dotenv
import os

load_dotenv()

DISCO_API_URL = os.getenv("DISCO_API_URL")
METER_ID = os.getenv("METER_ID")

TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_TOKEN = os.getenv("TWILIO_TOKEN")
TWILIO_WHATSAPP = os.getenv("TWILIO_WHATSAPP")
USER_WHATSAPP = os.getenv("USER_WHATSAPP")
