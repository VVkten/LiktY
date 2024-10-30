from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/', views.remove_from_cart, name='remove_from_cart'),

    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('', views.user_login, name='login'),

    path('home/', views.home, name='home'),
    path('about_us/', views.about_us, name='about_us'),
    path('from_sellers/', views.from_sellers, name='from_sellers'),
    path('shopping_cart/', views.shopping_cart, name='shopping_cart'),
    path('account/', views.account, name='account'),

    path('success/', views.success_view, name='success'),

    path('category/<int:category_id>/', views.category_detail, name='category_detail'),

    path('order/', views.order, name='order'),
    path('order_form/', views.order_form, name='order_form'),

    path('product_detail/<int:product_id>/', views.product_detail, name='product_detail')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
