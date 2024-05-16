########################################################################
# File:        create_raw_definition_sbnd.py
# Author:      tjyang@fnal.gov
#
# Script to declare SBND raw data files
#
# Usage: create_raw_definition_sbnd.py run_number
#
########################################################################

#!/usr/bin/env python

import sys
import samweb_cli

samweb = samweb_cli.SAMWebClient(experiment='sbnd')

if len(sys.argv) != 2:
    print ("Please specify run number.")
    sys.exit(1)
    
defname = "sbnd_runset_%s_raw" % (sys.argv[1])

#print("Definition name is %s"%defname)

defexist = True

try:
    info = samweb.descDefinition(defname)
except:
    defexist = False

if defexist:
    print("Definition exists:")
    print(info)
else:
    dimension = "run_number %s and data_tier raw and sbn_dm.detector sbn_nd" % (sys.argv[1])
    info = samweb.listFilesSummary(dimension)
    #print(info['file_count'])
    if info['file_count'] == 0:
        print("No files found with dimensions '%s'"%dimension)
        sys.exit(1)
    else:
        samweb.createDefinition(defname, dimension, "sbndpro")
        info = samweb.descDefinition(defname)
        print("New definition %s created:" % defname)
        print(info)
        print(samweb.listFilesSummary("defname: %s"%defname))
