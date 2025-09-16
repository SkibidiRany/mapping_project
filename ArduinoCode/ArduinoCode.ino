#include <LiquidCrystal_I2C.h> // LCD

// ==== Motor Pins ====
#define LeftMotor1 2
#define LeftMotor2 3
#define RightMotor1 4
#define RightMotor2 5

// ==== LED Pins ====
#define FrontLEDs 6
#define RightLEDs 7
#define BackLEDs 8
#define LeftLEDs 9

// ==== IR Sensor Pins ====
#define LeftIR A0
#define RightIR 10

// ==== Ultrasonic Pins ====
#define trigPin 11
#define echoPin 12

// ==== LCD ====
LiquidCrystal_I2C lcd(0x27, 16, 2);

// ==== Global Variables ====
bool FallingRight = false;
bool FallingLeft = false;
String lastCommand = "";

// ==== Constants ====
const String FrontCommand = "forward";
const String BackCommand  = "back";
const String RightCommand = "right";
const String LeftCommand  = "left";
const String StopCommand  = "stop";

// ==== Setup ====
void setup() {
  Serial.begin(9600);

  // Motor Pins
  pinMode(LeftMotor1, OUTPUT);
  pinMode(LeftMotor2, OUTPUT);
  pinMode(RightMotor1, OUTPUT);
  pinMode(RightMotor2, OUTPUT);

  // LEDs
  for(int i=6; i<=9; i++) pinMode(i, OUTPUT);

  // IR Sensors
  pinMode(LeftIR, INPUT);
  pinMode(RightIR, INPUT);

  // Ultrasonic
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  // LCD
  lcd.begin(16,2);
  lcd.backlight();
  PrintToLCD("Initializing...", true);
  delay(1500);
  PrintToLCD("Ready", true);
}

// ==== Main Loop ====
void loop() {
  // 1) Read sensors and send to Python
  float distance = GetDistanceCM();
  int leftIR = digitalRead(LeftIR);
  int rightIR = digitalRead(RightIR);

  Serial.print("S;");
  Serial.print("ultra="); Serial.print(distance); Serial.print(";");
  Serial.print("ir1="); Serial.print(leftIR); Serial.print(";");
  Serial.print("ir2="); Serial.println(rightIR);

  // 2) Read command from Python
  if(Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();
    lastCommand = cmd;
    Move(cmd);
  }

  // 3) Check fall
  CheckForFall();
  if(FallingRight || FallingLeft) DealWithFall();

  delay(100); // adjust sensor update speed
}

// ==== Fall Detection ====
void CheckForFall() {
  FallingLeft = digitalRead(LeftIR) == HIGH;
  FallingRight = digitalRead(RightIR) == HIGH;
}

void DealWithFall() {
  SkibidiStopMotors(true);
  float distance = GetDistanceCM();

  if(FallingRight && FallingLeft) PrintToLCD("Falling Both!", true);
  else if(FallingRight) PrintToLCD("Falling Right!", true);
  else if(FallingLeft) PrintToLCD("Falling Left!", true);

  delay(500);

  // Move away from edge
  SkibidiBackward(false);
  delay(700);

  if(FallingRight && !FallingLeft) SkibidiLeft(false);
  else if(FallingLeft && !FallingRight) SkibidiRight(false);

  delay(300);
  SkibidiStopMotors(false);
  FallingLeft = FallingRight = false;
}

// ==== Ultrasonic ====
float GetDistanceCM() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  long duration = pulseIn(echoPin, HIGH);
  float distance = duration * 0.034 / 2.0;
  return distance;
}

// ==== Movement ====
void Move(String direction) {
  if(direction == FrontCommand) SkibidiForward(true);
  else if(direction == BackCommand) SkibidiBackward(true);
  else if(direction == LeftCommand) SkibidiLeft(true);
  else if(direction == RightCommand) SkibidiRight(true);
  else SkibidiStopMotors(true);
}

// ==== Motors + LEDs ====
void moveMotors(int l1, int l2, int r1, int r2) {
  digitalWrite(LeftMotor1, l1);
  digitalWrite(LeftMotor2, l2);
  digitalWrite(RightMotor1, r1);
  digitalWrite(RightMotor2, r2);
}

void HandleLEDs(int front, int back, int right, int left) {
  digitalWrite(FrontLEDs, front);
  digitalWrite(BackLEDs, back);
  digitalWrite(RightLEDs, right);
  digitalWrite(LeftLEDs, left);
}

// ==== LCD ====
void PrintToLCD(String msg, bool override) {
  static String lastMsg = "";
  if(override) {
    if(lastMsg != msg) {
      lcd.clear();
      lastMsg = msg;
    } else return;
  }
  lcd.setCursor(0,0);
  lcd.print(msg);
}

// ==== Motor Functions ====
void SkibidiForward(bool toPrint) { if(toPrint) PrintToLCD("Forward",true); moveMotors(HIGH,LOW,HIGH,LOW); HandleLEDs(HIGH,LOW,LOW,LOW);}
void SkibidiBackward(bool toPrint){ if(toPrint) PrintToLCD("Back",true); moveMotors(LOW,HIGH,LOW,HIGH); HandleLEDs(LOW,HIGH,LOW,LOW);}
void SkibidiRight(bool toPrint)   { if(toPrint) PrintToLCD("Right",true); moveMotors(HIGH,LOW,LOW,LOW); HandleLEDs(LOW,LOW,HIGH,LOW);}
void SkibidiLeft(bool toPrint)    { if(toPrint) PrintToLCD("Left",true); moveMotors(LOW,LOW,HIGH,LOW); HandleLEDs(LOW,LOW,LOW,HIGH);}
void SkibidiStopMotors(bool toPrint){ if(toPrint) PrintToLCD("Stop",true); moveMotors(LOW,LOW,LOW,LOW); HandleLEDs(LOW,LOW,LOW,LOW);}
