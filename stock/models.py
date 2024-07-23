# models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
from decimal import Decimal


class Personne(AbstractUser):
    ROLES = (
        ('admin', 'Admin'),
        ('employe', 'Employé'),
        ('magasinier', 'Magasinier'),
    )
    role = models.CharField(max_length=10, choices=ROLES)

    def __str__(self):
        return self.username

class Produit(models.Model):
    designation = models.CharField(max_length=100)
    quantite = models.PositiveIntegerField(default=0)
    prix_precedant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    prix = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    cmup = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def update_cmup(self, prix, quantite_ajoutee):
        previous_cmup = Decimal(self.prix_precedant)
        new_price = Decimal(prix)
        total_quantity = Decimal(self.quantite) + Decimal(quantite_ajoutee)   
      #  if total_quantity > 0:
       #     self.cmup = (previous_cmup * Decimal(self.quantite) + new_price * Decimal(quantite_ajoutee)) / total_quantity
        #else:
         #   self.cmup = Decimal(0)

        self.prix_precedant = new_price
        self.quantite = total_quantity
        self.save()
    def __str__(self):
        return self.designation

class CommandeAvantValidation(models.Model):
    designation = models.CharField(max_length=255)
    num_ordre = models.IntegerField()
    validation = models.CharField(max_length=255, default='En attente') 
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    employe = models.ForeignKey(Personne, on_delete=models.CASCADE)
    quantite_commande = models.FloatField()

class Commande(models.Model):
    designation = models.CharField(max_length=255)
    num_ordre = models.IntegerField()
    validation = models.CharField(max_length=255, default='En attente') 
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    employe = models.ForeignKey(Personne, on_delete=models.CASCADE)
    quantite_commande = models.FloatField()

class Fournisseur(models.Model):
    nom = models.CharField(max_length=255)
    fax = models.CharField(max_length=50)
    adresse = models.CharField(max_length=255)
    email = models.EmailField()
    telephone = models.CharField(max_length=50)

class Entree(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()
    prix_achat = models.DecimalField(max_digits=10, decimal_places=2)
    date_entree = models.DateTimeField()

class Panier(models.Model):
    date_sortie = models.DateField()
    produit = models.ManyToManyField(Produit)
