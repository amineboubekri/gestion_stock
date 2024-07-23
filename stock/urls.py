from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_register, name='login'),
    path('register/', views.login_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('home/', views.home, name='home'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('employe_dashboard/', views.employe_dashboard, name='employe_dashboard'),
    path('magasinier_dashboard/', views.magasinier_dashboard, name='magasinier_dashboard'),
    path('ajouter_commande/', views.create_order, name='create_order'),
    path('employee_orders/', views.employee_orders, name='employee_orders'),  
    path('magasinier_liste_com/', views.magasinier_liste, name='magasinier_liste'), 
    path('valider_commande/<int:order_id>/', views.valider_commande, name='valider_commande'),
    path('refuser_commande/<int:order_id>/', views.refuser_commande, name='refuser_commande'),
    path('ajouter_produit/', views.add_product, name='add_product'),
    path('magasinier_produits/', views.magasinier_products, name='magasinier_products'),  
    path('admin_productts/', views.admin_products, name='admin_products'),  
    path('delete_product/<int:product_id>/', views.supprimer_produit, name='supprimer_produit'),
    path('modifier_commande/<int:order_id>/', views.modifier_commande, name='modifier_commande'),
    path('ajouter_stock/', views.ajouter_stock, name='ajouter_stock'),
    path('delete_product_admin/<int:product_id>/', views.supprimer_produit_admin, name='supprimer_produit_admin'),

]
