import scipy.io
import matplotlib.pyplot as plt
from scipy import signal
from scipy.fft import fft, fftshift
from scipy.signal import hilbert
from scipy.signal.windows import tukey 
import numpy as np

def tukey_vectorised(rcvData2D, alpha=0.1, noise_Length=300, plot =False):
    # Determine the shape of the input 2D array
    N, Nt = rcvData2D.shape 
    # Find the maximum value in the 2D array for normalisation later
    max_val = np.max(rcvData2D)
    # Calculate the dimensions of the transmit and receive arrays
    Ntx  = np.sqrt(N)
    Nrx = Ntx
    # Calculate the window length, excluding the noise length
    Nwin = Nt - noise_Length
    # Create a Tukey window with the given alpha parameter
    window = tukey(Nwin, alpha)
    # Create a padding array of zeros for the noise
    padding = np.zeros(noise_Length)
    # Combine the padding and tukey window together
    final_window = np.concatenate([padding, window])
    print(final_window.shape)
    print(Ntx)
    print(Nrx)
    # Replicate the 1D window into thte 2D array
    stack = np.tile(final_window, (N,1))
    rcvData2D = np.squeeze(rcvData2D)
    # Apply the window to the rcvData2D with element-wise multiplication
    winData2D = np.multiply(rcvData2D, stack)
    print (winData2D.size)
    if plot: 
        # Plot the winData2D
        plt.figure(figsize=(10, 6))  # Set the size of the plot
        plt.plot(winData2D/max_val, color='blue', linestyle='-', linewidth=0.2)  # waveform and its window
        plt.plot(winData2D/max_val, color='red', linestyle='-', linewidth=0.2)
        plt.savefig('winData2D_win.png', dpi=300)  # Saves the plot as a PNG file
        plt.show()
    return winData2D

def envelope_detection(winData2D):
    envData2D = hilbert(winData2D)
    # envData2D = np.abs(analytic_signal)
    # Compute and test the envelope function
    return envData2D


def createImagingVector(dx, Lx):
    Nx = round(Lx / dx)
    x_vec = np.arange(0, Nx) * dx - np.mean(np.arange(0, Nx) * dx)
    X, Y = np.meshgrid(x_vec, x_vec)
    # Reshape 2D grids X and Y into 1D arrays
    X_flat = X.flatten('F')
    Y_flat = Y.flatten('F')

    return X_flat, Y_flat # Returns a vector

#Two functions, one in 2D and one in 1D
def createImagingGrid(dx,Lx):
    Nx = round(Lx / dx)
    x_vec = np.arange(0, Nx) * dx - np.mean(np.arange(0, Nx) * dx)
    X, Y = np.meshgrid(x_vec, x_vec)
    return X, Y
    # Reshape 2D grids X and Y into 1D arrays

def calculateDistanceMap(Xd, Yd, Xp, Yp):
    # Calculate the distance map between detector coordinates and pixel coordinates.
    # Calculate squared distances
    dist_squared = (Xp - Xd) ** 2 + (Yp - Yd) ** 2
    # Return the square root of squared distances
    distance = np.sqrt(dist_squared)
    return distance

def calculateElementNormals():
    Nmodule = 16
    deltaTheta = 360/Nmodule
    moduleNormals = np.arange(0,deltaTheta,360-deltaTheta)
    # Calculate the normal angle for each individual element
    elementNormals = np.tile(moduleNormals,(Nmodule,1))
    elementNormals = elementNormals.flatten()
    sinvals = np.sin(elementNormals)
    cosvals = np.cos(elementNormals)
    
    elementNormalVec = np.concatenate(sinvals,cosvals)
    return elementNormalVec


def timeMap(distanceMap, speedOfSound):
    # Speed of sound in meters per second (m/s)
    # Convert distance from meters to time in seconds
    time = distanceMap / speedOfSound
    return time

def createDelayMap(elementPositions, X, Y):
    #Dimensions of elementPositions is 2x256 and X,Y is a 2D square matrix -> make everything into a vector
    Xd_vector = elementPositions[:,0]
    Yd_vector = elementPositions[:,1]
    print(np.size(Xd_vector))
    print(np.size(Yd_vector))


def getTravelTime(Xt, Yt, Xr, Yr, Xp, Yp, soundSpeed):
    # Calculate the distances
    distance_tx_to_pixel = np.sqrt((Xt - Xp)**2 + (Yt - Yp)**2)
    distance_pixel_to_rx = np.sqrt((Xr - Xp)**2 + (Yr - Yp)**2)

    # Calculate the total travel distance
    total_distance = distance_tx_to_pixel + distance_pixel_to_rx

    # Convert distance to travel time
    travelTime = total_distance / soundSpeed

    return travelTime

def time_to_sample_index(time, sample_frequency):
    return np.round(time * sample_frequency)

def accumulate_signal(Tx, Rx, Xp, Yp, elementPositions, soundSpeed, samplingFrequency, rcvData):
    # Extract the waveform for the Tx-Rx pair
    signal = rcvData[Tx, Rx, :]

    # Process the extracted waveform
    processed_signal = preProcessData(signal, alpha=0.2, noise_length=300)

    # Get Transmitter and Receiver coordinates
    Xt = elementPositions[Tx, 0]
    Yt = elementPositions[Tx, 1]
    Xr = elementPositions[Rx, 0]
    Yr = elementPositions[Rx, 1]

    # Calculate travel time
    travelTime = getTravelTime(Xt, Yt, Xr, Yr, Xp, Yp, soundSpeed)

    # Convert travel time to sample index
    sample_index = time_to_sample_index(travelTime, samplingFrequency)

    # Extract value if within bounds and return
    if 0 <= sample_index < len(processed_signal):
        return processed_signal[sample_index]
    else:
        return 0

