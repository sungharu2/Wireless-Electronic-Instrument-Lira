//#include <math.h>

int maxV = 100;
int APIN = A1;
void setup() {
  pinMode(APIN, INPUT);
  Serial.begin(9600);
}

void loop() {
  int r = analogRead(APIN);
  int v = map(r, 0, 1023, 0, maxV);
  /*
    Serial.print("<");
    for (int i=0; i<maxV; i++){
    if (i==v) {
      Serial.print("|");

    }
    else {
      Serial.print("-");
    }

    }
    Seiral.print("> ");
  */
  if (Serial.available()) {
    while(Serial.available()){
      int data = Serial.read();
    }
    Serial.println((String)v);
    Serial.flush();
  }

  delay(20);
}
