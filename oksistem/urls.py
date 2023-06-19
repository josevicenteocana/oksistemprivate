"""
URL configuration for oksistem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from eds import views as eds_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', eds_views.iniciar, name='iniciar') ,
    path('eds/', eds_views.eds, name='eds') ,
    path('login/', eds_views.autenticar, name='login'),
    path('panel/', eds_views.panel, name='panel'),
    path('cerrarsesion/', eds_views.cerrarsesion, name='cerrarsesion'),
    path('iniciar/', eds_views.iniciar, name='iniciar'),
    path('registroserialdiario/', eds_views.registroserialdiario, name='registroserialdiario'),
    path('listaseriales/', eds_views.listaseriales, name='listaseriales'),
    path('cierreserial/', eds_views.cierreserial, name='cierreserial'),
    path('eliminarserial/<id>', eds_views.eliminarserial, name='eliminarserial'),
    path('listacierres/', eds_views.listacierres, name='listacierres'),
    path('compras/', eds_views.compras, name='compras'),
    path('nuevafactura/', eds_views.nuevafactura, name='nuevafactura'),
    path('eliminarfactura/<id>', eds_views.eliminarfactura, name='eliminarfactura'),
    path('editarfactura/<id>', eds_views.editarfactura, name='editarfactura'),
    path('registrotanques/', eds_views.registrotanques, name='registrotanques'),
    path('eliminarregistrotanque/<id>', eds_views.eliminarregistrotanque, name='eliminarregistrotanque'),
    path('volumentanques', eds_views.volumentanques, name='volumentanques'),
    path('elivolumenmedida/<id>', eds_views.elivolumenmedida, name='elivolumenmedida'),
    path('autvolumenmedida', eds_views.autvolumenmedida, name='autvolumenmedida'),
    path('buscarmedidastanques', eds_views.buscarmedidastanques, name='buscarmedidastanques'),
    path('cierrediario', eds_views.cierrediario, name='cierrediario'),

    
]
