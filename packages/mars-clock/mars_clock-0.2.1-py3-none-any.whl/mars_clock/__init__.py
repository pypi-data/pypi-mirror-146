"""A package for determining Ls-values from mission sols"""
import os

__version__ = '0.2.1'
__author__ = 'Brian Jackson <bjackson@boisestate.edu>'
__all__ = ['Ls_utils', 'mission_sols']

mars_clock_dir = os.path.dirname(__file__)
DATADIR = os.path.join(mars_clock_dir, 'data/')

from .Ls_utils import *
from .mission_sols import *
