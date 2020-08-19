
//this code is to simulate a serial device which will be 
//replaced by a TeleGPS in the final

String randString = ""; //creates the random string
String randTele = ""; //creates the fake semi-random teleGPS string

void setup() {
  // put your setup code here, to run once:

  randomSeed(analogRead(0)); //creates a random seed based upon
  //one of the analog ports
  Serial.begin(9600); //starts the Serial line
  
}

void teleGPS() {//creates a fake TeleGPS string
  
  randTele = "TELEM 220710";
  
  for (int i = 0; i < 2; i++) {
    randTele = randTele + String(random(17,255), HEX);
  }
  
  randTele = randTele + "042501000117";
  
  for (int i = 0; i < 2; i++) {
    randTele = randTele + String(random(17,255), HEX);
  }
  
  randTele = randTele + "0000c0074b45384e494a0000312e382e36000000";
  
  randTele = randTele + String(random(17,255), HEX);
  
  randTele = randTele + "85";
}
  
  void loop() {
    // put your main code here, to run repeatedly:
  
  /*randString = String(random(10,255), HEX); //creates a random list of
  // 10 random numbers in a string
  
  for (int i = 0; i < 10; i++) {
    randString = randString + String(random(10,255), HEX);
  }*/

  

  teleGPS();

  Serial.println(randTele); //prints the random TeleGPS string
  

}
