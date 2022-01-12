#include <Keyboard.h>

int key1 = 10;
int key2 = 9;
int key3 = 8;
int key4 = 3;
int key5 = 2;
int key6 = 1;

void setup() {
  pinMode(key1, INPUT_PULLUP);
  pinMode(key2, INPUT_PULLUP);
  pinMode(key3, INPUT_PULLUP);
  pinMode(key4, INPUT_PULLUP);
  pinMode(key5, INPUT_PULLUP);
  pinMode(key6, INPUT_PULLUP);
  Keyboard.begin();
}

void pushKey1() {
// KEY 1
// home
Keyboard.press(KEY_RIGHT_CTRL);
Keyboard.press(97);
Keyboard.release(KEY_RIGHT_CTRL);
Keyboard.release(97);
  delay(300);
}
void pushKey2() {
// KEY 2
// end
Keyboard.press(KEY_RIGHT_CTRL);
Keyboard.press(101);
Keyboard.release(KEY_RIGHT_CTRL);
Keyboard.release(101);
  delay(300);
}
void pushKey3() {
// KEY 3
Keyboard.print("Hello World!");
  delay(300);
}
void pushKey4() {
// KEY 4

  delay(300);
}
void pushKey5() {
// KEY 5
// weird macro
Keyboard.press(KEY_RIGHT_CTRL);
Keyboard.press(97);
Keyboard.release(KEY_RIGHT_CTRL);
Keyboard.release(97);
Keyboard.press(34);
Keyboard.release(34);
Keyboard.press(KEY_RIGHT_CTRL);
Keyboard.press(101);
Keyboard.release(KEY_RIGHT_CTRL);
Keyboard.release(101);
Keyboard.press(34);
Keyboard.release(34);
Keyboard.print(",");
Keyboard.press(KEY_DOWN_ARROW);
Keyboard.release(KEY_DOWN_ARROW);
  delay(300);
}
void pushKey6() {
// KEY 6
// Sublime black
Keyboard.press(KEY_RIGHT_CTRL);
Keyboard.press(KEY_RIGHT_ALT);
Keyboard.press(98);
Keyboard.release(KEY_RIGHT_CTRL);
Keyboard.release(KEY_RIGHT_ALT);
Keyboard.release(98);
  delay(300);
}

void loop() {
  if (digitalRead(key1) == LOW) {
    pushKey1();
  }
  if (digitalRead(key2) == LOW) {
    pushKey2();
  }
  if (digitalRead(key3) == LOW) {
    pushKey3();
  }
  if (digitalRead(key4) == LOW) {
    pushKey4();
  }
  if (digitalRead(key5) == LOW) {
    pushKey5();
  }
  if (digitalRead(key6) == LOW) {
    pushKey6();
  }

}
