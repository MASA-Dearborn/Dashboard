# Dashboard
MASA web dashboard continuing development

## Framework Used
<b> Built with </b>
* Python
* HTML, Javascript, CSS
* [Flask Microframework](https://flask.palletsprojects.com/en/1.1.x/)
* Flask-Cors
* [Leaflet Javascript Library](https://leafletjs.com/)
* matplotlib
* numpy
* sqlalchemy
* [openCV](https://pypi.org/project/opencv-python/)
* crcmod

## Running the Dashboard
1. Open up the file dataserver.py and pass it a config file (using --config="\<filename\>"), this will be the data server code in the final
2. Open up the file app.py and pass it a config file  (using --config="\<filename\>"), this will be the web backend code in the final
3. Open up the file testclient.py and pass it a config file (using --config="\<filename\>"), this is simulating the input of the non-video M2RB data
4. Open up the file videoclient.py and pass it a config file (using --config="\<filename\>"), this is simulating the input of the video M2RB data

Note when testing you will want to use the config file "test.json". Also note that it is possible to run the Dashboard without simulating M2RB data.
