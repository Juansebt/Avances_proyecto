"""
URL configuration for project_DAlbas project.

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
from app_DAlbas import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("inicio/", views.inicio),
    path("", RedirectView.as_view(url="/inicio/")),
    path("vistaInicioNosotros/", views.vistaInicioNosotros),
    path("vistaProductos/", views.vistaInicioProductos),
    path("vistaInicioProductos/", views.mostrarProductos),
    path("vistaRegistrarCliente/", views.vistaRegistrarCliente),
    path("registrarCliente/", views.registrarCliente),
    path("vistaLogin/", views.vistaLogin),
    path("vistaPerfilUsuario/", views.vistaPerfilUsuario),
    path('login/', views.login, name='login'),
    path('cerrarSesion/', views.cerrarSesion),
    path('inicioAdministrador/', views.inicioAdministrador, name='inicioAdministrador'),
    path('inicioCliente/', views.inicioCliente, name='inicioCliente'),
    path('vistaRegistrarAdministrador/', views.vistaRegistrarAdministrador),
    path('registrarAdministrador/', views.registrarAdministrador),
    path('vistaRegistrarProducto/', views.vistaRegistrarProducto),
    path('registrarProductos/', views.registrarProductos),
    path('listarProductos/', views.listarProductos),
    path('nosotrosCliente/',views.nosotrosCliente),
    path('nosotrosAdministrador/',views.nosotrosAdministrador),
    path('productoCliente/',views.mostrarProductosCliente),
    path("vistaProductosCliente/", views.vistaProductosCliente),
    path('productoCremaCliente/',views.mostrarProductosCremaCliente),
    path("vistaProductoCremaCliente/", views.vistaProductosCremaCliente),
    path('productoCremaCliente/',views.mostrarProductosCupcakeCliente),
    path("vistaProductoCupcakeCliente/", views.vistaProductosCupcakeCliente),
    path('productoCremaCliente/',views.mostrarProductosGalletaCliente),
    path("vistaProductoGalletaCliente/", views.vistaProductosGalletaCliente),
    path('pedidoCliente',views.vistaRegistrarPedido),
    path("vistaRegistrarPedidos/", views.mostrarPedidosCliente),
    path('consultarProducto/<int:id>/',views.consultarProducto),
    path('actualizarProducto/',views.actualizarProductos),
    path('eliminarProducto/<int:id>/',views.eliminarProducto),
    path('vistaCarritoDeCompras/',views.vistaCarritoCompras),
    #path('productos/<str:catNombre>/', views.productosPorCategoria,name='cliente/productos.html'),
]

#Para poder tener acceso a la carpeta media y poder ver las fotos
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)