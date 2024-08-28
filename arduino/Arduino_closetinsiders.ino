#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN 10
#define RST_PIN 9
MFRC522 mfrc522(SS_PIN, RST_PIN); // Creating an instance of the Card Reader

#define MAX_REGISTERED 10 // Maximum number of registered items
String registered[MAX_REGISTERED] = {"A3 3A 33 1B", "B3 10 4C F5", "C3 26 00 9C"};
int registeredCount = 3; // Initial number of registered items

void setup() {
  Serial.begin(9600);
  SPI.begin();
  mfrc522.PCD_Init();
  Serial.println("Please Bring Up The Item You Want to Scan");
  Serial.println();
}

void loop() {
  // Checks if a new card is present
  if (!mfrc522.PICC_IsNewCardPresent()) {
    return; // If no card is detected
  }
  
  // Read the information
  if (!mfrc522.PICC_ReadCardSerial()) {
    return;
  }

  Serial.print("Card ID: ");
  String cardID = ""; // Stores the ID of the card 
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
    Serial.print(mfrc522.uid.uidByte[i], HEX);
    cardID.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));
    cardID.concat(String(mfrc522.uid.uidByte[i], HEX));
  }
  Serial.println();

  cardID.toUpperCase(); // Convert to uppercase

  bool isRegistered = false;
  for (int j = 0; j < registeredCount; j++) {
    if (cardID.substring(1) == registered[j]) {
      isRegistered = true;
      break;
    }
  }

  // Check if the card ID matches a specific authorized ID
  if (isRegistered || cardID.substring(1) == "D3 BB 86 11") {
    if (cardID.substring(1) == "D3 BB 86 11") {
      Serial.println("Welcome User");
    } else {
      Serial.println("Clothing Is Registered");
    }
    Serial.println();
    delay(3000); // A small delay
  } else {
    Serial.println("Clothing Item Has Not Been Registered");

    // Register the new card if there is space in the array
    if (registeredCount < MAX_REGISTERED) {
      registered[registeredCount] = cardID.substring(1);
      registeredCount++;
      Serial.println("Item Registered Successfully");
    } else {
      Serial.println("Registration Failed: Maximum limit reached");
    }
    Serial.println();
    delay(3000);
  }
}
