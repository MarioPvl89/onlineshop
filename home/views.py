from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import JsonResponse
from django.contrib.auth.models import User
from .forms import CommentForm
from .models import Comment, Products, Favorite, Cart, Categories
# from django.views.generic import DetailView, ListView
from django.core.paginator import Paginator


def check_username(request):
    username = request.GET.get('username', '').strip()
    exists = User.objects.filter(username=username).exists()
    return JsonResponse({'exists': exists})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('catalog:home')
    else:
        form = UserCreationForm()
    return render(request, 'home/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('catalog:home')
    else:
        form = AuthenticationForm()
    return render(request, 'home/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('catalog:home')


# @login_required
def home(request):
    comments = Comment.objects.filter(product__isnull=True).order_by('-created_at')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.product = None
            comment.save()
            return redirect('catalog:home')
    else:
        form = CommentForm()

    return render(request, 'home/home.html', {'form': form, 'comments': comments})


def catalog(request, category_slug=None):

    page = request.GET.get('page', 1)

    selected_category = request.GET.get("category") or category_slug or "all"
    
    if selected_category == "all":
        goods = Products.objects.all()
    else:
        goods = get_list_or_404(Products.objects.filter(category__slug=selected_category))

    paginator = Paginator(goods, 6)
    current_page = paginator.page(int(page))

    categories = Categories.objects.all()

    context = {
        "title": "Home - Каталог",
        "goods": current_page,
        "slug_url": selected_category,
        "categories": categories,
    }
    return render(request, "home/goods.html", context)


def product(request, category_slug, product_slug):
    if category_slug == "all":
        product = get_object_or_404(Products, slug=product_slug)
    else:
        product = get_object_or_404(Products, slug=product_slug, category__slug=category_slug)

    comments = product.comments.all().order_by('-created_at')

    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.product = product
            comment.save()
            return redirect('catalog:product', category_slug=category_slug, product_slug=product_slug)
    else:
        form = CommentForm() if request.user.is_authenticated else None

    context = {
        "product": product,
        "comments": comments,
        "form": form,
        "category_slug": category_slug,
        "title": f"{product.name} - {product.category.name}"
    }

    return render(request, "home/good_template.html", context=context)


def product_default(request, product_slug):
    product = get_object_or_404(Products, slug=product_slug)
    comments = product.comments.all().order_by('-created_at')

    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.product = product
            comment.save()
            return redirect('catalog:product_default', product_slug=product_slug)
    else:
        form = CommentForm() if request.user.is_authenticated else None

    context = {
        "product": product,
        "comments": comments,
        "form": form,
        "category_slug": "all",
        "title": f"{product.name} - Все товары"
    }

    return render(request, "home/good_template.html", context)


@login_required
def add_to_favorites(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    Favorite.objects.get_or_create(user=request.user, product=product)
    return redirect('catalog:catalog', category_slug=product.category.slug)


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('catalog:catalog', category_slug=product.category.slug)


@login_required
def cart_detail(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart_items)
    return render(request, 'home/cart_detail.html', {'cart_items': cart_items, 'total_price': total_price})


@login_required
def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.delete()
    return redirect('catalog:cart_detail')


@login_required
def favorite_list(request):
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'home/favorite_list.html', {'favorites': favorites})


@login_required
def remove_from_favorite(request, favorite_id):
    favorite = get_object_or_404(Favorite, id=favorite_id, user=request.user)
    favorite.delete()
    return redirect('catalog:favorite_list')


@login_required
def increase_quantity(request, item_id):
    item = get_object_or_404(Cart, id=item_id, user=request.user)
    item.quantity += 1
    item.save()
    return redirect('catalog:cart_detail')


@login_required
def decrease_quantity(request, item_id):
    item = get_object_or_404(Cart, id=item_id, user=request.user)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()
    return redirect('catalog:cart_detail')
