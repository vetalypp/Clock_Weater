#!/bin/bash
pid=$(</home/sysop/pi_weather/pid)
nohup sudo kill $pid & sudo xinit /home/sysop/clock.sh & echo $! > /home/sysop/pi_weather/pid & exit
