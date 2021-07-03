from django.db import models
from django.http import HttpResponseRedirect
from decimal import Decimal
from django.conf import settings
from datetime import date
from datetime import datetime



class Usuario(models.Model):
	nombre = models.CharField(max_length=20,blank=True,null=True)
	apellido = models.CharField(max_length=20,null=True)
	telefono = models.CharField(max_length=10,blank=True,null=True)
	email = models.EmailField(blank=True,null=True)
	bloqueado = models.BooleanField(default=False)
	clave = models.CharField(max_length=16,default='1234')
	dia = models.CharField(max_length=2,default="",null=True,blank=True)
	mes = models.CharField(max_length=15,default="",null=True,blank=True)
	anio = models.CharField(max_length=4,default="",null=True,blank=True)
	imgPerfil = models.ImageField(upload_to='Perifl',default="https://d500.epimg.net/cincodias/imagenes/2016/07/04/lifestyle/1467646262_522853_1467646344_noticia_normal.jpg")

	def __str__(self):
		return self.email


class Categoria(models.Model):
	nombre = models.CharField(max_length=50)
	imagen = models.ImageField(upload_to="ImgCategoria",default="",null=True)

	def __str__(self):
		return self.nombre


class subCategorias(models.Model):
	nombre = models.CharField(max_length=50)
	titulo = models.CharField(max_length=150,default="")
	intro = models.FileField(upload_to="Intro")
	precio = models.CharField(max_length=10)
	categoria = models.ForeignKey(Categoria,on_delete=models.CASCADE)
	duracion = models.CharField(max_length=6)
	descripcion = models.TextField()
	imagen = models.ImageField(upload_to="ImagenIntro")
	videoIntro = models.CharField(max_length=1000,default="https://www.youtube.com/embed/",null=True,blank=True)
	like = models.CharField(max_length=1000,default=0)
	fecha = models.CharField(max_length=10,default=date.today())
	consejo = models.CharField(max_length=200,default="")
	autor = models.CharField(max_length=50,default="")
	visto = models.CharField(max_length=1000,default=0)
	comentarios = models.CharField(max_length=10000,default=0)
	principal = models.BooleanField(default=False)



	def __str__(self):
		return self.nombre

class comentarioSubCategoria(models.Model):
	usuario = models.ForeignKey(Usuario,on_delete=models.CASCADE,default="",null=True)
	subcategoria = models.ForeignKey(subCategorias,on_delete=models.CASCADE)
	comentario = models.TextField(default="")
	fecha = models.CharField(max_length=10,default=date.today())
	nombre = models.CharField(max_length=40,default="",null=True)
	email = models.EmailField(default="",null=True)


class Cursos(models.Model):
	video = models.FileField(upload_to="Videos")
	titulo = models.CharField(max_length=150)
	descripcion = models.TextField()
	duracion = models.CharField(max_length=6)
	subcategoria = models.ForeignKey(subCategorias,on_delete=models.CASCADE,default="")
	imagen = models.ImageField(upload_to="ImagenCursos",null=True,blank=True)

	def __str__(self):
		return self.titulo

class CompraCurso(models.Model):
	subcategoria = models.ForeignKey(subCategorias,on_delete=models.CASCADE)
	user = models.ForeignKey(Usuario,on_delete=models.CASCADE)


class comentarioCurso(models.Model):
	usuario = models.ForeignKey(Usuario,on_delete=models.CASCADE)
	curso = models.ForeignKey(Cursos,on_delete=models.CASCADE)
	comentario = models.TextField()
	fecha = models.CharField(max_length=10)

class likeCurso(models.Model):
	usuario = models.ForeignKey(Usuario,on_delete=models.CASCADE)
	curso = models.ForeignKey(Cursos,on_delete=models.CASCADE)
	comentario = models.TextField()


class Suscripcion(models.Model):
	usuario = models.ForeignKey(Usuario,on_delete=models.CASCADE,null=True)
	email = models.EmailField(default="",null=True,blank=True)
	telefono = models.CharField(max_length=10,default=1234567890,null=True)



class Informacion(models.Model):
	texto_1 = models.TextField()


class Mensaje(models.Model):
	nombre = models.CharField(max_length=50)
	telefono = models.CharField(max_length=10)
	asunto = models.CharField(max_length=50)
	message = models.TextField()

	def __str__(self):
		return self.nombre + ' | '+self.telefono

	

class Carrito(object):
	def __init__(self,request):
		self.session = request.session
		cart = self.session.get(settings.CART_SESSION_ID)
		if not cart:
			cart = self.session[settings.CART_SESSION_ID] = {}
		self.cart = cart
		self.request = request

	def save(self):
		self.session[settings.CART_SESSION_ID]=self.cart
		self.session.modified = True

	def add(self,producto,cantidad = 0):
		if str(producto.pk) in self.cart:
			print('Entre al if')
			cnt = self.cart[str(producto.pk)]
			s = int(cnt['cantidad']) + int(cantidad)
			print(s,'cantidad')
			t = float(producto.precio) * float(s)
			cnt['total'] = t
			cnt['cantidad'] = s
			self.save()
		else:
			total = float(producto.precio) * float(cantidad)
			self.request.session['carrito'] += 1
			print('Entre al else que pasa')
			self.cart[str(producto.pk)] = {'codigo':producto.pk,'articulo':producto.nombre,'cantidad':cantidad,'precio':producto.precio,'total':total,'img':producto.imagen.url,
											'descripcion':producto.descripcion,'titulo':producto.titulo
											}
			
		print(self.cart)

	def remove(self,product):
		product_id = str(product.pk)
		if product_id in self.cart:
			del self.cart[product_id]
			self.save()

	def __iter__(self):
		product_ids = self.cart.keys()
		products = subCategorias.objects.filter(id__in=product_ids)
		for product in products:
			self.cart[str(product.id)]['product']=product

		for item in self.cart.values():
			item['precio']=float(item['precio'])
			item['total']=item['precio']*item['cantidad']
			yield item


	def __len__(self):
		return sum(item['cantidad'] for item in self.cart.values())

	def clear(self):
		del self.session[settings.CART_SESSION_ID]
		self.session.modified = True







class Token(models.Model):
	valor = models.CharField(max_length=30)


class Podcast(models.Model):
	video = models.FileField(upload_to='Podcast')
	titulo = models.CharField(max_length=50)

	def __str__(self):
		return self.titulo


class Transaction(models.Model):
	numero = models.CharField(max_length=20)


















