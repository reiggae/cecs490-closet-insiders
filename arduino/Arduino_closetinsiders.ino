#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN 10 //SDA
#define RST_PIN 9 //RST
MFRC522 mfrc522(SS_PIN, RST_PIN);  // Create MFRC522 instance
// SCK 13, MOSI 11, MISO 12
void setup() {
  Serial.begin(115200);
  SPI.begin();        // Init SPI bus
  mfrc522.PCD_Init(); // Init MFRC522
}


void loop() {
  // Look for new cards
  if (!mfrc522.PICC_IsNewCardPresent() || !mfrc522.PICC_ReadCardSerial()) {
    delay(50);
    return;
  }

  // Card detected, send the ID
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    if (mfrc522.uid.uidByte[i] < 0x10) {
      Serial.write('0'); // Send a leading zero for values less than 0x10
    }
    Serial.print(mfrc522.uid.uidByte[i], HEX);
  }
  Serial.println(); // Send a newline to indicate end of ID

  // Halt PICC and get ready for new read
  mfrc522.PICC_HaltA();
  mfrc522.PCD_StopCrypto1();

  delay(1000);  // Wait a bit before next read
}
