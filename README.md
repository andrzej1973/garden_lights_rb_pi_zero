**<p style="text-align: center;">GardenPi - The Garden Light Controller</p>**

<p align="center">
<img src="./hw/gardenpi_front.jpg" width="350" height="250"/>
</p>

GardenPi is a Raspberry Pi Zero based two channel garden light controller, which includes hardware platform and systemd service written in python. Lights are automatically switched on/off based on calculated sunset time for provided location. Manual lights control is also supported. General information about status of the platform can be obtained from GUI and through cli command gardenpi, which also provides self diagnostics and remote logging configuration capabilities.

Platform is powered by:
<p align="left">
<img src="./docs/decorations/raspberry-logo.png" width="50" height="40"/>
<img src="./docs/decorations/python-logo.png" width="50" height="40"/>
<img src="./docs/decorations/grafana-logo.png" width="50" height="40"/>
<img src="./docs/decorations/prometheus-logo.png" width="50" height="40"/>
<img src="./docs/decorations/kafka-logo.png" width="50" height="40"/>
<img src="./docs/decorations/rsyslog-logo.png" width="100" height="40"/>
</p>


**Key Features:**

- two software controlled relay 12V lighting channels with additional mechanical on/off switch (blue)
- main channel designated to control door lighting of the tool house
- secondary channel designated to control lighting of garden feature such as tree or sculpture
- both channels are switched on based on automatically calculated sunset time + predefined delay period
- main channel can be turned on with external on/off door switch as well
- configurable offset period controls delay between activation of main and secondary channel
- period when lights remain turned on can be configured separately for winter and summer time
- controller can be restarted by pressing Reset button
- controller can be shut down by toggling 5x the door switch within 1min interval
- door switch toggles are indicated by a beep.
- number of beeps correspond to the number of toggles, which occurred within 1min shutdown window
- after 1 min interval starting from the first switch on/off, toggle counter is reset to zero
- controller can be turned on and off by the green power switch
- when controller's boot sequence is finished after power on or restart, three short beeps are played 
- marked usb port can be used to ssh to the controller using cli command: ssh pi@gardenpi.local, pwd: raspberry
- wifi module is also configured and can be used whenever 2.4GHz wifi network is available
- real time is preserved at device shutdown using RTC module
- RTC module time is synchronized with network clock as soon as device is connected to LAN via Wi-Fi or USB
- Device is powered by 12V DC external power supplier (reversed polarity protection is implemented)
- Controller status is indicated by LED over RST/HLT button (steady/blinking - controller in operation)
- Grafana based simple GUI (dashboard) is available at http://gardenpi.local
- Simple unit diagnostics can be obtained by running command sudo gardenpi --test
- Buzzer volume can be controlled with potentiometer Buzz. Vol.
- Controller's syslog messages are forwarded to rsyslog server and kafka broker
- Remote logging enabled/configured/disabled using sudo gardenpi --logging option with parameters
- Power plug with additional digital line indicating source of power (solar vs. dc power supply) added
- Additional hardware unit switching automatically power source to dc power supply when battery voltage is too low released as a separate project (Solar / DC Backup Power Switch with Power Source Indicator). Unit is fully compatible with gardenpi controller version 5.0 and later.


**Design and Build Instructions**

HW design has been described in the following files:

* [Bill of Materials](./docs/gardenpi_bom.txt)
* [Circuit diagram](./docs/gardenpi_schematics.pdf)
* [HW Photos](./hw/)

Pi SW Image preparation process has been documented in the following command log file:

* SW Image Preparations command [log](./doc/gardenpi_cmd.txt).
* Latest stable SW image can be downloaded from [image repository](https://1drv.ms/u/s!AmoGY_QbIutmjDPu6R8zekghUcrf?e=fY6dYW)

Service python script, service file and initial configuration file storing service script settings are all located in:

* [Source Code Directory](./src)

All Pi configuration files, which were modified as part of this project are stored in:

* [Config Directory](./config)


**Initial Configuration**

* Connect GardenPi device to you linux host machine using usb cabel
* From host machine terminal ssh to GardenPi using following command:
	- ssh pi@gardenpi.local #password is set to: raspberry
* Modify solarcalc.ini  file with unit location information, all other parameters can be left at default.
	- nano ~/PyScripts/SolarCalc/solarcalc.ini
* Halt the device by toggling x5 door switch within 1min interval
* Unplug usb cable, place the device in target location and wire it to lighting and power source.
* If you need access to the list of config files and useful commands type gardenpi command.
* Enjoy the GardenPi device! :-)

**Device Operation**

Device does not require special maintenance, if GardenPi operates from location where there is no wifi access its RTC can drift so it is desirable to bring it within wifi coverage from time to time. Such behavior can be expected, but was not observed in real life yet.

**GUI**
Design of the GardenPi GUI has been detailed in gardenpi_gui.md document located in * [Docs Directory](./docs)
Grafana's dashboard has been specified in GardenPiController.json file located in * [Gui Directory](./gui)

GardenPi Dashboard:

<p align="center">
<img src="./gui/GardenPiController.png" width="600" height="150"/>
</p>

**gardenpi command**
When connected to the terminal window over **ssh (user: pi@gardenpi.local, pwd: raspberry)**, it is possible to execute gardenpi command, which offers basic information about controller configuration.
To execute device selftest execute: **sudo gardenpi --test**

**Contributing**

* Fork it!
* Create your feature branch: git checkout -b my-new-feature
* Commit your changes: git commit -am 'Add some feature'
* Push to the branch: git push origin my-new-feature
* Submit a pull request

**Release History**

* Release 1.0 - October 2021 - basic functionality allowing light control
* Release 2.0 - October 2022 - new functionality:
	* device configuration via .ini file, 
	* buzzer support added, 
	* bug fixes focusing on stability (handling of shutdown procedure)
	* gardenpi command and device baner with useful configuration info added
* Release 3.0 - October 2022 - new functionality:
    * Grafana/Prometheus based GUI added
* Release 4.0 - October 2022 - new functionality:
	* 	buzzer volume control added
	* 	gardenpi command enhanced with device self-test routine
* Release 4.1 - November 2022 - new functionality and bug fixes:
	- possibility to set different lights-on durations for winter and summer times added
	- syslog messages are forwarded to rsyslog server and kafka broker
	- gardenpi command enhanced with remote logging configuration options
	* 	bug fix: depreciated zone function replaced in tzlocal with get_localtz_name() function call
	* 	bug fix: time presission correted in some info traces
* 	Release 5.0 December 2022 - new functionality:
	- 	Power connector changed to unique type, preventing accidental power cable incorrect insertion
	- 	Support for power source indicator (solar vs. power supply added)
	
**Planned Functionality**

* External WiFi antenna support
* Gardenpi service logging to syslog
* man page for gardenpi command


Comments or Questions can be directed to: andrzej@mazur.info


