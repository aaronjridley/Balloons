#!/opt/local/bin/python

import cgi
import re
import datetime
import pytz
import os

def textbox(label, var, value, note):
    default = ''
    if (len(value) > 0):
        default = str(value)
    print("<LABEL for=\""+label+"\">"+label+": </LABEL>")
    print("  <INPUT type=\"text\" name=\""+var+"\" value=\""+default+"\">")
    print(note+"<br>")

form = cgi.FieldStorage()

longitude = form.getfirst('longitude','')
longitude = cgi.escape(longitude)

latitude = form.getfirst('latitude','')
latitude = cgi.escape(latitude)

altitude = form.getfirst('altitude','')
altitude = cgi.escape(altitude)

descent = form.getfirst('descent','')
descent = cgi.escape(descent)

payload = form.getfirst('payload','')
payload = cgi.escape(payload)

balloon = form.getfirst('balloon','')
balloon = cgi.escape(balloon)

parachute = form.getfirst('parachute','')
parachute = cgi.escape(parachute)

helium = form.getfirst('helium','')
helium = cgi.escape(helium)

callsign = form.getfirst('callsign','')
callsign = cgi.escape(callsign)

time = form.getfirst('time','')
time = cgi.escape(time)

# This is for an FTU:

bursttime = form.getfirst('bursttime','')
bursttime = cgi.escape(bursttime)

# This is for running real-time predictions:

aprs = form.getfirst('aprs','')
aprs = cgi.escape(aprs)

# This is for a zero pressure balloon:

hover = form.getfirst('hover','')
hover = cgi.escape(hover)

zero = form.getfirst('zero','')
zero = cgi.escape(zero)

debug = form.getfirst('debug','')
debug = cgi.escape(debug)

update = form.getfirst('update','')
update = cgi.escape(update)

volume = form.getfirst('volume','')
volume = cgi.escape(volume)

currenttime = form.getfirst('currenttime','')
currenttime = cgi.escape(currenttime)

radius = form.getfirst('radius','')
radius = cgi.escape(radius)

zpmass = form.getfirst('zpmass','')
zpmass = cgi.escape(zpmass)

# This is for running an ensemble os simulations:

nensembles = form.getfirst('nensembles','')
nensembles = cgi.escape(nensembles)

error = form.getfirst('error','')
error = cgi.escape(error)

# -----------------------------------------------------------------------
# start writing HTML
# -----------------------------------------------------------------------

print("Content-type: text/html")
print("")
print("<html>")
print("<body>")
print("<h1>University of Michigan Balloon Flight Prediction Page</h1>")

print("<FORM action=\"index.py\" method=\"post\">\n")

print("<h2>The absolute basics:</h2>")

textbox("Call Sign","callsign",callsign,
        "Your callsign.  If you don't have one, enter your first name.")
textbox("Longitude","longitude",longitude,
        "(deg) West longitudes are negative!")
textbox("Latitude","latitude",latitude,
        "(deg) Should work across the world now!")
textbox("Payload","payload",payload,
        "(lbs) Total weight of everything below the balloon (1-12 lbs).")
textbox("Parachute","parachute",parachute,
        "(feet) Diameter, typically 4-6 feet.")

TanksOfHelium = [0.5,0.75,1.0,1.25,1.50,1.75,2.0,2.25,2.5,2.75,3.0,3.5,4.0,5.0]
if (len(helium) < 1):
    helium = TanksOfHelium[2]
print("<LABEL for=\"TanksOfHelium\">Tanks of Helium: </LABEL>")
print("<select name=\"helium\">")
print("  <optgroup label=\"Tanks of Helium\" name=\"helium\">")
for tanks in TanksOfHelium:
    if (float(helium) == float(tanks)):
        sel = ' selected'
    else:
        sel = ''
    print("    <option"+sel+">"+str(tanks)+"</option>")
print("  </optgroup>\n")
print("</select>\n")

print("<a href=\"https://en.wikipedia.org/wiki/Gas_cylinder\">(K-type cylinders)</a><br>")



kaymontMass = [200, 300, 350, 450, 500, 
               600, 700, 800, 1000, 1200, 
               1500, 2000, 3000]
if (len(balloon) < 1):
    balloon = kaymontMass[8]
print("<LABEL for=\"Balloon Mass\">Balloon Mass: </LABEL>")
print("<select name=\"balloon\">")
print("  <optgroup label=\"Balloon Mass\" name=\"balloon\">")
for mass in kaymontMass:
    if (int(balloon) == int(mass)):
        sel = ' selected'
    else:
        sel = ''
    print("    <option"+sel+">"+str(mass)+"</option>")
print("  </optgroup>\n")
print("</select><br>\n")

i = 0
dates = []
for i in range(72):
    d = datetime.datetime.now(pytz.utc) + datetime.timedelta(hours=i)
    ds = d.strftime("%Y-%m-%d %H")
    dates.append(ds+' UTC')
if (len(time) < 1):
    time = dates[1]
print("<LABEL for=\"Time to Launch\">Time To Launch: </LABEL>")
print("<select name=\"time\">")
print("  <optgroup label=\"Time To Launch\" name=\"time\">")
for date in dates:
    m = re.match(time,date)
    if m:
        sel = ' selected'
    else:
        sel = ''
    print("    <option"+sel+">"+date+"</option>")
print("  </optgroup>\n")
print("</select><p>\n")

m = re.match('(\d\d\d\d)-(\d\d)-(\d\d) (\d\d)',time)
if m:
    yyyy = m.group(1)
    mm   = m.group(2)
    dd   = m.group(3)
    hh   = m.group(4)

print("<h2>These items below are optional, so don't fill them out unless you know what you are doing!</h2>")

print("This is for use when you want the code to update the weather model location dynamically:<br>")
updatechecked = ""
if (update == "1"):
    updatechecked = " checked"
print("<input type=\"checkbox\" name=\"update\" value=\"1\"")
print(updatechecked)
print(">Update the weather station location dynamically (can be slow!)<p>")


textbox("Altitude","altitude",altitude,
        "(feet!!!) Don't really need this unless trying to find a balloon from a last heard from position!")

checked = ""
if (descent == "1"):
    checked = " checked"
print("<input type=\"checkbox\" name=\"descent\" value=\"1\"")
print(checked)
print(">Only compute descent from initial altitude.<p>")



print("This is for use with a flight termination unit:<br>")

textbox("Burst Time Delay","bursttime",bursttime,
        "(minutes) Time after launch in which Flight Termination Unit will be initiated.")

textbox("Current Time of Flight","currenttime",currenttime,
        "(minutes) Current time after launch.")

print("If you want to run an ensemble to see a cluster of prediction points:<br>")

nEnsembles = [1, 5, 10, 25, 50, 100, 200]
if (len(nensembles) < 1):
    nensembles = nEnsembles[0]
print("<LABEL for=\"Number of Ensembles\">Number of Ensembles: </LABEL>")
print("<select name=\"nensembles\">")
print("  <optgroup label=\"Number of Ensembles\" name=\"nensembles\">")
for n in nEnsembles:
    if (int(nensembles) == int(n)):
        sel = ' selected'
    else:
        sel = ''
    print("    <option"+sel+">"+str(n)+"</option>")
print("  </optgroup>\n")
print("</select><br>\n")

Errors = [0.01, 0.05, 0.10, 0.20, 0.25]
if (len(error) < 1):
    error = Errors[2]
print("<LABEL for=\"Error in Ensembles\">Error in Ensembles: </LABEL>")
print("<select name=\"error\">")
print("  <optgroup label=\"Error in Ensembles\" name=\"error\">")
for e in Errors:
    if (float(error) == float(e)):
        sel = ' selected'
    else:
        sel = ''
    print("    <option"+sel+">"+str(e)+"</option>")
print("  </optgroup>\n")
print("</select><p>\n")

print("This is for predictions using current APRS positions:<br>")

checked = ""
if (aprs == "1"):
    checked = " checked"
print("<input type=\"checkbox\" name=\"aprs\" value=\"1\"")
print(checked)
print(">Use current APRS to find current position.<br>")

print("These are for use with a Zero Pressure balloon:<br>")

checked = ""
if (zero == "1"):
    checked = " checked"
print("<input type=\"checkbox\" name=\"zero\" value=\"1\"")
print(checked)
print(">Use a zero pressure balloon.<br>")

textbox("Zero Pressure Balloon Radius","radius",radius,
        "(meters) Radius of widest point for Zero Pressure Balloon.")

textbox("Zero Pressure Balloon Volume","volume",volume,
        "(meters^3) Volume of the Zero Pressure Balloon.")

textbox("Zero Pressure Balloon Mass","zpmass",zpmass,
        "(grams) Mass of the Zero Pressure Balloon.")

#textbox("Hover Altitude","hover",hover,
#        "(meters) Altitude at which Z.P. balloon goes neutrally buoyant.<p>")

checked = ""
if (debug == "1"):
    checked = " checked"
print("<input type=\"checkbox\" name=\"debug\" value=\"1\"")
print(checked)
print(">Run in debug mode.<p>")

print("<INPUT type=\"submit\" name=\"run\" value=\"Run\">\n")
print("</FORM>")

# print(longitude,"<br>")
# print(latitude,"<br>")
# print(payload,"<br>")
# print(callsign,"<br>")
# print(parachute,"<br>")
# print(balloon,"<br>")
# print(helium,"<br>")
# print(yyyy+mm+dd,"<br>")
# print(hh,"<br>")

OkToRun = 1
if (len(longitude) == 0): OkToRun = 0
if (len(latitude) == 0): OkToRun = 0
if (len(payload) == 0): OkToRun = 0
if (len(callsign) == 0): OkToRun = 0
if (len(parachute) == 0): OkToRun = 0
if (zero == "1"):
    print("Zero Pressure Balloon Mode!<br>")
    if (len(volume) == 0): OkToRun = 0
    if (len(radius) == 0): OkToRun = 0
    if (len(zpmass) == 0): OkToRun = 0
    if (OkToRun == 0):
        print("Make sure that you have filled in all of the appropriate boxes!<br>")


if (OkToRun == 1):

    tmpdir = "/tmp/balloon_"+callsign

    date = datetime.datetime.now()
    sTimeNow = date.strftime('%Y%m%d_%H%M%S')
    htmlfile = callsign+'_'+sTimeNow+'.html'
    kmlfile = callsign+'_'+sTimeNow+'.kml'
    csvfile = callsign+'_'+sTimeNow+'.csv'

    print("<a href=\"http://vmr.engin.umich.edu/Model/_balloon/"+htmlfile+"\" target=\"_blank\">Map Prediction of Simulation</a><br>")
    print("<a href=\"http://vmr.engin.umich.edu/Model/_balloon/"+kmlfile+"\" target=\"_blank\">KML Flight Path Prediction</a><br>")
    print("<a href=\"http://vmr.engin.umich.edu/Model/_balloon/"+csvfile+"\" target=\"_blank\">CSV Flight Path Prediction</a><p>")

    command = "mkdir "+tmpdir
    if (debug == "1"): 
        print(command+"<br>")
    os.system(command)

    command = "cd "+tmpdir+"; /bin/cp /www/VMR2/site/Model/_balloon/balloon.py ."
    if (debug == "1"): 
        print(command+"<br>")
    os.system(command)

    command = "cd "+tmpdir+"; /bin/cp /www/VMR2/site/Model/_balloon/StationList ."
    if (debug == "1"): 
        print(command+"<br>")
    os.system(command)

    command = "cd "+tmpdir+"; /bin/cp /www/VMR2/site/Model/_balloon/StationListWorld ."
    if (debug == "1"): 
        print(command+"<br>")
    os.system(command)

    command = "cd "+tmpdir+"; /bin/cp /www/VMR2/site/Model/_balloon/aprs* ."
    if (debug == "1"): 
        print(command+"<br>")
    os.system(command)

    command = "cd /tmp/balloon_"+callsign+"; ./balloon.py"
    command = command + " -lon="+longitude
    command = command + " -lat="+latitude
    if (len(altitude) > 0):
        command = command + " -alt="+altitude

    if (zero == "1"):
        command = command + " -balloon="+zpmass
    else:
        command = command + " -balloon="+balloon
    command = command + " -payload="+payload
    command = command + " -parachute="+parachute
    command = command + " -helium="+helium
    command = command + " -ymd="+yyyy+mm+dd
    command = command + " -hour="+hh
    command = command + " -html="+htmlfile
    command = command + " -kml="+kmlfile
    command = command + " -csv="+csvfile
    if (len(nensembles) > 0):
        if (int(nensembles) > 1):
            command = command + " -n="+nensembles
            command = command + " -errors="+error
    if (len(bursttime) > 0):
        command = command + " -bursttime="+bursttime
    if (len(currenttime) > 0):
        command = command + " -currenttime="+currenttime
    if (zero == "1"):
        command = command + " -zero"
        command = command + " -r="+radius
        command = command + " -v="+volume
    if (update == "1"):
        command = command + " -update"
    if (descent == "1"):
        command = command + " -descent"
    if (aprs == "1"):
        command = command + " -aprs"
    command = command + " -callsign="+callsign

#    if (len(hover) > 0):
#        command = command + " -hover="+hover

    command = command + " > log"
    if (debug == "1"): 
        print(command+"<p>")
    os.system(command)

    command = "/bin/mv "+tmpdir+"/"+htmlfile+" /www/VMR2/site/Model/_balloon/"
    if (debug == "1"): 
        print(command+"<br>")
    os.system(command)

    command = "/bin/mv "+tmpdir+"/"+kmlfile+" /www/VMR2/site/Model/_balloon/"
    if (debug == "1"): 
        print(command+"<br>")
    os.system(command)

    command = "/bin/mv "+tmpdir+"/"+csvfile+" /www/VMR2/site/Model/_balloon/"
    if (debug == "1"): 
        print(command+"<br>")
    os.system(command)

    command = "/bin/mv "+tmpdir+"/*png /www/VMR2/site/Model/_balloon/"
    if (debug == "1"): 
        print(command+"<br>")
    os.system(command)

    command = "/bin/cp "+tmpdir+"/aprs* /www/VMR2/site/Model/_balloon/"
    if (debug == "1"): 
        print(command+"<br>")
    os.system(command)

    command = "/bin/rm -rf "+tmpdir
    if (debug == "1"): 
        print(command+"<br>")
    os.system(command)

    #command = "find . -name \"*.png\" -mtime +5 -exec ls -l {} \;"


    
print("</body>")
print("</html>")

