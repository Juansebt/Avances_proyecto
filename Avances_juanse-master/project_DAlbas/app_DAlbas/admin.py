from django.contrib import admin
from app_DAlbas.models import *

# Register your models here.

admin.site.register(User)
admin.site.register(Clientes)
admin.site.register(Administradores)
admin.site.register(Pedidos)
admin.site.register(Abonos)
admin.site.register(Categorias)
admin.site.register(Productos)
admin.site.register(CarritoCompras)
admin.site.register(Ingredientes)
admin.site.register(AdicionDetalle)
admin.site.register(Comentarios)