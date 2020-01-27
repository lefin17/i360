// передаточное отношение шестерни
const int GEAR = 8;

// число оборотов шагового двигателя на один поворот платформы
const int MOTOR_STEPS_REVOLUTION = 1600;

//число шагов шагового двигателя для пуска, останова
const int STEP_MOTOR_TAIL = 100; 
// Шаг двигателя 

const byte STEP_PIN = 4;
// Напрваление вращения

const byte DIRECTION_PIN = 6;
// Включение двигателя

const byte ENABLE_PIN = 3;

// переменная плавного пуска, останова - каждый раз скорость за каждый шаг в уменьшается при торможении, 
// при ускорении увеличивается 
// #define STEP_MOTOR_TAIL MOTOR_STEPS_REVOLUTION / 4

// String cmd;

int direction = 0; //direction pin turned off by default

int steps = 50; //число микрошагов по умолчанию за один оборот

int delay_time = 8; //задержка по умолчанию 

int timer = 0;

int HEART_BEAT_INTERVAL = 10000;

// 2019-12-01 Направление вращения, скорость и количество шагов определяется входной командой по ком-порту
// где A, B, C - определение скорости вращения где А-2 оборота в минуту, B - 4 и т.д
// +- - определение направления движения
// число определяет отношение обратное обороту - 1 - один оборот, 2 - полоборота, 4 - четверть и т.д.
// https://docs.google.com/document/d/1mT125aGub8R5eLZ-dc_0-YjKOWmOtoCWApiYtK3MFn0/edit?usp=sharing
// https://github.com/lefin17/i360
// http://wiki.amperka.ru/%D0%BF%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82%D1%8B:troyka:stepper

void setMotorDelayTime(String command)
  {
        delay_time = command.substring(2).toInt();
        if (delay_time < 2) delay_time = 2;
        if (delay_time > 500) delay_time = 500;
        String DelayInfo = 'Delay_time: ' + String(delay_time);
        Serial.println(DelayInfo);
  }
  
void setMotorStepsByRun(String command)
  {
    steps = command.substring(2).toInt();
    if (steps < 1) steps = 1;
    if (steps > MOTOR_STEPS_REVOLUTION * GEAR) steps = MOTOR_STEPS_REVOLUTION * GEAR;
    String StepInfo = "Steps: " + String(steps);
    Serial.println(StepInfo);
  }  
  
void setMotorDirection(String command)
  {
    String ccw = "CCW"; 
    if (command.equals(ccw)) 
    {
      digitalWrite(DIRECTION_PIN, HIGH);
    }
    else
    digitalWrite(DIRECTION_PIN, LOW);
    String DirectionInfo = "Direction: " + command;
    Serial.println(DirectionInfo);
  }
  
  

void MotorRun()
  { 
  digitalWrite(ENABLE_PIN, HIGH);
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
//  digitalWrite(ENABLE_PIN, LOW);
  analogWrite(ENABLE_PIN, 100); //Блокировка шагового двигателя
  String RunInfo = 'RUN COMPLITE: T' + String(delay_time) + 'S'+ String(steps);
  Serial.println(RunInfo);
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
 
 //когда нужно включить шаговый двигатель (и возможно удерживать)
      pinMode(ENABLE_PIN, OUTPUT);
      
 //PIN ответственный за каждый шаг      
      pinMode(STEP_PIN, OUTPUT); 
 
 //пин определяющий направление вращения
      pinMode(DIRECTION_PIN, OUTPUT);
  //подключение к рабочему месту    
  Serial.begin(9600);
  delay(10);
  digitalWrite(ENABLE_PIN, LOW);

  digitalWrite(STEP_PIN, LOW);
//  
  info();
}

void info() { 
  Serial.println("\n\nTable with stepper motor. i360 Project");
  Serial.println("https://github.com/lefin17/i360.git");
  Serial.println("Commands: RUN - run the stepper");
  Serial.println("T[time(ms)] - delay time in ms");
  Serial.println("CV - Direction by clock watch");
  Serial.println("CCW - Direction contr clock watch");
  Serial.println("S[steps] - number of microsteps of stepper motor to next stop");
  
  String default_steps = "Default steps: " + String(steps);
  Serial.println(default_steps);
  
  String default_delay = "Default delay_time: " + String(delay_time) + " ms";
  Serial.println(default_delay);
  
  Serial.println("Quarter of stepper rotation is a soft start and stop system");
  Serial.println("When Run over - you got message");
  Serial.println("dot heart beat system");
  delay(10);
}

void current_info()
    {
  String CurrentSteps = "Current steps in one run: " + String(steps);
  Serial.println(CurrentSteps);
  
  String CurrentDelayTime = "Current delay_time: " + String(delay_time) + " ms";
  Serial.println(CurrentDelayTime);
  
  String CurrentDirection = "Current direction: " + direction;
  Serial.println(CurrentDirection);
  
  delay(100);
}

void loop() {
  heartBeat();
  while(Serial.available()) {
    String cmd = Serial.readString();// read the incoming data as string
    String letter = cmd.substring(1,2);
    if (cmd == "RUN") { MotorRun(); } 
    else if (letter == "T") { setMotorDelayTime(cmd); } 
    else if (cmd == "CW" || cmd == "CCW") { setMotorDirection(cmd);  } 
    else if (letter == "S") {  setMotorStepsByRun(cmd); }
    else if (cmd == "INFO") { current_info(); }  
    else Serial.print("Error: command " + cmd + " not detected");
  } 
}

