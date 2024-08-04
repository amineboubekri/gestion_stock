from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Personne, Commande, Produit, Entree, CommandeAvantValidation, Cart

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Personne
        fields = ('username', 'password1', 'password2', 'role')

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = Personne
        fields = ('username', 'password')

class CommandeForm(forms.ModelForm):
    class Meta:
        model = Commande
        fields = ['designation', 'num_ordre', 'produit', 'quantite_commande']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('validation', None)

class CommandeAvantvalidationForm(forms.ModelForm):
    class Meta:
        model = CommandeAvantValidation
        fields = ['designation', 'num_ordre', 'produit', 'quantite_commande']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('validation', None)

class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = ['designation', 'quantite', 'prix', 'image']

class CommandeUpdateForm(forms.ModelForm):
    class Meta:
        model = Commande
        fields = ['designation', 'produit', 'quantite_commande', 'validation']

class AjoutStockForm(forms.ModelForm):
    date_entree = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )    
    class Meta:
        model = Entree
        fields = ['produit', 'quantite', 'prix_achat', 'date_entree']


class CartAddProductForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['produit', 'quantite']
