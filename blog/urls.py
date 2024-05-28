from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name = 'home'),
    path('about/', about, name = 'about'),
    path('addpage/', addpage, name = 'add_page'),
    path('contact/', contact, name = 'contact'),
    path('logout/', logout_view, name='logout'),
    path('login_or_register/', login_or_register, name='login_or_register'),
    path('post/<int:post_id>/', show_post, name='post'),
    path('category/<int:cat_id>/', show_category, name = 'category'),
    ]
