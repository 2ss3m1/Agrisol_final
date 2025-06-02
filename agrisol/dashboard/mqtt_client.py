import json
import os
import threading

import django
import paho.mqtt.client as mqtt
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "agrisol.settings")
# django.setup()

from dashboard.models import Agriculteur
from dashboard.utils import check_alerts

from .recommendations import get_ai_recommendation


def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())
    token = data.get("token")
    try:
        agriculteur = Agriculteur.objects.get(mqtt_token=token)
    except Agriculteur.DoesNotExist:
        print("MQTT: Token invalide")
        return

    alerts = []
    if agriculteur:
        alerts = check_alerts(agriculteur, data)

    # Correction ici : extraire chaque feature
    humidite = data.get("humidity")
    temperature = data.get("temperature")
    ph = data.get("ph")
    lumiere = data.get("lumiere")
    co2 = data.get("co2")
    niveau_eau = data.get("niveau_eau")

    ai_recommendations = get_ai_recommendation(
        humidite, temperature, ph, lumiere, co2, niveau_eau
    )
    # Ajoute cette ligne pour forcer la conversion
    if hasattr(ai_recommendations, "item"):
        ai_recommendations = ai_recommendations.item()
    else:
        ai_recommendations = int(ai_recommendations)

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "sensor_data_group",
        {
            "type": "send_sensor_data",
            "message": {
                "sensor_data": data,
                "alerts": [
                    {"type": a.type_alerte, "message": a.message, "valeur": a.valeur} for a in alerts
                ],
                "recommendations": ai_recommendations,
            }
        }
    )


def mqtt_thread():
    client = mqtt.Client()
    # client.tls_set(ca_certs="chemin/vers/ca.crt")  # Désactive TLS pour le test local
    client.connect("localhost", 1883, 60)  # Port MQTT standard sans TLS
    client.subscribe("agrisol/data")
    client.on_message = on_message
    client.loop_forever()


def start():
    thread = threading.Thread(target=mqtt_thread)
    thread.daemon = True
    thread.start()
