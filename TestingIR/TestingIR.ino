int input = A0;
int input2 = A3;
int input3 = A4;

void setup() {
  pinMode(input, INPUT);
  pinMode(input2, INPUT);
  pinMode(input3, INPUT);
  Serial.begin(9600);
}

void loop() {
  int val1 = analogRead(input);
  int val2 = analogRead(input2);
  int val3 = analogRead(input3);
  
  Serial.print(val1);
  Serial.print(",");
  Serial.print(val2);
  Serial.print(",");
  Serial.println(val3);
}
