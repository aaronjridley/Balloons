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
    alt       = -1.0/0.3048

    verbose = 0
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
            
        m = re.match(r'-verbose',arg)
        if m:
            verbose = 1

        m = re.match(r'-verbose=(.*)',arg)
        if m:
            verbose = int(m.group(1))

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
        print("            -verbose  (turn print statements on)")
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

    args = {'balloon': balloon, 
            'payload': payload,
            'verbose': verbose,
            'helium': helium,
            'descent': IsDescent,
            'altitude': alt * 0.3048,
            'latitude': lat,
            'longitude': lon,
            'parachute': parachute,
            'area': area,
            'errors': errors,
            'nEnsembles': nEnsembles,
            'year': Year,
            'month': Month,
            'day': Day,
            'hour': Hour,
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

def set_args(
        payload = -1.0,
        balloon = -1.0,
        parachute = -1.0,
        helium = -1.0,
        lat = -91.0,
        lon = -361.0,
        alt = -1.0,
        verbose = 0,
        nEnsembles = -1,
        errors = 0.2,
        callsign = 'abcdef',
        BurstTime = 7.0*24.0*60.0*60.0,
        hover = 50000.0,
        IsZeroPressure = 0,
        BalloonR = 0.0,
        BalloonV = 0.0,
        UseAprs = 0,
        IsDescent = 0,
        loss = 0.0,
        update = 0,
        year = -1,
        month = -1,
        day = -1,
        hour = -1):
    
    CurrentTime = 0.0

    CurrentYear  = int(time.strftime("%Y"))
    CurrentMonth = int(time.strftime("%m"))
    CurrentDay   = int(time.strftime("%d"))
    CurrentHour  = int(time.strftime("%H"))

    date = datetime.datetime.now()
    sTimeNow = date.strftime('%Y%m%d_%H%M%S')

    htmlfile = 'balloon_'+sTimeNow+'.html'
    kmlfile  = 'balloon_'+sTimeNow+'.kml'
    csvfile  = 'balloon_'+sTimeNow+'.csv'

    if (balloon < 0):
        print("Need to set balloon size!!!")
        print("            -balloon=mass of the balloon, acceptable values:")
        print("                     200, 300, 350, 450, 500, 600, 700, 800,")
        print("                     1000, 1200, 1500, 2000, 3000")
        print("                     for a zero pressure balloon, put the ")
        print("                     real mass of the balloon in grams.")

    if payload < 0:
        print("Need to set payload=")
        balloon = -1

    if parachute < 0:
        print("Need to set parachute diameter (around 5-6 feet)")
        balloon = -1
    else:
        parachuteM = parachute * FtToMeters / 2

    if helium < 0:
        print("Need to set number of helium tanks (typically 1-2)")
        balloon = -1

    if lat < -90:
        print("Need to set lat")
        balloon = -1

    if lon < -360:
        print("Need to set longitude (west longitude is negative)")
        balloon = -1
        
    if ((year < 0) or
        (month < 0) or
        (day < 0) or
        (hour < 0)):
        print("Need to set year, month, day, and hour!")
        print("Setting them to current year, month, day, hour!!!")
        year  = int(time.strftime("%Y"))
        month = int(time.strftime("%m"))
        day   = int(time.strftime("%d"))
        hour  = int(time.strftime("%H"))
    LaunchTime = datetime.datetime(year,month,day,hour,0,0)
        
    area = 2*pi*(parachuteM * ParachuteFudge)**2
        
    args = {'balloon':balloon, 
            'payload':payload * LbsToKgs,
            'verbose':verbose,
            'helium':helium,
            'descent':IsDescent,
            'altitude': alt * 0.3048,
            'latitude':lat,
            'longitude':lon,
            'parachute':parachuteM,
            'area':area,
            'errors':errors,
            'nEnsembles':nEnsembles,
            'year':year,
            'month':month,
            'day':day,
            'hour':hour,
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

def get_station(longitude, latitude, args):

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

    fpin.close()

    DistSave = MinDist

    if (MinDist > 500):

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

        fpin.close()

    stat = StatSave
    date = datetime.datetime.now()
    sDateHour = date.strftime('%Y.%m.%d.%H')

    if (MinDist == DistSave):
        url = 'https://meteor.geol.iastate.edu/~ckarsten/bufkit/data/nam/nam_'+stat+'.buf'
    else:
        url = 'ftp://ftp.meteo.psu.edu/pub/bufkit/GFS/latest/gfs3_'+stat+'.buf'
        IsNam = 0

    outfile = stat+'.'+sDateHour+'.txt'

    if (not os.path.isfile(outfile)):
        command = '/opt/local/bin/curl -o '+outfile+' '+url+' >& .log.curl'
        if (args["verbose"] > 0):
            print(command)
        os.system(command)

    return (outfile, url, IsNam, SaveLat, SaveLon)

#-----------------------------------------------------------------------------
# Read RAP file
#-----------------------------------------------------------------------------

def read_rap(file, args, IsNam):

    if (args["verbose"] > 2):
        print(" -> Reading RAP file")
    
    if (IsNam):
        SearchString = 'CFRL HGHT'
    else:
        SearchString = 'HGHT'
        Hour = args['hour']
        Hour = int(Hour/3)*3
        args['hour'] = Hour
        if (args["verbose"] > 2):
            print("  --> modifying hour to be : "+str(args['hour']))
        
    fpin = open(file,'r')

    pressure = []
    altitude = []
    direction = []
    speed = []
    temperature = []

    IsDone = 0;
    nTimesInFile = 0
    firstTime = 0
    lastTime = 0
    requestedTime = datetime.datetime(args['year'], args['month'], args['day'], args['hour'], 0, 0)
    
    while (IsDone == 0):

        line = fpin.readline()

        if (not line):
            IsDone = 2
        else:

            m = re.search(r"TIME = (\d\d)(\d\d)(\d\d)/(\d\d)(\d\d)",line)
            if m:
                if (args["verbose"] > 2):
                    print('  --> time read : ',m.group(1),m.group(2),m.group(3),m.group(4))
                h = int(m.group(4))
                d = int(m.group(3))
                y = int(m.group(1)) + 2000
                m = int(m.group(2))
                if (nTimesInFile == 0):
                    firstTime = datetime.datetime(y, m, d, h, 0, 0)
                nTimesInFile += 1
                # This will update every time, and catch the last time
                lastTime = datetime.datetime(y, m, d, h, 0, 0)
                if (args["verbose"] > 2):
                    print('  --> searching... : ',args['year'],args['month'],args['day'],args['hour'])
                if (y == args['year'] and m == args['month'] and d == args['day'] and h == args['hour']):
                    IsDone = 1
            
    #print('done reading time!')

    if (IsDone == 1):
        IsDone = 0
    else:
        fpin.seek(0,0)
        IsDone = 0
        if ((requestedTime - lastTime).total_seconds() > 0.0):
            # switch to using last time in file
            print("  --> Could not file requested time - using last time in RAP file!!")
            print("      Requested Time : ", requestedTime)
            print("      last Time : ", lastTime)
            iTime = 0
            while (IsDone == 0):
                line = fpin.readline()
                if (not line):
                    IsDone = 2
                else:
                    m = re.search(r"TIME = (\d\d)(\d\d)(\d\d)/(\d\d)(\d\d)",line)
                    if m:
                        # Found a time line
                        if (iTime >= nTimesInFile - 1):
                            IsDone = 1
                        iTime += 1
            IsDone = 0
        else:
            print(" -> Could not find requested time! Just using first time in file!")
            
    while (IsDone == 0):

        line = fpin.readline()
        m = re.search(r"SLAT = (.*) SLON = (.*) SELV = (.*)",line)
        if m:
            lat = m.group(1)
            lon = m.group(2)
            alt = m.group(3)
            if (args["verbose"] > 1):
                print('  --> found lat, lon, alt : ', lat, lon, alt)

        m = re.search(SearchString,line)
        if m:
            # Read in all of the height data:
            # read first line
            line = fpin.readline()
            while ((len(line) > 40) and (IsDone == 0)):
                line = line.strip()
                column = line.split()
                if (column[0] == 'STN'):
                    IsDone = 1
                else:
                    pressure.append(float(column[0]))
                    temperature.append(float(column[1]))
                    direction.append(float(column[5]))
                    speed.append(float(column[6])*KnotsToMps)
                    #read second line
                    line = fpin.readline()
                    line = line.strip()
                    column = line.split()
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

    data = {'Altitude':altitude,
            'Pressure':pressure,
            'Temperature':temperature,
            'Veast':ve,
            'Vnorth':vn,
            'file': file}
            
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

    return (AscentRate, Diameter)

#-----------------------------------------------------------------------------
# 
#-----------------------------------------------------------------------------

def calc_descent_rate(RapData, altitude, payload, area):

    Gravity = SurfaceGravity * (EarthRadius/(EarthRadius + altitude))**2

    Temperature, Pressure = get_temperature_and_pressure(altitude, RapData)
    MassDensity = MassOfAir * Pressure / (Boltzmann * Temperature)

    DescentRate = np.sqrt(2 * payload * Gravity / (MassDensity * ParachuteDragCoefficient * area));

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
    speed = np.sqrt(vn * vn + ve * ve)
    return (ve, vn, speed)


#-----------------------------------------------------------------------------
# 
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# 
#-----------------------------------------------------------------------------

def write_html(args, ascentData, descentData,
               ensembleData, images):

    fpout = open(args['htmlfile'],'w')
    kmlout = open(args['kmlfile'],'w')
    csvout = open(args['csvfile'],'w')
    
    burstlat = descentData['lat'][0]
    burstlon = descentData['lon'][0]

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
    fpout.write("        var pinImageR = new google.maps.MarkerImage('http://labs.google.com/ridefinder/images/mm_20_red.png');\n");
    fpout.write("        var pinImageG = new google.maps.MarkerImage('http://labs.google.com/ridefinder/images/mm_20_green.png');\n");
    fpout.write("        var pinImageB = new google.maps.MarkerImage('http://labs.google.com/ridefinder/images/mm_20_black.png');\n");
    fpout.write("        var pinImageY = new google.maps.MarkerImage('http://labs.google.com/ridefinder/images/mm_20_yellow.png');\n");
    fpout.write("        var pinImageBl = new google.maps.MarkerImage('http://labs.google.com/ridefinder/images/mm_20_white.png');\n");
    fpout.write("        var pinImagePi = new google.maps.MarkerImage('http://labs.google.com/ridefinder/images/mm_20_purple.png');\n");
    fpout.write("        var pinImageCy = new google.maps.MarkerImage('http://labs.google.com/ridefinder/images/mm_20_blue.png');\n");
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
    lat = ascentData['lat'][0]
    lon = ascentData['lon'][0]
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
    for alt in ascentData['alt']:
        if i > 0:
            alt0 = int((ascentData['alt'][i-1]/FtToMeters)/10000)
            alt1 = int((alt/FtToMeters)/10000)
            if (alt1 != alt0):
                lat = ascentData['lat'][i]
                lon = ascentData['lon'][i]
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
    for alt in descentData['alt']:
        if i > 0:
            alt0 = int((descentData['alt'][i-1]/FtToMeters)/10000)
            alt1 = int((alt/FtToMeters)/10000)
            if (alt1 != alt0):
                lat = descentData['lat'][i]
                lon = descentData['lon'][i]
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
    lat = descentData['lat'][0]
    lon = descentData['lon'][0]
    fpout.write("        var marker = new google.maps.Marker({\n")
    fpout.write("           position: new google.maps.LatLng("+str(lat)+","+str(lon)+"),\n")
    fpout.write("           icon: pinImageB,\n")
    fpout.write("           map: map\n")
    fpout.write("        });\n")
    fpout.write("\n")

    #-------------------------------------------------------------
    # Landing Site
    #-------------------------------------------------------------
    lat = descentData['lat'][-1]
    lon = descentData['lon'][-1]
    fpout.write("        var marker = new google.maps.Marker({\n")
    fpout.write("           position: new google.maps.LatLng("+str(lat)+","+str(lon)+"),\n")
    fpout.write("           icon: pinImageY,\n")
    fpout.write("           map: map\n")
    fpout.write("        });\n")
    fpout.write("\n")

    LandingLat = lat
    LandingLon = lon

    ##-------------------------------------------------------------
    ## Current RealTime Location
    ##-------------------------------------------------------------
    #if (len(RealTimeLat) > 1):
    #    lat = RealTimeLat[0]
    #    lon = RealTimeLon[0]
    #    fpout.write("        var marker = new google.maps.Marker({\n")
    #    fpout.write("           position: new google.maps.LatLng("+str(lat)+","+str(lon)+"),\n")
    #    fpout.write("           icon: pinImageG,\n")
    #    fpout.write("           map: map\n")
    #    fpout.write("        });\n")
    #    fpout.write("\n")

    #-------------------------------------------------------------
    # Ascent
    #-------------------------------------------------------------
    fpout.write("var AscentCoordinates = [\n")
    i = 0
    t = 0.0
    for lat in ascentData['lat']:
        lon = ascentData['lon'][i]
        alt = ascentData['alt'][i]
        t = t + dt
        time = args['launchtime']+datetime.timedelta(seconds=ascentData['time'][i])
        timeS = time.strftime('%Y-%m-%dT%H:%M:%SZ')
        kmlout.write(str(lon)+","+str(lat)+","+str(alt)+"\n")
        csvout.write(timeS+","+str(t)+","+str(lon)+","+str(lat)+","+str(alt)+"\n")
        fpout.write("  new google.maps.LatLng("+str(lat)+","+str(lon)+"),\n")
        i=i+1
    fpout.write("      ];\n")
    fpout.write("\n")
    fpout.write("      var flightPathAscent = new google.maps.Polyline({\n")
    fpout.write("        path: AscentCoordinates,\n")
    fpout.write("        strokeColor: \"#FF0000\",\n")
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
    for lat in descentData['lat']:
        t = t + dt
        lon = descentData['lon'][i]
        alt = descentData['alt'][i]
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
    fpout.write("        strokeColor: \"#0000FF\",\n")
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
    for lat in ascentData['StatLat']:
        lon = ascentData['StatLon'][i]
        if (args["verbose"] > 2):
            print("  --> Weather Station lan and lon: ", lat,lon)
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
    for lat in ensembleData['lat']:
        lon = ensembleData['lon'][i]
        fpout.write("        var marker = new google.maps.Marker({\n")
        fpout.write("           position: new google.maps.LatLng("+str(lat)+","+str(lon)+"),\n")
        fpout.write("           icon: pinImageG,\n")
        fpout.write("           map: map\n")
        fpout.write("        });\n")
        fpout.write("\n")
        i=i+1

    ##-------------------------------------------------------------
    ## RealTime
    ##-------------------------------------------------------------
    #if (len(RealTimeLat) > 1):
    #    fpout.write("var RealTimeCoordinates = [\n")
    #    i = 0
    #    for lat in RealTimeLat:
    #        lon = RealTimeLon[i]
    #        fpout.write("  new google.maps.LatLng("+str(lat)+","+str(lon)+"),\n")
    #        i=i+1
    #    fpout.write("      ];\n")
    #    fpout.write("\n")
    #    fpout.write("      var flightPathRealTime = new google.maps.Polyline({\n")
    #    fpout.write("        path: RealTimeCoordinates,\n")
    #    fpout.write("        strokeColor: \"#000000\",\n")
    #    fpout.write("        strokeOpacity: 1.0,\n")
    #    fpout.write("        strokeWeight: 3\n")
    #    fpout.write("      });\n")
    #    fpout.write("\n")
    #    fpout.write("      flightPathRealTime.setMap(map);\n")
    #    fpout.write(" \n")

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
    fpout.write("    Black Pin indicates burst<br>\n")
    fpout.write("    Blue Pins indicate every 10,000 ft on descent (roughly 3 km)<br>\n")
    fpout.write("    Yellow Pin indicates landing<br>\n")
    fpout.write("    Green Pins indicates landing scatter (with ensembles)<br>\n")
    fpout.write("    White Pin indicates weather stations<br>\n")
    fpout.write("    <b>Output Parameters:</b><br>\n")

    PeakAltitude = ascentData['alt'][-1]
    FinalAltitudes = ensembleData['alt']
    nEnsembles = len(FinalAltitudes)
    if (nEnsembles > 2):
        diff = np.array(FinalAltitudes) - PeakAltitude
        diff = np.sqrt(np.sum(diff * diff) / nEnsembles)
    else:
        diff = 0
    fpout.write("    Peak Altitude : "+str(round(PeakAltitude))+"+/-"+str(round(diff))+' m ('+
                str(round(PeakAltitude/FtToMeters))+"+/-"+str(round(diff/FtToMeters))+' ft)<br>')
    
    ascentRate = (ascentData['alt'][-1] - ascentData['alt'][0]) / \
        (ascentData['time'][-1] - ascentData['time'][0])
    dummy = np.round(ascentRate*100.0)/100.0
    dummy2 = np.round(ascentRate/FtToMeters*60.0*100.0)/100.0
    fpout.write("    Ascent Rate   : "+str(dummy)+" m/s ("+str(dummy2)+" fpm)<br>\n")
    fpout.write("    Ascent Time  : "+str(np.round(ascentData['time'][-1]/60.0))+" minutes<br>\n")

    descentRate = (descentData['alt'][0] - descentData['alt'][-1]) / \
        (descentData['time'][-1] - descentData['time'][0])
    
    dummy = np.round(descentRate*100.0)/100.0
    fpout.write("    Descent Rate  : "+str(dummy)+" m/s<br>\n")
    fpout.write("    Descent Time : "+str(np.round(descentData['time'][-1]/60.0))+" minutes<br>\n")
    fpout.write("    Total Time : "+str(np.round((ascentData['time'][-1] + descentData['time'][-1])/60.0))+" minutes<br>\n")

    # convert meters to miles:
    TotalDistance = (ascentData['distance'] + descentData['distance'])/1609.34
    fpout.write("    Total Distance Traveled : "+str(np.round(TotalDistance))+" Miles<br>\n")
    fpout.write("    Distance Between Launch and Landing : "+str(np.round(distance))+" Miles<br>\n")

    fpout.write("    <b>Input Parameters:</b><br>\n")
    fpout.write("    Starting Latitude : "+str(ascentData['lat'][0])+"<br>\n")
    fpout.write("    Starting Longitude : "+str(ascentData['lon'][0])+"<br>\n")
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
# copy dictionary
#-----------------------------------------------------------------------------

def copy_dictionary(inDict):
    outDict = {}
    for key in inDict:
        outDict[key] = inDict[key]
    return outDict

#-----------------------------------------------------------------------------
# Want to get the altitude profile of the atmosphere close to the
# latitude and longitude of the balloon
# -----------------------------------------------------------------------------

def get_weather_data(longitude, latitude, args, OldData = []):

    filename, url, IsNam, StatLat, StatLon = get_station(longitude, latitude, args)
    if (len(OldData) == 0):
        RapData = read_rap(filename, args, IsNam)
        RapData['StatLat'] = [StatLat]
        RapData['StatLon'] = [StatLon]
        RapData['Updated'] = True
    else:
        if (OldData['file'] == filename):
            RapData = copy_dictionary(OldData)
            RapData['Updated'] = False
        else:
            RapData = read_rap(filename, args, IsNam)
            RapData['StatLat'] = OldData['StatLat']
            RapData['StatLat'].append(StatLat)
            RapData['StatLon'] = OldData['StatLon']
            RapData['StatLon'].append(StatLon)
            RapData['Updated'] = True            

    return RapData
    
#-----------------------------------------------------------------------------
# Convert Veast and Vnorth (m/s) to deg/s and calc dlat and dlon
#-----------------------------------------------------------------------------

def convert_mps_to_dlon_dlat(Veast, Vnorth, alt, lat, dt):
    DegPerMeter = 360.0 / (2*pi * (EarthRadius + alt))
    dLon = Veast * DegPerMeter / np.cos(lat*dtor) * dt
    dLat = Vnorth * DegPerMeter * dt
    distance = np.sqrt(dLon * dLon + dLat * dLat) / DegPerMeter
    return dLon, dLat, distance
    
#-----------------------------------------------------------------------------
# Calculate ascent from starting altitude to burst altitude
#   errors needs to be a percentage (ratio 0-1) for amount of
#      normalized uncertainty for helium, burst diameter, bursttime, speed 
#-----------------------------------------------------------------------------

def calc_ascent(longitude, latitude, altitude, args, errors = 0):

    if (args['verbose'] > 0):
        print(' -> Starting Ascent Calculation')
        print('  --> Starting at Altitude : ', altitude, ' m')
    
    # allow perturbations in the drivers to put some uncertainty in
    # the results:
    
    NumberOfHelium = calculate_helium(args['helium'])
    BurstDiameter = KaymontBalloonBurst(args['balloon'])
    
    NumberOfHelium = random.normalvariate(NumberOfHelium, NumberOfHelium * errors/4)
    BurstDiameter = random.normalvariate(BurstDiameter, BurstDiameter * errors/4)
    bursttime = random.normalvariate(args['bursttime'], args['bursttime'] * errors/4)

    RapData = get_weather_data(longitude, latitude, args)

    TotalDistance = 0.0

    AscentTime = [0.0]
    AscentLongitude = [longitude]
    AscentLatitude  = [latitude]
    AscentAltitude  = [altitude]
    Veast, Vnorth, speed = get_wind(RapData, altitude)
    WindSpeed = [speed]

    Diameter = 0.0
    while (Diameter < BurstDiameter and altitude > -1.0):

        if (args['update'] == 1):
            RapData = get_weather_data(longitude, latitude, args, RapData)
            
        NumberOfHelium = NumberOfHelium * (1.0-args['loss']/100.0/60.0*dt)

        Veast, Vnorth, speed = get_wind(RapData, altitude)
        AscentRate, Diameter = calc_ascent_rate(RapData, NumberOfHelium, args, altitude)

        Veast  = random.normalvariate(Veast, speed * errors)
        Vnorth = random.normalvariate(Vnorth, speed * errors)
        dLon, dLat, distance = convert_mps_to_dlon_dlat(Veast, Vnorth, altitude, latitude, dt)
        longitude = longitude + dLon
        latitude  = latitude + dLat
        if (altitude < args['hover']):
            altitude = altitude + AscentRate*dt

        TotalDistance += distance

        AscentLongitude.append(longitude)
        AscentLatitude.append(latitude)
        AscentAltitude.append(altitude)
        WindSpeed.append(speed)

        AscentTime.append(AscentTime[-1] + dt)

        if (AscentTime[-1] > bursttime):
            print('Burst Time Triggered!')
            Diameter = BurstDiameter*2

        if (args['descent'] == 1):
            print('Descent Only Triggered!')
            Diameter = BurstDiameter * 2

    # Pack up ascent data to return
    AscentData = {
        "lon" : AscentLongitude,
        "lat" : AscentLatitude,
        "alt" : AscentAltitude,
        "speed" : WindSpeed,
        "time" : np.array(AscentTime),
        "distance" : TotalDistance,
        "StatLat": RapData["StatLat"],
        "StatLon": RapData["StatLon"]}
    return AscentData

#-----------------------------------------------------------------------------
# Calculate descent from starting altitude to ground
#-----------------------------------------------------------------------------

def calc_descent(longitude, latitude, altitude, args, errors = 0):

    if (args['verbose'] > 0):
        print(' -> Starting Descent Calculation')
        print('  --> Starting at Altitude : ', altitude, ' m')
    
    payload = random.normalvariate(args['payload'], args['payload'] * errors/10.0)
    area = random.normalvariate(args['area'], args['area'] * errors)
    
    DescentTime = [0.0]
    DescentLongitude = [longitude]
    DescentLatitude = [latitude]
    DescentAltitude = [altitude]
                        
    RapData = get_weather_data(longitude, latitude, args)
    Veast, Vnorth, speed = get_wind(RapData, altitude)
    WindSpeed = [speed]
    TotalDistance = 0.0
    
    if (altitude < 0.0):
        altitude = RapData['Altitude'][0] + 1.0

    while (altitude > RapData['Altitude'][0]):

        Veast, Vnorth, speed = get_wind(RapData, altitude)
        Veast  = random.normalvariate(Veast, speed * errors)
        Vnorth = random.normalvariate(Vnorth, speed * errors)
        dLon, dLat, distance = convert_mps_to_dlon_dlat(Veast, Vnorth, altitude, latitude, dt)
        longitude = longitude + dLon
        latitude  = latitude + dLat

        WindSpeed.append(speed)
        TotalDistance += distance

        DescentRate = calc_descent_rate(RapData, altitude, payload, area)
        altitude = altitude - DescentRate*dt

        DescentLongitude.append(longitude)
        DescentLatitude.append(latitude)
        DescentAltitude.append(altitude)

        DescentTime.append(DescentTime[-1] + dt)

    # Pack up ascent data to return
    DescentData = {
        "lon" : DescentLongitude,
        "lat" : DescentLatitude,
        "alt" : DescentAltitude,
        "speed" : WindSpeed,
        "time" : np.array(DescentTime),
        "distance" : TotalDistance,
        "StatLat": RapData["StatLat"],
        "StatLon": RapData["StatLon"]}

    return DescentData

#-----------------------------------------------------------------------------
# Calculate whole flight
#-----------------------------------------------------------------------------

def calc_whole_flight(args, errors = 0):

    if (args['verbose'] > 0):
        print('Starting Whole Flight Calculation')
    
    longitude = args['longitude']
    latitude = args['latitude']
    RapData = get_weather_data(longitude, latitude, args)

    Diameter = 0.0
    AscentTime = 1.0

    if (args['altitude'] < 0.0):
        altitude = RapData['Altitude'][0]
    else:
        altitude = args['altitude']


    ascentData = calc_ascent(longitude, latitude, altitude, args, errors)
    longitude = ascentData['lon'][-1]
    latitude = ascentData['lat'][-1]
    altitude = ascentData['alt'][-1]
    descentData = calc_descent(longitude, latitude, altitude, args, errors)
    
    return ascentData, descentData

#-----------------------------------------------------------------------------
# Run ensembles
#-----------------------------------------------------------------------------

def run_ensembles(args):
        
    nEnsembles = args['nEnsembles']
    errors = args['errors']
    FinalLongitudes = []
    FinalLatitudes  = []
    FinalAltitudes  = []

    DifferenceInPeakAltitude = 0.0

    i = 0
    while (i < nEnsembles):
        if (args['verbose'] > 0):
            print('Starting Ensemble Member #', i)
        ascentDataP, descentDataP = calc_whole_flight(args, errors)
        FinalLongitudes.append(descentDataP['lon'][-1])
        FinalLatitudes.append(descentDataP['lat'][-1])
        FinalAltitudes.append(descentDataP['alt'][-1])
        i = i + 1
            
    ensembleData = {
        'lon': FinalLongitudes,
        'alt': FinalAltitudes,
        'lat': FinalLatitudes}

    return ensembleData

#-----------------------------------------------------------------------------
# Summary of the run
#-----------------------------------------------------------------------------

def report_summary(ascentData, descentData, verbose):
    
    AscentAltitude  = ascentData['alt']
    AscentTime = ascentData['time']
    TotalDistance = ascentData['distance']
        
    PeakAltitude = ascentData['alt'][-1]
    AscentRate = (AscentAltitude[-1] - AscentAltitude[0]) / AscentTime[-1]
        
    if (verbose > 0):
        print(' -> Summaries: ')
        print('  --> Final Peak Altitude :', PeakAltitude, ' m')
        print('  --> Ascent Time :', AscentTime[-1]/60.0, ' minutes')
        print('  --> Average Ascent Rate :', AscentRate, ' m/s')

    DescentAltitude  = descentData['alt']
    DescentTime = descentData['time'] + ascentData['time'][-1]
    DescentRate = (DescentAltitude[0] - descentData['alt'][-1]) / (DescentTime[-1] - DescentTime[0])
    TotalDistance = TotalDistance + descentData['distance']
        
    if (verbose > 0):
        print('  --> Final Descent Altitude :', DescentAltitude[-1], ' m')
        print('  --> Descent Time :', (DescentTime[-1] - DescentTime[0]) / 60.0, ' minutes')
        print('  --> Total Flight Time :', DescentTime[-1] / 60.0,' minutes')
        print('  --> Descent Rate :', DescentRate, ' m/s')

    return

#-----------------------------------------------------------------------------
# Make plots for the run
#-----------------------------------------------------------------------------

def make_plots(ascentData, descentData, args):

    AscentAltitude  = ascentData['alt']
    DescentAltitude  = descentData['alt']
    AscentTime = ascentData['time']
    DescentTime = descentData['time'] + ascentData['time'][-1]
    
    Altitudes = np.concatenate((AscentAltitude, DescentAltitude))
    TotalTime = np.concatenate((AscentTime, DescentTime))
    WindSpeed = np.concatenate((ascentData['speed'], descentData['speed']))
        
    images = []
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
    
    return images
    
