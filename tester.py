import os, pty, serial

ser = serial.Serial('/dev/pts/18',19200)

while(1):
	var = raw_input("Enter a command: ")
	ser.write(str(var))