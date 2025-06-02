from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from .models import Alerte


def check_alerts(agriculteur, data):
    alerts_created = []

    thresholds = getattr(settings, 'ALERT_THRESHOLDS', {})

    for key, value in data.items():
        if key not in thresholds:
            continue
        
        seuils = thresholds[key]
        val = float(value)

        if val < seuils['min'] or val > seuils['max']:
            message = f"Attention : La valeur {key} = {val} est hors intervalle ({seuils['min']} - {seuils['max']})."
            
            alerte = Alerte.objects.create(
                agriculteur=agriculteur,
                type_alerte=key,
                valeur=val,
                message=message,
                created_at=timezone.now()
            )
            alerts_created.append(alerte)

            send_mail(
                subject=f'Alerte {key} pour {agriculteur.prenom}',
                message=message,
                from_email='oussama.hamdi@sesame.com.tn',
                recipient_list=[agriculteur.email],
                fail_silently=True,
            )
    return alerts_created
