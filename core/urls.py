from django.urls import path

from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('categories/<int:category_id>', views.get_products_by_categories, name='category_products'),
    path('products/<int:product_id>', views.product_detail, name='product_detail'),
    path('sopping_cart/<str:username>', views.shopping_cart, name='shopping_cart'),
    path('registration', views.registration_view, name='registration'),
    path('login', views.login_view, name='login'),
    path('logout', views.user_logout, name='logout'),
    path('<int:obj_id>/', views.add_like, name='add_like'),
    path('favorites/', views.liked_products, name='favorites'),
    path('search/', views.SearchResults.as_view(), name='search')
    ]
