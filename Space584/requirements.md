
# Project Specifications and Requirements

## Overview

The goal of our project is to take measurements with sensors of
atmospheric pressure, temperature, humidity and wind speed from the
ground to 100,000 ft. (30 km) as well as take video and pictures of the
atmosphere and ground from altitude. Teams will integrated a number of
sensors with a microcontroller, log data obtained onboard for later
analysis, and design a tracking device that transmits positional
telemetry to the ground throughout the flight.  Teams must track and
retrieve the package.  This means that the system must contain a
flight termination unit that is either triggered from the ground or
can trigger on its own.  It is mandatory that all FAA regulations be
followed in the process.  Teams also must plan for a ride share on
their payload train with Engin 100 student payloads.  Teams must plan
to integrate up to four Engin 100 payloads into their final payload
train on launch day.

## System Requirements

Each team will be responsible for creating:

1. A sensor package that records data to an SD card.

2. A camera payload.

3. Three copies of a tracker.

4. Three copies of a Primary Flight Termination Unit (FTU), micro FTU,
or a ground station.

Because we are desiring robustness and redundancy in the tracking, each team's
tracking system needs to be a different technology.  The three technologies that
we are desiring are:

1. Communication through the APRS network, using a 144.29 MHz radio.

2. Communication through a satellite communication system.

3. Communication through a low power, analog, fox-hunt system.

Each system also needs some way of cutting the balloon away from the
main payload train (Primary FTU) and the individual packages from the
payload train (micro FTUs).  One team will be responsible for the Primary
FTUs and another team will be responsible for the micro FTUs.

Each system also needs some way of getting the tracking data from the
payloads and displaying it in a way that is helpful in the balloon
chase. One team will be responsible for creating the ground stations.

## Satellite Tracker Requirements

1. The tracker must use some form of satellite communications, such as
a RockBLOCK Iridium SatComm Module.  

2. The tracker must broadcast its position approximately once every
2-5 minutes.

3. The tracker should indicate that it has GPS lock and is working
properly.  This information should be displayed in such a way that the
case does not have to be opened.

4. The satellite comm module should be fully removeable from the system, so it can be
reused (i.e., cables or headers with mother/daughter boards should be
used.)

5. The tracker should be able to operate for at least 2.5 hours at
external temperatures of -60C.  It should be able to endure severe
turbulence with no damage.

6. The tracker should be *professional* in that it should be mounted
into a nice housing, have an external switch, have exterior attachment
points, etc.  It should look and operate like a system that people
would actually want to purchase.

## Beacon Tracker Requirements

1. The tracker must operate like a micro-fox hunt system, in that it is a low power system that beacons in the 2-meter band.

2. At least two team members must be licensed to operate the
    tracker and ground station.
    
3. The beacon message must be the GPS coordinates (latitude and longitude) in some way.

4. The tracker must broadcast its position approximately once every
minute.

5. Power must be controlled by a remove before flight pin or a
    switch so it can be initiated without opening the package at the
    launch site and remain on during the flight with no chance of it
    accidentally being turned off.
    
6. The tracker should indicate that it has GPS lock and is working
properly.  This information should be displayed in such a way that the
case does not have to be opened.

7. Antennas must be protected so that they can not be ripped off during turbulence.

8. The system must broadcast its position for at least 5 hours.

## APRS Tracker Requirements

1. The tracker must broadcast its position approximately once a minute
    ($\pm 10s$) over 144.39 MHz in a format that can be decoded by the
    APRS network.
    
2. At least two team members must be licensed to operate the
    tracker and ground station.
    
3. At least two team members must be able to operate the ground
    station to receive data packets that upload properly to the APRS
    site.

4. The battery should be sized to provide at least 2.5 hours of
    power, but should not be oversized due to weight constraints.

5. Power must be controlled by a remove before flight pin or a
    switch so it can be initiated without opening the package at the
    launch site and remain on during the flight with no chance of it
    accidentally being turned off.
    
6. Headers must be used for any components that are expensive, so
    they can be recovered and reused later.

7. There should be connection points at the top and bottom of the
    payload to allow connection to the main train, with the weight of
    the packages below being supported. Conversely, the tracker could
    be connected with a single connection point at the top and hang
    off the main train. A connection point must be made available for
    a backup safety line to run through.

8. The tracker must be less than 0.75 lbs. An extra 0.25 lbs is
    available if a camera is incorporated.

9. The tracker must be able to operate after being subjected to
    extreme environments of acceleration and temperature.

10. It is critical that GPS have lock during the flight and that
    transmission (and reception) occurs during the last minutes of the
    flight.

## Main Science Payload Requirements

1. Record inside and outside temperature, pressure, humidity, and
    acceleration at least once every 10s during the flight.

2. One additional sensor of your choosing beyond the basic
    requirements must be added.  You should justify why you want to
    add this sensor and describe how it will be used.  A budget of up
    to \$50/team is allowed for this sensor.

3. Data should be recorded to an SD or Micro-SD card.

4. It would be good to record GPS position on the main science
    payload, but it is not required.
    
5. The battery should be sized to provide at least 2.5 hours of
     power, but should not be oversized due to weight constraints.

6. Power must be controlled by a remove before flight pin or a
      switch so it can be initiated without opening the package at the
      launch site and remain on during the flight with no chance of it
      accidentally being turned off.

7. Headers must be used for any components that are expensive,
      so they can be recovered and reused later.

8. There should be connection points at the top and bottom of
      the payload to allow connection to the main train, with the
      weight of the packages below being supported. Conversely, the
      main science payload could be connected with a single connection
      point at the top and hang off the main train. A connection point
      must be made available for a backup safety line to run through.

9. The main science payload must be less than 0.75 lbs. An
      extra 0.25 lbs is available if a camera is incorporated.

10. The science payload must be able to operate during and after
    being subjected to extreme environments of acceleration and
    temperature.

## Primary Flight Termination Unit Requirements

1. The FTU will be launched in its own structure, mounted below
    the balloon, but above the parachute on the payload train.

2. The working FTU must include a timer, a battery pack, a radio
    receiver, and whatever circuitry you need to initiated a timed
    burn of the nichrome wire (or other technique) to cut down the
    package.  The FTU could be triggered due to time expiring, going
    outside of a given lat/lon box, ascent rate too slow, by a ground
    signal, etc.
	
3. Power must be controlled by a remove before flight pin or a
    switch so it can be initiated without opening the package at the
    launch site and remain on during the flight with no chance of it
    accidentally being turned off.
    
4. The battery should be sized to provide at least 2.0 hours of
    power for the system, and be able to provide power to operate the
    termination mechanism, but should not be too over-powered due to
    weight.
    
5. Connection points to the payload train must be included in the
    design, so that **the package does not need to be opened at the
    launch site.**
      
6. The FTU needs to be robust against line stress, since the
    nichrome is easy to dislodge and/or break.
    
7. FTU must weigh less than 0.5 lbs.
  
## Micro Flight Termination Unit Requirements

1. The micro-FTU will be the attachment point for all payloads, so that they
   can all be cut down with a single signal from the ground.

2. The working FTU must include a battery pack, a radio receiver, and
    whatever circuitry you need to initiated a burn of the nichrome
    wire (or other technique) to cut down the package.  The micro-FTU
    should be triggered by sending an extremely simple tone signal.
	
3. Power must be controlled by an external switch so it can be
   initiated without opening the package at the launch site and remain
   on during the flight with no chance of it accidentally being turned
   off.
    
4. The battery should be sized to provide at least 2.0 hours of power
   for the system, and be able to provide power to operate the
   termination mechanism, but should not be too over-powered due to
   weight.
    
5. Connection points to the payload train must be included in the
   design, so that **the package does not need to be opened at the
   launch site.**
      
6. The micro FTU needs to be robust against line stress, since the
    nichrome is easy to dislodge and/or break.
    
7. FTU must weigh less than 0.25 lbs.
  
(It is unclear if these requirements can be met at this time....)

## Camera System

Specifications on the camera system:

1. Need at least two cameras pointing in orthogonal directions (e.g.,
horizon and up towards balloon).

2. Need to take video or high-quality images every few seconds.

3. Must be less than 1 pound, preferably less than 0.5 lbs.

4. Must operate for at least 2 hours at external temperatures of -40C.

5. It is desired that the camera system be contained in one box,
preferably with a method for turning the system on without having to
open the box.

6. The camera system and the sensor system can be combined into one
box if desired.

7. A heater system can be designed to warm the cameras if desired.

## Ground Station Requirements:

1. Needs to contain a processing system, a display system, some type
of internet connection system (e.g., cell-phone WiFi), a radio, a GPS,
and a USB battery system that can be charged in the car, but can be
run autonomously also.

2. Needs to display the locations of the balloon(s) and ground
station(s) all operating on our network.

3. etc.

## Lab Specifications

This class will have mostly lab sessions. I expect students to show up
during class times to work with their fellow teammates. We will have
weekly team meetings to make sure that the teams are keeping up with
the plan.

We will have to order things online. You should work with the teaching
staff to put in orders.  He will consolidate the orders and try to
minimize shipping. If you absolutely **HAVE** to order something on your
own (highly discouraged!!!), the parts must be shipped to the climate and space research building
here at the University or you will not be reimbursed. Pay attention to
shipping costs! We do not want to pay outrageous shipping costs for
last-minute orders!  Plan ahead!

The following list makes up the lab reports that you must complete in
order to get a grade and launch, and in those labs, there are a number
of requirements that need to be met:

- [Lab 1: Microcontroller, Sensors, and Data Logging](Labs/lab01.md)

- [Lab 2: Microcontroller + GPS](Labs/lab02.md)

- [Lab 3: Tracker](Labs/lab03.md)

- [Lab 4: Flight Termination Units](Labs/lab04.md)

- [Lab 5: Ground Stations](Labs/lab05.md)

- [Lab 6: PCB designs](Labs/lab06.md)

- [Lab 7: Interface Control Document](Labs/lab07.md)

- [Lab 8:  Tracking Test Results](Labs/lab08.md)

- [Lab 9:  Camera endurance and cold test](Labs/lab09.md)

- [Lab 10:  System Testing](Labs/lab10.md)

- [Lab 11: Final Report](Labs/lab11.md)

\end{document}
