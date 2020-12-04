
# ArduinoReader -> _AR.read()
import ArduinoReader as _AR
# bd_connector ->  find_user(number) , insert_hr(number,data) 
import db_connector as db
import sqlite3
from sqlite3 import Error

# Verify DB
number_active = db.db_check()

if number_active != "":

	print("....Utilizaremos el Numero de celular {} para registrar...".format(number_active))
	_AR.insert_hr_data(number_active)
	
else: #La base de datos si existe

	print("Escribe el numero con el que deseas registrar la información del sensor")
	numero = "whatsapp:+521"+input();
	#Se debe revisar si el número ya existe en la base de datos

	#Primero nos conectamos a la base de datos
	con = sqlite3.connect('mydatabase.db')
	cursorObj = con.cursor()
	#Se ecribe y se ejecuta la consulta
	sql = 'select * from Paciente where Numero="%s"' % (numero)
	cursorObj.execute(sql)
	#Se almacena en rows los datos del renglón
	rows = cursorObj.fetchall()
	con.close() # se cierra la conexión
	if(len(rows) == 0): #Si el tamaño es 0, no existe el número
		print("El número ingresado no está dado de alta")
		nombre = input("Escribe tu nombre\n");
		apellido = input("Escribe tu apellido\n");
		email = input("Escribe tu email\n");
		con = sqlite3.connect('mydatabase.db')
		cursorObj = con.cursor()
		sql = 'INSERT INTO Paciente (Numero, Nombre, Apellido, Email) VALUES ("{}","{}","{}","{}")'.format(numero,nombre,apellido,email)
		cursorObj.execute(sql)
		con.commit() # se guarda
		con.close() # se cierra la conexión

        
	_AR.insert_hr_data(numero)


	
#2361360161


	