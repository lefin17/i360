import serial
import time
import os


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

def ard_cmd(command, arduino):
	print (command)
	arduino.write(command)
	time.sleep(1)
	a = read_all(arduino)
	print (a)
	time.sleep(1)



arduino=serial.Serial(
# 	 port = '/dev/ttyACM0', 
	 port = '/dev/ttyUSB0', 
	 baudrate = 115200,
#    parity = serial.PARITY_NONE,
#    stopbits = serial.STOPBITS_ONE,
#    bytesize = serial.EIGHTBITS,
	 timeout = 0.5,
	 inter_byte_timeout = 0.1)
time.sleep(3)

# a = arduino.read(100)

a  = read_all(arduino)
print (a)

prefix = "_gm5_"
ard_cmd(b'G92 X0\r\n', arduino)
for i in range(32):
	print (i);
	strnum = str(i + 1)		
	if (i < 9):
		strnum = "0" + strnum
	os.system("gphoto2 --filename './photos/i360" + prefix + strnum + ".jpg' --capture-image-and-download")
	time.sleep(2)
	command = "G0 X" + str((i + 1) * 2) + "\r\n"
	print (command) 
	ard_cmd(command.encode(), arduino)
# arduino.write(b'G0 X2')
# time.sleep(1)
#a = read_all(arduino)
#  print (a)
arduino.close()



