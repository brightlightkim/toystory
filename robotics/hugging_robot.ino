#include <AccelStepper.h>

// Define motor 1 connections
#define STEP_PIN1 9
#define DIR_PIN1 8
#define ENABLE_PIN1 7

// Define motor 2 connections
#define STEP_PIN2 10
#define DIR_PIN2 12
#define ENABLE_PIN2 13

// Define ultrasonic sensor pins
#define TRIG_PIN 5
#define ECHO_PIN 6

// Initialize two stepper motors
AccelStepper stepper1(AccelStepper::DRIVER, STEP_PIN1, DIR_PIN1);
AccelStepper stepper2(AccelStepper::DRIVER, STEP_PIN2, DIR_PIN2);

void setup() {
  // Initialize serial monitor
  Serial.begin(9600);

  // Set ultrasonic sensor pins
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  // Enable stepper motors
  pinMode(ENABLE_PIN1, OUTPUT);
  pinMode(ENABLE_PIN2, OUTPUT);
  digitalWrite(ENABLE_PIN1, LOW);
  digitalWrite(ENABLE_PIN2, LOW);

  // Set max speed and acceleration for both motors
  stepper1.setMaxSpeed(1000);
  stepper1.setAcceleration(500);
  stepper1.setCurrentPosition(0);

  stepper2.setMaxSpeed(1000);
  stepper2.setAcceleration(500);
  stepper2.setCurrentPosition(0);
}

// Function to get distance from ultrasonic sensor
float getDistance() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  long duration = pulseIn(ECHO_PIN, HIGH);
  float distance = duration * 0.0343 / 2;  // Convert to cm

  return distance;
}

// Function to perform hugging gesture
void hugGesture() {
  Serial.println("Object detected! Moving motors for hug.");
  
  // Move both motors towards each other (hugging motion)
  stepper1.moveTo(200);
  stepper2.moveTo(-200);

  while (stepper1.distanceToGo() != 0 || stepper2.distanceToGo() != 0) {
    stepper1.run();
    stepper2.run();
  }

  delay(5000); // Hold position for 5 seconds

  returnToHome();
}

// Function to return motors to original position
void returnToHome() {
  Serial.println("Returning to original position.");
  
  stepper1.moveTo(0);
  stepper2.moveTo(0);

  while (stepper1.distanceToGo() != 0 || stepper2.distanceToGo() != 0) {
    stepper1.run();
    stepper2.run();
  }
  
  Serial.println("Ready for next action.");
}

void loop() {
  // Check for serial commands
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    
    if (command.indexOf("START") >= 0) {
      Serial.println("Starting gesture sequence");
      
      // Motor 1 gesture
      stepper1.moveTo(150);
      while (stepper1.distanceToGo() != 0) {
        stepper1.run();
      }
      delay(5000);
      
      // Motor 2 gesture
      stepper2.moveTo(-150);
      while (stepper2.distanceToGo() != 0) {
        stepper2.run();
      }
      delay(5000);
      
      returnToHome();
    }
    else if (command == "STOP") {
      returnToHome();
    }
  }

  // Check ultrasonic sensor (priority over serial commands)
  float distance = getDistance();
  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println(" cm");

  // If an object is detected within 10 cm, perform hug gesture
  if (distance <= 10) {
    hugGesture();
  }

  delay(100); // Small delay before checking again
}