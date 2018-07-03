from django.urls import path
from django.contrib.auth import views as auth_views

from. import views

urlpatterns = [
    path('login/', views.blog_login, name='blog_login'),
    path('register/', views.blog_register, name='blog_register'),
    path('logout/', views.logout, name='logout'),
    path('password_change/', auth_views.password_change, {"post_change_redirect": '/account/password_change_done'},
         name='password_change'),
    path('password_change_done/',
         auth_views.password_change_done,
         name='password_change_done'),
    path('myself/', views.myself, name='myself'),
    path('edit_myself/', views.edit_myself, name='edit_myself'),
]
