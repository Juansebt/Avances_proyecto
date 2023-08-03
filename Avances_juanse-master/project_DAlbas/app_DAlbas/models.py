from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from datetime import datetime
from django.utils import timezone

# Create your models here.

tipoUsuarios = [
    ('Cliente',"Cliente"),
    ('Administrativo',"Administrativo"),
]

estadosPedido = [
    ('Pendiente','Pendiente'),
    ('En proceso','En proceso'),
    ('Enviado','Enviado'),
    ('Entregado','Entregado'),
    ('Cancelado','Cancelado'),
]

metodosDePago = [
    ('Transferencia','Transferencia'),
    ('Efectivo','Efectivo')
]

class User(AbstractUser):
    fotoUsuario = models.FileField(upload_to=f"usuarios/",null=True,blank=True,db_comment="Foto del Usuario")
    tipoUsuario = models.CharField(max_length=15,choices=tipoUsuarios,default='Cliente',db_comment="Nombre del Tipo de usuario")
    fechaHoraCreacion  = models.DateTimeField(auto_now_add=True,db_comment="Fecha y hora del registro")
    fechaHoraActualizacion = models.DateTimeField(auto_now=True,db_comment="Fecha y hora última actualización")
    
    def __str__(self) -> str:
        return f"{self.username}"
    
class Clientes(User):
    identificacionCliente = models.CharField(max_length=20,unique=True,db_comment='Identificación del cliente, puede ser cédula o NUIP')
    direccionCliente = models.CharField(max_length=255,null=True,db_comment='Dirección de residencia del cliente')
    telefonoCliente = models.CharField(max_length=20,null=True,db_comment='Número telefono del cliente')
    fechaHoraCreacionCliente = models.DateTimeField(auto_now_add=True,db_comment='Fecha y hora del registro del cliente')
    fechaHoraActualizacionCliente = models.DateTimeField(auto_now=True,db_comment='Fecha y hora última actualización')

    def __str__(self) -> str:
        return f'{self.identificacionCliente}'

class Administradores(User):
    cargoAdministrador = models.CharField(max_length=50,null=True,db_comment='Cargo que ocupa el administrador a registrar')
    fechaHoraCreacionAdmin = models.DateTimeField(auto_now_add=True,db_comment='Fecha y hora del registro')
    fechaHoraActualizacionAdmin = models.DateTimeField(auto_now=True,db_comment='Fecha y hora última actualización')

    def __str__(self) -> str:
        return f'{self.cargoAdministrador}'
    
class Pedidos(models.Model):
    fechaPedido = models.DateTimeField(default=timezone.now,db_comment="Fecha en que realiza el pedido")
    fechaEnvioPedido = models.DateField(db_comment="Fecha en la que se envia el pedido")
    metodoPago = models.CharField(max_length=20,choices=metodosDePago,db_comment="Metodos de pago disponibles")
    valorPedido = models.DecimalField(max_digits=15,decimal_places=2,db_comment="valor del pedido")
    direccionPedido = models.CharField(max_length=15,db_comment="Dirección donde se enviará el pedido")
    estadoPedido = models.CharField(max_length=15,choices=estadosPedido,db_comment="Estado")
    #clientePedido = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,db_comment="Fk del cliente que realiza el pedido")
    fechaHoraCreacion  = models.DateTimeField(auto_now_add=True,db_comment="Fecha y hora del registro")
    fechaHoraActualizacion = models.DateTimeField(auto_now=True,db_comment="Fecha y hora última actualización")
    
    def __str__(self) -> str:
        return f"{self.clientePedido}-{self.estadoPedido}"
    
class Abonos(models.Model):
    fotoComprobanteAbono = models.FileField(upload_to=f"abonos/",null=True,blank=True,db_comment="Foto del comprobante de pago del primer abono del pedido")
    codigoComprobanteAbono = models.CharField(max_length=50,unique=True,db_comment="Código del comprobante del pago del primer abono")
    valorAbono = models.DecimalField(max_digits=15,decimal_places=2,db_comment="Valor de pago del primer abono cincuenta porciento del valor del pedido")
    pedidoAbono = models.ForeignKey(Pedidos,on_delete=models.PROTECT,db_comment="Fk de la tabla pedidos")
    fechaHoraCreacion  = models.DateTimeField(auto_now_add=True,db_comment="Fecha y hora del registro")
    fechaHoraActualizacion = models.DateTimeField(auto_now=True,db_comment="Fecha y hora última actualización")
    
    def __str__(self) -> str:
        return f"{self.pedidoAbono}-{self.valorAbono}-{self.codigoComprobanteAbono}"
    
class Categorias(models.Model):
    catNombre = models.CharField(max_length=50,unique=True,db_comment="Nombre de la categoria")
    
    def __str__(self) -> str:
        return self.catNombre
    
class Productos(models.Model):
    nombreProducto = models.CharField(max_length=50,db_comment="Nombre de producto")
    precioProducto = models.DecimalField(max_digits=15,decimal_places=2,db_comment="precio unitario del producto")
    descripcionProducto = models.TextField(db_comment="Descripción de cada producto de la pasteleria")
    imagenProducto = models.FileField(upload_to=f"productos/",null=True,blank=True,db_comment="Imagen del producto")
    categoriaProducto = models.ForeignKey(Categorias,on_delete=models.PROTECT,db_comment="Fk de la categoria a la que pertenece el producto")
    #adminProducto = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,db_comment="Fk del usuario administrador que registra cada producto")
    fechaHoraCreacion  = models.DateTimeField(auto_now_add=True,db_comment="Fecha y hora del registro")
    fechaHoraActualizacion = models.DateTimeField(auto_now=True,db_comment="Fecha y hora última actualización")
    
    def __str__(self) -> str:
        return f"{self.nombreProducto}-{self.categoriaProducto}"
    
class CarritoCompras(models.Model):
    cantidadProducto = models.IntegerField(db_comment="Cantidad de productos que se el cliente comprará")
    costoProductos = models.DecimalField(max_digits=15,decimal_places=2,db_comment="Costo acumulable de los productos que se van a pedir")
    pedidoCompra = models.ForeignKey(Pedidos,on_delete=models.PROTECT,db_comment="Fk de la tabla pedido")
    productoCompra = models.ForeignKey(Productos,on_delete=models.PROTECT,db_comment="Fk de la tabla productos")
    fechaHoraCreacion  = models.DateTimeField(auto_now_add=True,db_comment="Fecha y hora del registro")
    fechaHoraActualizacion = models.DateTimeField(auto_now=True,db_comment="Fecha y hora última actualización")
    
    def __str__(self) -> str:
        return f"{self.costoProductos}"
    
class Ingredientes(models.Model):
    nombreIngrediente = models.CharField(max_length=20,db_comment="Nombre del ingrediente que se desea adicionar")
    precioIngrediente = models.DecimalField(max_digits=15,decimal_places=2,db_comment="Precio unitario del ingrediente")
    cantidadIngrediente = models.IntegerField(db_comment="Cantidad del ingrediente que se adicionará")
    unidadMedida = models.CharField(max_length=50,null=True,db_comment="unidad de medida del ingrediente")
    color = models.CharField(max_length=30,null=True,db_comment="Color del ingrediente")
    sabor = models.CharField(max_length=30,null=True,db_comment="tipo de sabor del ingrediente si llegase a ser necesario")
    descripcionIngrediente = models.TextField(db_comment="descripción detallada del ingrediente")
    fechaHoraCreacion  = models.DateTimeField(auto_now_add=True,db_comment="Fecha y hora del registro")
    fechaHoraActualizacion = models.DateTimeField(auto_now=True,db_comment="Fecha y hora última actualización")
    
    def __str__(self) -> str:
        return f"{self.nombreIngrediente}-{self.descripcion}"
    
class AdicionDetalle(models.Model):
    descripcionAdicion = models.TextField(db_comment="Descripción detallada de la adición que se la va a hacer al pedido")
    valorAdicion = models.DecimalField(max_digits=15,decimal_places=2,db_comment="valor que le agregará al valor del pedio por realizar un adición extra")
    ingredienteAdicion = models.ForeignKey(Ingredientes,on_delete=models.PROTECT,db_comment="Fk de la tabla ingredientes")
    pedidoAdicion = models.ForeignKey(Pedidos,on_delete=models.PROTECT,db_comment="Fk del pedido al que se le hará la adición")
    fechaHoraCreacion  = models.DateTimeField(auto_now_add=True,db_comment="Fecha y hora del registro")
    fechaHoraActualizacion = models.DateTimeField(auto_now=True,db_comment="Fecha y hora última actualización")
    
    def __str__(self) -> str:
        return f"{self.valorAdicion}"
    
class Comentarios(models.Model):
    contenidoComentario = models.TextField(db_comment="Contenido del comentario")
    #usuarioComentario = models.ForeignKey(User,on_delete=models.PROTECT,db_comment="FK del usuario que escribe el comentario")
    fechaHoraCreacion  = models.DateTimeField(auto_now_add=True,db_comment="Fecha y hora del registro")
    fechaHoraActualizacion = models.DateTimeField(auto_now=True,db_comment="Fecha y hora última actualización")
    
    def __str__(self) -> str:
        return f"{self.contenidoComentario}"