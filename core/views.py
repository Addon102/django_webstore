from .models import Product, Category, Comment, Like, FavoriteProduct
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import RegistrationForm, LoginForm, CommentForm
from django.views.generic import ListView
from django.db.models import Q
from django.shortcuts import get_object_or_404


def home_view(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'core/index.html', context)


class HomeView(ListView):
    template_name = 'core/index.html'
    context_object_name = 'products'
    model = Product


class SearchResults(HomeView):
    def get_queryset(self):
        print(self.request.GET)
        query = self.request.GET.get('q')
        return Product.objects.filter(
            Q(title__iregex=query) | Q(short_description__iregex=query)
        )


def get_products_by_categories(request, category_id):

    products = Product.objects.filter(category__id=category_id)
    context = {

        'products': products
    }
    return render(request, 'core/index.html', context)


def product_detail(request, product_id):
    product = Product.objects.get(pk=product_id)
    comments = product.comments.all()
    try:
        product.likes
    except Exception as e:
        Like.objects.create(product=product)
    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user
            form.product = product
            form.save()
            return redirect('product_detail', product.pk)
    else:
        form = CommentForm()

    context = {
        'product': product,
        'comments': comments,
        'form': form
    }

    return render(request, 'core/product_detail.html', context)


def shopping_cart(request, username):
    # user_id = User.objects.get(user_id=user_id)
    user = User.objects.get(username=username)
    products = Product.objects.filter(author=user)
    context = {
        'products': products
    }
    return render(request, 'core/shopping_cart.html', context)


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()

    context = {
        'form': form
    }
    return render(request, 'core/login.html', context)


def registration_view(request):
    if request.method == 'POST':
        print(request.POST)
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'core/registration.html', context)


def user_logout(request):
    logout(request)
    return redirect('home')


def add_vote(request, obj_type, obj_id):
    from django.shortcuts import get_object_or_404

    obj = None
    if obj_type == 'product':
        obj = get_object_or_404(Product, pk=obj_id)

    try:
        obj.likes
    except Exception as e:
        if obj.__class__ is Product:
            Like.objects.create()

        if request.user in obj.likes.user.all():
            obj.likes.user.remove(request.user.pk)
        else:
            obj.likes.user.add(request.user.pk)
            obj.dislikes.user.remove(request.user.pk)
    # http://127.0.0.1:8000/articles/1
    return redirect(request.environ['HTTP_REFERER'])


# def add_to_favorites(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     user = request.user
#     return FavoriteProduct.objects.create(user=user, product=product)
#
#
# def is_favorite(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     user = request.user
#     return FavoriteProduct.objects.filter(user=user, product=product).exists()
#
#
# def delete_from_favorites(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     user = request.user
#     return FavoriteProduct.objects.filter(user=user, product=product).delete()


def add_like(request, obj_id):
    from django.shortcuts import get_object_or_404
    obj = get_object_or_404(Product, pk=obj_id)
    try:
        obj.likes
    except Exception as e:
        Like.objects.create(product=obj)

    if request.user in obj.likes.user.all():
        obj.likes.user.remove(request.user.pk)
    else:
        obj.likes.user.add(request.user.pk)

    return redirect(request.environ['HTTP_REFERER'])


def liked_products(request):
    favorites = Like.objects.filter(user=request.user)
    products = [favorite.product for favorite in favorites]
    context = {
        'products': products
    }
    return render(request, 'core/favorites.html', context)
