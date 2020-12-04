import serial
import db_connector as db
#Nota importante: Para correr este archivo desde la terminal en VisualStudio Code,
# se debe usar python3. La sintáxis es: "python3 ArduinoReader.py"
def insert_hr_data(number):
	try:
			# set up the serial line
			# set up serial port
			# set up timeout
		ser = serial.Serial('/dev/cu.usbmodem1412201',9600, timeout = 2)
			#show the dataf
		
		while True:
			#get data from serial port:
			try:
				data = int(ser.readline().decode("utf-8"))
				if data:
					print(data)
					db.insert_hr(number,data)
			except ValueError:
				pass
	except Exception as e:
		print(e)

# si quieren probar la lectura del puerto serial desactivar la linea 22
if __name__ == "__main__":
	insert_hr_data("6576")		