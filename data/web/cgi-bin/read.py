#!/usr/bin/python3

# Turn on debug mode.
import cgitb
cgitb.enable()

from  subprocess import Popen

# Print necessary headers.
print("Content-Type: application/json")
print()

with open("../../settings.json", "r") as file:
    settings = file.read()
live_data = Popen('sudo python3 -m mh_z19 --all')
print(live_data)