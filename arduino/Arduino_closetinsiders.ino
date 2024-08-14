#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN 10
#define RST_PIN 9
MFRC522 mfrc522(SS_PIN, RST_PIN); // setting up the Start of the Reader

void setup() {
  Serial.begin(9600); // Init serial communication
  SPI.begin(); // Init the bus
  mfrc522.PCD_Init(); // Init RFID 
  Serial.println("Please Scan the Clothing item....");
}

void loop() {
  // New Card? OOh it works
  if (!mfrc522.PICC_IsNewCardPresent()) {
    return; // No Card? Womp Womp
  }

  // Try to read the card's serial number
  if (!mfrc522.PICC_ReadCardSerial()) {
    return; // Could not read the card, exit the loop
  }

  // Create a string to store the card ID
  String cardID = "";
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    cardID += String(mfrc522.uid.uidByte[i] < 0x10 ? "0" : "");
    cardID += String(mfrc522.uid.uidByte[i], HEX);
  }

  // Send the card ID to the Raspberry Pi
  Serial.println(cardID);
  delay(1000); // Add a delay to prevent flooding the serial buffer
}