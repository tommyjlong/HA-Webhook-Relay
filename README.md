Vivint/Vivotek HTTP Relay For Home Assistant Web Hook Application
------------------
*For Use With Home Assistant In a Python Environment*

Home Assistant has a feature called a webhook that once received, can be used as an event to trigger an automation.  Webhooks in Home Assistant are simply an HTTPS/HTTP POST of a particular url that contains `/api/webhook/XXXX` where XXXX is a webhook string.

Vivint/Vivotek IP Cameras can be configured to send a HTTP GET with a webhook url to a given IP address.<br/>
For the Vivint Doorbell camera, this could be sent say when someone pushed the doorbell.<br/>
For Vivotek cameras, this could be sente as an action for a motion detection event.<br/>

A couple of problems exist with Vivint/Vivotek cameras sending webhooks.  One is that the cameras may only be able to send an HTTP GET (instead of a POST).  Another is that Home Assistant can be configured to only support HTTPS (instead of HTTP).  This code's intent is to solve these two problems.

This code will take the URL received from a camera's http GET, which contains /api/webhook/XXXX (where XXXX is the webhook) and relay it to Home Assistant using either an http or https POST. The code does check for the presence of `/api/webhook` in the url, but otherwise relays the remaining portion of the URL, containing the webhook XXXX, transparently to Home Assistant.

Configuration
----------
The file `ha_http_relay.py` holds the configuration and has to be modified in a couple of places.
* `HA_URL1 = ` This is the URL (including port number) to reach your home assistant say from a web browser. 
* `PORT_NUMBER = XXXX`  This is the port number this code will listen on to receive http GET from the camera.

There are also a couple of places you can configure the logger which you can change when debugging.  There are instructions for this, also in the file.


How to Use with Home Assistant
-------
You simply configure it, test it out, and then set this to run automatically using the method of your choice.

License
-------
    - MIT License

