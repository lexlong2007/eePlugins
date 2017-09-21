#!/bin/bash
#makes LCD on Read eagle box darker than selected in GUI in standby
#after 5:30AM it switch to normal brightness

#it is initiated by e2 through /usr/script/StandbyEnter.sh 
beforeTime=530
afterTime=2100
MinBrightness=1
setBrightness=15
waitTime=60
[ -e /tmp/setRedEagleLCD.heartBeat ] && rm -f /tmp/setRedEagleLCD.heartBeat
sleep 2
echo 26 > /proc/stb/lcd/brightness #to assure the workflow works properly
while true
do
    HourMinute=$(date +"%H%M")
    LCDstate=$(cat /proc/stb/lcd/brightness)
    PLIstate=$(wget -q http://127.0.0.1/web/powerstate -O -|tr '\n' ' '|grep -o '<e2in.*standby>'|grep -c true)
    if [ $PLIstate -ne 1 ];then
        echo "PLI not in standby" >> /tmp/setRedEagleLCD.heartBeat
    fi
    if [ $HourMinute -le $beforeTime ] || [ $HourMinute -ge $afterTime ];then
        if [ $LCDstate -ne $MinBrightness ];then
            echo "$HourMinute - setting brightness to $MinBrightness" >> /tmp/setRedEagleLCD.heartBeat
            echo $MinBrightness > /proc/stb/lcd/brightness
        fi
    else
        if [ $LCDstate -ne $setBrightness ];then
            echo $[LCDstate + 1] > /proc/stb/lcd/brightness
            if [ $? -eq 0 ];then
                echo "$HourMinute - brightness set to ($LCDstate + 1)" >> /tmp/setRedEagleLCD.heartBeat
            else
                echo $setBrightness > /proc/stb/lcd/brightness
                echo "$HourMinute - brightness set to $setBrightness" >> /tmp/setRedEagleLCD.heartBeat
            fi
        fi
    fi
    touch /tmp/setRedEagleLCD.heartBeat
    sleep $waitTime=60
done
