#include <AccelStepper.h>

// Define motor 1 connections
#define STEP_PIN1 9
#define DIR_PIN1 8
#define ENABLE_PIN1 7

// Define motor 2 connections
#define STEP_PIN2 10
#define DIR_PIN2 12
#define ENABLE_PIN2 13

// Define ultrasonic sensor pins (Corrected)
#define TRIG_PIN 5 // Corrected to pin 5
#define ECHO_PIN 6 // Corrected to pin 6

// Initialize two stepper motors
AccelStepper stepper1(AccelStepper::DRIVER, STEP_PIN1, DIR_PIN1);
AccelStepper stepper2(AccelStepper::DRIVER, STEP_PIN2, DIR_PIN2);

void setup()
{
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
float getDistance()
{
    digitalWrite(TRIG_PIN, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIG_PIN, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIG_PIN, LOW);

    long duration = pulseIn(ECHO_PIN, HIGH);
    float distance = duration * 0.0343 / 2; // Convert to cm

    return distance;
}

void loop()
{
    // Get and print ultrasonic sensor distance
    float distance = getDistance();
    Serial.print("Distance: ");
    Serial.print(distance);
    Serial.println(" cm");

    delay(500); // Short delay before next measurement

    // Move both motors towards each other (hugging motion)
    stepper1.moveTo(200);
    stepper2.moveTo(-200);

    while (stepper1.distanceToGo() != 0 || stepper2.distanceToGo() != 0)
    {
        stepper1.run();
        stepper2.run();
    }

    delay(1000); // Pause

    // Move both motors back (opening motion)
    stepper1.moveTo(0);
    stepper2.moveTo(0);

    while (stepper1.distanceToGo() != 0 || stepper2.distanceToGo() != 0)
    {
        stepper1.run();
        stepper2.run();
    }

    delay(1000); // Pause
}