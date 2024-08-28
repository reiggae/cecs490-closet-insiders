#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN 10
#define RST_PIN 9
MFRC522 mfrc522(SS_PIN, RST_PIN); // Creating an instance of the Card Reader

// Using a fixed-size String array for registered IDs
String registered[] = {"A3 3A 33 1B", "B3 10 4C F5", "C3 26 00 9C"};

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
  for (int j = 0; j < sizeof(registered) / sizeof(registered[0]); j++) {
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
    Serial.println();
    delay(3000);
  }
}
