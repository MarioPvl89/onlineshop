from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('check-username/', views.check_username, name='check_username'),
    path('catalog/<slug:category_slug>/', views.catalog, name='catalog'),
    path('catalog/', views.catalog, name='catalog_default'),
    path('product/<slug:product_slug>/', views.product_default, name='product_default'),
    path('catalog/<slug:category_slug>/<slug:product_slug>/', views.product, name='product'),
    path('favorite/add/<int:product_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('favorite/remove/<int:favorite_id>/', views.remove_from_favorite, name='remove_from_favorite'),
    path('favorites/', views.favorite_list, name='favorite_list'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/remove/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/increase/<int:item_id>/', views.increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),
]
