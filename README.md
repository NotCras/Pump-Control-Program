# Pump-Control-Program
Program for controlling New Era syringe pumps with Pronterface for use with our silicone 3D printer.

### new_era.py
Provides initial functions to be used later in pump_control.py. These include:
  - "run" (for ALL pumps) and "stop" (for ALL and specific pumps) functions for running, stopping syringe pumps
  - "set rate" function for setting flow rate of individual syringe pumps
  - "prime" function for priming liquid through PE/2 tubing prior to use
  
### middleMan.py
Provides virtual serial port to connect Pronterface to. Virtual serial port...
  - Sorts pump commands (P commands) and printer commands (gcode and Mcode commands)
  - Commands syringe pumps with functions from new_era.py
  - Sends commands to printer
  - *for future consideration* modify gcode commands on the fly, such as print speed
  
### pumpTester.py, printTester.py, tester.py
Simple serial port modules for debugging purposes.
  -pumpTester.py receives all pump commands in lieu of pumps
  -printTester.py receives all printer commands in lieu of printer
  -tester.py sends out commands in lieu of pronterface
      -provides terminal for users to send their own commands, for debugging purposes

### NOT USED - pump_control.py
Sets up the interface for the pump control system, which includes:
  - Pump numbers
  - Syringe pulldown menu
  - Text boxes for syringe contents
  - Flow rate boxes (in uL/hr)
  - Prime button
  - Status bar (running vs. stopped)

Defines "run update" function that enables adjustment of flow rates while currently running

Defines "syringe update" function that enables adjustment of syringe parameters if flow rates are stopped

Defines "prime pumps" function that allows for initialization, termination of priming syringes

Defines shutdown paramaters

### NOT USED- set_pump_number.py

Links pump number to a particular syringe pump; prints that number on interface

# Program Usage
Make sure to read all instructions before trying to run it yourself.

*On Linux*
1. Run printTester.py and pumpTester.py in their own terminal windows.
  - note the serial ports denoted.
  - if using actual printer and syringe pumps, ensure the correct lines are uncommented
2. Prepare middleMan.py
  - if using printTester.py and pumpTester.py, enter their serial ports into the indicated serial object in middleMan.py (look for the comments).
3. Run middleMan.py
  - note the serial port denoted. 
  - enter the serial port into pronterface or tester.py (if debugging).
4. *for debugging* - run tester.py in its own terminal window.
  - enter your own commands and hit enter, and the program will send that command out.
4. *for printing* - having entered in the serial port into pronterface, connect to the printer.
*Usage Note:* if multiple syringe pump connected, currently several useless syringe pump commands must be sent to ensure all syringe pumps successfully connect.
