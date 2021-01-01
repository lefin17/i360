import serial
import time

def read_all(port, chunk_size=200):
    """Read all characters on the serial port and return them."""
    if not port.timeout:
        raise TypeError('Port needs to have a timeout set!')

    read_buffer = b''

    while True:
        # Read in chunks. Each chunk will wait as long as specified by
        # timeout. Increase chunk_size to fail quicker
        byte_chunk = port.read(size=chunk_size)
        read_buffer += byte_chunk
        if not len(byte_chunk) == chunk_size:
            break

    return read_buffer

arduino=serial.Serial(
	 port = '/dev/ttyACM0', 
	 baudrate = 9600,
#    parity = serial.PARITY_NONE,
#    stopbits = serial.STOPBITS_ONE,
#    bytesize = serial.EIGHTBITS,
	 timeout = 0.5,
	 inter_byte_timeout = 0.1)
time.sleep(2)

# a = arduino.read(100)

a  = read_all(arduino)
print (a)

arduino.write(b'D595')
time.sleep(4)
a = read_all(arduino)
print (a)
arduino.close()



