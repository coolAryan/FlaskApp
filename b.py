#!/usr/bin/python
import paho.mqtt.client as mqtt
from flask import Flask, render_template, request
app = Flask(__name__)

mqttc=mqtt.Client()
mqttc.connect("20.207.197.178",1883,60)
mqttc.loop_start()

# Create a dictionary called pins to store the pin number, name, and pin state:
pins = {
   0: {'name': 'LIGHT 1', 'board': 'esp8266', 'topic': 'esp8266/0', 'state': 'False'},
   1: {'name': 'LIGHT 2', 'board': 'esp8266', 'topic': 'esp8266/1', 'state': 'False'},
   3: {'name': 'LIGHT 3', 'board': 'esp8266', 'topic': 'esp8266/3', 'state': 'False'},
   2: {'name': 'LIGHT 2', 'board': 'esp8266', 'topic': 'esp8266/2', 'state': 'False'},
   4: {'name': 'LIGHT 4', 'board': 'esp8266', 'topic': 'esp8266/4', 'state': 'False'},
   5: {'name': 'LIGHT 5', 'board': 'esp8266', 'topic': 'esp8266/5', 'state': 'False'},
 #  9: {'name': 'COMMON LIGHT/FAN 1', 'board': 'esp8266', 'topic': 'esp8266/9', 'state': 'False'},
 # 10: {'name' : 'COMMON LIGHT/FAN 2', 'board' : 'esp8266', 'topic' : 'esp8266/10', 'state' : 'False'},
   12: {'name' : 'FAN 1', 'board' : 'esp8266', 'topic' : 'esp8266/12', 'state' : 'False'},
   13: {'name' : 'FAN 2', 'board' : 'esp8266', 'topic' : 'esp8266/13', 'state' : 'False'},
   14: {'name' : 'FAN 3', 'board' : 'esp8266', 'topic' : 'esp8266/14', 'state' : 'False'},
   15: {'name' : 'FAN 4', 'board' : 'esp8266', 'topic' : 'esp8266/15', 'state' : 'False'},
   16: {'name' : 'FAN 5', 'board' : 'esp8266', 'topic' : 'esp8266/16', 'state' : 'False'}
   }

# Put the pin dictionary into the template data dictionary:
templateData = {
   'pins' : pins
   }

@app.route("/")
def main():
   # Pass the template data into the template main.html and return it to the user
   return render_template('main.html', **templateData)

# The function below is executed when someone requests a URL with the pin number and action in it:
@app.route("/<board>/<changePin>/<action>")

def action(board, changePin, action):
   # Convert the pin from the URL into an integer:
   changePin = int(changePin)
   # Get the device name for the pin being changed:
   devicePin = pins[changePin]['name']
   # If the action part of the URL is "on," execute the code indented below:
   if action == "1" and board == 'esp8266':
      mqttc.publish(pins[changePin]['topic'],"1")
      pins[changePin]['state'] = 'True'

   if action == "0" and board == 'esp8266':
      mqttc.publish(pins[changePin]['topic'],"0")
      pins[changePin]['state'] = 'False'

   # Along with the pin dictionary, put the message into the template data dictionary:
   templateData = {
      'pins' : pins
   }

   return render_template('main.html', **templateData)

if __name__ == "__main__":
   app.run(host='0.0.0.0',port=80, debug=True)