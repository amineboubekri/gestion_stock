from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CommandeForm, ProduitForm, CommandeUpdateForm, AjoutStockForm, CommandeAvantValidation, CartAddProductForm
from .models import Commande, Produit, Entree, Cart
from django.http import HttpResponse
from django.template.loader import render_to_string
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import  SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing, Line
from django.contrib.staticfiles import finders
from django.views.decorators.csrf import csrf_exempt
from uuid import uuid4
import uuid
from datetime import datetime

def login_register(request):
    if request.method == 'POST':
        login_form = CustomAuthenticationForm(request, data=request.POST)
        register_form = CustomUserCreationForm(request.POST)
        if 'login' in request.POST and login_form.is_valid():
            user = login_form.get_user()
            auth_login(request, user)
            return redirect('home')
        elif 'register' in request.POST and register_form.is_valid():
            user = register_form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        login_form = CustomAuthenticationForm()
        register_form = CustomUserCreationForm()

    return render(request, 'stock/login_register.html', {
        'login_form': login_form,
        'register_form': register_form
    })

@login_required
def home(request):
    user_role = request.user.role
    if user_role == 'admin':
        return redirect('admin_dashboard')
    elif user_role == 'employe':
        return redirect('employe_dashboard')
    elif user_role == 'magasinier':
        return redirect('magasinier_dashboard')
    else:
        return redirect('login')  

@login_required
def admin_dashboard(request):
    return render(request, 'stock/admin_dashboard.html')

@login_required
def employe_dashboard(request):
    return render(request, 'stock/employe_dashboard.html')

@login_required
def magasinier_dashboard(request):
    return render(request, 'stock/magasinier_dashboard.html')

def user_logout(request):
    auth_logout(request)
    return redirect('login')


from uuid import uuid4

@login_required
def create_order(request):
    if request.user.role != 'employe':
        return redirect('home')

    if request.method == 'POST':
        produit_id = request.POST.get('produit')
        quantite_commande = int(request.POST.get('quantite_commande', 0))

        produit = Produit.objects.get(id=produit_id)

        if produit.quantite >= quantite_commande and quantite_commande > 0:
            num_ordre = str(uuid4())

            order = Commande(
                designation=f'Commande pour {produit.designation}', 
                num_ordre=num_ordre,  
                produit=produit,
                employe=request.user,
                quantite_commande=quantite_commande,
                validation='En attente',
                quantite_commande_avant=quantite_commande
            )

            produit.quantite -= quantite_commande
            produit.save()
            order.save()

            original_order = CommandeAvantValidation(
                designation=order.designation,
                num_ordre=order.num_ordre,
                validation=order.validation,
                produit=order.produit,
                employe=order.employe,
                quantite_commande=order.quantite_commande
            )
            original_order.save()

            return redirect('employee_orders')
        else:
            error_message = 'Quantité commandée supérieure à la quantité disponible ou invalide.'
            return render(request, 'stock/ajouter_commande.html', {'products': Produit.objects.all(), 'error_message': error_message})

    return render(request, 'stock/ajouter_commande.html', {'products': Produit.objects.all()})



@login_required
def employee_orders(request):
    if request.user.role != 'employe' and request.user.role != 'magasinier':
        return redirect('home')

    orders = Commande.objects.filter(employe=request.user)

    grouped_orders = {}
    for order in orders:
        if order.num_ordre not in grouped_orders:
            grouped_orders[order.num_ordre] = []
        grouped_orders[order.num_ordre].append(order)

    return render(request, 'stock/liste_commandes.html', {'grouped_orders': grouped_orders})



@login_required
def commandes_history(request):
    if request.user.role != 'employe' and request.user.role != 'magasinier':
        return redirect('home')
    if request.user.role == 'employe':
        orders = CommandeAvantValidation.objects.filter(employe=request.user)
    else:
        orders = CommandeAvantValidation.objects.all()
    return render(request, 'stock/commandes_hisrory.html', {'orders': orders})

@login_required
def magasinier_liste(request):
    if request.user.role != 'magasinier':
        return redirect('home')
    orders = Commande.objects.filter(validation='En attente')
    return render(request, 'stock/magasinier_liste_comm.html', {'orders': orders})

@login_required
def valider_commande(request, order_id):
    order = get_object_or_404(Commande, id=order_id)
    order.validation = 'valide'
    order.save()
    return redirect(reverse('magasinier_liste'))

@login_required
def refuser_commande(request, order_id):
    order = get_object_or_404(Commande, id=order_id)

    if request.method == 'POST':
        raison_refus = request.POST.get('raison_refus', '')
        produit = order.produit
        produit.quantite += order.quantite_commande
        produit.save()

        order.validation = 'refuse'
        order.raison_refus = raison_refus
        order.save()

        return redirect(reverse('magasinier_liste'))

    return redirect(reverse('magasinier_liste'))


@login_required
def add_product(request):
    if request.user.role != 'admin':
        return redirect('home')

    if request.method == 'POST':
        form = ProduitForm(request.POST, request.FILES)
        if form.is_valid():
            produit = form.save(commit=False)
            prix = form.cleaned_data['prix']  
            produit.prix_precedant = prix
            produit.cmup = prix
            produit.save()             
            return redirect('admin_products')
    else:
        form = ProduitForm()

    return render(request, 'stock/ajouter_produit.html', {'form': form})

@login_required
def magasinier_products(request):
    if request.user.role != 'magasinier':
        return redirect('home')
    products = Produit.objects.all()
    return render(request, 'stock/liste_produits.html', {'products': products})

@login_required
def admin_products(request):
    if request.user.role != 'admin':
        return redirect('home')
    products = Produit.objects.all()
    return render(request, 'stock/admin_products.html', {'products': products})

@login_required
def supprimer_produit(request, product_id):
    produit = get_object_or_404(Produit, id=product_id)

    if produit.image:
        produit.image.delete(save=False)

    produit.delete()
    return redirect(reverse('admin_products'))


@login_required
def modifier_commande(request, order_id):
    order = get_object_or_404(Commande, id=order_id)
    if request.method == 'POST':
        form = CommandeUpdateForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('magasinier_liste') 
    else:
        form = CommandeUpdateForm(instance=order)
    
    return render(request, 'stock/modifier_commande.html', {'form': form, 'order': order})


@login_required
def ajouter_stock(request):
    if request.user.role != 'magasinier':
        return redirect('home')

    if request.method == 'POST':
        form = AjoutStockForm(request.POST)
        if form.is_valid():
            entree = form.save(commit=False)
            produit = entree.produit
            quantite = entree.quantite
            prix_achat = entree.prix_achat
            date_entree = entree.date_entree

            produit.quantite += quantite

            valeur_stock_precedent = produit.quantite * produit.cmup
            valeur_achat_nouvelle_entree = quantite * prix_achat
            nouvelle_valeur_stock = valeur_stock_precedent + valeur_achat_nouvelle_entree
            produit.cmup = nouvelle_valeur_stock / (produit.quantite + quantite)
            produit.prix = produit.cmup
            produit.save()
            entree.save()
            return redirect('magasinier_dashboard')
    else:
        form = AjoutStockForm()

    return render(request, 'stock/ajouter_stock.html', {'form': form})


@login_required
def supprimer_produit_admin(request, product_id):
    produit = get_object_or_404(Produit, id=product_id)
    produit.delete()
    return redirect(reverse('admin_products'))

@login_required
def generate_order_pdf(request, order_id):
    order = get_object_or_404(Commande, id=order_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="order_{order_id}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    normal_style = styles['BodyText']

    content = []

    content.append(Paragraph('Détails de la Commande', title_style))
    content.append(Paragraph(f'Produit: <b>{order.produit.designation}</b>', normal_style))
    content.append(Paragraph(f'Employe: <b>{order.employe.username}</b>',normal_style ))
    content.append(Paragraph(f'Quantité: <b>{order.quantite_commande}</b>', normal_style))
    content.append(Paragraph(f'Désignation: <b>{order.designation}</b>', normal_style))
    content.append(Paragraph(f'Validation: <b>{order.validation}</b>', normal_style))

    doc.build(content)

    return response



@login_required
def add_to_cart(request):
    if request.method == 'POST':
        products = Produit.objects.all()
        cart_items = []
        for product in products:
            quantity = request.POST.get(f'quantity_{product.id}', 0)
            if quantity:
                quantity = int(quantity)
                if quantity > 0 and quantity <= product.quantite:
                    cart_item = Cart(
                        user=request.user,
                        produit=product,
                        quantite=quantity,
                        grouped=request.POST.get('grouped', False)  
                    )
                    cart_items.append(cart_item)
        if cart_items:
            Cart.objects.bulk_create(cart_items)
            return redirect('view_cart')
    else:
        products = Produit.objects.all()

    return render(request, 'stock/add_to_cart.html', {'products': products})



@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    return render(request, 'stock/view_cart.html', {'cart_items': cart_items})

@login_required
def place_order(request):
    cart_items = Cart.objects.filter(user=request.user)
    if request.method == 'POST':
        if cart_items:
            num_ordre = str(uuid4())

            for item in cart_items:
                produit = item.produit
                quantite = item.quantite
                if produit.quantite >= quantite:
                    order = Commande(
                        designation=f'Commande pour {produit.designation}',
                        num_ordre=num_ordre,  
                        produit=produit,
                        employe=request.user,
                        quantite_commande=quantite,
                        validation='En attente',
                        quantite_commande_avant=quantite
                    )
                    produit.quantite -= quantite
                    produit.save()
                    order.save()

                    original_order = CommandeAvantValidation(
                        designation=order.designation,
                        num_ordre=num_ordre,  
                        validation=order.validation,
                        produit=order.produit,
                        employe=order.employe,
                        quantite_commande=order.quantite_commande
                    )
                    original_order.save()

            cart_items.delete()
            return redirect('employee_orders')

    return render(request, 'stock/place_order.html', {'cart_items': cart_items})



def modifier_produit(request, product_id):
    product = get_object_or_404(Produit, id=product_id)
    if request.method == 'POST':
        form = ProduitForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('admin_products')
    else:
        form = ProduitForm(instance=product)
    return render(request, 'stock/modifier_produit.html', {'form': form, 'product': product})

def modifier_produit(request, product_id):
    product = get_object_or_404(Produit, id=product_id)
    if request.method == 'POST':
        form = ProduitForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('admin_products')
    else:
        form = ProduitForm(instance=product)
    return render(request, 'stock/modifier_produit.html', {'form': form, 'product': product})

@login_required
def generate_cart_pdf(request, num_ordre):
    orders = Commande.objects.filter(num_ordre=num_ordre, validation='valide')

    if not orders:
        return HttpResponse("Pas de commandes", status=404)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Commande_{num_ordre}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    normal_style = styles['BodyText']

    content = []

    current_date = datetime.now().strftime('%d/%m/%Y')
    date_paragraph = Paragraph(f'<b>Date:</b> {current_date}', normal_style)
    content.append(date_paragraph)
    content.append(Spacer(1, 12))

    logo_path = finders.find('images/abhlogo.png')
    if logo_path:
        logo = Image(logo_path)
        logo.drawWidth = 3 * inch 
        logo.drawHeight = 1.2 * inch 
        logo.hAlign = 'CENTER'
        content.append(logo)
        content.append(Spacer(1, 24))

    content.append(Paragraph('Bon de réception', title_style))
    content.append(Spacer(1, 12)) 
    
    for order in orders:
        content.append(Paragraph(f'Produit: <b>{order.produit.designation}</b>', normal_style))
        content.append(Paragraph(f'Quantité: <b>{order.quantite_commande}</b>', normal_style))
        content.append(Spacer(1, 12))

        line = Drawing(8.5 * inch, 1)  
        line.add(Line(0, 0, 6 * inch, 0, strokeColor=colors.black, strokeWidth=1))
        content.append(line)
        content.append(Spacer(1, 12)) 

    employe_name = orders.first().employe.username
    content.append(Spacer(1, 24)) 
    
    content.append(Spacer(1, 48)) 
    table_data = [
        [employe_name, '', 'Signature du Chef:', '', 'Signature du Magasinier:'],
        ['', '', '', '', '']
    ]
    table = Table(table_data, colWidths=[2.5 * inch, 0.5 * inch, 2.5 * inch, 0.5 * inch, 2.5 * inch])
    table.setStyle(TableStyle([
        ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]))
    content.append(table)

    doc.build(content)

    return response



@login_required
def magasinier_orders(request):
    if request.user.role != 'employe' and request.user.role != 'magasinier':
        return redirect('home')

    orders = Commande.objects.all()

    grouped_orders = {}
    for order in orders:
        if order.num_ordre not in grouped_orders:
            grouped_orders[order.num_ordre] = []
        grouped_orders[order.num_ordre].append(order)

    return render(request, 'stock/liste_commandes_magasinier.html', {'grouped_orders': grouped_orders})