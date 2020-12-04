float factor = 0.75; // Coeficiente de filtro pasa bajo
float maxValue = 0.0; // Almacena valor máximo
int minGapHR = 300; // Distancia entre pulsos
float bfrVal = 500; // Almacena los valores previos
int pulse = 0; // Contador de pulsos
  
int ledPin = 8;
int limite = 65; // Se define un límite de pulso cardiaco, para levantar una bandera en caso de que se supere
int senalSensor = A0; // Un int que guardará el calor recibido en el pin A0

void setup() {
  pinMode(13, OUTPUT); // El pin 13 del arduino se designa que es de salida
  Serial.begin(9600); // Serial empieza a 9600 bps (bits por segundo)
  //Serial.println("Midiendo");
  pinMode(ledPin, OUTPUT); // El pin ledPin que en este caso es el 8 del arduino se designa que es de salida

}
void loop() {
  
  static unsigned long timePM = millis(); // Latidos por minuto [Tiempo Actual]
  static unsigned long btwBeat = millis(); // Tiempo entre latidos Tiempo Actual]
  
  
  int readValue = analogRead(senalSensor);
  float valFilter = factor * bfrVal + (1 - factor) * readValue;  // Filtro pasa bajas
  float change = valFilter - readValue; // Diferencia entre el filtro del valor y el valor leído como tal
  bfrVal = valFilter;

  if((change >= maxValue) && (millis() > btwBeat + minGapHR)) {
     maxValue = change;
     digitalWrite(13, HIGH);
     btwBeat = millis();
     pulse++;
  } 
  else { 
    digitalWrite(13, LOW);
  }
  
  maxValue = maxValue * 0.97;
  if(millis() >= timePM + 15000) {
    // Se agrega un if para revisar si el pulso cardiaco es mayor a un cierto límite
    if((pulse * 4) > limite) {
      digitalWrite(ledPin, HIGH); // Se manda una señal "alta" en el puerto al que ledPin hace referencia
      delay(2000); // Se mantiene el led encendido 2 segundos
      digitalWrite(ledPin, LOW); // Se apaga el led
    }
    //Serial.println("Latidos: ");
    Serial.print(pulse * 4);
    pulse = 0;
    timePM = millis();
  }
  delay(50);
  
}
