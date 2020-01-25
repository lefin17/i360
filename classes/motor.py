import serial 

class Motor:

# class to initiate arduino connection
# put some settings to motor such as speed, direction, steps to start and stops, connection speed  
    speed = 8
    delay = 8
    serial_port = "TTY" #we need to define correct and choose which one is correct
    connection_speeds = ['1200','2400', '4800', '9600', '19200', '38400', '57600', '115200']
    connection_speed = 9600
    realport = None
    connected = False
    directions = { "CCW" : "CCW", "CW" : "CW" } 

    def __init__(self, delay, steps, direction):
        print ("motor object initiated")
        self.steps = steps
        self.delay = int(delay) # need the limits?
        self.direction = self.directions.get(direction, "CCW")


    def set_param(self)
        self.set_delay(self.delay)
        self.set_steps(self.steps)
        self.set_direction(self.direction)
        self.read_param()


    def read_param(self)
        #get some info from controller (values of variables)
        self.send("INFO");


    def set_serial_port(self, serial_port)
        self.serial_port = serial_port
 

    def connect(self):
        try:
            self.realport = serial.Serial(self.serial_port, int(self.connection_speed))
            time.sleep(2)
            connected = True
            print ("Arduino connected")
            while self.realport.inWaiting() > 0: 
                print self.realport.readline() #get info from arduino
        except Exception as e:
            print(e)


    def send(self, cmd):
        # https://qna.habr.com/q/537925 
        # line.decode().strip()
        #     отправка команды на контроллер, по хорошему должна завершаться подтверждением 
        #    выполнения или выходить с ошибкой при не получении по истечении срока лимита времени
        result = []
        if self.realport:
            self.realport.write(cmd)
            time.sleep(0.2) #delay from operation send to controller
            while self.realport.inWaiting > 0:
                line = self.realport.readline()
                result.append(line.decode.strip())                 
            return result
        return False


    def make_step(self)
        #basic functional of this module
        self.send("RUN") #make the step with current direction by needed steps and delay
        time.sleep((self.delay * self.steps / 1000) + 1) #wail till it will stop + 1 second
        while self.realport.inWaiting() > 0:
            print self.realport.readline()


    def set_delay(self, delay)
    # задержка между микрошагами шагового двигателя при установившемся движении
        self.delay = delay
        if res = self.send("T" + self.delay):
            print res


    def set_steps(self, steps)
        # число шагов шагового двигателя при одном шаге поворота платформы
        self.steps = steps
        if res = self.send("S" + self.steps): 
            print res 


    def set_direction(self, direction)
        # Определение направление вращения платформы
        self.direction = direction
        if res = self.send(direction): #direction { "CW" || "CCW" } 
            print res

    
    def serial_ports():
    # info about which port for arduino we can use
    """ https://stackoverflow.com/users/300783/thomas
        Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result

