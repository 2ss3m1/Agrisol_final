# 🌱 Agrisol - Smart Agriculture Dashboard

Agrisol est une plateforme intelligente de gestion agricole, combinant IoT, intelligence artificielle et automatisation pour optimiser l’irrigation, la ventilation et la nutrition des cultures.

---

## 🚀 Prérequis

- **Python 3.10+**
- **PostgreSQL** (base de données)
- **Mosquitto MQTT Broker** (communication IoT)
- **Node-RED** (orchestration des flux MQTT/HTTP, optionnel)
- **pip** (gestionnaire de paquets Python)
- (Recommandé) **Environnement virtuel Python** (`venv`)

---

## ⚙️ Installation

1. **Clone le projet**
   ```sh
   git clone https://github.com/ton-utilisateur/agrisol.git
   cd Agrisol-master
   ```

2. **Crée et active un environnement virtuel**
   ```sh
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Installe les dépendances**
   ```sh
   pip install -r requirements.txt
   ```

4. **Configure la base de données**
   - Modifie `agrisol/agrisol/settings.py` avec tes identifiants PostgreSQL :
     ```python
     DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.postgresql',
             'NAME': 'agrisol',
             'USER': 'postgres',
             'PASSWORD': 'motdepasse',
             'HOST': 'localhost',
             'PORT': '5432',
         }
     }
     ```

5. **Applique les migrations**
   ```sh
   python manage.py migrate
   ```

6. **Crée un superutilisateur**
   ```sh
   python manage.py createsuperuser
   ```

7. **(Optionnel) Entraîne le modèle IA**
   ```sh
   python dashboard/train_recommender.py
   ```
   - Le fichier `recommender_model.joblib` sera généré dans `dashboard/`.

8. **Lance le serveur Django**
   ```sh
   python manage.py runserver
   ```
   - Pour activer les WebSockets (Channels) :
     ```sh
     daphne -p 8001 agrisol.asgi:application
     ```
   - Tu peux lancer les deux serveurs pour profiter de toutes les fonctionnalités.

9. **Lance Node-RED** (si utilisé)
   ```sh
   node-red
   ```
   - Configure un flux pour publier sur le topic MQTT `agrisol/data` avec un JSON :
     ```json
     {
       "humidity": 15,
       "temperature": 35,
       "ph": 7.5,
       "token": "TON_TOKEN_MQTT"
     }
     ```

---

## 🖥️ Utilisation

- Accède à l’interface sur [http://localhost:8000/](http://localhost:8000/) ou [http://localhost:8001/](http://localhost:8001/) selon le port utilisé.
- Les recommandations IA s’affichent en temps réel sur le dashboard.
- Utilise Node-RED pour simuler ou orchestrer des capteurs/commandes.
- Les commandes peuvent être envoyées via GraphQL ou MQTT.
NB :      daphne -p 8001 agrisol.asgi:application
Pour fonction le site correctement car le seul pour lancer server de websocket et n oblier d installer : pip install whitenoise 
---

## 📡 Exemple de message MQTT

```json
{
  "humidity": 15,
  "temperature": 35,
  "ph": 7.5,
  "token": "TON_TOKEN_MQTT"
}
```

---

## 🧠 Fonctionnalités principales

- Dashboard temps réel (WebSocket)
- Historique des alertes et actions
- Recommandations IA (irrigation, ventilation, nutriments)
- Commandes devices via GraphQL ou MQTT
- Sécurité par token d’authentification
- Extensible pour d’autres capteurs (CO2, lumière, etc.)

---

## 🤖 Intelligence Artificielle

- Le modèle IA analyse les données reçues et propose des actions optimales.
- **Personnalisation** : adapte le modèle à tes propres données pour de meilleures recommandations.
- Pour réentraîner le modèle, modifie `dashboard/train_recommender.py` et relance l’entraînement.

---

## 🛠️ Dépannage

- **Module manquant** : installe-le avec `pip install nom_module`
- **Problème de base de données** : vérifie la configuration dans `settings.py`
- **WebSocket/Channels** : assure-toi que `daphne` et `channels-redis` sont installés

---

## 📄 Licence

Projet open-source sous licence MIT.

---


**N’oublie pas d’adapter le modèle IA à tes vraies données pour de meilleures recommandations !**