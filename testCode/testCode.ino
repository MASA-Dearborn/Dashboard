
//this code is to simulate a serial device which will be 
//replaced by a TeleGPS in the final

String randString = ""; //creates the random string

void setup() {
  // put your setup code here, to run once:

  randomSeed(analogRead(0)); //creates a random seed based upon
  //one of the analog ports
  Serial.begin(9600); //starts the Serial line
  
}

void loop() {
  // put your main code here, to run repeatedly:

randString = String(random(10,99)); //creates a random list of
// 10 random numbers in a string

for (int i = 0; i < 10; i++) {
  randString = randString + String(random(10,99));
}

Serial.println(randString); //prints the string

}
