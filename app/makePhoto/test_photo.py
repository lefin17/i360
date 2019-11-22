bashCommand = "gphoto2 --filename './i/test.jpg' --capture-image-and-download"

import subprocess 

process = subprocess.Popen(bashCommand.split(),stdout=subprocess.PIPE)
output, error = process.communicate()
print('Output:', output)
print('Error:', error)