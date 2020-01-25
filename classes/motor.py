class Motor:
import serial 
# class to initiate arduino connection
# put some settings to motor such as speed, direction, steps to start and stops, connection speed  
    speed = 8
    delay = 8
    serial_port = "TTY" #we need to define correct and choose which one is correct
    connection_speeds = ['1200','2400', '4800', '9600', '19200', '38400', '57600', '115200']
    connection_speed = 9600
    realport = None

    def __init__(self):
        print ("motor initiated")
    

    def set_serial_port(serial_port)
        self.serial_port = serial_port
 
    def connect(self):
        try:
            self.realport = serial.Serial(self.serial_port,int(self.connection_speed))
            self.ConnectButton.setStyleSheet("background-color: green")
            self.ConnectButton.setText('Подключено')
        except Exception as e:
            print(e)
    
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

