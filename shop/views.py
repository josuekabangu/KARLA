from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import *

# Gestion des messages
SUCCESS_MESSAGE = "Produit ajouté au panier avec succès!"
UPDATE_SUCCESS_MESSAGE = "Quantité du produit mise à jour avec succès!"
UPDATE_ERROR_MESSAGE = "Quantité demandée non disponible en stock."
REDUCE_QUANTITY_MESSAGE = "La quantité du produit a été réduite."
REMOVE_PRODUCT_MESSAGE = "Le produit a été retiré de votre panier."

# Afficher toutes les catégories
def category_list(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'shop/category_list.html', context)

# Afficher tous les produits avec des options de tri
def product_list(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()

    paginator = Paginator(products, 9)  # 10 produits par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Compter les éléments dans le panier pour l'utilisateur actuel
    cart_items_count = 0
    if request.user.is_authenticated:
        cart = Cart.objects.get_or_create(user=request.user, complete=False)[0]
        cart_items_count = cart.get_cart_items

    context = {
        "page_obj": page_obj,
        "query": query if query is not None else "", # Assurez-vous que query ne soit pas None dans le template
        'cart_items_count': cart_items_count
        }
    return render(request, 'shop/product_list.html', context)


# Afficher le détail d'un produit
def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'shop/product_detail.html', {'product': product})

# Afficher le panier d'un utilisateur
@login_required
def cart_detail(request):
    cart, _ = Cart.objects.get_or_create(user=request.user, complete=False)
    content = {
        'cart': cart
    }
    return render(request, 'shop/cart_detail.html', content)


# Ajouter un produit au panier
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if created:
        messages.success(request, SUCCESS_MESSAGE)
    elif cart_item.quantity < product.stock:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, UPDATE_SUCCESS_MESSAGE)
    else:
        messages.error(request, UPDATE_ERROR_MESSAGE)

    return redirect('shop:cart_detail')

# Supprimer un produit du panier
@login_required
def remove_from_cart(request, product_id):
    cart_item = get_object_or_404(CartItem, product_id=product_id, cart__user=request.user, cart__complete=False)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
        messages.info(request, REDUCE_QUANTITY_MESSAGE)
    else:
        cart_item.delete()
        messages.info(request, REMOVE_PRODUCT_MESSAGE)
    return redirect('shop:cart_detail')

# Modifier la quantité d'un produit dans le panier
@login_required
def change_item_quantity(request, product_id, quantity):
    cart_item = get_object_or_404(CartItem, product_id=product_id, cart__user=request.user, cart__complete=False)
    product = cart_item.product
    if 0 < quantity <= product.stock:
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, UPDATE_SUCCESS_MESSAGE)
    else:
        messages.error(request, UPDATE_ERROR_MESSAGE)
    return redirect('shop:cart_detail')
