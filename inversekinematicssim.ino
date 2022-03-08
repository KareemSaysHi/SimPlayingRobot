#include <Stepper.h>

float r1 = 81.15; //in mm
float r2 = 98.5;
float currentX = 0;
float currentY = 0;
int currentStep1 = 0;
int currentStep2 = 0;
int newStep1 = 0;
int newStep2 = 0;
int counter = 0;

bool stringComplete = false;

String inputString = "";

const int stepsPerRevolution = 200;  // change this to fit the number of steps per revolution
// for your motor


// initialize the stepper library on pins 8 through 11:
Stepper stepper1(stepsPerRevolution, 8, 9, 10, 11);
Stepper stepper2(stepsPerRevolution, 4, 5, 6, 7);


int stepCount = 0;  // number of steps the motor has taken

void setup() {
  stepper1.setSpeed(60);
  stepper2.setSpeed(60);

  currentStep1 = 0;
  currentStep2 = 0;
  newStep1 = 0;
  newStep2 = 0;

  Serial.begin(9600);
}

void loop() {

  if (Serial.available() > 0) serialEvent();



  if (stringComplete) {

    int yInd = inputString.indexOf("Y");   //put in x and y vals
    float xVal = (inputString.substring(1, yInd)).toFloat();

    int zInd = inputString.indexOf("Z");
    float yVal = (inputString.substring(yInd+1, zInd)).toFloat();

    float zVal = (inputString.substring(zInd+1, inputString.length()+1)).toFloat();

    float theta2 = findTheta2(xVal, yVal);   //find theta values
    float theta1 = findTheta1(xVal, yVal, theta2);

    //convert to some step amount, first multiplied by 2 for gear ratio stuff
    if newStep1 % 0 == 1 {
        newStep1 = floorf(float(convertToSteps(theta1)) * 2.5) + counter; //really stupid ass odd/even garbage

        if (counter == 0) {
          counter = 1;
        } else counter = 0;
    } else newStep1 = convertToSteps(theta1) * 2.5; 

     newStep2 = convertToSteps(theta2) + newStep1;

    Serial.println(newStep1);
    Serial.println(newStep2);

    setNewPos(currentStep1, currentStep2, newStep1, newStep2, 5);   //move

    currentStep1 = newStep1;
    currentStep2 = newStep2;
   
    inputString = "";
    stringComplete = false;

  }
 

 
 



 
 
}

void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    inputString += inChar;
    if (inChar == '\n') {
      stringComplete = true;
    }
  }
}

float findTheta2(float x, float y) {
  float theta2 = acos((pow(x, 2) + pow(y, 2) - pow(r1, 2) - pow(r2, 2))/(2*r1*r2));
  return theta2;
}

float findTheta1(float x, float y, float theta2) {
  float theta1 = atan(y/x) - atan((r2*sin(theta2))/(r1 + r2*cos(theta2)));
  return theta1;
}

int convertToSteps(float theta) {
  float thetaInSteps = theta * stepsPerRevolution / (2*PI);
 
  if (thetaInSteps - floorf(thetaInSteps) < 0.5){  //round
    return thetaInSteps = floorf(thetaInSteps);
  } else {
    return thetaInSteps = floorf(thetaInSteps) + 1;
  }
}

void setNewPos(int oldStep1, int oldStep2, int newStep1, int newStep2, int numSteps) {
 
  int quotient1 = (abs(newStep1 - oldStep1)) / numSteps;
  int remainder1 = (abs(newStep2 - oldStep2)) % numSteps;
  if ((newStep1 - oldStep1) < 0) {
    quotient1 = -1*quotient1;
    remainder1 = -1*remainder1;
  }

  int quotient2 = (abs(newStep2 - oldStep2)) / numSteps;
  int remainder2 = (abs(newStep2 - oldStep2)) % numSteps;
  if ((newStep2 - oldStep2) < 0) {
    quotient2 = -1*quotient2;
    remainder2 = -1*remainder2;
  }
 
  for (int i = 0; i < numSteps; i++) {
    stepper1.step(quotient1);
    stepper2.step(quotient2);
  }

  stepper1.step(remainder1);
  stepper2.step(remainder2);
}



/*for (int i = 0; i < 40; i++) {
    stepper1.step(2);
    stepper2.step(1);
  }
  delay(500);
  for (int i = 0; i < 40; i++) {
    stepper1.step(-2);
    stepper2.step(-1);
  }
  delay(500);*/
