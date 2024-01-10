
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

The payload components you are responsible for designing, building,
testing, and launching are: stand-alone Flight Termination Unit (FTU),
a radio tracker (e.g., Trackuino), and main science payload with
sensors.

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

## Flight Termination Unit Requirements

1. The FTU will be launched in its own structure, mounted below
    the balloon, but above the parachute on the payload train.

2. The working FTU must include a timer, a battery pack, and whatever
    circuitry you need to initiated a timed burn of the nichrome wire
    (or other technique) to cut down the package.  The FTU could also
    be extremely sophisticated with a radio (e.g., X-Bee) connected to
    the main science payload that can trigger the flight
    termination. This could be triggered due to going outside of a
    given lat/lon box, ascent rate too slow, etc.
	
3. Power must be controlled by a remove before flight pin or a
    switch so it can be initiated without opening the package at the
    launch site and remain on during the flight with no chance of it
    accidentally being turned off.
    
4. The battery should be sized to provide at least 2.0 hours of
    power for the system, and be able to provide power to operate the
    termination mechanism, but should not be too over-powered due to
    weight.
    
5. Connection points to the payload train must be included in the
    design, so that {\bf the package does not need to be opened at the
      launch site.}
      
6. The FTU needs to be robust against line stress, since the
    nichrome is easy to dislodge and/or break.
    
7. FTU must weigh less than 0.5 lbs.
  

## Camera System

Specifications on the camera system:

1. Need at least two cameras pointing in orthogonal directions (e.g.,
horizon and up towards balloon).

2. Need to take video or high-quality images.

3. Must be less than 1 pound.

4. Must operate for at least 2 hours at external temperatures of -60C.

5. It is desired that the camera system be contained in one box,
preferably with a method for turning the system on without having to
open the box.

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

- [Lab 4: Flight Termination Unit](Labs/lab04.md)


\subsection{Lab 6: PCB design}

{\bf Due by: Thursday before Spring Break}

\noindent
{\bf Requirements:}

\begin{itemize}
    \item Develop PCB board layout for the main payload, Trackuino,
      and the FTU.
    \item The payload PCB should incorporate the sensors, the data
      logger, the micro-controller, the X-Bee (if used), the payload
      and any supporting circuitry.
    \item Nothing that costs more than \$20 should be soldered to the
      PCB - headers should be mounted to the PCB and the components
      should be put into the headers.
    \item Lab should show pictures of the completed circuit board with
      data showing that everything works ok on it.
    \item All files needed to order PCBs must be reviewed by at least
      2 other teams and delivered before class on the Thursday before
      spring break.
    \begin{itemize}
        \item All independent boards should be combined into a single
          PCB in order to minimize cost.
    \end{itemize}
\end{itemize}

\subsection{Interface Control Document}

{\bf Due by: March 17th}

\noindent
{\bf Requirements:}

\begin{itemize}
    \item Work with 3-4 ENGR100 teams to design interfaces between
      their ride-share payloads and the payload train.
    \item These teams will be given requirements with options and they
      will write you a memo describing how they will be attaching to
      the train and how they will meet the requirements.
    \item You will verify that the design meets the requirement and
      modify if you need to, creating a formal interface control
      document.
    \item On the Wednesday/Thursday before launch, you should meet
      with the ENGR 100 teams to verify that they have complied with
      the ICD.
\end{itemize}

\subsection{Lab 7:  Tracking Test Results}

{\bf Due by: Flight Readiness Review}

\noindent
{\bf Requirements:}

\begin{itemize}
  \item At least two team members must be licensed Ham radio
    technicians.
  \item Demonstrate ability to set up ground station and attach it
      to your car. Verify that at least two members of your group
      understand the procedure to set up and work ground station.
    \item Demonstrate MBuRST provided Micro-track working with ground
      stations, broadcasting to APRS (using wifi or cell from the
      ground station laptop).
    \item Demonstrate your tracker communicating with the ground
      station by including a number of packets transmitted to it from
      screenshot on APRS.
    \item Lab write-up should include screenshots from aprs.fi that
      show that the Micro-track and tracker are broadcasting the
      correct call sign and that the ground station is working for at
      least 30 minutes while moving around in line of sight of
      receiver.
\end{itemize}

\subsection{Lab 8:  Camera endurance and cold test}

{\bf Due by: Flight Readiness Review}

\noindent
{\bf Requirements:}

\begin{itemize}
    \item Camera working and verified to work at $-40^\circ$
    \item Measure battery lifetime prior to cold test, during cold
      test, after cold test, report on performance.
    \item The lab should show that the camera can work for at least 60
      minutes at $-40^\circ$.
\end{itemize}

\subsection{Lab 9:  System Testing}

{\bf Due by: Flight Readiness Review}

\noindent
{\bf Requirements:}

\begin{itemize}
    \item An end-to-end test needs to be completed on the complete
      system, including cold testing ($-40^\circ$C for at least 2
      hour) and endurance testing (operating for at least 3 hours).
    \item 20 ft drop and kick test and fix anything that didn’t hold
      up.
    \item A car chase needs to be completed with results that show
      that the complete system worked flawlessly during the entire
      chase (this includes the ground station and all of the sensors).
    \item Video demonstration of the FTU test.
    \item You will not be allowed to launch until the tests are completed.
    \item Tests {\bf must be completed at least 24 hours before
      launch}, so they can be reviewed.
    \item A spreadsheet providing information on masses of packages
      must be provided.
    \item Launch day predictions with launch and landind sites must be
      provided.
\end{itemize}

\subsection{Lab 10: Final Report}

{\bf Due by: day/time of final exam}

\noindent
{\bf Final report should contain the following:}

\begin{itemize}
    \item A terse summary of the system design
    \item A summary of launch day activities
\begin{itemize}
        \item What worked and what did not?
\end{itemize}
    \item Map of balloon trajectory including google map and altitude profile
    \item Plots of the data recovered and analysis of results
    \item Video/images should be provided in a shared google drive
\end{itemize}



\end{document}
