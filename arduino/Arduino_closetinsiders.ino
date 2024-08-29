#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN 3 //SDA
#define RST_PIN 2 //RST
MFRC522 mfrc522(SS_PIN, RST_PIN); // Creating an instance of the Card Reader

// SCK 13, MOSI 11, MISO 12

#define ClothingCapacity 10 // A Cap on the size of the closet (could be increased)
#define UserCapacity 2  // A Cap on the number of authorized users

// Arrays for registered items and users
String clothingItem[ClothingCapacity] = {"A3 3A 33 1B", "B3 10 4C F5", "C3 26 00 9C"};
bool isCheckedIn[ClothingCapacity] = {true, true, true}; // Status if it's inside the closet
int registeredItemCount = 3;

String registeredUsers[UserCapacity] = {"D3 BB 86 11"};
int registeredUserCount = 1; // currently only one person is registered in the system

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

  bool isRegisteredUser = false;
  for (int i = 0; i < registeredUserCount; i++) {
    if (cardID.substring(1) == registeredUsers[i]) {
      isRegisteredUser = true;
      break;
    }
  }

  if (isRegisteredUser) {
    // Allow the user to handle item registration or checking in/out
    handleAuthorizedUser();
  } else {
    Serial.println("Access Denied: Unauthorized User");
    Serial.println();
    delay(3000);
  }
}

void handleAuthorizedUser() {
  Serial.println("Authorized User Detected");
  Serial.println("Please Scan an Item to Check In/Out or Register");
  
  while (true) {
    // Wait for the user to scan a card
    if (!mfrc522.PICC_IsNewCardPresent()) {
      continue; // If no card is detected, continue waiting
    }
    if (!mfrc522.PICC_ReadCardSerial()) {
      continue;
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

    // Check if the scanned card is a registered user card
    bool isRegisteredUser = false;
    for (int i = 0; i < registeredUserCount; i++) {
      if (cardID.substring(1) == registeredUsers[i]) {
        isRegisteredUser = true;
        delay(3000);
        break;
      }
    }

    if (isRegisteredUser) {
      // If the user scans their card again, break the loop and exit
      Serial.println("Exiting Authorized Mode");
      Serial.println();
      delay(3000);
      return;
    }

    handleItemRegistration(cardID);
    
    // Add a delay to prevent the same card from being scanned twice quickly
    delay(1000); // 1 second delay, can be adjusted if necessary
  }
}

void handleItemRegistration(String cardID) {
  bool isRegisteredItem = false;
  int itemIndex = -1;
  for (int j = 0; j < registeredItemCount; j++) {
    if (cardID.substring(1) == clothingItem[j]) {
      isRegisteredItem = true;
      itemIndex = j;
      break;
    }
  }

  if (isRegisteredItem) {
    // Toggle the status of the item
    isCheckedIn[itemIndex] = !isCheckedIn[itemIndex];
    if (isCheckedIn[itemIndex]) {
      Serial.println("Clothing Item Checked In");
    } else {
      Serial.println("Clothing Item Checked Out");
    }
    Serial.println();
    delay(3000); // A small delay
  } else {
    Serial.println("Clothing Item Has Not Been Registered");
    char response;

    // Prompt the user to register the item until they provide a valid response (Y/N)
    do {
      Serial.println("Do you want to register this clothing item? (Y/N)");
      while (!Serial.available()); // Wait until something is entered
      response = Serial.read(); // Read the input
      response = toupper(response); // Convert to uppercase
    } while (response != 'Y' && response != 'N');

    if (response == 'Y') {
      // Register the new card if there is space in the array
      if (registeredItemCount < ClothingCapacity) {
        clothingItem[registeredItemCount] = cardID.substring(1);
        isCheckedIn[registeredItemCount] = true; // Initially checked in
        registeredItemCount++;
        Serial.println("Item Registered Successfully");
      } else {
        Serial.println("Registration Failed: User Has Declined to Register Clothing Item");
      }
    } else {
      Serial.println("Clothing Item Not Registered");
    }
    Serial.println();
    delay(3000);
  }
}
