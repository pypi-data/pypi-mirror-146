"""
Defines the landing dates/times for Mars missions
"""

from astropy.time import Time
from .Ls_utils import convert_to_float_delta_J2000, calc_Ls

# dictionary of mission names, landing dates, and how the mission numbered the
# first sol
#
# I tried to include the synonyms for missions.
mission_landing_dates = {}

# InSight - https://mars.nasa.gov/insight/mission/quick-facts/
mission_landing_dates["InSight"] =\
        {"landing_date": Time("2018-11-26 15:52:59"), "first_sol": 0}

# Perseverance - https://en.wikipedia.org/wiki/Mars_2020
mission_landing_dates["Perseverance"] =\
        {"landing_date": Time("2021-02-18 20:55"), "first_sol": 0}
mission_landing_dates["Mars 2020"] = mission_landing_dates["Perseverance"]

# Viking 1 - https://pubs.giss.nasa.gov/abs/al05000n.html
mission_landing_dates["Viking 1"] =\
        {"landing_date": Time("1976-07-20 11:53:06"), "first_sol": 0}

# Viking 2 - https://pubs.giss.nasa.gov/abs/al05000n.html
mission_landing_dates["Viking 2"] =\
        {"landing_date": Time("1976-09-03 22:37:50"), "first_sol": 0}

# Mars Pathfinder - https://pubs.giss.nasa.gov/abs/al05000n.html
mission_landing_dates["Mars Pathfinder"] =\
        {"landing_date": Time("1997-07-04 16:56:55"), "first_sol": 1}
mission_landing_dates["Pathfinder"] = mission_landing_dates["Mars Pathfinder"]
mission_landing_dates["MPF"] = mission_landing_dates["Mars Pathfinder"]

# Curiosity - 
#   Landing date - http://www-mars.lmd.jussieu.fr/mars/time/martian_time.html
#   first sol number - https://mars.nasa.gov/raw_images/778074/?site=msl
mission_landing_dates["Curiosity"] =\
        {"landing_date": Time("2012-08-06 05:17:57"), "first_sol": 0}
mission_landing_dates["MSL"] = mission_landing_dates["Curiosity"]
mission_landing_dates["Mars Science Laboratory"] =\
        mission_landing_dates["Curiosity"]

# Phoenix - 
#   Landing date - http://www-mars.lmd.jussieu.fr/mars/time/martian_time.html
#   first sol number - https://atmos.nmsu.edu/PDS/data/phmt_0001/DATA/
mission_landing_dates["Phoenix"] =\
        {"landing_date": Time("2008-05-25 23:38:23"), "first_sol": 0}

# Opportunity - 
#   Landing date - http://www-mars.lmd.jussieu.fr/mars/time/martian_time.html
#   first sol number - https://en.wikipedia.org/wiki/Opportunity_(rover)#Mission_overview
#
#   ...why the heck is Opportunity MER-1 but also MER-B 
#   but Spirit is MER-2 and MER-A...?
#
#   Also, did Opportunity really start numbering sols at 1 but Spirit at 0?
mission_landing_dates["Opportunity"] =\
        {"landing_date": Time("2004-01-25 04:55:00"), "first_sol": 1}
mission_landing_dates["MER-1"] = mission_landing_dates["Opportunity"]
mission_landing_dates["MER-B"] = mission_landing_dates["Opportunity"]

# Spirit - 
#   Landing date - http://www-mars.lmd.jussieu.fr/mars/time/martian_time.html
#   first sol number - https://mars.nasa.gov/mer/gallery/all/2/p/398/2P161703020EFFA500P2371L7M1.HTML
mission_landing_dates["Spirit"] =\
        {"landing_date": Time("2004-01-04 04:26:00"), "first_sol": 0}
mission_landing_dates["MER-1"] = mission_landing_dates["Spirit"]
mission_landing_dates["MER-B"] = mission_landing_dates["Spirit"]

# Beagle 2 - 
#   Landing date - http://www-mars.lmd.jussieu.fr/mars/time/martian_time.html
#   first sol number - ?
#mission_landing_dates["Beagle 2"] =\
#       {"landing_date": Time("2003-12-25 02:45:00"), "first_sol": 0}

available_missions = list(mission_landing_dates.keys())

def convert_mission_sol_to_Ls(mission_sol, mission_name="InSight"):
    """
    Converts given sol number for a given mission to Ls

    Args:
        mission_sol (float or array of floats): desired sol 
        mission_name (str): must be the name of a cataloged mission, see
        available_missions for options

    Returns:
        Ls (float or array of floats)

    Notes:
        Be careful! This doesn't really check user input. For example, if you
        ask for a mission sol that occurred after a mission actually ended,
        this code will happily give you the Ls-value.
    """

    # Check that desired mission is actually available
    if(not (mission_name in available_missions)):
        raise ValueError("%s is not an available mission." % mission_name)

    # Get Julian date - J2000 for mission's first sol
    first_sol_J2000 =\
            convert_to_float_delta_J2000(\
            mission_landing_dates[mission_name]["landing_date"])

    # Now shift by J2000
    desired_sol_JD_J2000 = first_sol_J2000 +\
            (mission_sol - mission_landing_dates[mission_name]["first_sol"])

    return calc_Ls(desired_sol_JD_J2000)
