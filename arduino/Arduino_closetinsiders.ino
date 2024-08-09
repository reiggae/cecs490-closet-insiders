#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN 10
#define RST_PIN 9
MFRC522 mfrc522(SS_PIN, RST_PIN); // creating the general instance of the Card Reader

void setup(){ // why the fuck is the naming convention so stupid
// General setup to run a single time
  Serial.begin(9600);
  SPI.begin();
  mfrc522.PCD_Init();
  Serial.println("Please hold the ID card you want to read..");
  Serial.println();
}


void loop(){
  //checks if the ID card is being help present
  if(!mfrc522.PICC_IsNewCardPresent()) {
    return; // if not card is being detected
  }
  //read the information
  if(!mfrc522.PICC_ReadCardSerial()){
    return;
  }

  Serial.print("Card ID: ");
  String cardID = ""; //Stores the ID of the card 
  for (byte i = 0; i<mfrc522.uid.size; i++){
    Serial.print(mfrc522.uid.uidByte[i] < 0x10 ?" 0" : " " );         // formats the ID
    Serial.print(mfrc522.uid.uidByte[i], HEX);                        // prints in Hex
    cardID.concat(String(mfrc522.uid.uidByte[i]< 0x10 ?" 0" : " " )); //stores the ID
    cardID.concat(String(mfrc522.uid.uidByte[i], HEX));
}
Serial.println();

// Check if the card ID matches a specific authorized ID

cardID.toUpperCase();
// D3 BB 86 11 - Card
// A3 3A 33 1B - Gym Tag
if(cardID.substring(1) == "A3 3A 33 1B")
{
  Serial.println("Good Job, You actually did it: ");
  Serial.println();
  delay(3000); // a small delay
  } else {
  Serial.println("Womp, Womp");
  Serial.println();
  delay(3000);
  }
}