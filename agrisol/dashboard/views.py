import secrets
from functools import wraps

from django.contrib import messages
from django.contrib.auth import (authenticate, login, logout,
                                 update_session_auth_hash)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (AuthenticationForm, PasswordChangeForm,
                                       UserCreationForm)
from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import AgriculteurForm, PasswordChangeForm
from .models import Agriculteur, Alerte


# Create your views here.
def register_view(request):
    if request.method == 'POST':
        form = AgriculteurForm(request.POST)
        if form.is_valid():
            agriculteur = form.save(commit=False)
            # Hash the password before saving
            agriculteur.mot_de_passe = make_password(form.cleaned_data['mot_de_passe'])
            # Generate a unique MQTT token if not already set
            if not getattr(agriculteur, 'mqtt_token', None):
                agriculteur.mqtt_token = secrets.token_hex(32)
            agriculteur.save()
            messages.success(request, "Inscription réussie !")
            return redirect('home')
        else:
            messages.error(request, "Erreur lors de l'inscription.")
    else:
        form = AgriculteurForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            agriculteur = Agriculteur.objects.get(email=email)
            
            # Vérifie le mot de passe avec check_password
            if check_password(password, agriculteur.mot_de_passe):
                # Stocke l'ID de l'agriculteur dans la session
                request.session['agriculteur_id'] = agriculteur.id
                request.session['agriculteur_email'] = agriculteur.email
                messages.success(request, "Connexion réussie !")
                return redirect('home')
            else:
                messages.error(request, "Mot de passe incorrect.")
        except Agriculteur.DoesNotExist:
            messages.error(request, "Aucun compte avec cet email.")
    
    return render(request, 'login.html')

def logout_view(request):
    if 'agriculteur_id' in request.session:
        del request.session['agriculteur_id']
    messages.success(request, "Vous avez été déconnecté.")
    return redirect('home')

def agriculteur_est_connecte(request):
    return 'agriculteur_id' in request.session
def login_required_custom(view_func):
    """
    Décorateur qui vérifie si l'agriculteur est connecté.
    Redirige vers la page de login si non connecté.
    """
    @wraps(view_func)  # Préserve les métadonnées de la fonction originale
    def wrapper(request, *args, **kwargs):
        if 'agriculteur_id' not in request.session:
            messages.error(request, "Veuillez vous connecter pour accéder à cette page.")
            return redirect('login')  # Remplace 'login' par le nom de ta URL de connexion
        return view_func(request, *args, **kwargs)
    return wrapper

@login_required_custom
def home(request):
    # Exemple de vue protégée
    agriculteur_id = request.session.get('agriculteur_id')
    agriculteur = Agriculteur.objects.get(id=agriculteur_id)
    return render(request, 'home.html', {'agriculteur': agriculteur})



@login_required_custom
def profil(request):
    agriculteur = Agriculteur.objects.get(id=request.session['agriculteur_id'])
    if request.method == 'POST':
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        if email:
            agriculteur.email = email
        else:
            # Si l'email est vide, conserve l'email existant
            messages.error(request, "L'email ne peut pas être vide.")
            return redirect('profil')
        
        agriculteur.telephone = telephone
        agriculteur.nom = nom
        agriculteur.prenom = prenom
        agriculteur.save()

        messages.success(request, 'Profil mis à jour avec succès.')
        return redirect('profil')  # Rediriger vers la page de profil après enregistrement

    return render(request, 'profil.html', {'agriculteur': agriculteur})
@login_required_custom
def change_password(request):
    # Vérification plus robuste du profil agriculteur
    try:
        agriculteur = request.user.agriculteur
    except (AttributeError, Agriculteur.DoesNotExist):
        messages.error(request, "Profil agriculteur non trouvé. Veuillez contacter l'administrateur.")
        return redirect('profil')
    
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Mot de passe mis à jour avec succès!')
            
            agriculteur.password_last_updated = timezone.now()
            agriculteur.save()
            
            return redirect('profil')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'dashboard/change_password.html', {
        'form': form,
        'agriculteur': agriculteur
    })

@login_required_custom
def temperature_dashboard(request):
    try:
        # Récupérez les données de température depuis votre modèle ou API
        # Exemple avec des données simulées :
        context = {
            'current_temp': 24.5,
            'temp_data': {
                'labels': ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim'],
                'values': [22, 24, 25, 23, 26, 28, 24]
            },
            'max_temp': 28,
            'min_temp': 18,
            'optimal_temp': 22,
            'alert_threshold': 30
        }
        return render(request, 'dashboard/temperature.html', context)
    
    except Exception as e:
        messages.error(request, f"Erreur de chargement des données: {str(e)}")
        return redirect('home')

@login_required_custom
def dashboard_view(request):
    try:
        agriculteur_id = request.session['agriculteur_id']
        agriculteur = Agriculteur.objects.get(id=agriculteur_id)
        
        # Get the 5 latest alerts for this agriculteur
        recent_alerts = agriculteur.alertes.order_by('-created_at')[:5]

        context = {
            'agriculteur': agriculteur,
            'nom': 'Aucune culture sélectionnée',
            'humidity': 0,
            'temperature': 0,
            'lumiere': 0,
            'N_eau': 0,
            'ph': 0,
            'co2': 0,
            'chart_labels': [],
            'humidity_data': [],
            'temperature_data': [],
            'niveau_d_eau_data': [],
            'ph_data': [],
            'co2_data': [],
            'lumiere_data': [],
            'intervalles': None,
            'recent_alerts': recent_alerts,  # Add this line
        }
        return render(request, 'dashboard.html', context)
    except KeyError:
        messages.error(request, "Session invalide, veuillez vous reconnecter")
        return redirect('login')
    except Agriculteur.DoesNotExist:
        messages.error(request, "Profil agriculteur introuvable")
        return redirect('login')
# @login_required_custom
# def mes_cultures(request):
#     agriculteur_id = request.session.get('agriculteur_id')
#     agriculteur = get_object_or_404(Agriculteur, id=agriculteur_id)

#     if request.method == 'POST':
#         plante_id = request.POST.get('plante_id')
#         if not plante_id:
#             messages.error(request, "Aucune plante sélectionnée")
#             return redirect('mes_cultures')
            
#         try:
#             plante = Plante.objects.get(id=plante_id)
            
#             # Créer une nouvelle culture avec un nom unique
#             culture = Culture(
#                 nomCulture=f"Culture {plante.nom} - {timezone.now().strftime('%Y-%m-%d')}",
#                 plante=plante,
#                 agriculteur=agriculteur
#             )
#             culture.save()  # Sauvegarde effective dans la base de données
            
#             messages.success(request, f"Culture de {plante.nom} ajoutée avec succès!")
#             return redirect('mes_cultures')
            
#         except Plante.DoesNotExist:
#             messages.error(request, "Plante introuvable")
#             return redirect('mes_cultures')

#     # Récupérer les cultures existantes et les plantes disponibles
#     cultures_existantes = Culture.objects.filter(agriculteur=agriculteur).order_by('-date_creation')
#     plantes = Plante.objects.all()

#     return render(request, 'mes_cultures.html', {
#         'cultures': cultures_existantes,
#         'plantes': plantes
#     })
# @login_required_custom
# def delete_culture(request, culture_id):
#     agriculteur_id = request.session.get('agriculteur_id')
#     agriculteur = Agriculteur.objects.get(id=agriculteur_id)
    
#     culture = get_object_or_404(Culture, id=culture_id, agriculteur=agriculteur)
    
#     if request.method == 'POST':
#         culture.delete()
#         return redirect('mes_cultures')
    
#     return redirect('mes_cultures')
@login_required_custom
def alert_history(request):
    agriculteur_id = request.session.get('agriculteur_id')
    agriculteur = Agriculteur.objects.get(id=agriculteur_id)
    # Récupère toutes les alertes de cet agriculteur, les plus récentes d'abord
    alertes = Alerte.objects.filter(agriculteur=agriculteur).order_by('-created_at')
    return render(request, 'alert.html', {'agriculteur': agriculteur, 'alertes': alertes})
