

import os, pty, serial

import new_era

master, slave = pty.openpty()
s_name = os.ttyname(slave)

#write name of fake 3d printer for pronterface
#this is what is inserted into the pronterface connection
print "------------------------------"
print "Pronterface connection port: "
print s_name

#fake 3D printer com port that pronterface will attach to
f3dp = serial.Serial(s_name,19200)

#syringe pump serial port
pump = serial.Serial('/dev/serial/by-id/usb-Prolific_Technology_Inc._USB-Serial_Controller_D-if00-port0', 19200)
#pump = serial.Serial('/dev/pts/18',19200)

#actual 3D printer that all pronterface commands will be routed to
#3dp= serial.Serial('/dev/ttyACM3',19200)
r3dp = serial.Serial('/dev/pts/17',19200)

#dictionary list for syringe pump commands
pumpCommands = {'1':'RUN', #P1 is for running all syringe pumps at once
'2':'STP', #P2 is for stopping all syringe pumps at once
'3':'*DIRINF\x0D', #P3 is to set all syringe pumps forward
'4':'*DIRWDR\x0D', #P4 is to set all syringe pumps backwards
'5':'RAT'} #P5 is for rates, since there's more to it I'm just gonna make an arbitrary thing for the program to look out for later

#test writing to fake 3d printer COM port 
r3dp.write("Middleman Connected. This is real 3D printer.")
pump.write("Middleman Connected. This is the syringe pump.")

os.write(master,"This is a response test")

#find all the syringe pumps

while(1):
	#first, make sure that the fake 3D printer port is open
	if f3dp.isOpen():
		#next, make sure that the real 3D printer port is open
		#if 3dp.isOpen():

			#read the fake printer serial port for anything written to it
			val = os.read(master,1000)

			#write that value to the actual 3d printer
			#r3dp.write(val)
			#if val is "M105":
			#	os.write(master,"0/85.0")

#			#check if the first character of the command is a P (P for pump)
			if val[0][0] is "P":
				#check if we will selectively choose a pump to run
				if pumpCommands[val[1]] is 'RUN':
					if len(val) > 2: #val[2] is "-": #command will be P1_adr
						adr = int(val[3:])
						new_era.run_pump(pump, adr)

					else:
						new_era.run_all(pump)

				#check if we will selectively choose a pump to stop
				elif pumpCommands[val[1]] is 'STP':
					if len(val) > 2: #val[2] is "-": #command will be P2_adr
						adr = int(val[3:])
						new_era.stop_pump(pump, adr)

					else:
						new_era.stop_all(pump)

#				#then we will check the second letter to determine what the command actually is
				elif pumpCommands[val[1]] is 'RAT':
					#rate2set = dict()
					#run the rate stuff, this is on the rest of the signal -
					#if val[2] is "-": #command will be P5_ad_rate
						#brute forcing the logic to get adr (1 or 2 values)
					if val[4] is '_': #one address digit
						adr = int(val[3])
						rat = float(val[5:])
					else: #two address digits
						adr = int(val[3]+val[4])
						rat = float(val[6:])

					rate2set = {adr:rat}
					new_era.set_rates(pump,rate2set)

					#pump.write(new_era.set_rates(pump,val[0][2:]))

				#if its anything else, its probably a printer command
				else:
					pump.write(pumpCommands[val[1]])
				
#			if val:
#				pump.write(val)
#
#				print "----------------------"
#				print "Sent to Syringe Pump: "
#				print val
			else:
				r3dp.write(val)