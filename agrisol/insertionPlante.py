import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agrisol.settings')
django.setup()

from dashboard.models import Plante, Intervalle

# Données des plantes
plantes_data = [
    {
        "nom": "menthe",
        "temperature": (18, 24),
        "humidite": (50, 70),
        "ph": (6.0, 7.5),
        "niveau_eau": (5, 10),
        "co2": (300, 800),
        "lumiere": (15000, 25000)
    },
    {
        "nom": "laitue",
        "temperature": (16, 22),
        "humidite": (60, 80),
        "ph": (6.0, 7.0),
        "niveau_eau": (4, 8),
        "co2": (250, 800),
        "lumiere": (12000, 20000)
    },
    {
        "nom": "epinard",
        "temperature": (10, 20),
        "humidite": (60, 70),
        "ph": (6.2, 7.5),
        "niveau_eau": (6, 10),
        "co2": (300, 700),
        "lumiere": (14000, 22000)
    },
    {
        "nom": "basilic",
        "temperature": (20, 27),
        "humidite": (50, 70),
        "ph": (5.5, 6.5),
        "niveau_eau": (5, 9),
        "co2": (300, 800),
        "lumiere": (15000, 25000)
    },
    {
        "nom": "comcombre",
        "temperature": (22, 28),
        "humidite": (60, 80),
        "ph": (5.5, 6.8),
        "niveau_eau": (6, 10),
        "co2": (350, 900),
        "lumiere": (18000, 26000)
    },
    {
        "nom": "fraise",
        "temperature": (18, 24),
        "humidite": (70, 80),
        "ph": (5.8, 6.5),
        "niveau_eau": (6, 9),
        "co2": (300, 850),
        "lumiere": (16000, 25000)
    },
    {
        "nom": "tomate",
        "temperature": (20, 26),
        "humidite": (60, 75),
        "ph": (5.5, 6.8),
        "niveau_eau": (5, 9),
        "co2": (350, 900),
        "lumiere": (18000, 26000)
    },
    {
        "nom": "pomme de terre",
        "temperature": (15, 22),
        "humidite": (60, 70),
        "ph": (5.0, 6.0),
        "niveau_eau": (4, 8),
        "co2": (300, 800),
        "lumiere": (12000, 20000)
    },
    {
        "nom": "ognion",
        "temperature": (13, 24),
        "humidite": (55, 70),
        "ph": (6.0, 7.0),
        "niveau_eau": (5, 8),
        "co2": (250, 750),
        "lumiere": (12000, 18000)
    }
]

# Insertion dans PostgreSQL
for p in plantes_data:
    temp = Intervalle.objects.create(min=p["temperature"][0], max=p["temperature"][1])
    hum = Intervalle.objects.create(min=p["humidite"][0], max=p["humidite"][1])
    ph = Intervalle.objects.create(min=p["ph"][0], max=p["ph"][1])
    eau = Intervalle.objects.create(min=p["niveau_eau"][0], max=p["niveau_eau"][1])
    co2 = Intervalle.objects.create(min=p["co2"][0], max=p["co2"][1])
    lumiere = Intervalle.objects.create(min=p["lumiere"][0], max=p["lumiere"][1])

    Plante.objects.create(
        nom=p["nom"],
        temperature=temp,
        humidite=hum,
        ph=ph,
        niveau_eau=eau,
        co2=co2,
        lumiere=lumiere
    )

print("✅ Les 9 plantes ont été ajoutées à PostgreSQL avec succès.")
