const int potPin1 = A0; // 最初のポテンショメータ用ピン
const int potPin2 = A1; // 二つ目のポテンショメータ用ピン
const int startButtonPin = 2; // スタートボタン用ピン
const int stopButtonPin = 3; // ストップボタン用ピン

bool isMeasuring = false;
unsigned long startTime;
unsigned long previousMillis = 0;
const unsigned long interval = 100; // 0.1秒

void setup() {
  pinMode(potPin1, INPUT);
  pinMode(potPin2, INPUT);
  pinMode(startButtonPin, INPUT_PULLUP);
  pinMode(stopButtonPin, INPUT_PULLUP);
  Serial.begin(9600);
}

void loop() {
  if (digitalRead(startButtonPin) == LOW && !isMeasuring) {
    isMeasuring = true;
    startTime = millis();
  }

  if (digitalRead(stopButtonPin) == LOW && isMeasuring) {
    isMeasuring = false;
  }

  if (isMeasuring) {
    unsigned long currentMillis = millis();
    if (currentMillis - previousMillis >= interval) {
      previousMillis = currentMillis;
      unsigned long elapsedTime = currentMillis - startTime;
      int angle1 = map(analogRead(potPin1), 0, 1023, 0, 180); // 0-1023の範囲を0-180度にマップ
      int angle2 = map(analogRead(potPin2), 0, 1023, 0, 180); // 同上

      unsigned long totalSeconds = elapsedTime / 1000;
      unsigned long hours = totalSeconds / 3600;
      unsigned long minutes = (totalSeconds % 3600) / 60;
      unsigned long seconds = totalSeconds % 60;
      unsigned long centiseconds = (elapsedTime % 1000) / 10;

      Serial.print(hours);
      Serial.print(":");
      Serial.print(minutes);
      Serial.print(":");
      Serial.print(seconds);
      Serial.print(".");
      Serial.print(centiseconds);
      Serial.print(",");
      Serial.print(angle1);
      Serial.print(",");
      Serial.println(angle2);
    }
  }
}
