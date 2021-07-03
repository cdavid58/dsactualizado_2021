from django.conf.urls import url
from .views import *

urlpatterns=[
		url(r'^$',home,name="home"),
		url(r'^cursos/(\d+)/(\d+)/$',cursos,name="cursos"),
		url(r'^salir/$',salir,name="salir"),
		url(r'^videoIntro/(\d+)/$',videoIntro,name="videoIntro"),
		url(r'^loginHome/$',loginHome,name="loginHome"),
		url(r'^registroCurso/$',registroCurso,name="registroCurso"),
		url(r'^recuperaPass/$',recuperaPass,name="recuperaPass"),
		url(r'^setPass/(\w+)/(\d+)/$',setPass,name="setPass"),
		url(r'^informacion/$',informacion,name="informacion"),

		url(r'^addcart/$',addcart,name="addcart"),
		url(r'^detailscart/$',detailscart,name="detailscart"),
		url(r'^cart_remove/$',cart_remove,name="cart_remove"),


		url(r'^cuenta/$',cuenta,name="cuenta"),
		url(r'^curso/(\d+)/$',curso,name="curso"),

		# url(r'^cuentaUsuario/(\d+)/$',cuentaUsuario,name="cuentaUsuario"),
		# url(r'^misCursos/(\w+)/$',misCursos,name="misCursos"),
	]