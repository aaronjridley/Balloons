#!/opt/local/bin/python

from balloon_functions import *

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
# Test running the code with manually setting parameters
#   Full flight!
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------

# Parameters:
# payload in pounds
# balloon size in grams
# parachute diameter in feet
# helium in tanks
# lat / lon in degrees north and east
# alt in feet
# nEnsembles is how many times to run the code
# errors is % error to add to things for ensembles
# IsDescent sets whether to do descent only
# update is to check for weather stations along the way
# year, month, day, hour is launch time
# verbose is how much info is printed

args =  set_args( payload = 10.0,
                  balloon = 1500,
                  parachute = 6.0,
                  helium = 1.5,
                  lat = 42.1,
                  lon = -84.5,
                  alt = -1.0,
                  verbose = 0,
                  nEnsembles = 0,
                  errors = 0.2,
                  IsDescent = 0,
                  update = 1,
                  year = -1,
                  month = -1,
                  day = -1,
                  hour = -1)

BurstDiameter = KaymontBalloonBurst(args['balloon'])
if (BurstDiameter < 0):
    print("Could not determine burst diameter, exiting")
    exit()

#-----------------------------------------------------------------
# Do main calculation:
#-----------------------------------------------------------------
    
errors = 0.0
ascentData, descentData = calc_whole_flight(args, errors)

#-----------------------------------------------------------------
# Report and make plots:
#-----------------------------------------------------------------

report_summary(ascentData, descentData, args['verbose'])
images = make_plots(ascentData, descentData, args)

#-----------------------------------------------------------------
# Redo calculation a few times with variations
#-----------------------------------------------------------------

ensembleData = run_ensembles(args)

#-----------------------------------------------------------------
# write web page:
#-----------------------------------------------------------------

write_html(args, ascentData, descentData, ensembleData, images)
