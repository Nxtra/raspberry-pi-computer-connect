# Raspberry Pi <-> Computer connection

Set up a connection between your RaspberryPi (server) and computer (client)

Steps to setup:
* update `RASPBERRY_PI_IP` in `computer-client.py` to the ip of your raspberry pi on your network
* copy `server-pi.py` from `raspberryPi` directory to your pi.
* start your server: run `python3 server.py` on your Raspberry Pi
* start your client: run `python3 client.py` on your computer
* start sending actions and receiving state!

![demo](static/demo.gif)

