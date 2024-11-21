const int rows[] = {2, 3}; // Row pins
const int cols[] = {4, 5, 6}; // Column pins
bool buttons[2][3]; // Current button states
bool lastButtons[2][3]; // Previous button states
int lastVolume = 0; 

void setup() {
  for (int i = 0; i < 2; i++) pinMode(rows[i], OUTPUT); // Set rows as outputs
  for (int i = 0; i < 3; i++) pinMode(cols[i], INPUT_PULLUP); // Set columns as inputs with pullups
  Serial.begin(9600); // Start serial communication
  // Initialize last button states to match the current state
  for (int r = 0; r < 2; r++) {
    for (int c = 0; c < 3; c++) {
      lastButtons[r][c] = false;
    }
  }
}

void loop() {
  // Scan the button matrix
  volumeRead();
  for (int r = 0; r < 2; r++) {
    digitalWrite(rows[r], LOW); // Activate this row
    for (int c = 0; c < 3; c++) {
      buttons[r][c] = !digitalRead(cols[c]); // Read and invert logic (pressed = true)
      // Print only if the state has changed
      if (buttons[r][c] != lastButtons[r][c]) {
        if (buttons[r][c]) { // Button pressed
          printButtonState(r, c, 1);
        }
        lastButtons[r][c] = buttons[r][c]; // Update the last state
      }
    }
    digitalWrite(rows[r], HIGH); // Deactivate this row
  }
  delay(50); // Debounce
}

void printButtonState(int row, int col, bool state) {
  if (state) { // Only send when pressed
    int buttonNumber = row * 3 + col + 1;
    switch (buttonNumber) {
      case 1: Serial.println("bt1"); break;
      case 2: Serial.println("bt2"); break;
      case 3: Serial.println("bt3"); break;
      case 4: Serial.println("bt4"); break;
      case 5: Serial.println("bt5"); break;
      case 6: Serial.println("bt6"); break;
    }
  }
}

void volumeRead(){
    float value = round(analogRead(A0)*(0.09775171065));
    
  if(value!=lastVolume){
    int intValue = static_cast<int>(round(value));
      Serial.print("V");
      Serial.println(intValue);
    lastVolume=value;
    }
      delay(1);
}