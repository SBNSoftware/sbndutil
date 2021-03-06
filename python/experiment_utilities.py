#!/usr/bin/env python
# ----------------------------------------------------------------------
#
# Name: project_utilities.py
#
# Purpose: A python module containing various experiment-specific
#          python utility functions.
#
# Created: 28-Oct-2013  H. Greenlee
# Modified: 10-Jul-2017 T. Brooks (tbrooks@fnal.gov) - now works with
#           LArSoft v06
#
# Modified: 17-Feb-2020 I. de Icaza Astiz (icaza@fnal.gov)
#           Python3 compliant and Python2 backwards compatible.
# ----------------------------------------------------------------------

import os
from io import StringIO

# Don't fail (on import) if samweb is not available.

try:
    import samweb_cli
except ImportError:
    pass


def get_dropbox(filename):

    # Get metadata.

    md = {}
    exp = 'sbnd'
    if 'SAM_EXPERIMENT' in os.environ:
        exp = os.environ['SAM_EXPERIMENT']
    samweb = samweb_cli.SAMWebClient(experiment=exp)
    try:
        md = samweb.getMetadata(filenameorid=filename)
    except:
        pass

    # Extract the metadata fields that we need.

    file_type = ''
    group = ''
    data_tier = ''

    if 'file_type' in md:
        file_type = md['file_type']
    if 'group' in md:
        group = md['group']
    if 'data_tier' in md:
        data_tier = md['data_tier']

    if not file_type or not group or not data_tier:
        raise RuntimeError(
            'Missing or invalid metadata for file %s.' % filename)

    # Construct dropbox path.

    #path = '/sbnd/data/sbndsoft/dropbox/%s/%s/%s' % (file_type, group, data_tier)
    if 'FTS_DROPBOX' in os.environ:
        dropbox_root = os.environ['FTS_DROPBOX']
    else:
        dropbox_root = '/pnfs/sbnd/scratch/sbndpro/dropbox'
    path = '%s/%s/%s/%s' % (dropbox_root, file_type, group, data_tier)
    return path

# Return fcl configuration for experiment-specific sam metadata.


def get_sam_metadata(project, stage):
    result = 'services.FileCatalogMetadataSBN: {\n'
    if type(stage.fclname) == type('') or type(stage.fclname) == type(''):
        result = result + '  FCLName: "%s"\n' % os.path.basename(stage.fclname)
    else:
        result = result + '  FCLName: "'
        for fcl in stage.fclname:
            result = result + '%s/' % os.path.basename(fcl)
        result = result[:-1]
        result = result + '"\n'
    result = result + '  FCLVersion: "%s"\n' % project.release_tag
    result = result + '  ProjectName: "%s"\n' % project.name
    result = result + '  ProjectStage: "%s"\n' % stage.name
    result = result + '  ProjectVersion: "%s"\n' % project.release_tag
    result = result + '}\n'

    return result

# Function to return path to the setup_sbnd.sh script


def get_setup_script_path():

    CVMFS_DIR = "/cvmfs/sbnd.opensciencegrid.org/products/sbnd/"
    FERMIAPP_DIR = "/grid/fermiapp/products/sbnd/"

    if os.path.isfile(FERMIAPP_DIR+"setup_sbnd.sh"):
        setup_script = FERMIAPP_DIR+"setup_sbnd.sh"
    elif os.path.isfile(CVMFS_DIR+"setup_sbnd.sh"):
        setup_script = CVMFS_DIR+"setup_sbnd.sh"
    else:
        raise RuntimeError("Could not find setup script at " +
                           FERMIAPP_DIR+" or "+CVMFS_DIR)

    return setup_script

# Construct dimension string for project, stage.


def dimensions(project, stage):

    data_tier = ''
    if ana:
        data_tier = stage.ana_data_tier
    else:
        data_tier = stage.data_tier
    dim = 'file_type %s' % project.file_type
    dim = dim + ' and data_tier %s' % data_tier
    dim = dim + ' and ub_project.name %s' % project.name
    dim = dim + ' and ub_project.stage %s' % stage.name
    dim = dim + ' and ub_project.version %s' % project.release_tag
    if stage.pubs_output:
        first_subrun = True
        for subrun in stage.output_subruns:
            if first_subrun:
                dim = dim + \
                    ' and run_number %d.%d' % (stage.output_run, subrun)
                first_subrun = False

                # Kluge to pick up mc files with wrong run number.

                if stage.output_run > 1 and stage.output_run < 100:
                    dim = dim + ',1.%d' % subrun
            else:
                dim = dim + ',%d.%d' % (stage.output_run, subrun)
    elif project.run_number != 0:
        dim = dim + ' and run_number %d' % project.run_number
    dim = dim + ' and availability: anylocation'
    return dim


def get_ups_products():
    return 'sbndcode'
