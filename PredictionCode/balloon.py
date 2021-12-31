#!/opt/local/bin/python

import re
import datetime
import os
import numpy as np
import matplotlib.pyplot as plt
import sys
import random
import time

ParachuteFudge = 0.333
BalloonDragCoefficient = 0.5
ParachuteDragCoefficient = 1.5

dt = 10.0

KnotsToMps = 0.514444
LbsToKgs = 0.453592
pi = 3.1415927
FtToMeters = 0.3048
dtor = pi/180.0
MilesPerMeter = 0.000621371

#UniversalGasConstant = 8.31432
#AirGasConstant = 286.9     # Joules / mol / K
#HeliumGasConstant = 2077.0 # Joules / mol / K

Boltzmann = 1.38070e-23

MassOfAir = 4.88e-26 # kg
MassOfHelium = 6.69e-27 # kg

SurfaceGravity = 9.80665 # m/s2
EarthRadius = 6372000.0 # m

#-----------------------------------------------------------------------------
# Figure out arguments
#-----------------------------------------------------------------------------

def get_args(argv):

    payload   = -1.0
    balloon   = -1.0
    parachute = -1.0
    helium    = -1.0
    lat       = -91.0
    lon       = -361.0
    alt       = -1.0

    nEnsembles = -1
    errors     = 0.2
    
    CurrentTime = 0.0

    CurrentYear  = int(time.strftime("%Y"))
    CurrentMonth = int(time.strftime("%m"))
    CurrentDay   = int(time.strftime("%d"))
    CurrentHour  = int(time.strftime("%H"))

    Day = -1
    Hour = -1

    date = datetime.datetime.now()
    sTimeNow = date.strftime('%Y%m%d_%H%M%S')

    htmlfile = 'balloon_'+sTimeNow+'.html'
    kmlfile  = 'balloon_'+sTimeNow+'.kml'
    csvfile  = 'balloon_'+sTimeNow+'.csv'

    callsign = 'abcdef'
    BurstTime = 7.0*24.0*60.0*60.0
    hover = 50000.0

    IsZeroPressure = 0
    BalloonR = 0.0
    BalloonV = 0.0

    UseAprs = 0
    IsDescent = 0

    loss = 0.0

    update = 0

    for arg in argv:

        m = re.match(r'-callsign=(.*)',arg)
        if m:
            callsign = m.group(1)

        m = re.match(r'-html=(.*)',arg)
        if m:
            htmlfile = m.group(1)

        m = re.match(r'-kml=(.*)',arg)
        if m:
            kmlfile = m.group(1)

        m = re.match(r'-csv=(.*)',arg)
        if m:
            csvfile = m.group(1)

        m = re.match(r'-payload=(.*)',arg)
        if m:
            payload = float(m.group(1))*LbsToKgs

        m = re.match(r'-balloon=(.*)',arg)
        if m:
            balloon = float(m.group(1))

        m = re.match(r'-r=(.*)',arg)
        if m:
            BalloonR = float(m.group(1))

        m = re.match(r'-v=(.*)',arg)
        if m:
            BalloonV = float(m.group(1))

        m = re.match(r'-zero',arg)
        if m:
            IsZeroPressure = 1

        m = re.match(r'-aprs',arg)
        if m:
            UseAprs = 1

        m = re.match(r'-update',arg)
        if m:
            update = 1

        m = re.match(r'-parachute=(.*)',arg)
        if m:
            parachute = float(m.group(1))*FtToMeters/2

        m = re.match(r'-helium=(.*)',arg)
        if m:
            helium = float(m.group(1))

        m = re.match(r'-loss=(.*)',arg)
        if m:
            loss = float(m.group(1))

        m = re.match(r'-de',arg)
        if m:
            IsDescent = 1

        m = re.match(r'-alt=(.*)',arg)
        if m:
            alt = float(m.group(1))

        m = re.match(r'-lat=(.*)',arg)
        if m:
            lat = float(m.group(1))

        m = re.match(r'-lon=(.*)',arg)
        if m:
            lon = float(m.group(1))

        m = re.match(r'-day=(.*)',arg)
        if m:
            Day = int(m.group(1))

        m = re.match(r'-currenttime=(.*)',arg)
        if m:
            CurrentTime = float(m.group(1))*60.0

        m = re.match(r'-ymd=(.*)',arg)
        if m:
            Ymd = m.group(1)
            m = re.match(r'(\d\d\d\d)(\d\d)(\d\d)',Ymd)
            if m:
                CurrentYear  = int(m.group(1))
                CurrentMonth = int(m.group(2))
                CurrentDay   = int(m.group(3))
            else:
                m = re.match(r'(\d\d)(\d\d)(\d\d)',Ymd)
                if m:
                    CurrentYear  = 2000 + int(m.group(1))
                    CurrentMonth = int(m.group(2))
                    CurrentDay   = int(m.group(3))
                else:
                    print("Can not understand format of -ymd=YYYYMMDD")
                    help = 1

        m = re.match(r'-hour=(.*)',arg)
        if m:
            Hour = int(m.group(1))

        m = re.match(r'-n=(.*)',arg)
        if m:
            nEnsembles = float(m.group(1))

        m = re.match(r'-error=(.*)',arg)
        if m:
            errors = float(m.group(1))
            if (errors > 1.0):
                errors=errors/100

        m = re.match(r'-bursttime=(.*)',arg)
        if m:
            BurstTime = float(m.group(1))*60.0

        m = re.match(r'-hover=(.*)',arg)
        if m:
            hover = float(m.group(1))
            print("Hover Altitude set!")
            print(hover)

    help = 0
    if payload < 0:
        print("Set payload=")
        help = 1

    if parachute < 0:
        print("Set parachute=")
        help = 1

    if balloon < 0: 
        print("Set balloon=")
        help = 1

    if helium < 0:
        print("Set helium=")
        help = 1

    if lat < -90:
        print("Set lat=")
        help = 1

    if lon < -360:
        print("Set lon=")
        help = 1

    if (IsZeroPressure):
        if (BalloonR == 0):
            print ("For Zero Pressure Balloon, must set balloon radius (-r=???)")
            help = 1
        if (BalloonV == 0):
            print ("For Zero Pressure Balloon, must set balloon volume (-v=???)")
            help = 1
        

    if help == 1:
        balloon = -1.0
        print("./balloon.py options:")
        print("            -balloon=mass of the balloon, acceptable values:")
        print("                     200, 300, 350, 450, 500, 600, 700, 800,")
        print("                     1000, 1200, 1500, 2000, 3000")
        print("                     for a zero pressure balloon, put the ")
        print("                     real mass of the balloon in grams.")
        print("            -payload=WEIGHT of payload (in lbs)")
        print("            -parachute=diameter of parachute (in feet)")
        print("            -helium=tanks of helium (typically between 1-2)")
        print("            -lat=Initial Latitude")
        print("            -lon=Initial Longitude")
        print("            -alt=Initial Altitude (feet)")
        print("            -descent (force descent mode - no ascent!)")
        print("        optional:")
        print("            -bursttime=N (time in minutes for FTU initiation)")
        print("            -update  (Update the weather file based on position - slow!)")
        print("            -aprs  (use the current APRS position as starting point - for real time!)")
        print("            -zero  (simulate a zero pressure balloon)")
        print("            -r=radius (for zero pressure balloon, in meters)")
        print("            -v=total volume of balloon (for zero pressure balloon, in meters^3)")
        print("            -hover=Altitude of neutral buoyant point (ZP balloon - although automatic now)")
        print("            -loss=percentage loss rate of helium through balloon (% per minute)")
        print("            -n=Number of Ensembles to run")
        print("            -error=fractional error for winds")
        print("                   (error in burst diam = error/4")
        print("                   (error in moles of helium = error/4")
        print("            -callsign=call sign of person running code ")
        print("            -html=html output file")
        print("            -cleanup will delete temporary files ")
        print("example: ")
        print("  ./balloon.py -payload=6.0 -balloon=1000 -parachute=6.0 -helium=1.5 -lat=42.0 -lon=-84.0")

    area = 2*pi*(parachute * ParachuteFudge)**2

    Year  = CurrentYear
    Month = CurrentMonth
    if (Day > -1):
        if (Day < CurrentDay):
            Month = Month + 1
            if (Month > 12):
                Month = 1
                Year = Year + 1
    else:
        Day = CurrentDay

    if (Hour < 0):
        Hour = CurrentHour

    LaunchTime = datetime.datetime(Year,Month,Day,Hour,0,0)

    args = {'balloon':balloon, 
            'payload':payload,
            'helium':helium,
            'descent':IsDescent,
            'altitude':alt*0.3048,
            'latitude':lat,
            'longitude':lon,
            'parachute':parachute,
            'area':area,
            'errors':errors,
            'nEnsembles':nEnsembles,
            'year':Year,
            'month':Month,
            'day':Day,
            'hour':Hour,
            'htmlfile':htmlfile,
            'kmlfile':kmlfile,
            'csvfile':csvfile,
            'callsign':callsign,
            'loss':loss,
            'update':update,
            'hover':hover,
            'bursttime':BurstTime,
            'r':BalloonR,
            'v':BalloonV,
            'zero':IsZeroPressure,
            'aprs':UseAprs,
            'currenttime':CurrentTime,
            'launchtime':LaunchTime,
            'stime':sTimeNow}

    return args

#-----------------------------------------------------------------------------
# Determine which station(s) is(are) closest to the latitude and longitude
#-----------------------------------------------------------------------------

def get_station(longitude, latitude):

    fpin = open('StationList','r')

    MinDist = 1.0e32

    IsNam = 1
    SaveLat = 0.0
    SaveLon = 0.0

    for line in fpin:

        m = re.match(r'(.*) SLAT = (.*) SLON = (.*) SELV = (.*)',line)
        if m:
            inStat = m.group(1)
            inLat = float(m.group(2))
            inLon = float(m.group(3))
            dist  = (inLat-latitude)**2 + (inLon-longitude)**2

            if (dist < MinDist):
                MinDist = dist
                StatSave = inStat
                SaveLat = inLat
                SaveLon = inLon
                #print("New Closest : ",StatSave,inLat,inLon)

    fpin.close()

    DistSave = MinDist

    if (MinDist > 500):

        #print("Expanding list of stations....")

        fpin = open('StationListWorld','r')

        for line in fpin:

            m = re.match(r'(.*) SLAT = (.*) SLON = (.*) SELV = (.*)',line)
            if m:
                inStat = m.group(1)
                inLat = float(m.group(2))
                inLon = float(m.group(3))
                dist  = (inLat-latitude)**2 + (inLon-longitude)**2

                if (dist < MinDist):
                    MinDist = dist
                    StatSave = inStat
                    SaveLat = inLat
                    SaveLon = inLon
                    #print("New Closest : ",StatSave,inLat,inLon)

        fpin.close()

    print(MinDist, DistSave)

    stat = StatSave
    date = datetime.datetime.now()
    sDateHour = date.strftime('%Y.%m.%d.%H')

    if (MinDist == DistSave):
        url = 'http://www.meteor.iastate.edu/~ckarsten/bufkit/data/nam/nam_'+stat+'.buf'
#        url = 'ftp://ftp.meteo.psu.edu/pub/bufkit/latest/nam_'+stat+'.buf'
    else:
        url = 'ftp://ftp.meteo.psu.edu/pub/bufkit/GFS/latest/gfs3_'+stat+'.buf'
        IsNam = 0

    outfile = stat+'.'+sDateHour+'.txt'

    print(url)
    print(outfile)

    if (not os.path.isfile(outfile)):
        # command = '/sw/bin/wget -O '+outfile+' '+url+' >& .log'
        command = '/opt/local/bin/curl -o '+outfile+' '+url+' >& .log.curl'
        print(command)
        os.system(command)

    return (outfile,url,IsNam,SaveLat,SaveLon)

#-----------------------------------------------------------------------------
# Read RAP file
#-----------------------------------------------------------------------------

def read_rap(file,args,IsNam):

    if (IsNam):
        SearchString = 'CFRL HGHT'
    else:
        SearchString = 'HGHT'
        Hour = args['hour']
        Hour = int(Hour/3)*3
        args['hour'] = Hour
        print("modifying hour to be : "+str(args['hour']))

    fpin = open(file,'r')

    pressure = []
    altitude = []
    direction = []
    speed = []
    temperature = []

    IsDone = 0;
    while (IsDone == 0):

        line = fpin.readline()

        if (not line):
            IsDone = 2
        else:

            m = re.search(r"TIME = (\d\d)(\d\d)(\d\d)/(\d\d)(\d\d)",line)
            if m:
                print('time read : ',m.group(1),m.group(2),m.group(3),m.group(4))
                h = int(m.group(4))
                d = int(m.group(3))
                y = int(m.group(1)) + 2000
                m = int(m.group(2))
                print('searching... : ',args['year'],args['month'],args['day'],args['hour'])
                if (y == args['year'] and m == args['month'] and d == args['day'] and h == args['hour']):
                    IsDone = 1
            
    #print('done reading time!')

    if (IsDone == 1):
        IsDone = 0
    else:
        print("Could not find requested time! Just using first time in file!")
        fpin.seek(0,0)
        IsDone = 0

    while (IsDone == 0):

        line = fpin.readline()
        m = re.search(r"SLAT = (.*) SLON = (.*) SELV = (.*)",line)
        if m:
            lat = m.group(1)
            lon = m.group(2)
            alt = m.group(3)
            print(lat,lon,alt)

        m = re.search(SearchString,line)
        if m:
            # Read in all of the height data:
            # read first line
            line = fpin.readline()
            while (len(line) > 40):
                line = line.strip()
                column = line.split()
                pressure.append(float(column[0]))
                temperature.append(float(column[1]))
                direction.append(float(column[5]))
                speed.append(float(column[6])*KnotsToMps)
                #read second line
                line = fpin.readline()
                line = line.strip()
                column = line.split()
                #print(column)
                altitude.append(float(column[IsNam]))
                #read first line (put here to check for zero size)
                line = fpin.readline()
            IsDone = 1
            
    fpin.close

    altitude = np.array(altitude)
    pressure = np.array(pressure)*100.0
    temperature = np.array(temperature)+273.15
    dir = np.array(direction)
    speed = np.array(speed)
    vn = speed * np.sin((270.0-dir)*dtor)
    ve = speed * np.cos((270.0-dir)*dtor)

    data = {'Altitude':altitude, 'Pressure':pressure, 'Temperature':temperature,
            'Veast':ve, 'Vnorth':vn}
            
    return data


#-----------------------------------------------------------------------------
# 
#-----------------------------------------------------------------------------

def KaymontBalloonBurst(BalloonMass):

    # Balloon Masses
    kaymontMass = [200, 300, 350, 450, 500, 
                   600, 700, 800, 1000, 1200, 
                   1500, 2000, 3000]

    # Burst diameter in meters
    kaymontBurstDiameter = [3.00, 3.78, 4.12, 4.72, 4.99, 
                            6.02, 6.53, 7.00, 7.86, 8.63, 
                            9.44, 10.54, 13.00]

    burst = -1.0

    i = 0
    for mass in kaymontMass:
        if (BalloonMass == mass):
            burst = kaymontBurstDiameter[i]
        i=i+1

    return burst


#-----------------------------------------------------------------------------
# 
#-----------------------------------------------------------------------------

def calculate_helium(NumberOfTanks):

    # Assumes Room Temperature:
    RoomTemp = 294.261

    # Assumes K-size cylinder:
    TankVolume = 43.8 * 0.001

    # Assumes Tank Pressure
    TankPressure = 14500*1000.0

    #NumberOfMoles = NumberOfTanks * TankPressure * TankVolume / UniversalGasConstant / RoomTemp
    NumberOfHe = NumberOfTanks * TankPressure * TankVolume / Boltzmann / RoomTemp

    return NumberOfHe

#-----------------------------------------------------------------------------
# 
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# 
#-----------------------------------------------------------------------------

def calc_ascent_rate(RapData, NumberOfHelium, args, altitude):

    Temperature,Pressure = get_temperature_and_pressure(altitude,RapData)

    Volume = NumberOfHelium * Boltzmann * Temperature/Pressure

    if (args['zero'] == 1):
        if (Volume > args['v']):
            NumberOfHelium = args['v'] * Pressure / (Boltzmann * Temperature)
        Radius = args['r']
        Diameter = Radius * 2
    else:
        Diameter =  2.0 * (3.0 * Volume / (4.0*pi))**(1.0/3.0)
        Radius   = Diameter/2.0

    Gravity = SurfaceGravity * (EarthRadius/(EarthRadius+altitude))**2

    NetLiftMass = NumberOfHelium * (MassOfAir - MassOfHelium)

    NetLiftForce = (NetLiftMass - args['payload'] - args['balloon']/1000) * Gravity;

    MassDensity = MassOfAir * Pressure / (Boltzmann * Temperature)

    Area = pi * Radius * Radius

    if (args['zero'] == 0):
        # With the real formula for the balloon ascent rate, the balloon accelerates
        # upward.  This doesn't seem to be the case in real launches.  A more
        # uniform ascent rate is often observed.  Through trial and error, we found
        # that using a corrector as below is good...
        t,p = get_temperature_and_pressure(1000.0,RapData)
        v = NumberOfHelium * Boltzmann * t/p
        r = (3.0 * v / (4.0*pi))**(1.0/3.0)
        # This is basically assuming that the first ascent rate is the correct on,
        # while the higher ones are a bit too fast, so they have to be slowed down:
        corrector = r/Radius
    else:
        corrector = 1.0

    if (NetLiftForce > 0.0):
        AscentRate = np.sqrt(2*NetLiftForce * corrector / (BalloonDragCoefficient*Area*MassDensity))
    else:
        AscentRate = -np.sqrt(-2*NetLiftForce * corrector / (BalloonDragCoefficient*Area*MassDensity))

    #print(AscentRate,Volume,Diameter,corrector)

    return (AscentRate, Diameter)

#-----------------------------------------------------------------------------
# 
#-----------------------------------------------------------------------------

def calc_descent_rate(RapData, args, altitude):

    Gravity = SurfaceGravity * (EarthRadius/(EarthRadius+altitude))**2

    Temperature,Pressure = get_temperature_and_pressure(altitude,RapData)
    MassDensity = MassOfAir * Pressure / (Boltzmann * Temperature)

    DescentRate = np.sqrt(2 * args['payload'] * Gravity / (MassDensity * ParachuteDragCoefficient * args['area']));

    return DescentRate

#-----------------------------------------------------------------------------
# 
#-----------------------------------------------------------------------------

def get_temperature_and_pressure(altitude,RapData):

    i = 0

    while (altitude > RapData['Altitude'][i] and i < len(RapData['Altitude'])-1):
        i=i+1

    if (i == 0 or i == len(RapData['Altitude'])):
        temp = RapData['Temperature'][i]
        pres = RapData['Pressure'][i]
    else:
        da = RapData['Altitude'][i]-RapData['Altitude'][i-1]
        x = (altitude-RapData['Altitude'][i-1])/da
        temp = x*RapData['Temperature'][i] + (1-x)*RapData['Temperature'][i-1]
        pres = x*RapData['Pressure'][i] + (1-x)*RapData['Pressure'][i-1]
        alt = x*RapData['Altitude'][i] + (1-x)*RapData['Altitude'][i-1]

    return (temp,pres)


#-----------------------------------------------------------------------------
# 
#-----------------------------------------------------------------------------

def get_wind(RapData,altitude):

    i = 0

    while (altitude > RapData['Altitude'][i] and i < len(RapData['Altitude'])-1):
        i=i+1

    if (i == 0 or i == len(RapData['Altitude'])):
        vn = RapData['Vnorth'][i]
        ve = RapData['Veast'][i]
    else:
        da = RapData['Altitude'][i]-RapData['Altitude'][i-1]
        x = (altitude-RapData['Altitude'][i-1])/da
        vn = x*RapData['Vnorth'][i] + (1-x)*RapData['Vnorth'][i-1]
        ve = x*RapData['Veast'][i] + (1-x)*RapData['Veast'][i-1]

    return (ve,vn)


#-----------------------------------------------------------------------------
# 
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# 
#-----------------------------------------------------------------------------

def write_html(args,AscentLongitudes,AscentLatitudes,AscentAltitudes,
               DescentLongitudes,DescentLatitudes,DescentAltitudes,
               AscentTime, DescentTime,
               AscentRate, DescentRate,
               FinalLongitudes,FinalLatitudes,
               PeakAltitude,PeakAltitudeDiff, url,
               TotalDistance, images,
               RealTimeLon, RealTimeLat,
               StationLon, StationLat):

    fpout = open(args['htmlfile'],'w')
    kmlout = open(args['kmlfile'],'w')
    csvout = open(args['csvfile'],'w')
    
    burstlat = DescentLatitudes[0]
    burstlon = DescentLongitudes[0]

    fpout.write("<!DOCTYPE html>\n")
    fpout.write("<html>\n")
    fpout.write("  <head>\n")
    fpout.write("    <meta name=\"viewport\" content=\"initial-scale=1.0, user-scalable=yes\" />\n")
    fpout.write("    <meta http-equiv=\"refresh\" content=\"content=60\" />\n")
    fpout.write("    <style type=\"text/css\">\n")
    fpout.write("      html { height: 100% } \n")
    fpout.write("      body { height: 75%; margin: 20; padding: 20 }\n")
    fpout.write("    </style>\n")
    fpout.write("    <script type=\"text/javascript\"\n")
    fpout.write("      src=\"http://maps.googleapis.com/maps/api/js?key=AIzaSyD60d34mCUoQ63hWqsCdZwwa1_Ywhm_4wE&sensor=true\">\n")
    fpout.write("    </script>\n")
    fpout.write("    <script type=\"text/javascript\">\n")
    fpout.write("      function initialize() {\n")
    fpout.write("        var mapOptions = {\n")
    fpout.write("           center: new google.maps.LatLng("+str(burstlat)+", "+str(burstlon)+"),\n")
    fpout.write("           zoom: 9,\n")
    fpout.write("           mapTypeId: google.maps.MapTypeId.ROADMAP\n")
    fpout.write("        };\n")
    fpout.write("        var map = new google.maps.Map(document.getElementById(\"map_canvas\"),mapOptions);\n")
    fpout.write(" \n")
    fpout.write("        var pinColorR = \"FF6666\";\n")
    fpout.write("        var pinImageR = new google.maps.MarkerImage(\"http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|\" + pinColorR,\n")
    fpout.write("           new google.maps.Size(21, 34),\n")
    fpout.write("           new google.maps.Point(0,0),\n")
    fpout.write("           new google.maps.Point(10, 34));\n")
    fpout.write(" \n")
    fpout.write("        var pinColorG = \"66FF66\";\n")
    fpout.write("        var pinImageG = new google.maps.MarkerImage(\"http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|\" + pinColorG,\n")
    fpout.write("           new google.maps.Size(21, 34),\n")
    fpout.write("           new google.maps.Point(0,0),\n")
    fpout.write("           new google.maps.Point(10, 34));\n")
    fpout.write(" \n")
    fpout.write("        var pinColorB = \"6666FF\";\n")
    fpout.write("        var pinImageB = new google.maps.MarkerImage(\"http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|\" + pinColorB,\n")
    fpout.write("           new google.maps.Size(21, 34),\n")
    fpout.write("           new google.maps.Point(0,0),\n")
    fpout.write("           new google.maps.Point(10, 34));\n")
    fpout.write(" \n")
    fpout.write("        var pinColorY = \"FFFF66\";\n")
    fpout.write("        var pinImageY = new google.maps.MarkerImage(\"http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|\" + pinColorY,\n")
    fpout.write("           new google.maps.Size(21, 34),\n")
    fpout.write("           new google.maps.Point(0,0),\n")
    fpout.write("           new google.maps.Point(10, 34));\n")
    fpout.write(" \n")
    fpout.write("        var pinColorBl = \"909090\";\n")
    fpout.write("        var pinImageBl = new google.maps.MarkerImage(\"http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|\" + pinColorBl,\n")
    fpout.write("           new google.maps.Size(21, 34),\n")
    fpout.write("           new google.maps.Point(0,0),\n")
    fpout.write("           new google.maps.Point(10, 34));\n")
    fpout.write(" \n")
    fpout.write("        var pinColorPi = \"FFC0C0\";\n")
    fpout.write("        var pinImagePi = new google.maps.MarkerImage(\"http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|\" + pinColorPi,\n")
    fpout.write("           new google.maps.Size(21, 34),\n")
    fpout.write("           new google.maps.Point(0,0),\n")
    fpout.write("           new google.maps.Point(10, 34));\n")
    fpout.write(" \n")
    fpout.write("        var pinColorCy = \"C0C0FF\";\n")
    fpout.write("        var pinImageCy = new google.maps.MarkerImage(\"http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|\" + pinColorCy,\n")
    fpout.write("           new google.maps.Size(21, 34),\n")
    fpout.write("           new google.maps.Point(0,0),\n")
    fpout.write("           new google.maps.Point(10, 34));\n")
    fpout.write(" \n")

    #-------------------------------------------------------------
    # KML File Header
    #-------------------------------------------------------------

    kmlout.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
    kmlout.write("<kml xmlns=\"http://www.opengis.net/kml/2.2\">\n")
    kmlout.write("<Document>\n");
    kmlout.write("<name>Testing Testing</name>\n");
    kmlout.write("<description>This is a test of the whatever system</description>\n")
    kmlout.write("<Style id=\"yellowLineBluePoly\">\n");
    kmlout.write("<LineStyle><color>7f00ffff</color><width>10</width></LineStyle>\n")
    kmlout.write("<PolyStyle><color>7fff0000</color></PolyStyle>\n")
    kmlout.write("</Style>\n")

    kmlout.write("<Placemark>")
    kmlout.write("<name>Absolute Extruded</name>")
    kmlout.write("<description>Transparent blue wall with yellow outlines</description>")
    kmlout.write("<styleUrl>#yellowLineBluePoly</styleUrl>")
    kmlout.write("<LineString>")
    kmlout.write("<altitudeMode>absolute</altitudeMode>")
    kmlout.write("<coordinates>")

    #-------------------------------------------------------------
    # Launch Site
    #-------------------------------------------------------------
    lat = AscentLatitudes[0]
    lon = AscentLongitudes[0]
    fpout.write("        var marker = new google.maps.Marker({\n")
    fpout.write("           position: new google.maps.LatLng("+str(lat)+","+str(lon)+"),\n")
    fpout.write("           icon: pinImageR,\n")
    fpout.write("           map: map\n")
    fpout.write("        });\n")
    fpout.write("\n")

    LaunchLat = lat
    LaunchLon = lon

    #-------------------------------------------------------------
    # Ascent Locations
    #-------------------------------------------------------------
    i = 0
    for alt in AscentAltitudes:
        if i > 0:
            alt0 = int((AscentAltitudes[i-1]/FtToMeters)/10000)
            alt1 = int((alt/FtToMeters)/10000)
            if (alt1 != alt0):
                lat = AscentLatitudes[i]
                lon = AscentLongitudes[i]
                fpout.write("        var marker = new google.maps.Marker({\n")
                fpout.write("           position: new google.maps.LatLng("+str(lat)+","+str(lon)+"),\n")
                fpout.write("           icon: pinImagePi,\n")
                fpout.write("           map: map\n")
                fpout.write("        });\n")
                fpout.write("\n")                
        i=i+1

    #-------------------------------------------------------------
    # Descent Locations
    #-------------------------------------------------------------
    i = 0
    for alt in DescentAltitudes:
        if i > 0:
            alt0 = int((DescentAltitudes[i-1]/FtToMeters)/10000)
            alt1 = int((alt/FtToMeters)/10000)
            if (alt1 != alt0):
                lat = DescentLatitudes[i]
                lon = DescentLongitudes[i]
                fpout.write("        var marker = new google.maps.Marker({\n")
                fpout.write("           position: new google.maps.LatLng("+str(lat)+","+str(lon)+"),\n")
                fpout.write("           icon: pinImageCy,\n")
                fpout.write("           map: map\n")
                fpout.write("        });\n")
                fpout.write("\n")                
        i=i+1
        
    #-------------------------------------------------------------
    # Burst Location
    #-------------------------------------------------------------
    lat = DescentLatitudes[0]
    lon = DescentLongitudes[0]
    fpout.write("        var marker = new google.maps.Marker({\n")
    fpout.write("           position: new google.maps.LatLng("+str(lat)+","+str(lon)+"),\n")
    fpout.write("           icon: pinImageB,\n")
    fpout.write("           map: map\n")
    fpout.write("        });\n")
    fpout.write("\n")

    #-------------------------------------------------------------
    # Landing Site
    #-------------------------------------------------------------
    i = len(DescentLatitudes)
    lat = DescentLatitudes[i-1]
    lon = DescentLongitudes[i-1]
    fpout.write("        var marker = new google.maps.Marker({\n")
    fpout.write("           position: new google.maps.LatLng("+str(lat)+","+str(lon)+"),\n")
    fpout.write("           icon: pinImageY,\n")
    fpout.write("           map: map\n")
    fpout.write("        });\n")
    fpout.write("\n")

    LandingLat = lat
    LandingLon = lon

    #-------------------------------------------------------------
    # Current RealTime Location
    #-------------------------------------------------------------
    if (len(RealTimeLat) > 1):
        lat = RealTimeLat[0]
        lon = RealTimeLon[0]
        fpout.write("        var marker = new google.maps.Marker({\n")
        fpout.write("           position: new google.maps.LatLng("+str(lat)+","+str(lon)+"),\n")
        fpout.write("           icon: pinImageG,\n")
        fpout.write("           map: map\n")
        fpout.write("        });\n")
        fpout.write("\n")

    #-------------------------------------------------------------
    # Ascent
    #-------------------------------------------------------------
    fpout.write("var AscentCoordinates = [\n")
    i = 0
    t = 0.0
    for lat in AscentLatitudes:
        lon = AscentLongitudes[i]
        alt = AscentAltitudes[i]
        t = t + dt
        time = args['launchtime']+datetime.timedelta(seconds=t)
        timeS = time.strftime('%Y-%m-%dT%H:%M:%SZ')
        kmlout.write(str(lon)+","+str(lat)+","+str(alt)+"\n")
        csvout.write(timeS+","+str(t)+","+str(lon)+","+str(lat)+","+str(alt)+"\n")
        fpout.write("  new google.maps.LatLng("+str(lat)+","+str(lon)+"),\n")
        i=i+1
    fpout.write("      ];\n")
    fpout.write("\n")
    fpout.write("      var flightPathAscent = new google.maps.Polyline({\n")
    fpout.write("        path: AscentCoordinates,\n")
    fpout.write("        strokeColor: \"\#FF0000\",\n")
    fpout.write("        strokeOpacity: 1.0,\n")
    fpout.write("        strokeWeight: 3\n")
    fpout.write("      });\n")
    fpout.write("\n")
    fpout.write("      flightPathAscent.setMap(map);\n")
    fpout.write(" \n")

    #-------------------------------------------------------------
    # Descent
    #-------------------------------------------------------------
    fpout.write("var DescentCoordinates = [\n")
    i = 0
    for lat in DescentLatitudes:
        t = t + dt
        lon = DescentLongitudes[i]
        alt = DescentAltitudes[i]
        time = args['launchtime']+datetime.timedelta(seconds=t)
        timeS = time.strftime('%Y-%m-%dT%H:%M:%SZ')
        kmlout.write(str(lon)+","+str(lat)+","+str(alt)+"\n")
        csvout.write(timeS+","+str(t)+","+str(lon)+","+str(lat)+","+str(alt)+"\n")
        fpout.write("  new google.maps.LatLng("+str(lat)+","+str(lon)+"),\n")
        i=i+1
    fpout.write("      ];\n")
    fpout.write("\n")
    fpout.write("      var flightPathDescent = new google.maps.Polyline({\n")
    fpout.write("        path: DescentCoordinates,\n")
    fpout.write("        strokeColor: \"\#0000FF\",\n")
    fpout.write("        strokeOpacity: 1.0,\n")
    fpout.write("        strokeWeight: 3\n")
    fpout.write("      });\n")
    fpout.write("\n")
    fpout.write("      flightPathDescent.setMap(map);\n")
    fpout.write(" \n")

    #-------------------------------------------------------------
    # Weather Station Locations
    #-------------------------------------------------------------
    i = 0
    for lat in StationLat:
        lon = StationLon[i]
        print(lat,lon)
        fpout.write("        var marker = new google.maps.Marker({\n")
        fpout.write("           position: new google.maps.LatLng("+str(lat)+","+str(lon)+"),\n")
        fpout.write("           icon: pinImageBl,\n")
        fpout.write("           map: map\n")
        fpout.write("        });\n")
        fpout.write("\n")
        i=i+1

    #-------------------------------------------------------------
    # Perturbed Landing Sites
    #-------------------------------------------------------------
    i = 0
    for lat in FinalLatitudes:
        lon = FinalLongitudes[i]
        fpout.write("        var marker = new google.maps.Marker({\n")
        fpout.write("           position: new google.maps.LatLng("+str(lat)+","+str(lon)+"),\n")
        fpout.write("           icon: pinImageG,\n")
        fpout.write("           map: map\n")
        fpout.write("        });\n")
        fpout.write("\n")
        i=i+1

    #-------------------------------------------------------------
    # RealTime
    #-------------------------------------------------------------
    if (len(RealTimeLat) > 1):
        fpout.write("var RealTimeCoordinates = [\n")
        i = 0
        for lat in RealTimeLat:
            lon = RealTimeLon[i]
            fpout.write("  new google.maps.LatLng("+str(lat)+","+str(lon)+"),\n")
            i=i+1
        fpout.write("      ];\n")
        fpout.write("\n")
        fpout.write("      var flightPathRealTime = new google.maps.Polyline({\n")
        fpout.write("        path: RealTimeCoordinates,\n")
        fpout.write("        strokeColor: \"\#000000\",\n")
        fpout.write("        strokeOpacity: 1.0,\n")
        fpout.write("        strokeWeight: 3\n")
        fpout.write("      });\n")
        fpout.write("\n")
        fpout.write("      flightPathRealTime.setMap(map);\n")
        fpout.write(" \n")

    fpout.write("      }\n")
    fpout.write("    </script>\n")
    fpout.write("  </head>\n")
    fpout.write("  <body onload=\"initialize()\">\n")
    fpout.write("    <div id=\"map_canvas\" style=\"width:100%; height:100%\"></div>\n")

    kmlout.write("</coordinates>\n")
    kmlout.write("</LineString>\n")
    kmlout.write("</Placemark>\n")
    kmlout.write("</Document>\n")
    kmlout.write("</kml>\n")

    #-------------------------------------------------------------
    # Extra Information
    #-------------------------------------------------------------
    
    earth_radius_miles = 3956.0

    #Find the distance between each station and the user's coordinates
    #accounting for spherical geometery
    dlat = np.radians(LandingLat) - np.radians(LaunchLat)
    dlon = np.radians(LandingLon) - np.radians(LaunchLon)
    a = np.square(np.sin(dlat/2.0)) + np.cos(np.radians(LaunchLat)) * \
        np.cos(np.radians(LandingLat)) * np.square(np.sin(dlon/2.0))
    great_circle_distance = 2 * np.arcsin(np.sqrt(a))
    distance = earth_radius_miles * great_circle_distance

    fpout.write("    Red Pin indicates launch/start<br>\n")
    fpout.write("    Pink Pins indicate every 10,000 ft on ascent (roughly 3 km)<br>\n")
    fpout.write("    Blue Pin indicates burst<br>\n")
    fpout.write("    Cyan Pins indicate every 10,000 ft on descent (roughly 3 km)<br>\n")
    fpout.write("    Yellow Pin indicates landing<br>\n")
    fpout.write("    Green Pin indicates weather stations<br>\n")
    fpout.write("    <b>Output Parameters:</b><br>\n")
    fpout.write("    Peak Altitude : "+str(round(PeakAltitude))+"+/-"+str(round(PeakAltitudeDiff))+' m ('+
                str(round(PeakAltitude/FtToMeters))+"+/-"+str(round(PeakAltitudeDiff/FtToMeters))+' ft)<br>')
    dummy = np.round(AscentRate*100.0)/100.0
    dummy2 = np.round(AscentRate/FtToMeters*60.0*100.0)/100.0
    fpout.write("    Ascent Rate   : "+str(dummy)+" m/s ("+str(dummy2)+" fpm)<br>\n")
    fpout.write("    Ascent Time  : "+str(np.round(AscentTime/60.0))+" minutes<br>\n")
    dummy = np.round(DescentRate*100.0)/100.0
    fpout.write("    Descent Rate  : "+str(dummy)+" m/s<br>\n")
    fpout.write("    Descent Time : "+str(np.round(DescentTime/60.0))+" minutes<br>\n")
    fpout.write("    Total Time : "+str(np.round((AscentTime + DescentTime)/60.0))+" minutes<br>\n")
    fpout.write("    Total Distance Traveled : "+str(np.round(TotalDistance))+" Miles<br>\n")
    fpout.write("    Distance Between Launch and Landing : "+str(np.round(distance))+" Miles<br>\n")

    fpout.write("    <b>Input Parameters:</b><br>\n")
    fpout.write("    Starting Latitude : "+str(args['latitude'])+"<br>\n")
    fpout.write("    Starting Longitude : "+str(args['longitude'])+"<br>\n")
    fpout.write("    Tanks of Helium : "+str(args['helium'])+"<br>\n")
    fpout.write("    Balloon Size : "+str(args['balloon'])+" g <br>\n")
    d = args['parachute']*3.3*2
    fpout.write("    Parachute Diameter: "+str(d)+" ft<br>\n")
    wt = args['payload']*2.2
    fpout.write("    Payload Weight : "+str(wt)+" lbs<br>\n")
    fpout.write("    Launch time : "+str(args['year'])+"-"+str(args['month'])+"-"+str(args['day'])+" "+str(args['hour'])+" UT")

    fpout.write("    <p>\n")
    fpout.write("    <b>Images:</b><br>\n")
    for image in images:
        fpout.write("    <img src=\""+image+"\"><br>")

    fpout.write("  </body>\n")
    fpout.write("</html>\n")

    fpout.close()
    kmlout.close()
    csvout.close()


#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
# Main Code!
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------

args = get_args(sys.argv)

if (args['balloon'] > 0):

    BurstDiameter = KaymontBalloonBurst(args['balloon'])
    if (BurstDiameter < 0 and args['zero'] == 1):
        BurstDiameter = args['r']*2.001

    if (BurstDiameter < 0):
        print("Could not determine burst diameter! Stopping!")

    NumberOfHelium = calculate_helium(args['helium'])

    TotalKm = 0.0

    if (BurstDiameter > 0):

        longitude = args['longitude']
        latitude = args['latitude']

        filename,url,IsNam,StatLat,StatLon = get_station(longitude, latitude)
        StationLat = [StatLat]
        StationLon = [StatLon]
        RapData = read_rap(filename,args,IsNam)

        Diameter = 0.0
        AscentTime = 1.0
        print(args['altitude'])

        if (args['altitude'] < 0.0):
            altitude = RapData['Altitude'][0]
        else:
            altitude = args['altitude']
            if (args['descent']):
                Diameter = BurstDiameter*2.0
                AscentRate = 0.0

        AscentLongitude = []
        AscentLatitude  = []
        AscentAltitude  = []

        DescentLongitude = []
        DescentLatitude  = []
        DescentAltitude  = []

        FinalLongitudes = []
        FinalLatitudes  = []

        # Ascent:

        AscentLongitude.append(longitude)
        AscentLatitude.append(latitude)
        AscentAltitude.append(altitude)

        TotalDistance = 0.0

        WindSpeed = []
        TotalTime = []
        Altitudes = []

        if (args['update'] == 1):
            oldfilename,url,IsNam,StatLat,StatLon = get_station(longitude, latitude)
            if (StatLat != StationLat[-1]):
                StationLat.append(StatLat)
                StationLon.append(StatLon)
            RapData = read_rap(oldfilename,args,IsNam)
        else:
            filename,url,IsNam,StatLat,StatLon = get_station(longitude, latitude)
            if (StatLat != StationLat[-1]):
                StationLat.append(StatLat)
                StationLon.append(StatLon)
            RapData = read_rap(filename,args,IsNam)
        
        while (Diameter < BurstDiameter and altitude > -1.0):

            print(altitude)

            if (args['update'] == 1):
                filename,url,IsNam,StatLat,StatLon = get_station(longitude, latitude)
                if (StatLat != StationLat[-1]):
                    StationLat.append(StatLat)
                    StationLon.append(StatLon)
                if (filename != oldfilename):
                    RapData = read_rap(filename,args,IsNam)
                    oldfilename = filename
            
            NumberOfHelium = NumberOfHelium * (1.0-args['loss']/100.0/60.0*dt)

            Veast,Vnorth = get_wind(RapData,altitude)
            DegPerMeter = 360.0 / (2*pi * (EarthRadius + altitude))
            longitude = longitude + Veast  * DegPerMeter * dt / np.cos(latitude*dtor)
            latitude  = latitude  + Vnorth * DegPerMeter * dt

            WindSpeed.append(np.sqrt(Veast*Veast + Vnorth*Vnorth))
            TotalDistance += np.sqrt(Veast*Veast + Vnorth*Vnorth)*dt*MilesPerMeter

            AscentRate,Diameter = calc_ascent_rate(RapData, NumberOfHelium, args, altitude)
            if (altitude < args['hover']):
                altitude = altitude + AscentRate*dt

            AscentLongitude.append(longitude)
            AscentLatitude.append(latitude)
            AscentAltitude.append(altitude)

            AscentTime = AscentTime + dt

            TotalTime.append(AscentTime)
            Altitudes.append(altitude)

            if (AscentTime > args['bursttime']):
                Diameter = BurstDiameter*2
            
        print('Final Peak Altitude :',altitude,' m')
        print('Ascent Time :',AscentTime/60.0,' minutes')

        PeakAltitude = altitude
        AscentRateSave = (altitude-AscentAltitude[0])/AscentTime
        print('Ascent Rate :',AscentRate,' m/s')
        AscentTimeSave = AscentTime

        BurstAltitude  = altitude
        BurstLatitude  = latitude
        BurstLongitude = longitude

        # Descent:
        DescentTime = 0.0

        DescentLongitude.append(longitude)
        DescentLatitude.append(latitude)
        DescentAltitude.append(altitude)

        if (altitude < 0.0):
            altitude = RapData['Altitude'][0] + 1.0

        while (altitude > RapData['Altitude'][0]):

            Veast,Vnorth = get_wind(RapData,altitude)
            DegPerMeter = 360.0 / (2*pi * (EarthRadius + altitude))
            longitude = longitude + Veast  * DegPerMeter * dt / np.cos(latitude*dtor)
            latitude  = latitude  + Vnorth * DegPerMeter * dt

            WindSpeed.append(np.sqrt(Veast*Veast + Vnorth*Vnorth))
            TotalDistance += np.sqrt(Veast*Veast + Vnorth*Vnorth)*dt*MilesPerMeter

            DescentRate = calc_descent_rate(RapData, args, altitude)
            altitude = altitude - DescentRate*dt

            DescentLongitude.append(longitude)
            DescentLatitude.append(latitude)
            DescentAltitude.append(altitude)

            DescentTime = DescentTime + dt
            TotalTime.append(AscentTime+DescentTime)
            Altitudes.append(altitude)

            #print(DescentRate,altitude, latitude, longitude)

        print('Final Descent Altitude :',altitude,' m')
        print('Descent Time :',DescentTime/60.0,' minutes')
        print('Total Time :',(AscentTimeSave+DescentTime)/60.0,' minutes')

        DescentRateSave = (DescentAltitude[0]-altitude)/DescentTime
        print('Descent Rate :',DescentRate,' m/s')

        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        something = ax.plot(np.array(TotalTime)/60.0, WindSpeed)
        ax.set_title('Speed (m/s) vs time')
        ax.set_xlabel('Time (minutes)')
        ax.set_ylabel('Speed (m/s)')
        file = 'speed.'+args['stime']+'.png'
        images = [file]
        fig.savefig(file)

        fig = plt.figure()
        ax2 = fig.add_subplot(1,1,1)
        something = ax2.plot(np.array(TotalTime)/60.0, Altitudes)
        ax2.set_title('Altitude (meters) vs time')
        ax2.set_xlabel('Time (minutes)')
        ax2.set_ylabel('Altitude (meters)')
        file = 'altitude.'+args['stime']+'.png'
        images.append(file)
        fig.savefig(file)

        #-----------------------------------------------------------------
        # Redo calculation a few times with variations
        #-----------------------------------------------------------------

        i = 0

        nEnsembles = args['nEnsembles']
        errors     = args['errors']

        DifferenceInPeakAltitude = 0.0

        while (i < nEnsembles):

            i=i+1

            longitude = AscentLongitude[0]
            latitude = AscentLatitude[0]
            altitude = AscentAltitude[0]

            Diameter = 0

            NumberOfHelium = calculate_helium(args['helium'])
            NumberOfHeliumPerturbed = random.normalvariate(NumberOfHelium,NumberOfHelium*errors/4)
            BurstDiameterPertrubed = random.normalvariate(BurstDiameter,BurstDiameter*errors/4)

            bt = random.normalvariate(args['bursttime'],args['bursttime']*errors/4)

            AscentTime = 0

            while (Diameter < BurstDiameter and altitude > -1.0):

                NumberOfHelium = NumberOfHelium * (1.0-args['loss']/100.0/60.0*dt)

                if (args['update'] == 1):
                    filename,url,IsNam,StatLat,StatLon = get_station(longitude, latitude)
                    if (StatLat != StationLat[-1]):
                        StationLat.append(StatLat)
                        StationLon.append(StatLon)
                    if (filename != oldfilename):
                        RapData = read_rap(filename,args,IsNam)
                        oldfilename = filename

                Veast,Vnorth = get_wind(RapData,altitude)

                Veast  = random.normalvariate(Veast, np.abs(Veast)*errors)
                Vnorth = random.normalvariate(Vnorth,np.abs(Vnorth)*errors)

                DegPerMeter = 360.0 / (2*pi * (EarthRadius + altitude))
                longitude = longitude + Veast  * DegPerMeter * dt / np.cos(latitude*dtor)
                latitude  = latitude  + Vnorth * DegPerMeter * dt

                AscentRate,Diameter = calc_ascent_rate(RapData, NumberOfHeliumPerturbed, args, altitude)

                if (altitude < args['hover']):
                    altitude = altitude + AscentRate*dt

                AscentTime = AscentTime + dt
                if (AscentTime > args['bursttime']):
                    Diameter = BurstDiameter*2


            DifferenceInPeakAltitude = DifferenceInPeakAltitude + (altitude-PeakAltitude)**2

            if (altitude < 0.0):
                altitude = RapData['Altitude'][0] + 1.0

            while (altitude > RapData['Altitude'][0]):

                Veast,Vnorth = get_wind(RapData,altitude)

                Veast  = random.normalvariate(Veast, np.abs(Veast)*errors)
                Vnorth = random.normalvariate(Vnorth,np.abs(Vnorth)*errors)

                DegPerMeter = 360.0 / (2*pi * (EarthRadius + altitude))
                longitude = longitude + Veast  * DegPerMeter * dt / np.cos(latitude*dtor)
                latitude  = latitude  + Vnorth * DegPerMeter * dt

                DescentRate = calc_descent_rate(RapData, args, altitude)
                altitude = altitude - DescentRate*dt

            FinalLongitudes.append(longitude)
            FinalLatitudes.append(latitude)
            
        if (nEnsembles > 1):
            DifferenceInPeakAltitude = np.sqrt(DifferenceInPeakAltitude/nEnsembles)

        RealTimeLat = []
        RealTimeLon = []
        RealTimeAlt = []

        if (args['aprs'] == 1):

            callsign = args['callsign']
            tmpfile1 = ".aprs."+callsign
            tmpfile2 = ".aprs."+callsign+".2"
            aprsfile = "aprs."+callsign+"."+str(args['year'])+str(args['month'])+str(args['day'])

            command = "wget -O "+tmpfile1+" \"http://api.aprs.fi/api/get?name="+callsign+"&what=loc&apikey=42457.M4AFa3hdkXG31&format=xml\""
            print(command)
            os.system(command)

            command = "cat "+aprsfile+" "+tmpfile1+" > "+tmpfile2
            print(command)
            os.system(command)

            command = "mv "+tmpfile2+" "+aprsfile
            print(command)
            os.system(command)

            fpin = open(aprsfile,'r')

            aprsLat = []
            aprsLon = []
            aprsAlt = []
            aprsTime = []

            IsDone = 0;
            while (IsDone == 0):

                line = fpin.readline()

                if (not line):
                    IsDone = 2
                else:

                    m = re.search(r"<lat>(.*)</lat><lng>(.*)</lng><altitude>(.*)</altitude>",line)
                    if m:
                        print('time lat : ',m.group(1),m.group(2),m.group(3))
                        aprsLat.append(float(m.group(1)))
                        aprsLon.append(float(m.group(2)))
                        aprsAlt.append(float(m.group(3)))

            NumberOfHelium = calculate_helium(args['helium'])

            Diameter = 0.0

            RealTimeLat.append(aprsLat[-1])
            RealTimeLon.append(aprsLon[-1])
            RealTimeAlt.append(aprsAlt[-1])


            RtAlt = aprsAlt[-1]
            RtLon = aprsLon[-1]
            RtLat = aprsLat[-1]

            RtAscentTime = args['currenttime']

            while (Diameter < BurstDiameter and altitude > -1.0):

                if (args['update'] == 1):
                    filename,url,IsNam,StatLat,StatLon = get_station(RtLon, RtLat)
                    if (StatLat != StationLat[-1]):
                        StationLat.append(StatLat)
                        StationLon.append(StatLon)
                    if (filename != oldfilename):
                        RapData = read_rap(filename,args,IsNam)
                        oldfilename = filename
            
                NumberOfHelium = NumberOfHelium * (1.0-args['loss']/100.0/60.0*dt)

                Veast,Vnorth = get_wind(RapData,RtAlt)
                DegPerMeter = 360.0 / (2*pi * (EarthRadius + RtAlt))
                RtLon = RtLon + Veast  * DegPerMeter * dt / np.cos(RtLat*dtor)
                RtLat  = RtLat  + Vnorth * DegPerMeter * dt

                AscentRate,Diameter = calc_ascent_rate(RapData, NumberOfHelium, args, RtAlt)
                if (RtAlt < args['hover']):
                    RtAlt = RtAlt + AscentRate*dt
                    
                RealTimeLon.append(RtLon)
                RealTimeLat.append(RtLat)
                RealTimeAlt.append(RtAlt)

                RtAscentTime = RtAscentTime + dt

                #print(RtAscentTime, RtAlt)

                if (RtAscentTime > args['bursttime']):
                    Diameter = BurstDiameter*2

            if (RtAlt < 0.0):
                RtAlt = RapData['Altitude'][0] + 1.0

            while (RtAlt > RapData['Altitude'][0]):

                Veast,Vnorth = get_wind(RapData,RtAlt)
                DegPerMeter = 360.0 / (2*pi * (EarthRadius + altitude))
                RtLon = RtLon + Veast  * DegPerMeter * dt / np.cos(RtLat*dtor)
                RtLat  = RtLat  + Vnorth * DegPerMeter * dt

                DescentRate = calc_descent_rate(RapData, args, RtAlt)
                RtAlt = RtAlt - DescentRate*dt

                RealTimeLon.append(RtLon)
                RealTimeLat.append(RtLat)
                RealTimeAlt.append(RtAlt)

        write_html(args,AscentLongitude,AscentLatitude,AscentAltitude,
                   DescentLongitude,DescentLatitude,DescentAltitude,
                   AscentTimeSave,DescentTime,
                   AscentRateSave,DescentRateSave,
                   FinalLongitudes,FinalLatitudes,
                   PeakAltitude,DifferenceInPeakAltitude, url, 
                   TotalDistance, images,
                   RealTimeLon, RealTimeLat,
                   StationLon, StationLat)
