import scipy.io
import os
import matplotlib.pyplot as plt
from scipy.io import loadmat
from scipy import signal
from scipy.fft import fft, fftshift
from scipy.signal import hilbert
from scipy.signal.windows import tukey 
import numpy as np
import vectorised_hf as vhf
import h5py 
from matplotlib import colormaps as cm
from scipy.interpolate import RegularGridInterpolator

h5_filename = 'heart.h5'
mat_filename = 'data/25-01-2024-Open-UST-Liver3-SART-07-02-2024.mat'

def load_h5_data(h5_filename, mat_filename):
    # Open the H5 file
    with h5py.File(h5_filename, 'r') as data:
        Image = np.array(data.get('Image'))
        Xp = np.array(data.get('Xp'))
        Yp = np.array(data.get('Yp'))

    # Reshape Xp and Yp
    n = np.size(Xp)
    x = int(np.sqrt(n))
    Xp = Xp.reshape((x, x))
    Yp = Yp.reshape((x, x))

    # Open the .mat file
    data2 = scipy.io.loadmat(mat_filename, variable_names=['gridVec', 'soundSpeedSART'])
    gridVec = data2['gridVec'].flatten('F')  # It's square
    soundSpeedSART = data2['soundSpeedSART']

    # Interpolate sound speed
    intgrid = RegularGridInterpolator((gridVec, gridVec), soundSpeedSART, bounds_error=False)
    soundspeedint = intgrid((Xp, Yp))

    # Return the loaded and processed data
    return Image, Xp, Yp, soundspeedint