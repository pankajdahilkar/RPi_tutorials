
#include <Keypad.h>
#include "Keyboard.h"
const byte ROWS = 4; //four rows
const byte COLS = 4; //four columns
//define the cymbols on the buttons of the keypads
byte hexaKeys[ROWS][COLS] = {
  {'1','2','3', '\350' },
  {'4','5','6','\344'},
  {'7','8','9','\346'},
  {'*','0','#','\342'}
};
byte rowPins[ROWS] = {2, 3, 4, 5}; //connect to the row pinouts of the keypad
byte colPins[COLS] = {6, 7, 8, 9}; //connect to the column pinouts of the keypad


//initialize an instance of class NewKeypad
Keypad customKeypad = Keypad( makeKeymap(hexaKeys), rowPins, colPins, ROWS, COLS); 

void setup(){
 // Serial.begin(9600);
 Keyboard.begin();
}  
void loop(){
  char customKey = customKeypad.getKey();
  
  if (customKey){
   // Serial.println(customKey);
    Keyboard.print(customKey);
  }
}
