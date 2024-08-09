#include <FastLED.h>

#define NUM_LEDS 60
#define STRIP_TYPE WS2812B
#define Data_Pin 2

CRGB LED[NUM_LEDS];

/*
SIDE NOTES:
- All LEDs work
- Color Order is GRB
*/

void setup() {
  FastLED.addLeds<STRIP_TYPE, Data_Pin, GRB>(LED, NUM_LEDS);
  //To make sure arduino doesnt draw too much power
  FastLED.setMaxPowerInVoltsAndMilliamps(5,500);
  FastLED.clear();
  FastLED.show();
}

void loop() {
  for(int i = 0; i < NUM_LEDS; i++) {
    FastLED.clear();
    LED[i] = CRGB(255,0,0);
    delay(100);
    FastLED.show();
  }
  for(int i = 0; i < NUM_LEDS; i++) {
    FastLED.clear();
    LED[i] = CRGB(0,255,0);
    delay(100);
    FastLED.show();
  }
  for(int i = 0; i < NUM_LEDS; i++) {
    FastLED.clear();
    LED[i] = CRGB(0,0,255);
    delay(100);
    FastLED.show();
  }
}
