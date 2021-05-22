# Dashboard
MASA web dashboard continuing development

## Framework Used
<b> Built with </b>
* Python
* HTML, Javascript, CSS
* [Flask Microframework](https://flask.palletsprojects.com/en/1.1.x/) (pip install Flask)
* Flask-Cors (pip install Flask-Cors)
* [Leaflet Javascript Library](https://leafletjs.com/)
* matplotlib (pip install matplotlib)
* numpy
* sqlalchemy (pip install sqlalchemy)
* [openCV](https://pypi.org/project/opencv-python/) (pip install opencv-python)
* crcmod (pip install crcmod)
* pyserial (pip install pyserial)

## Running the Dashboard
1. Open up the file dataserver.py and pass it a config file (using --config="\<filename\>"), this will be the data server code in the final
2. Open up the file app.py and pass it a config file  (using --config="\<filename\>"), this will be the web backend code in the final
3. Open up the file testclient.py and pass it a config file (using --config="\<filename\>"), this is simulating the input of the non-video M2RB data
4. Open up the file videoclient.py and pass it a config file (using --config="\<filename\>"), this is simulating the input of the video M2RB data

Note when testing you will want to use the config file "test.json". Also note that it is possible to run the Dashboard without simulating M2RB data.

## Dashboard To Do
* Remove references to Eggfinder and replace with TeleGPS development (data types need an overhaul)
* Integrate GPS map development (frontend and backend currently separated into two branches)
* Video needs to be simulated being sent through a COM port
* Create all the infrastructure for the M2RB data (will most likely be unable to integrate the M2RB until that board continues development, so the Dashboard should be ready for integration, ie. set up with simulated packets) (data types need an overhaul)
* The Dashboard app should run without incoming data, so it will be possible to find the rocket through the map
* The Dashboard needs to be implemented on a web server
* The data client should have the option to a) be disconnected and reconnected to the Dashboard and b) save all data locally

## Dashboard Problems
* The documentation will need an almost complete overhaul, I still don’t understand many of the internals
* Might want to shuffle around the look of the UI, especially for the map
* Swap Button is a bit unresponsive, sometimes takes multiple clicks to register, something is probably going on with the backend
* The Dashboard is not sized to my computer, need to look into variable sizing for all devices
* Toggle for plot elements do not toggle the plot elements
* The Dashboard needs a single runable file to run the entire Dashboard so that testing, debugging and actually running the Dashboard is easier
* Video also needs to be linked into the configuration file as current it calls for it but does not use the config file
