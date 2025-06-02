import json

import graphene
import paho.mqtt.publish as publish
from graphene_django import DjangoObjectType

from .models import Agriculteur, Alerte


class AgriculteurType(DjangoObjectType):
    class Meta:
        model = Agriculteur
        fields = ("id", "nom", "prenom", "email", "telephone")

class AlerteType(DjangoObjectType):
    class Meta:
        model = Alerte
        fields = ("id", "type_alerte", "valeur", "message", "created_at")

class Query(graphene.ObjectType):
    all_agriculteurs = graphene.List(AgriculteurType)
    all_alertes = graphene.List(AlerteType)

    def resolve_all_agriculteurs(root, info):
        return Agriculteur.objects.all()

    def resolve_all_alertes(root, info):
        return Alerte.objects.all()

class SendDeviceCommand(graphene.Mutation):
    class Arguments:
        command = graphene.String(required=True)
        token = graphene.String(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, command, token):
        try:
            agriculteur = Agriculteur.objects.get(mqtt_token=token)
        except Agriculteur.DoesNotExist:
            return SendDeviceCommand(ok=False)
        publish.single("agrisol/command", json.dumps({"command": command, "token": token}), hostname="localhost")
        return SendDeviceCommand(ok=True)

class Mutation(graphene.ObjectType):
    send_device_command = SendDeviceCommand.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)