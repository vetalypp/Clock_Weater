#! /usr/bin/env python

import xml.etree.ElementTree as ET
import gzip, urllib

import urllib.request

#fileDate = open("/tmp/dataweather.txt", 'w')
#fileDate_json = open("/tmp/weather_json.txt", 'w')
chisinau = 242405
luton = 329149


def celsius(temp):
    t= (5 * (int(temp)-32))/9
    return int(t)

def get_weather():
    # filehandlv = urllib.urlopen('http://lgemobilewidget.accu-weather.com/widget/lgemobilewidget/weather-data.asp?location=cityId%3A242405&langid=25')
    #https://www.accuweather.com/ru/gb/luton/lu1-3/weather-warnings/329149
    #Luton id: 329149
    #Chisinau id: 242405
    url = "http://lgemobilewidget.accu-weather.com/widget/lgemobilewidget/weather-data.asp?location=cityId%3A242405&langid=25"
    request = urllib.request.Request(url)
    request.add_header('User-Agent', 'Dalvik/1.6.0 (Linux; U; Android 4.1.2; LG-F160S Build/JZO54K)')
    request.add_header('Host',  'lgemobilewidget.accu-weather.com')

    request.add_header('Connection', 'Keep-Alive')
    filehandle = urllib.request.urlopen(request)
    file_content = filehandle.read()

    root = ET.fromstring(file_content)


    humidity = root[2][5].text
    curentTemp = celsius(root[2][3].text)
    curWeatherIcon = root[2][7].text
    curWeatherText = root[2][6].text.encode('utf-8')
    curHighTemp = celsius(root[3][1][5][3].text)
    curLowTemp = celsius(root[3][1][5][4].text)
    #----------------------------------------------
    day1 =root[3][2][2].text.encode('utf-8')[0:4]
    #----------------------------------------------
    weatherIcon1 = root[3][2][5][2].text
    HighTemp1 = celsius(root[3][2][5][3].text)
    LowTemp1 = celsius(root[3][2][5][4].text)

    #----------------------------------------------
    day2 =root[3][3][2].text.encode('utf-8')[0:4]
    #----------------------------------------------

    weatherIcon2 = root[3][3][5][2].text
    HighTemp2 = celsius(root[3][3][5][3].text)
    LowTemp2 = celsius(root[3][3][5][4].text)

    #----------------------------------------------
    day3 =root[3][4][2].text.encode('utf-8')[0:4]
    #----------------------------------------------


    weatherIcon3 = root[3][4][5][2].text
    HighTemp3 = celsius(root[3][4][5][3].text)
    LowTemp3 = celsius(root[3][4][5][4].text)


    data_weather= {"win": curWeatherIcon , "tn" : str(curentTemp), "hu" :  humidity, "tmax": str(curHighTemp), "tlow": \
     str(curLowTemp), "day1": day1, "day2": day2, "day3": day3 , "wi1": weatherIcon1, "tmax1" : str(HighTemp1), \
     "tlow1": str(LowTemp1) , "wi2": weatherIcon2, "tmax2": str(HighTemp2), "tlow2":str(LowTemp2), "wi3": \
     weatherIcon3, "tmax3" : str(HighTemp3), "tlow3": str(LowTemp3) , "wtext" : curWeatherText}
    return data_weather

    #fileDate.write(data)
    #fileDate_json.write(data_json)
    #fileDate_json.close()
    #fileDate.close()
