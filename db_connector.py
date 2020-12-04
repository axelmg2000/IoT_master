import os
import sys
import sqlite3
from sqlite3 import Error
from datetime import datetime
from matplotlib import pyplot as plt
#from matplotlib.backends.backend_pdf import PdfPages

def find_user(number):
    
    con = sqlite3.connect('mydatabase.db')
    cursorObj = con.cursor()
    sql = 'select * from Paciente where numero="%s"' % (number)
    print(sql)
    cursorObj.execute(sql)
    rows = cursorObj.fetchall()
    for row in rows:
        return(row[1])

#print(find_user("whatsapp:+525514200581"))

def insert_hr(number,data):
    con = sqlite3.connect('mydatabase.db')
    cursorObj = con.cursor()
    sql = 'insert into HeartRate ("id","Numero","Data","Fecha","id_paciente") VALUES (NULL, "{}","{}","{}","{}");'.format(number,data,datetime.now().strftime("%d/%m/%Y %H:%M:%S"),number)
    print(sql)
    cursorObj.execute(sql)
    con.commit()
    con.close()

def create_img(number):
    con = sqlite3.connect('mydatabase.db')
    cursorObj = con.cursor()
    sql = 'select * from HeartRate where Numero="%s"' % (number)
    print(sql)
    cursorObj.execute(sql)
    rows = cursorObj.fetchall()
    con.close()

    x = []
    y = []

    for item in rows:    
        # Este es el orden para seleccionar los datos en la iteración de [rows]
        # 0 -> id, 1 -> Numero, 2 -> Data, 3 -> Fecha, 4 -> id_paciente
        x.append(item[3])
        y.append(item[2])

    fig, ax = plt.subplots()
    fig2 = fig
    ax.plot(x, y)
    ax.set(xlabel='Fecha de consulta', ylabel='HR', title='Heart Rate Graph')
    ax.grid()
    fig.savefig(number.replace(":","_")+".png")
    return

#create_img("whatsapp:+525514200581")  


def db_check():
    if os.path.isfile('mydatabase.db'):        
        print("La Base de Datos existe")    
        return ""   

    else:
        print("La Base de Datos no Existe")
        print("Primero deberas registrar tus datos")
        print()

        print("escribe tu numero celular")        
        numero = "whatsapp:+521"+input();

        print("escribe tu Nombre")        
        nombre = input();

        print("escribe tu Apellido")
        apellido = input();

        print("escribe tu Email")
        email = input();

        con = sqlite3.connect('mydatabase.db')
        cursorObj = con.cursor()

        sql = "CREATE TABLE Paciente ( Numero text PRIMARY KEY, Nombre text, Apellido text, Email text)";
        cursorObj.execute(sql)
        print("tabla paciente -> ok")

        sql = 'INSERT INTO Paciente (Numero, Nombre, Apellido, Email) VALUES ("{}","{}","{}","{}")'.format(numero,nombre,apellido,email);
        cursorObj.execute(sql)
        print("usuario registrado")

        sql = "CREATE TABLE HeartRate ( id INTEGER PRIMARY KEY AUTOINCREMENT, Numero text, Data text, Fecha text, id_paciente text , CONSTRAINT fk_id_paciente FOREIGN KEY(id_paciente) REFERENCES Paciente (Numero))";
        cursorObj.execute(sql)
        print("tabla HeartRate -> ok")
        
        sql = "CREATE TABLE Spo2 ( id INTEGER PRIMARY KEY AUTOINCREMENT, Numero text , Data text, Fecha text, id_paciente text , CONSTRAINT fk_id_paciente FOREIGN KEY(id_paciente) REFERENCES Paciente (Numero))";
        cursorObj.execute(sql)
        print("tabla Spo2 -> ok")

        # guardamos
        con.commit()        
        # cerramos la conexión
        con.close()

        print("Base de Datos creada....")
        return numero


