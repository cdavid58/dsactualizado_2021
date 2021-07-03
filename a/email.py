from django.utils.crypto import get_random_string
import smtplib 
import requests
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from .models import Token

def recueparPassword(request,email,pk):

    token = get_random_string(length=30)
    Token(
    	valor = token
    ).save()

    remitente = 'fotografiamaqueta@gmail.com'
    destinatarios = ['fotografiamaqueta@gmail.com',str(email)]
    asunto = 'Recuperación de contraseña'

    html = """\
		<!DOCTYPE html>
		<html>
		<head>
			<title></title>
			<style>
				#img{
					background: black;
					position: absolute;
					width: 200px;
					height: 200px;
					top:100px;
					left: 600px;
				}
				#img img{
					width: 200px;
					height: 200px;
				}
				#texto{
					position: absolute;
					top: 350px;
					left: 400px;

				}
			</style>
		</head>
		<body>
			<div id="img">
				<img src="http://localhost:8000/static/curso/img/core-img/logo_dr.gif">
			</div>
			<div id="texto">
				<h3>Dr. Santiago duque te invita a recuperar tu contraseña <a href="http://localhost:8000/setPass/$(token)/$(pk)">Aquí</a></h3>
			</div>
			
		</body>
		</html>


    """
    html = html.replace("$(token)",token)
    html = html.replace("$(pk)",str(pk))

    mensaje = MIMEMultipart()
 
    mensaje['From'] = remitente
    mensaje['To'] = ", ".join(destinatarios)
    mensaje['Subject'] = asunto
 
    mensaje.attach(MIMEText(html,'html'))

    sesion_smtp = smtplib.SMTP('smtp.gmail.com', 587)
    sesion_smtp.starttls()
    sesion_smtp.login('fotografiamaqueta@gmail.com','megatron12#$')
    texto = mensaje.as_string()

    sesion_smtp.sendmail(remitente, destinatarios, texto)
    sesion_smtp.quit()
