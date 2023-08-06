"""
Test the functionality of mars_clock
"""

import numpy as np
from astropy import units as u
from astropy.time import Time

from mars_clock import Ls_utils as ut

def test_convert_to_float_delta_J2000():
    # Landing date/time of Perseverance
    ts = Time('2021-02-18 20:55', scale='utc')
    float_JD_ts = ut.convert_to_float_delta_J2000(ts) # convert to JD - J2000
    assert(np.isclose(float_JD_ts, 7719.371527777985))

def test_calc_Ls():
    # Testing dates from Picqueux+ (2015) to check for Ls = 0
    data = np.genfromtxt("Piqueux2015_Table1.csv", delimiter=',', names=True)

    # Dates on which Ls should be equal to zero
    dates_delta_J2000 = data["delta_J2000"]
    calculated_Ls = ut.calc_Ls(dates_delta_J2000)

    # Need to wrap around 360 degrees
    ind = calculated_Ls > 350.
    calculated_Ls[ind] -= 360.
    Picqueux_quoted_accuracy = 0.0073 # degrees

    # Check that results agree with zero to within given accuracy
    assert(np.all(np.isclose(np.abs(calculated_Ls), 0., rtol=0., atol=Picqueux_quoted_accuracy)))

def test_Ls2JD():
    data = np.genfromtxt("Piqueux2015_Table1.csv", delimiter=',', names=True)
    JDs = Ls2JD(np.zeros_like(data['Mars_year']), data['Mars_year'])
    # Off by, at worst, about 18 min between 1607 and 2141. 
    # Usually off by about 7 min
    resids = (JDs - data['delta_J2000'])
    # Better than 18 minutes
    assert(np.max(np.abs(resids)) < 0.0125)
