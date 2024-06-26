#!/opt/local/bin/python

from balloon_functions import *

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
# Main Code!
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------

args = get_args(sys.argv)

if (args['balloon'] < 0):
    print("balloon set to < 0, exiting")
    exit()
    
BurstDiameter = KaymontBalloonBurst(args['balloon'])
if (BurstDiameter < 0 and args['zero'] == 1):
    BurstDiameter = args['r']*2.001

if (BurstDiameter < 0):
    print("Could not determine burst diameter! Stopping!")

NumberOfHelium = calculate_helium(args['helium'])
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
