bashCommand = "echo 0"
import subprocess 
process = subprocess.Popen(bashCommand.split(),stdout=subprocess.PIPE)
output, error = process.communicate()
print('Output:', output)
print('Error:', error)