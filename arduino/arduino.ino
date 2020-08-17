#define PINPWM 5
#define PINRED 13

long span_high, span_low, lasttime_low, lasttime_high, time_running;
long ppm;
int val_pwm_prev = LOW;
  
void setup() {
  Serial.begin(9600);
  pinMode(PINPWM, INPUT);
  pinMode(PINRED, OUTPUT);
}

void loop() {
  long time_running = millis();
  int val_pwm = digitalRead(PINPWM);
  
  if (val_pwm == HIGH) {
    digitalWrite(PINRED, HIGH);
    if (val_pwm != val_pwm_prev) {
      lasttime_high = time_running;
      span_low = lasttime_high - lasttime_low;
      
      val_pwm_prev = val_pwm;
    }
  }  else {
    digitalWrite(PINRED, LOW);
    if (val_pwm != val_pwm_prev) {
      lasttime_low = time_running;
      span_high = lasttime_low - lasttime_high;
      
      val_pwm_prev = val_pwm;
      /* 
        C_ppm = 2,000 x (T_H - 2[ms])/(T_H + T_L - 4[ms])
          T_H: PWM(span high)
          T_L: PWM(span low)
          2[ms]/4[ms]: criterion signal(?)
       */
      ppm = 2000 * (span_high - 2) / (span_high + span_low - 4);
      
      Serial.println("PPM = " + String(ppm));
      Serial.println(" span_high:" + String(span_high) + ", span_low: " + String(span_low));
    }
  }
  if(ppm >= 2000){
    Serial.println("ppm value Overflow");
    val_pwm = 0;
  }
}
