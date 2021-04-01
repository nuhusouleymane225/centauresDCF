"""Demande URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

#for pdf only




from demande.views import demande_affiche, demande_save, welcome, \
    error404, welcome_admin, rapport_mensuel, logoutTlogin, demande_traitement, demande_traffiche, ViewPDF, ImprimePdf

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', welcome, name='client'),
    path('client/demande/', demande_save, name='faire_demande'), # pas touche
    
    path('demandes/', demande_affiche, name='demandes'), # pas touche
    
    path('error404/', error404),

     path('demandes/traite/pdf/<int:id>', ImprimePdf, name="pdf_view"), #pdf print
    

    path('account/', welcome_admin, name='home'),
    path('rapport/', rapport_mensuel, name='rapport'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('demandes/traitement/<int:id>', demande_traitement, name='traiter-demande'), # pas touche
    path('demandes/traite/', demande_traffiche, name='dtraite'),
    
    path('rapport/', rapport_mensuel, name='rapport'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', logoutTlogin, name='logout'),
    path('account/logout/', lambda request: redirect('logout', permanent=False)),
    path('rapport/logout/', lambda request: redirect('logout', permanent=False)),
    path('demandes/logout/', lambda request: redirect('logout', permanent=False)),
    
    path('demandes/traite/logout/', lambda request: redirect('logout', permanent=False)),
    path('demandes/traitement/logout/', lambda request: redirect('logout', permanent=False)),
    path('login/welcome_admin/', lambda request: redirect('home', permanent=False)),
    
   



]

urlpatterns += static(settings.STATIC_URL, document_root= settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)