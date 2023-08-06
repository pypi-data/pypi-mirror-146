import numpy as np
from astropy import units as u
from astropy.time import Time
import mars_clock
import os

# Define some constants
mars_solar_day = 24.*u.hour + 39.*u.minute + 35.244*u.second
mars_sol = mars_solar_day # This is what's referred to as a sol
mars_tropical_year_in_sols = 668.5921*mars_solar_day
mars_sidereal_day = 24.*u.hour + 37.*u.min + 22.663*u.second

mars_tropical_year = 668.5921*mars_sol
mars_sidereal_year = 668.5991*mars_sol

# J2000 epoch in Julian date
J2000 = Time('2000-01-01 12:00:00', scale='tt')
float_J2000 = J2000.jd # into a float
float_MJD_2000 = J2000.mjd # into a float

def convert_to_float_delta_J2000(time):
    """
    Converts an astropy.Time object into a Julian day float with J2000 subtracted
    
    Args:
        time (astropy.Time or str): time or times to convert
        
    Returns:
        float or array of floats
    """
    
    # J2000 epoch in Julian date
    J2000 = Time('2000-01-01 12:00:00', scale='tt')
    float_J2000 = J2000.jd # into a float

    loc_time = time
    if(type(time) is str):
        loc_time = Time(time)

    float_JD_time = loc_time.jd - float_J2000
    
    return float_JD_time

def convert_to_centuries(time):
    """
    Convert time from days to centuries
    
    Args:
        time (float or array of floats): time in days
        
    Returns:
        time in centuries
    """

    return time/(100.*365.24217)
    
def calc_alpha(delta_J2000, mod_360=True):
    """
    Returns the Sun angle using Eq 2 from Piqueux+ (2015)
    
    Args:
        delta_J2000 (float or array of floats): Julian date difference between desired time and J2000 (2000 Jan 1 12:00:00)
        mod_360 (bool, optional): take the modulus with 360 degrees
        
    Returns:
        Sun angle (float or array of floats in degrees)
    """
    
    alpha_0  = 270.389001822 # degrees
    lin_coeff = 0.52403850205 # degrees per day
    quad_coeff = -0.000565452 # degrees per century per century
    
    T_centuries = convert_to_centuries(delta_J2000)
    
    alpha = alpha_0 + lin_coeff*delta_J2000 + quad_coeff*T_centuries*T_centuries
    
    if(mod_360):
        alpha = alpha % 360.
    
    return alpha

def calc_mean_anomaly(delta_J2000):
    """
    Returns the mean anomaly using Eq 3 from Piqueux+ (2015)
    
    Args:
        delta_J2000 (float or array of floats): Julian date difference between desired time and J2000 (2000 Jan 1 12:00:00)
        
    Returns:
        mean anomaly (float or array of floats in degrees)
    """
      
    M_0 = 19.38028331517 # degrees
    lin_coeff = 0.52402076345 # degrees per day
    
    return M_0 + lin_coeff*delta_J2000

def calc_eccentricity(delta_J2000):
    """
    Calculate evolving eccentricity from Eq 4 from Piqueux+ (2015)
    
    Args:
        delta_J2000 (float or array of floats): Julian date difference between desired time and J2000 (2000 Jan 1 12:00:00)
        
    Returns:
        eccentricity
    """
    
    e0 = 0.093402202
    lin_coeff = 0.000091406
    
    T_centuries = convert_to_centuries(delta_J2000)
    
    return e0 + lin_coeff*T_centuries

def calc_PPS(delta_J2000):
    """
    The planetary perturbation terms from Piqueux+ (2015) - you probably don't need to call this!
    
    Args:
        delta_J2000 (float or array of floats): Julian date difference between desired time and J2000 (2000 Jan 1 12:00:00)
    
    Returns:
        planetary perturbation terms (float or array of floats) from Eq 6
    """
    
    # amplitudes in degrees
    amplitudes = np.array([7.0591, 6.0890, 4.4462, 3.8947, 2.4328, 2.0400, 1.7746, 1.34607, 1.03438, 0.88180, 0.72350, 0.65555, 0.81460, 0.74578, 0.58359, 0.42864])*1e-3
    
    # periods in days
    tau = np.array([816.3755210, 1005.8002614, 408.1877605, 5765.3098103, 779.9286472, 901.9431281, 11980.9332471, 2882.1147, 4332.2204, 373.07883, 1069.3231, 343.49194, 1309.9410, 450.69255, 256.06036, 228.99145])
    
    # phases in degrees
    phi = np.array([48.48944, 167.55418, 188.35480, 19.97295, 12.03224, 95.98253, 49.00256, 288.7737, 37.9378, 65.3160, 175.4911, 98.8644, 186.2253, 202.9323, 212.1853, 32.1227])
        
    PPS = np.zeros_like(delta_J2000)
    
    for i in range(len(amplitudes)):
        PPS += amplitudes[i]*np.cos(2.*np.pi*delta_J2000/tau[i] + phi[i]*np.pi/180.)
    
    return PPS

def calc_equation_of_center(delta_J2000):
    """
    Eqn 5 from Piqueux+ (2015)
    
    Args:
        delta_J2000 (float or array of floats): Julian date difference between desired time and
        J2000 (2000 Jan 1 12:00:00)
        
    Returns:
        difference between true anomaly and mean motion (float or array of floats)
    """
    
    ecc = calc_eccentricity(delta_J2000)
    # Convert mean anomaly to radians
    mean_anomaly = calc_mean_anomaly(delta_J2000)*np.pi/180.
    
    # various orders of sine of the mean anomaly
    sin_M = np.sin(mean_anomaly)
    sin_2M = np.sin(2.*mean_anomaly)
    sin_3M = np.sin(3.*mean_anomaly)
    sin_4M = np.sin(4.*mean_anomaly)
    sin_5M = np.sin(5.*mean_anomaly)
    sin_6M = np.sin(6.*mean_anomaly)
    
    # various powers of the eccentricity
    ecc2 = ecc*ecc
    ecc3 = ecc2*ecc
    ecc4 = ecc3*ecc
    ecc5 = ecc4*ecc
    ecc6 = ecc5*ecc
    
    # And then the combinations
    sin_M_term = (2.*ecc - ecc3/4. + 5.*ecc5/96.)*sin_M
    sin_2M_term = (5.*ecc2/4. - 11*ecc4/24. + 17*ecc6/192.)*sin_2M
    sin_3M_term = (13.*ecc3/12 - 43.*ecc5/64)*sin_3M
    sin_4M_term = (103./96*ecc4 - 451.*ecc6/480)*sin_4M
    sin_5M_term = 1097.*ecc5/960*sin_5M
    sin_6M_term = 1223.*ecc5/960*sin_6M
    
    return sin_M_term + sin_2M_term + sin_3M_term + sin_4M_term +\
        sin_5M_term + sin_6M_term

def calc_Ls(delta_J2000, mod_360=True):
    """
    Calculate Mars' seasonal angle Ls using Eq 7 from Piqueux+ (2015)
    
    Args:
        delta_J2000 (float or array of floats): Julian date difference between desired time and J2000 (2000 Jan 1 12:00:00)
        mod_360 (bool, optional): take the modulus with 360 degrees
    
    Returns:
        Mars' seasonal angle Ls
    
    """
    
    alpha = calc_alpha(delta_J2000)
    nu = calc_equation_of_center(delta_J2000)
    PPS = calc_PPS(delta_J2000)
    
    Ls = alpha + 180./np.pi*nu + PPS
    
    if(mod_360):
        Ls = Ls % 360.
        
    return Ls

def MY2JD(MY, data_file="Piqueux2015_Table1.csv"):
    """
    Returns the number of Julian days since J2000 for the beginning of a given Mars year

    Args:
        MY (float or array of floats): desired Mars year
        data_file (str, optional): CSV file with Mars_year and delta J2000 dates,
        defaults to Piqueux2015_Table1.csv

    Returns:
        float or array of floats: number of seconds since J2000 for the beginning of a given Mars year

    """

    # Read in data table which must map Mars year to Earth date
    data_file_path = os.path.join(mars_clock.DATADIR, data_file)
    date_data = np.genfromtxt(data_file_path, delimiter=',', names=True)

    # Take the floor function
    desired_MY = np.floor(MY)

    if(np.isscalar(desired_MY)):

        # Check that desired_MY is in range
        if((desired_MY < np.min(date_data['Mars_year'])) |\
           (desired_MY > np.max(date_data['Mars_year']))):
            raise ValueError("desired_MY is out of range!")

        # Calculate Julian date
        ind = np.argmin(np.abs(date_data['Mars_year'] - desired_MY))
        j_et = date_data['delta_J2000'][ind]

        et = j_et

    else:
        et = np.array([])
        for i in range(len(desired_MY)):

            if((desired_MY[i] < np.min(date_data['Mars_year'])) |\
               (desired_MY[i] > np.max(date_data['Mars_year']))):
                raise ValueError("desired_MY is out of range!")

            ind = np.argmin(np.abs(date_data['Mars_year'] - desired_MY[i]))

            j_et = date_data['delta_J2000'][ind]
            et = np.append(et, j_et)

    return et
def scalar_Ls2JD(Ls, MY, JD_resolution=0.1):
    """
    Calculate the Delta J2000 Julian date for a given Ls during Mars year MY
    
    Args:
        Ls (float): solar longitude in degrees
        MY (float): Mars year
        JD_resolution (float, optional): initial resolution of JD grid; defaults to 1 day resolution
        fac (int, optional): how far out in either direction to extend JD grid
        
    Returns:
        Delta J2000 Julian date corresponding to Mars year MY and Ls
    
    """
    num_days_in_Mars_year = 687.
    
    # Create grid of Ls-values for the whole Mars year
    MY_JD = MY2JD(MY)
    
    lower_JD = MY_JD - 0.5*num_days_in_Mars_year
    upper_JD = MY_JD + 0.5*num_days_in_Mars_year
    JDs = np.arange(lower_JD, upper_JD, JD_resolution)
    
    Lss = calc_Ls(JDs)
    
    # Need to make sure Ls grid wraps around
    #
    # If the index of the minimum Ls-value is not zero, need to wrap
    mn_ind = np.argmin(Lss)
    if(mn_ind > 0):
        ind = range(0, mn_ind)
        Lss[ind] -= 360
    
    ret = np.interp(Ls, Lss, JDs)
    
    return ret

# Cheat to make a vectorized version
Ls2JD = np.vectorize(scalar_Ls2JD)
