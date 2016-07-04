import scipy
import scipy.stats as stats
import numpy as np
import pylab as pl
import matplotlib as mpl
import matplotlib.pyplot as plt
import os as os
import pandas as pd
import astropy.table

from astropy.coordinates import SkyCoord
from astropy import units as u
from astropy.coordinates import match_coordinates_sky
from astropy.coordinates.distances import Distance
from astropy import cosmology

from matplotlib import rc

#Uploading data
#My Functions--------------------------------------------------------
from LuoModule import matchcolumn, genlen

#Setting LaTeX font
rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=False)

#os.chdir("C:\\Users\\Danny\\Dropbox\\Programs\\")
#print ('Directory is now:', os.getcwd())
