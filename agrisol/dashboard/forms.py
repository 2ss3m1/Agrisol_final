from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import validate_email
from .models import Agriculteur
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import PasswordChangeForm as AuthPasswordChangeForm

class AgriculteurForm(forms.ModelForm):
    mot_de_passe = forms.CharField(widget=forms.PasswordInput,min_length=8,help_text="Le mot de passe doit contenir au moins 8 caractères.")

    class Meta:
        model = Agriculteur
        fields = ['nom', 'prenom', 'email', 'mot_de_passe', 'telephone']

    def save(self, commit=True):
        agriculteur = super().save(commit=False)
        agriculteur.mot_de_passe = make_password(self.cleaned_data['mot_de_passe'])  #  Hash du mot de passe
        if commit:
            agriculteur.save()
        return agriculteur


class PasswordChangeForm(AuthPasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personnalisation des champs
        self.fields['old_password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Ancien mot de passe'
        })
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Nouveau mot de passe'
        })
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirmation du nouveau mot de passe'
        })
        
        # Personnalisation des labels si nécessaire
        self.fields['old_password'].label = "Ancien mot de passe"
        self.fields['new_password1'].label = "Nouveau mot de passe"
        self.fields['new_password2'].label = "Confirmation du nouveau mot de passe"