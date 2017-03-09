#Controlling multiple systems from Pronterface



## Pump-Control-Program
Program for controlling New Era syringe pumps with Pronterface for use with our silicone 3D printer. Used by mLab at Oregon State University. This program utilizes a raspberry pi as a middleman between pronterface, the syringe pump, and the smoothieboard.

### pf_filter_comm.py
Provides virtual serial port to connect Pronterface to. Virtual serial port...
  - Sorts syringe pump commands (S-code commands) and printer commands (G-code and M-code commands)
  - Commands syringe pumps with functions from new_era.py
  - Sends commands to printer
  - Sends printer communications back to pronterface
  - *for future consideration* modify gcode commands on the fly, such as print speed

### new_era.py
Provides initial functions to be used later in pump_control.py. These include:
  - "run" (for ALL pumps) and "stop" (for ALL and specific pumps) functions for running, stopping syringe pumps
  - "set rate" function for setting flow rate of individual syringe pumps
  - "prime" function for priming liquid through PE/2 tubing prior to use
  
### NOT USED - pump_control.py
Sets up the interface for the pump control system, which includes:
  - Pump numbers
  - Syringe pulldown menu
  - Text boxes for syringe contents
  - Flow rate boxes (in uL/hr)
  - Prime button
  - Status bar (running vs. stopped)

Functions defined:
  - "run update" - enables adjustment of flow rates while currently running
  - "syringe update" - enables adjustment of syringe parameters if flow rates are stopped
  - "prime pumps" - allows for initialization, termination of priming syringes
  - Defines shutdown parameters

Might be utilized later.

### NOT USED- set_pump_number.py

Links pump number to a particular syringe pump; prints that number on interface

Might be utilized later.

# Program Usage
Make sure to read all instructions before trying to run it yourself. Setup will continue to be made as simple as possible.

## Setting up the Code

Perform the steps in the given order and you should be all set. I will try to make the instructions simple.

### Getting the Smoothieboard Ready

Follow the directions to set up the board given on the [smoothieboard website](http://smoothieware.org/3d-printer-guide). Provided in the config folder is the configuration file we used as a reference.

### Getting the Raspberry Pi Ready

For the pi ethernet, we need to set a static IP address on this and on the computer its running on.

  - Go to /etc/network/interfaces

  - static IP address assignment. Helpful links: [1](help.ubuntu.com/lts/serverguide/network-configuration.html), [2](https://www.swiftstack.com/docs/install/configure_networking.html), [3](https://www.swiftstack.com/docs/install/configure_networking.html), [4](elinux.org/RPI_Stting_up_a_static_IP_in_Debian)
    - Link 1 sets it to 10.0.0.100, and we will do the same

  - Connect the syringe pump and smoothieboard
    - We need to make sure that the raspberry pi has the correct serial port to connect to the syringe pump and smoothieboard
      - I like to use the serial ID linux provides
      - In terminal or in a file manager, go to \dev\serial\by-id\
        - If you have the syringe pump and smoothieboard connected, there should be two options there.
          - They should look similar to what exists on lines 12 and 15 of the pf_filter_comm.py file
          - Make sure they match. Edit the file so it matches whats in there

raspberrypi.stackechange.com how do I set up raspberry pi 3 networking

### Getting the host computer ready

First, install [Pronterface](https://github.com/kliment/Printrun) and connect the raspberry pi by ethernet to your computer. 

For static IP setting, I current have good instructions for Linux. On the host computer, you can edit it the same way as described above, or you can do it in the connection manager.
  - Connection manager -> [edit connections] 
    - Add a new ethernet connection and set the static address that you want

To set up Pronterface:
  - enter the static IP of the Raspberry Pi (with correct port) into the [Port] option in the upper left 
    - If you followed the default IP mentioned above, that should be 10.0.0.100:5005
  - for convenience sake, I would suggest adding custom buttons to the Pronterface UI
    - you can do this at the bottom of the plater window in the center

### Added linux help
To connect to the pi from the file manager, use the following command in terminal:
  - sftp://pi@10.0.0.100/

You can also connect to the pi from ssh, so you don't need to connect a monitor to the device. 
  - ssh [username]@[IP OF THE PI GOES HERE]
    - default username is pi
    - then enter password, and you should be in!
      - you can navigate the raspberry pi from terminal as if you are on the pi itself

*Usage Note:* if multiple syringe pump are connected, currently several useless syringe pump commands must be sent to ensure all syringe pumps successfully connect. This is done in the beginning when all system connections are checked.

