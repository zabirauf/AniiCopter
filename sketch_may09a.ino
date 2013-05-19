int R_UD = 0;
int R_LR = 0;
int L_UD = 0;
int L_LR = 0;

int R_StartUD = -1;
int R_StartLR = -1;
int L_StartUD = -1;
int L_StartLR = -1;

// this constant won't change:
const int  buttonPin = 2;    // the pin that the pushbutton is attached to
// Variables will change:
int buttonState = 0;         // current state of the button
int lastButtonState = 0;     // previous state of the button

int DEFAULT_MIN_THRESHOLD = 5;
boolean L_FLAG = false;
boolean R_FLAG = false;

void setup() {
  // initialize the button pin as a input:
  pinMode(buttonPin, INPUT);
  Serial.begin(9600);
}

void loop() {
  R_UD = analogRead(A0);
  R_LR = analogRead(A1);
  L_UD = analogRead(A3);
  L_LR = analogRead(A4);
  
  // read the pushbutton input pin:
  buttonState = digitalRead(buttonPin);
  
  if(R_StartUD == -1 || R_StartLR == -1)
  {
    R_StartUD = R_UD;
    R_StartLR = R_LR;
    Serial.print("RUD");
    Serial.println(R_UD,DEC);
    Serial.print("RLR");
    Serial.println(R_LR,DEC);  
    delay(200);
  }
  
  if(L_StartUD == -1 || L_StartLR == -1)
  {
    L_StartUD = L_UD;
    L_StartLR = L_LR;
    Serial.print("LUD");
    Serial.println(L_UD,DEC);
    Serial.print("LLR");
    Serial.println(L_LR, DEC);
    delay(200);
    //Serial.println("Go Ahead");  
  }
  
  if(R_UD > R_StartUD+DEFAULT_MIN_THRESHOLD || R_UD < R_StartUD-DEFAULT_MIN_THRESHOLD || R_LR > R_StartLR+DEFAULT_MIN_THRESHOLD || R_LR < R_StartLR-DEFAULT_MIN_THRESHOLD)
  {
    Serial.print("RUD");
    Serial.println(R_UD,DEC);
    Serial.print("RLR");
    Serial.println(R_LR,DEC); 
    R_FLAG = true;
  }  
  else /*if(R_FLAG)*/
  {
    Serial.print("RUD");
    Serial.println(R_StartUD,DEC);
    Serial.print("RLR");
    Serial.println(R_StartLR,DEC);
    R_FLAG = false;
  }
  
  if(L_UD > L_StartUD+DEFAULT_MIN_THRESHOLD || L_UD < L_StartUD-DEFAULT_MIN_THRESHOLD || L_LR > L_StartLR+DEFAULT_MIN_THRESHOLD || L_LR < L_StartLR-DEFAULT_MIN_THRESHOLD)
  {
    Serial.print("LUD");
    Serial.println(L_UD,DEC);
    Serial.print("LLR");
    Serial.println(L_LR, DEC); 
    L_FLAG = true;
  }
  else/* if(L_FLAG)*/
  {
    Serial.print("LUD");
    Serial.println(L_StartUD,DEC);
    Serial.print("LLR");
    Serial.println(L_StartLR, DEC); 
    L_FLAG = false;
  }
  
  // compare the buttonState to its previous state
  if (buttonState != lastButtonState) {
    // if the state has changed, increment the counter
    if (buttonState == HIGH) {
      // if the current state is HIGH then the button
      // wend from off to on:
      Serial.print("BTN");
      Serial.println(1,DEC);
    } 
    else {
      // if the current state is LOW then the button
      // wend from on to off:
      Serial.print("BTN");
      Serial.println(0,DEC); 
    }
  }
  // save the current state as the last state, 
  //for next time through the loop
  lastButtonState = buttonState;
  //delay(200);
}
