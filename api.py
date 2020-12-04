# API
import os
from flask import Flask, request, send_file
from flask_restful import Resource, Api
from flask_cors import CORS
from twilio.rest import Client
import db_connector as db
import time

app = Flask(__name__)
api = Api(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

#Al ejecutar este archivo y para llevar a cabo la conexión con twilio, primero se debe abrir el puerto 
# Se debe utilizar el commando "./ngrok http 5013" en la terminal
# Al hacer eso se ejecutará una sesión de 8 horas y se generará un a liga
# la cual se pegará en el sandbox de twilio para que twilio al recibir los mensaje transifera los datos a la sesión abierta
# De twilio se deberán copiar el SID: "AC50abe9338c2a1586d3c046db46fbc036"
# También, se copia el auth token: "c0846e71a440211ef0809d0d22e9c6c2"



#cambiar las variables de configuración
account_sid = 'AC50abe9338c2a1586d3c046db46fbc036' 
auth_token = 'c0846e71a440211ef0809d0d22e9c6c2'

class MESSAGE(Resource):
    def post(self):
        req = request.json
        
        #Aquí se obtienen los datos del mensaje recibido por el usuario
        number = request.form['From']
        message_body = request.form['Body'].lower()    
        mensaje =""
                
        client = Client(account_sid, auth_token) 

        if message_body.find("heart rate") == 0:
          db.create_img(number)
          mensaje = " "+db.find_user(number)+ " esta es la información actual de tus registros"          
          print(number)
          message = client.messages.create (
                                      from_='whatsapp:+14155238886',  
                                      body= mensaje,
                                      media_url=['https://094cb2edab24.ngrok.io/image?number='+number],
                                      to= number
                                  )
        else:        
          try:          
            mensaje = "Hola "+db.find_user(number)+ " puedes pedirme tu Heart Rate por el momento."
            message = client.messages.create (
                                    from_='whatsapp:+14155238886',  
                                    body= mensaje,                                  
                                    to= number
                                )                 

          except:
            mensaje = "No estas registrado. Escribe ->  Nombre:Ruben Raya  <- todo junto por favor"            
            message = client.messages.create (
                                    from_='whatsapp:+14155238886',  
                                    body= mensaje,                                  
                                    to= number
                                )                 
            

class IMAGE(Resource):
    def get(self):        
        number = request.args.get('number')
        number = number.replace(": ","_+")        
        print(number)
        filename = number+'.png'
        return send_file(filename, mimetype='image/png')

api.add_resource(MESSAGE, '/message')  # Route_1
api.add_resource(IMAGE, '/image')  # Route_2

if __name__ == '__main__':
    app.run(port='5013')
