from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import *

# Create your views here.

# Afficher tous les produits avec des options de trie
def category_list(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'shop/category_list.html', context)

def product_list(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()

    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "query": query if query is not None else ""
    }
    return render(request, 'shop/product_list.html', context)


def product_detail(request, product_id):
    # Récupération du produit ou renvoi d'une erreur 404 si non trouvé
    product = get_object_or_404(Product, pk=product_id)
    # Rendu des détails du produit avec le contexte du produit spécifique
    return render(request, 'shop/product_detail.html', {'product': product})


# Afficher le panier d'un utilisateur
@login_required  # L'utilisateur doit être connecté pour voir son panier
def cart_detail(request):
    # Récupération ou création du panier de l'utilisateur connecté
    cart, created = Cart.objects.get_or_create(user=request.user)
    # Rendu du panier avec le contexte du panier de l'utilisateur
    return render(request, 'shop/cart_detail.html', {'cart': cart})

# Ajouter un produit au panier
@login_required  # L'utilisateur doit être connecté pour ajouter un produit au panier
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if created:
        # L'article a été créé, donc la quantité par défaut est déjà 1.
        messages.success(request, "Produit ajouté au panier avec succès!")
    else:
        # L'article existe déjà dans le panier, augmentez la quantité.
        if cart_item.quantity < product.stock:
            cart_item.quantity += 1
            cart_item.save()
            messages.success(request, "Quantité du produit mise à jour avec succès!")
        else:
            messages.error(request, "Quantité du produit non disponible en stock.")

    # Redirection vers le détail du panier après l'ajout du produit
    return redirect('cart_detail')

# Supprimer un produit du panier
@login_required  # L'utilisateur doit être connecté pour supprimer un produit du panier
def remove_from_cart(request, product_id):
    cart_item = get_object_or_404(CartItem, product_id=product_id, cart__user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
        messages.info(request, "La quantité du produit a été réduite.")
    else:
        cart_item.delete()
        messages.info(request, "Le produit a été retiré de votre panier.")
    # Redirection vers le détail du panier après la suppression du produit
    return redirect('cart_detail')

# Modifier la quantité d'un produit dans le panier
@login_required  # L'utilisateur doit être connecté pour modifier la quantité d'un produit dans le panier
def change_item_quantity(request, product_id, quantity):
    cart_item = get_object_or_404(CartItem, product_id=product_id, cart__user=request.user)
    product = cart_item.product
    if 0 < quantity <= product.stock:
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, "La quantité du produit a été mise à jour.")
    else:
        messages.error(request, "Quantité demandée non disponible en stock.")
    # Redirection vers le détail du panier après la modification de la quantité
    return redirect('cart_detail')
