from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Autenticação
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),

    # Dashboard principal
    path('', views.dashboard, name='dashboard'),

    # CRUD de Bancas
    path('bancas/criar/', views.banca_criar, name='banca_criar'),
    path('bancas/<int:pk>/', views.banca_detalhe, name='banca_detalhe'),
    path('bancas/<int:pk>/editar/', views.banca_editar, name='banca_editar'),
    path('bancas/<int:pk>/deletar/', views.banca_deletar, name='banca_deletar'),

    # CRUD de Apostas
    path('bancas/<int:banca_pk>/apostas/criar/', views.aposta_criar, name='aposta_criar'),
    path('apostas/<int:pk>/editar/', views.aposta_editar, name='aposta_editar'),
    path('apostas/<int:pk>/deletar/', views.aposta_deletar, name='aposta_deletar'),
]
