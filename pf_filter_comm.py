

import serial
import socket
import new_era

#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------

#syringe pump serial port
pump = serial.Serial('/dev/serial/by-id/usb-Prolific_Technology_Inc._USB-Serial_Controller_D-if00-port0', 19200)

#actual 3D printer that all pronterface commands will be routed to
r3dp = serial.Serial('/dev/serial/by-id/usb-Uberclock_Smoothieboard_0901100BAEAB2005551F8D76F50020C4-if00',19200)

#dictionary list for syringe pump commands
pumpCommands = {'S1':'RUN', #S1 is for running all syringe pumps at once
'S2':'STP', #S2 is for stopping all syringe pumps at once
'S3':'*DIRINF\x0D', #S3 is to set all syringe pumps forward
'S4':'*DIRWDR\x0D', #S4 is to set all syringe pumps backwards
'S5':'RAT'} #S5 is for rates, since there's more to it I'm just gonna make an arbitrary thing for the program to look out for later

#important socket setup
TCP_IP = '10.0.0.100'
TCP_PORT = 5005
BUFFER_SIZE = 50  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------

pronter, addr = s.accept()
print 'Connected!'

while(1):
        #need to store the commands into a queue so we don't lose commands
        
    #next, make sure connection to real 3d printer is good
    if r3dp.isOpen():

        #next, check that the syringe connection is good
        if pump.isOpen():

            new_era.run_all(pump)
            new_era.stop_all(pump) #this is to wake up the pump
            
            #set the all go variable!
            allSystemsGo = 1

        else:
            print "The syringe pump connection is no good."

    else:
        print "The 3D printer connection is no good."

#--------------------------------------------------------------------------------------------------
    #Can we do stuff??
    if allSystemsGo:

        #read in the command from pronterface
        val = pronter.recv(BUFFER_SIZE)

        

        #then time to filter!
        #what to do with our pump commands
        if val[0] is 'S':
	    #check if we will selectively choose a pump to run
            if pumpCommands[val[0]+val[1]] is 'RUN':

                #further figure out what kind of 
                if len(val) > 2: #val[2] is "-": #command will be P1_adr
                    adr = int(val[3:])
                    new_era.run_pump(pump, adr)
    
        	else:
                    new_era.run_all(pump)

	    #check if we will selectively choose a pump to stop
	    elif pumpCommands[val[0]+val[1]] is 'STP':
		if len(val) > 2: #val[2] is "-": #command will be P2_adr
		    adr = int(val[3:])
		    new_era.stop_pump(pump, adr)

		else:
		    new_era.stop_all(pump)

#	    #then we will check the second letter to determine what the command actually is
	    elif pumpCommands[val[0]+val[1]] is 'RAT':
		#brute forcing the logic to get adr (1 or 2 values)
                
		if val[4] is '_': #one address digit
		    adr = int(val[3])
		    rat = float(val[5:])
		    
		else: #two address digits
		    adr = int(val[3]+val[4])
		    rat = float(val[6:])

		    rate2set = {adr:rat}
		    new_era.set_rates(pump,rate2set)
    
	    else:
                pump.write(pumpCommands[val[1]])

        #if its not fancy like a pump command, then we need to send it to the printer
        else:
            r3dp.write(val)

    #if that's not working, don't do anything
    else:
        pass

    #check if theres anything else to communicate
    #back to pronterface from the printer
    check = r3dp.inWaiting()
    if check:
        printer = r3dp.read(check)
        pronter.send(printer)    

