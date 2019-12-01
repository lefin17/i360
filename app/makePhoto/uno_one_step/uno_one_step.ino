// Характеристика двигателя,
// количество шагов на один оборот вала
#define MOTOR_STEPS_REVOLUTION 200

//отношение передачи между поворотным стором и мотором
#define GEAR 8

// Шаг двигателя 
#define STEP_PIN 5
// Напрваление вращения
#define DIR_PIN 6
// Включение двигателя
#define EN_PIN 7

// переменная плавного пуска, останова - каждый раз скорость за каждый шаг в уменьшается при торможении, 
// при ускорении увеличивается 
#define STEP_MOTOR_TAIL MOTOR_STEPS_REVOLUTION / 4

// String cmd;

int steps = 50; //число шагов по умолчанию

int delay_time = 8; //задержка по умолчанию 

int timer = 0;

int HEART_BEAT_INTERVAL = 10000;

// 2019-12-01 Направление вращения, скорость и количество шагов определяется входной командой по ком-порту
// где A, B, C - определение скорости вращения где А-2 оборота в минуту, B - 4 и т.д
// +- - определение направления движения
// число определяет отношение обратное обороту - 1 - один оборот, 2 - полоборота, 4 - четверть и т.д.
// https://docs.google.com/document/d/1mT125aGub8R5eLZ-dc_0-YjKOWmOtoCWApiYtK3MFn0/edit?usp=sharing
// https://github.com/lefin17/i360

void setMotorDelayTime(String command)
  {
        delay_time = command.substring(2).toInt();
        if (delay_time < 2) delay_time = 2;
        if (delay_time > 500) delay_time = 500;
        Serial.println('Delay_time: ' + delay_time);
  }
  
void setMotorStepsByRun(String command)
  {
    steps = command.substring(2).toInt();
    if (steps < 1) steps = 1;
    if (steps > MOTOR_STEPS_REVOLUTION * GEAR) steps = MOTOR_STEPS_REVOLUTION * GEAR;
    Serial.print("Steps: " + steps);
  }  
  
void setMotorDirection(String command)
  {
    String ccw = "CCW"; 
    if (command.equals(ccw)) 
    {
      digitalWrite(DIR_PIN, HIGH);
    }
    else
    digitalWrite(DIR_PIN, LOW);
    Serial.print("Direction: " + command);
  }
  
  

void MotorStep()
  { 
  digitalWrite(EN_PIN, HIGH);
  for (int i = 0; i < steps; ++i)
    {
      //плавный пуск останов за число шагов step_motor_tail
      int delay_time_total = delay_time;
      if (i < STEP_MOTOR_TAIL) delay_time_total += (STEP_MOTOR_TAIL - i) * delay_time;
      if (i > steps - STEP_MOTOR_TAIL) delay_time_total += (i + STEP_MOTOR_TAIL - steps) * delay_time;
      
      digitalWrite(STEP_PIN, HIGH);
      delay(delay_time_total);
      digitalWrite(STEP_PIN, LOW);
      delay(delay_time_total);
    }      
  digitalWrite(EN_PIN, LOW);
  Serial.println('RUN COMPLITE: T' + delay_time + 'S'+ steps);
  }

void heartBeat()
  {
    // Если идет команда управления - жизненный цикл немного сдвигается
    delay(1);
    timer++;
    if (timer >= HEART_BEAT_INTERVAL) 
      {
        timer = 0;
        Serial.print(".");
      }
  }
  
void setup() {
  // put your setup code here, to run once:
  for (int i = STEP_PIN; i <= EN_PIN; ++i)
      pinMode(i, OUTPUT);
  //инициализация подключения
  Serial.begin(9600);
  
  Serial.println("\n\nTable with stepper motor. i360 Project \n");
  Serial.println("https://github.com/lefin17/i360 \n");
  Serial.println("Commands: RUN - run the stepper");
  Serial.println("T[time(ms)] - delay time in ms");
  Serial.println("CV - Direction by clock watch");
  Serial.println("CCW - Direction contr clock watch");
  Serial.println("S[steps] - step to next stop");
  Serial.println("Default steps: " + steps);
  Serial.println("Default delay_time: " + delay_time + " ms");
  Serial.println("Quarter of stepper rotation is a soft start and stop system");
  Serial.println("When Run over - you got message");
  Serial.println("dot heart beat system");
}

void loop() {
  heartBeat();
  while(Serial.available()) {
    String cmd = Serial.readString();// read the incoming data as string
    String letter = cmd.substring(1,2);
    if (cmd == "RUN") { MotorStep(); } 
    else if (letter == "T") { setMotorDelayTime(cmd); } 
    else if (cmd == "CW" || cmd == "CCW") { setMotorDirection(cmd);  } 
    else if (letter == "S") {  setMotorStepsByRun(cmd); } 
    else Serial.print("Error: command " + cmd + " not detected");
  } 
}

