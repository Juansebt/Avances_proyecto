from django.shortcuts import render, redirect
from django.db import Error, transaction
from django.contrib.auth.models import Group
from app_DAlbas.models import *
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from smtplib import SMTPException
from django.contrib import auth, messages
from django.urls import reverse
from django.conf import settings
from email.mime.text import MIMEText
from django import forms
import urllib.parse
import urllib.request
import threading
#import requests
import smtplib
import time
import sqlite3
import urllib
import json
import random
import string
import os

# Create your views here.

# VISTAS INICIALES
def inicio(request):
    return render(request, "inicio.html")

def vistaInicioProductos(request):
    return render(request, "productos.html")

def vistaInicioNosotros(request):
    return render(request, "nosotros.html")

def mostrarProductos(request):
    try:
        productos = Productos.objects.all()
        mensaje = ""
        # print(productos)
    except Error as error:
        mensaje = f"Problemas al alistar los productos {error}"
    retorno = {"mensaje": mensaje, "listaProductos": productos}
    return render(request, "productos.html", retorno)


# FUNCIÓN PARA GENERAR UNA CONTRASEÑA
def generarPassword():
    longitud = 8
    caracteres = string.ascii_lowercase + \
        string.ascii_uppercase + string.digits + string.punctuation
    password = ''
    for i in range(longitud):
        password += ''.join(random.choice(caracteres))
    return password


# FUNCIÓN PARA ENVIAR CORREO ELECTRONICO
def enviarCorreo(asunto=None, mensaje=None, destinatario=None):
    remitente = settings.EMAIL_HOST_USER
    template = get_template('enviarCorreo.html')
    contenido = template.render({
        'destinatario': destinatario,
        'mensaje': mensaje,
        'asunto': asunto,
        'remitente': remitente,
    })
    try:
        correo = EmailMultiAlternatives(
            asunto, mensaje, remitente, [destinatario])
        correo.attach_alternative(contenido, 'text/html')
        correo.send(fail_silently=True)
    except SMTPException as error:
        print(error)
    
    
# REGISTRO CLIENTE
def vistaRegistrarCliente(request):
    roles = Group.objects.all()
    retorno = {"roles": roles, "user": None, "tipoUsuario": tipoUsuarios}
    return render(request, "administrador/registrarCliente.html", retorno)

def registrarCliente(request):
    estado = False
    mensaje = f""
    try:
        nombres = request.POST["txtNombres"]
        apellidos = request.POST["txtApellidos"]
        identificacion = request.POST["txtIdentificacion"]
        correo = request.POST["txtCorreo"]
        direccion = request.POST["txtDireccion"]
        telefono = request.POST["txtTelefono"]
        # tipo = "Cliente"
        foto = request.FILES.get("fileFoto", False)
        passwordGenerado = generarPassword()
        idRol = 2
        
        phone = f'+57{telefono}'

        with transaction.atomic():
            user = Clientes(identificacionCliente=identificacion, direccionCliente=direccion,
                            telefonoCliente=phone, username=correo, first_name=nombres, last_name=apellidos,
                            email=correo, fotoUsuario=foto, password=passwordGenerado)
            user.save()
            
            rol = Group.objects.get(pk=idRol)
            user.groups.add(rol)

            user.save()

            # Ecriptar contraseña

            passwordGenerado = generarPassword()
            print(f"constraseña: {passwordGenerado}")

            user.set_password(passwordGenerado)

            user.save()

            estado = True
            mensaje = f"Ususario agregado correctamente"
            retorno = {"mensaje": mensaje, "estado": estado}

            # enviar correo al usuario
            asunto = "Registro Cliente - D'Albas Pastelería"
            mensaje = f"""
                    <html>
                        <head></head>
                        <body>
                            <p>Cordial saludo, {user.first_name} {user.last_name}.</p>
                            <p>¡Bienvenido(a) a nuestro sistema D'Albas! Su registro ha sido exitoso.</p>
                            <p>A continuación, le proporcionamos sus datos de acceso:</p>
                            <ul>
                                <li>Nombre de usuario: {user.username}</li>
                                <li>Contraseña: {passwordGenerado}</li>
                            </ul>
                            <p>Le recomendamos que mantenga su contraseña confidencial y no la comparta con nadie.</p>
                            <p>Por favor, ingrese al sistema utilizando los datos de acceso establecidos</p>
                            <p>Si tiene alguna pregunta o necesita ayuda, no dude en contactarnos:</p>
                            <ul>
                                <li>Teléfonos: 3185504427 - 3178860724</li>
                                <li>Correo: dalbas.288@gmail.com</li>
                            </ul>
                            <p class="">Te invitamos a que visites nuestra página de <a href="https://www.facebook.com/dalbaspasteleria" style="text-decoration: none; color: #F26699;">Facebook</a>.</p>
                        </body>
                    </html>
                    """
            threa = threading.Thread(
                target=enviarCorreo, args=(asunto, mensaje, user.email))
            threa.start()
            # time.sleep(5)
            return redirect("/vistaLogin/", retorno)
    except Error as error:
        transaction.rollback()
        mensaje = f"{error}"
    retorno = {"mensaje": mensaje, "user": user, "estado": estado}
    return render(request, "administrador/registrarCliente.html", retorno)


# REGISTRO ADMINISTRADOR
def vistaRegistrarAdministrador(request):
    roles = Group.objects.all()
    retorno = {"roles": roles, "user": None, "tipoUsuario": tipoUsuarios}
    return render(request, "administrador/registrarAdministrador.html", retorno)

def registrarAdministrador(request):
    estado = False
    mensaje = f""
    try:
        nombres = request.POST["txtNombres"]
        apellidos = request.POST["txtApellidos"]
        correo = request.POST["txtCorreo"]
        tipoUser = "Administrativo"
        cargo = request.POST["txtCargo"]
        foto = request.FILES.get("fileFoto", False)
        passwordGenerado = generarPassword()
        idRol = 1

        with transaction.atomic():
            user = Administradores(cargoAdministrador=cargo, username=correo, first_name=nombres,
                                   last_name=apellidos, email=correo, tipoUsuario=tipoUser,
                                   fotoUsuario=foto, password=passwordGenerado)
            
            user.save()

            rol = Group.objects.get(pk=idRol)
            user.groups.add(rol)
            
            if(rol.name=="Administrador"):
                user.is_staff = True
                user.is_superuser = True

            user.save()

            # Ecriptar contraseña

            passwordGenerado = generarPassword()
            print(f"contraseña: {passwordGenerado}")

            user.set_password(passwordGenerado)

            user.save()

            estado = True
            mensaje = f"Ususario agregado correctamente"
            retorno = {"mensaje": mensaje, "estado": estado}

            # enviar correo al usuario
            asunto = "Registro Administrador - D'Albas Pastelería"
            mensaje = f"""
                    <html>
                        <head></head>
                        <body>
                            <p>Cordial saludo, {user.first_name} {user.last_name}.</p>
                            <p>Felicidades, has sido registrado como administrador en nuestra plataforma.</p>
                            <p>¡Es hora de poner manos a la obra y mantener todo funcionando sin problemas!</p>
                            <p>A continuación, le proporcionamos sus datos de acceso:</p>
                            <ul>
                                <li>Nombre de usuario: {user.username}</li>
                                <li>Contraseña: {passwordGenerado}</li>
                            </ul>
                            <p>Le recomendamos que mantenga su contraseña confidencial y no la comparta con nadie.</p>
                            <p>Por favor, ingrese al sistema utilizando los datos de acceso establecidos</p>
                            <p>Si tiene alguna pregunta o necesita ayuda, escribenos: dalbas.288@gmail.com</p>
                        </body>
                    </html>
                    """
            threa = threading.Thread(
                target=enviarCorreo, args=(asunto, mensaje, user.email))
            threa.start()
            # time.sleep(5)
            return redirect("/vistaLogin/", retorno)
    except Error as error:
        transaction.rollback()
        mensaje = f"{error}"
    retorno = {"mensaje": mensaje, "user": user, "estado": estado}
    return render(request, "administrador/registrarAdministrador.html", retorno)








# REGISTRO DE PRODUCTOS - modificar!
def vistaRegistrarProducto(request):
    user =  Administradores.objects.all()
    categoriasProducto = Categorias.objects.all()
    retorno = {"user":user,"categoriasProducto":categoriasProducto}
    return render(request, "administrador/registrarProducto.html", retorno)

def registrarProductos(request):
    estado = False
    mensaje = ""
    try:
        nombre = request.POST["txtNombreProducto"]
        precio = int(request.POST["txtPrecio"])
        descripcion = request.POST["txtDescripcion"]
        imagen = request.FILES.get("fileFoto", False)
        idCategoria = int(request.POST["cbCategoria"])
        # Obtener la categoria de acuerdo al id
        catProducto = Categorias.objects.get(pk=idCategoria)
        
        with transaction.atomic():
            product = Productos(nombreProducto=nombre, precioProducto=precio, descripcionProducto=descripcion,
                                imagenProducto=imagen, categoriaProducto=catProducto)
            
            product.save()
            mensaje="Producto agregado correctamente"
            return redirect("/listarProductos/")
    except Error as error:
        transaction.rollback()
        mensaje=f"Problemas al realizar el proceso de agregar un producto: {error}"
    retorno={"mensaje":mensaje,"estado":estado}
    return render(request, "administrador/registrarProducto.html", retorno)

def listarProductos(request):
    try:
        productos = Productos.objects.all()
        categorias = Categorias.objects.all()
        mensaje=""
        # print(productos)
    except Error as error:
        mensaje=f"Problemas al alistar los productos {error}"
    retorno={"mensaje":mensaje,"listaProductos":productos,"categorias":categorias}
    return render(request,"administrador/listarProducto.html", retorno)









# LOGIN
def vistaLogin(request):
    # return render(request, "login.html")
    if (cerrarSesion):
        mensaje = f"Se ha cerrado sesión"
    retorno = {"mensaje": mensaje}
    return render(request, "login.html", retorno)

def cerrarSesion(request):
    logout(request)
    # eliminar la sesión actual
    request.session.flush()
    return redirect("/vistaLogin/")

def login(request):
    # validar recaptcha
    """ Begin reCAPTCHA validation """
    recaptcha_response = request.POST.get('g-recaptcha-response')
    url = 'https://www.google.com/recaptcha/api/siteverify'
    values = {
        'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
        'response': recaptcha_response
    }
    data = urllib.parse.urlencode(values).encode()
    req = urllib.request.Request(url, data=data)
    response = urllib.request.urlopen(req)
    result = json.loads(response.read().decode())
    print(result)
    """ End reCAPTCHA validation """
    
    if result['success']:
        username = request.POST['txtUsername']
        password = request.POST['txtPassword']
        user = authenticate(username=username, password=password)
        if user is not None:
            # registrar la varibale de sesión
            auth.login(request, user)
            if user.groups.filter(name='Administrador').exists():
                return redirect('/inicioAdministrador/')
            else:
                return redirect('/inicioCliente/')
        else:
            mensaje = f"Usuario o contraseña incorrectas"
            return render(request,"login.html",{"mensaje":mensaje})
    else:
        mensaje = f"Debe validar primero el recaptcha"
        return render(request,"login.html",{"mensaje":mensaje})

def inicioAdministrador(request):
    if request.user.is_authenticated:
        return render(request, "administrador/inicioAdministrador.html")
    else:
        retorno = {"mensaje": "Debe ingresar con sus credenciales"}
        return render(request, "login.html", retorno)

def inicioCliente(request):
    if request.user.is_authenticated:
        return render(request, "cliente/inicioCliente.html")
    else:
        retorno = {"mensaje": "Debe ingresar con sus credenciales"}
        return render(request, "login.html", retorno)
    
    
def nosotrosCliente(request):
    if request.user.is_authenticated:
        return render(request, "cliente/nosotros.html")
    else:
        retorno = {"mensaje": "Debe ingresar con sus credenciales"}
        return render(request, "login.html", retorno)
    
    
def nosotrosAdministrador(request):
    if request.user.is_authenticated:
        return render(request, "administrador/nosotros.html")
    else:
        retorno = {"mensaje": "Debe ingresar con sus credenciales"}
        return render(request, "login.html", retorno)







def mostrarProductosCliente (request):
    if request.user.is_authenticated:
        return render(request, "cliente/productos.html")
    else:
        retorno = {"mensaje": "Debe ingresar con sus credenciales"}
        return render(request, "login.html", retorno)


def vistaProductosCliente(request):
    try:
        productos = Productos.objects.all()
        mensaje = ""
        # print(productos)
    except Error as error:
        mensaje = f"Problemas al alistar los productos {error}"
    retorno = {"mensaje": mensaje, "listaProductos": productos}
    return render(request, "cliente/productos.html", retorno)





def mostrarProductosCremaCliente(request):
    if request.user.is_authenticated:
        return render(request, "cliente/productosCrema.html")
    else:
        retorno = {"mensaje": "Debe ingresar con sus credenciales"}
        return render(request, "login.html", retorno)


def vistaProductosCremaCliente(request):
    try:
        productos = Productos.objects.all()
        mensaje = ""
        # print(productos)
    except Error as error:
        mensaje = f"Problemas al alistar los productos {error}"
    retorno = {"mensaje": mensaje, "listaProductos": productos}
    return render(request, "cliente/productosCrema.html", retorno)


def mostrarProductosCupcakeCliente(request):
    if request.user.is_authenticated:
        return render(request, "cliente/productosCupcakes.html")
    else:
        retorno = {"mensaje": "Debe ingresar con sus credenciales"}
        return render(request, "login.html", retorno)


def vistaProductosCupcakeCliente(request):
    try:
        productos = Productos.objects.all()
        mensaje = ""
        # print(productos)
    except Error as error:
        mensaje = f"Problemas al alistar los productos {error}"
    retorno = {"mensaje": mensaje, "listaProductos": productos}
    return render(request, "cliente/productosCupcakes.html", retorno)


def mostrarProductosGalletaCliente(request):
    if request.user.is_authenticated:
        return render(request, "cliente/productosGalletas.html")
    else:
        retorno = {"mensaje": "Debe ingresar con sus credenciales"}
        return render(request, "login.html", retorno)


def vistaProductosGalletaCliente(request):
    try:
        productos = Productos.objects.all()
        mensaje = ""
        # print(productos)
    except Error as error:
        mensaje = f"Problemas al alistar los productos {error}"
    retorno = {"mensaje": mensaje, "listaProductos": productos}
    return render(request, "cliente/productosGalletas.html", retorno)


def vistaRegistrarPedido(request):
    if request.user.is_authenticated:
        return render(request, "cliente/registrarPedido.html")
    else:
        retorno = {"mensaje": "Debe ingresar con sus credenciales"}
        return render(request, "login.html", retorno)
    
    
def mostrarPedidosCliente(request):
    try:
        pedidos = Pedidos.objects.all()
        mensaje = ""
        # print(productos)
    except Error as error:
        mensaje = f"Problemas al alistar los pedidos {error}"
    retorno = {"mensaje": mensaje, "listaPedidos": pedidos}
    return render(request, "cliente/registrarPedido.html", retorno)


def vistaPerfilUsuario(request):
    return render(request, "cliente/perfilusuario.html")


def consultarProducto(request, id):
    try:
        producto=Productos.objects.get(id=id)
        mensaje=""
        precio=int(producto.precioProducto)
    except Error as error:
        mensaje=f"Problemas {error}"
        
    retorno={"mensaje":mensaje,"producto":producto,"precio":precio}
    return render(request,"administrador/frmEditar.html",retorno)

def actualizarProductos(request):
    idProducto=int(request.POST["idProducto"])
    nombre=request.POST["txtNombre"]
    precio=int(request.POST["txtPrecio"])
    descripcion=request.POST["txtDescripcion"]
    archivo=request.FILES.get("fileFoto", False)
    try:
        producto=Productos.objects.get(id=idProducto)
        producto.nombreProducto=nombre
        producto.precioProducto=precio
        producto.descripcionProducto=descripcion
        if archivo:
            producto.imagenProducto=archivo
        else:
            producto.imagenProducto=producto.imagenProducto
        producto.save()
        mensaje="Producto actualizado correctamente"
        return redirect("/listarProductos/")
    except Error as error:
        mensaje=f"Problemas al realizar el proceso de actualizar el producto {error}"
        retorno={"mensaje":mensaje,"producto":producto}
        return render(request,"administrador/frmEditar.html",retorno)
    
    
    
def eliminarProducto(request,id):
    try:
        producto=Productos.objects.get(id=id)
        if producto.imagenProducto:
            imagen=producto.imagenProducto.path
            if os.path.exists(imagen):
                os.remove(imagen)
        producto.delete()
        mensaje="Producto eliminado correctamente"
    except Error as error:
        mensaje=f"Problemas al eliminar el producto {error}"
    retorno={"mensaje":mensaje}
    return redirect("/listarProductos/", retorno)


#para revisar

def vistaCarritoCompras(request):
    if request.user.is_authenticated:
        return render(request, "cliente/carrito.html")
    else:
        retorno = {"mensaje": "Debe ingresar con sus credenciales"}
        return render(request, "login.html", retorno)



# def productosPorCategoria(request,catNombre):
#     categoria = Categorias.objects.get(Categorias=catNombre)
#     producto = Productos.objects.filter(categoria=categoria)
#     context = {'categoria':categoria, 'producto':producto}
#     return render(request,"cliente/productos.html",context)

