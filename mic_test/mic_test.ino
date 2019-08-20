#include <MsTimer2.h>
const int numReadings = 13;

int readings[numReadings];      // the readings from the analog input
int readIndex = 0;              // the index of the current reading
long int total = 0;                  // the running total
int average = 0;                // the average
int PTT_pin = 7;
int sound_value = 0;
boolean flag = 0;
void check_value()
{
  sound_value = getValue();
  Serial.println(sound_value);
  if (sound_value > 600)
  {
    flag = 1;
  }
  if (sound_value < 400) flag = 0;
}
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
  pinMode(PTT_pin, OUTPUT);
  MsTimer2::set(15, check_value); // 500ms period
  MsTimer2::start();
}


void loop() {


  if (flag == 1)
  {
    digitalWrite(PTT_pin, HIGH);
    delay(2000);
  }
  else
  {
    
    digitalWrite(PTT_pin, LOW);
  }
  delay(10);        // delay in between reads for stability
}

float getValue()
{
  total = 0;
  float final_reading_average;
  for (int thisReading = 0; thisReading < numReadings; thisReading++) {
    readings[thisReading] = analogRead(A0);
    total = total + readings[thisReading];
    delay(1);
  }
  final_reading_average = total / numReadings;
  return final_reading_average;
}
