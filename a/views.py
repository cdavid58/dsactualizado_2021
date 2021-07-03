from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from .models import *
from .email import recueparPassword
from datetime import date
from datetime import datetime
import json


def salir(request):
	del request.session['login']
	del request.session['carrito']
	cart = Carrito(request)
	cart.clear()
	return redirect('/')

def home(request):
	print('Entre')
	if 'carrito' not in request.session:
		request.session['carrito'] = 0
		request.session['location'] = '/'
		request.session['curso'] = 0
	cat = Categoria.objects.all()
	subcategoria = subCategorias.objects.filter(principal=True)
	info = Informacion.objects.get(pk=1)
	if request.is_ajax():
		
		
		if request.GET.get("a") is not None or request.GET.get("b") is not None:
			sms = ""
			try:
				sus = Suscripcion.objects.get(Q(email=request.GET.get("a")) | Q(telefono=request.GET.get("b")))
			except Suscripcion.DoesNotExist:
				sus = None

			if sus is not None:
				sms = "Ya Estas suscrito"
			else:
				Suscripcion(
					email = request.GET.get("a") if request.GET.get("a") != "" else None,
					telefono = request.GET.get("b") if request.GET.get("b") != "" else None
				).save()
				sms = "Suscripción Exitosa!"
			return HttpResponse(sms)
		else:
			datos = request.POST
			Mensaje(
				nombre = datos.get('name'),
				telefono = datos.get('email'),
				asunto = datos.get('subject'),
				message = datos.get('message')
			).save()
			return HttpResponse("OK")

	paginator = Paginator(subcategoria,6)

	page  = request.GET.get('page')

	try:
		products = paginator.page(page)
	except PageNotAnInteger :
		products = paginator.page(1)
	except EmptyPage:
		products = paginator.page(paginator.num_pages)

	podcasts = Podcast.objects.all()

	return render(request,'home/index.html',{'categoria':cat,'products':products,'subcategoria':subcategoria,'info':info,'podcasts':podcasts})

def cursos(request,estilo,pk):

	request.session['location'] = '/cursos/'+str(estilo)+'/'+str(pk)+'/'
	request.session['curso'] = pk
	request.session['estilo'] = estilo
	categoria = Categoria.objects.get(pk=pk)
	subcategoria = subCategorias.objects.filter(categoria=categoria)

	if request.is_ajax():
		sub = subCategorias.objects.get(pk=request.GET.get('id'))
		like = int(sub.like) + 1
		sub.like = like
		sub.save()
		return HttpResponse(like)
	cat = Categoria.objects.all()

	paginator = Paginator(subcategoria,6)

	page  = request.GET.get('page')

	try:
		products = paginator.page(page)
	except PageNotAnInteger :
		products = paginator.page(1)
	except EmptyPage:
		products = paginator.page(paginator.num_pages)

	pages = []
	for i in range(paginator.num_pages):
		pages.append(int(i) + 1)
	print(pages)

	if int(estilo) == 1:
		return render(request,'curso/archive-list.html',{'subcategoria':products,'categoria':cat,'productos':products,'lista':pages})
	return render(request,'curso/archive-grid.html',{'subcategoria':products,'categoria':cat,'productos':products,'lista':pages})


def videoIntro(request,pk):

	if request.method == 'POST':
		try:
			usu = Usuario.objects.get(email = request.POST.get('email'))
		except Usuario.DoesNotExist:
			usu = None
		subcat = subCategorias.objects.get(pk=pk)
		if usu is not None:
			comentarioSubCategoria(
				usuario = usu,
				subcategoria = subcat,
				comentario = request.POST.get('mensaje'),
				fecha = date.today()
			).save()
		else:
			comentarioSubCategoria(
				subcategoria = subcat,
				comentario = request.POST.get('mensaje'),
				fecha = date.today(),
				nombre = request.POST.get('name'),
				email = request.POST.get('email')
			).save()

	subcategoria = subCategorias.objects.get(pk=pk)
	sv = int(subcategoria.visto) + 1
	subcategoria.visto = sv
	comentario = comentarioSubCategoria.objects.filter(subcategoria=subcategoria)
	c = len(comentario) + int(subcategoria.comentarios)
	subcategoria.comentarios = c
	subcategoria.save()
	cat = Categoria.objects.all()


	paginator = Paginator(comentario,10)
	page  = request.GET.get('page')

	try:
		products = paginator.page(page)
	except PageNotAnInteger :
		products = paginator.page(1)
	except EmptyPage:
		products = paginator.page(paginator.num_pages)


	pages = []
	for i in range(paginator.num_pages):
		pages.append(int(i) + 1)
	print(pages)	

	try:
		cursoSiguiente = subCategorias.objects.get(pk= (int(pk) + 1) )
	except Exception as e:
		cursoSiguiente = ""

	try:
		cursoAnterior = subCategorias.objects.get(pk= (int(pk) - 1) )
	except Exception as e:
		cursoAnterior = ""
	
	return render(request,'curso/video-post.html',{'i':subcategoria,'comentario':products,'nc':cursoSiguiente,'pc':cursoAnterior,'categoria':cat,'lista':pages,'productos':products})


def loginHome(request):
	error = False
	if request.method == 'POST':
		try:
			usu = Usuario.objects.get(email=request.POST.get('email'),clave=request.POST.get('pass'))
		except Usuario.DoesNotExist:
			usu = None
		if usu is not None:
			request.session['login'] = request.POST.get('email')
			return redirect(request.session['location'])
		else:
			error = True
			print('Error')
	subcategoria = subCategorias.objects.all()
	cat = Categoria.objects.all()
	return render(request,'curso/login.html',{'categoria':cat,'subcategoria':subcategoria,'error':error})

def registroCurso(request):
	error = False
	if request.method == 'POST':
		try:
			usu = Usuario.objects.get(email=request.POST.get('email'))
		except Usuario.DoesNotExist:
			usu = None
		if usu is not None:
			error = True
			print('Error')
		else:
			Usuario(
				telefono = request.POST.get('tel'),
				email = request.POST.get('email'),
				clave = request.POST.get('pass'),
				dia = request.POST.get('dia'),
				mes = request.POST.get('mes'),
				anio = request.POST.get('anio')
			).save()
			request.session['login'] = request.POST.get('email')
			return redirect(request.session['location'])

	subcategoria = subCategorias.objects.all()
	cat = Categoria.objects.all()
	return render(request,'curso/register.html',{'error':error,'categoria':cat,'subcategoria':subcategoria})

def recuperaPass(request):
	error = False
	if request.method == 'POST':
		try:
			usu = Usuario.objects.get(email=request.POST.get('email'))
		except Usuario.DoesNotExist:
			usu = None

		if usu is not None:
			recueparPassword(request,usu.email,usu.pk)
			return redirect('/informacion/')
		else:
			print('Error')
			error = True


	subcategoria = subCategorias.objects.all()
	cat = Categoria.objects.all()

	return render(request,'curso/recuperarPass.html',{'categoria':cat,'subcategoria':subcategoria,'error':error})

def detailscart(request):

	cart = Carrito(request)
	cat = Categoria.objects.all()
	subcategoria = subCategorias.objects.all()
	transaction = Transaction.objects.get(pk=1)

	suscat = subCategorias.objects.filter(principal=True)

	if request.is_ajax():
		n = int(transaction.numero) + 1
		transaction.numero = n
		transaction.save()
		for i in cart:
			CompraCurso(
				subcategoria = subCategorias.objects.get(pk=i['codigo']),
				user = Usuario.objects.get(email=request.session['login'])
			).save()
		cart.clear()
		request.session['carrito'] = 0
		return HttpResponse(True)

	paginator = Paginator(suscat,6)
	page  = request.GET.get('page')

	total = 0
	for i in cart:
		total += (float(i['total']))


	try:
		products = paginator.page(page)
	except PageNotAnInteger :
		products = paginator.page(1)
	except EmptyPage:
		products = paginator.page(paginator.num_pages)


	return render(request,'home/cart.html',{'cart':cart,'categoria':cat,'subcategoria':subcategoria,
											'products':products,'total':total,'transaction':transaction
											})

def setPass(request,pk,id_usuario):
	if request.method == 'POST':
		try:
			usu = Usuario.objects.get(pk=id_usuario)
		except Usuario.DoesNotExist:
			usu = None
		if usu is not None:
			usu.clave = request.POST.get('pass')
			usu.save()
			return redirect('/loginHome/')
	try:
		Token.objects.get(valor=pk).delete()
		return render(request,'curso/setPass.html')
	except Token.DoesNotExist:
		return render(request,'404.html')


def informacion(request):
	subcategoria = subCategorias.objects.all()
	cat = Categoria.objects.all()
	return render(request,'curso/informacion.html',{'categoria':cat,'subcategoria':subcategoria})



##################################################################################################


def cuenta(request):
	cat = Categoria.objects.all()
	compraCurso = CompraCurso.objects.filter(user=Usuario.objects.get(email=request.session['login']))
	for i in compraCurso:
		print(i)
	return render(request,'cuenta/index.html',{'compraCurso':compraCurso,'categoria':cat})


def curso(request,pk):
	cat = Categoria.objects.all()
	subcategorias = subCategorias.objects.get(pk=pk)
	cursos = Cursos.objects.filter(subcategoria = subcategorias)
	return render(request,'cuenta/video-post.html',{'cursos':cursos,'categoria':cat,'sub':subcategorias})






##################################################################################################


def addcart(request):
	if request.is_ajax():
		print(request.GET.get("id"))
		cart = Carrito(request)
		producto = subCategorias.objects.get(pk=request.GET.get("id"))
		cart.add(producto,1)
		return HttpResponse(request.session['carrito'])


def cart_remove(request):
	if request.is_ajax():
		cart = Carrito(request)
		product = subCategorias.objects.get(pk=request.GET.get('id'))
		cart.remove(product)
		resta = int(request.session['carrito']) - 1
		request.session['carrito'] = resta
		return HttpResponse(request.session['carrito'])





