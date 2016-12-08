import os, pty, serial

import new_era

master, slave = pty.openpty()
s_name = os.ttyname(slave)

#write name of fake 3d printer for pronterface
#this is what is inserted into the pronterface connection
print "------------------------------"
print "Fake Real printer connection port: "
print s_name

#fake 3D printer com port that pronterface will attach to
ser = serial.Serial(s_name,19200)

#a test node to ensure that middleman can correctly send messages between syringe pump and printer.
while(1):
	val = os.read(master,1000)
	print val