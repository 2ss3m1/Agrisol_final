from rest_framework import serializers

from .models import Agriculteur, Alerte


class AgriculteurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agriculteur
        fields = ['id', 'nom', 'prenom', 'email', 'telephone']

class AlerteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alerte
        fields = ['id', 'type_alerte', 'valeur', 'message', 'created_at']