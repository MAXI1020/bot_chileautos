import requests
from bs4 import BeautifulSoup
import time
import telegram

# Configuración del bot de Telegram
TOKEN = "AQUÍ_TU_TOKEN"
CHAT_ID = "AQUÍ_TU_CHAT_ID"

bot = telegram.Bot(token=TOKEN)

# Guardar los IDs de autos ya enviados para evitar duplicados
vistos = set()

def obtener_autos():
    url = "https://www.chileautos.cl/compra-de-autos-usados"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Error al acceder a Chileautos")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    autos = []

    for link in soup.select("a[class*=listing-card]"):
        href = link.get("href")
        if href and "/vehiculo/" in href:
            auto_id = href.split("/")[-1]
            if auto_id not in vistos:
                vistos.add(auto_id)
                autos.append("https://www.chileautos.cl" + href)

    return autos

def enviar_autos_nuevos():
    print("🔍 Buscando autos nuevos...")
    nuevos = obtener_autos()

    if nuevos:
        for auto in nuevos:
            bot.send_message(chat_id=CHAT_ID, text=f"🚗 Nuevo auto: {auto}")
        print(f"✅ {len(nuevos)} autos nuevos enviados.")
    else:
        print("😕 No hay autos nuevos.")

if __name__ == "__main__":
    while True:
        try:
            enviar_autos_nuevos()
            time.sleep(600)  # Esperar 10 minutos
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(600)
