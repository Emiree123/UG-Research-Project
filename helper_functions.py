import scipy.io
import matplotlib.pyplot as plt
from scipy import signal
from scipy.fft import fft, fftshift
from scipy.signal import hilbert
from scipy.signal.windows import tukey 
import numpy as np

def tukey_window(waveform, alpha=0.1, noise_length=300):
    max_val = np.max(waveform)
    Nt = np.size(waveform)
    Nwin = Nt - noise_length
    window = tukey(Nwin, alpha)
    padding = np.zeros((noise_length,))
    print(padding)
    #Squeeze the waveform so it has the same shape as the window, so the multiply function works properly
    print(padding.shape)
    print(window.shape)
    final_window = np.concatenate([padding, window])
    waveform = np.squeeze(waveform)
    waveform_win = np.multiply(final_window , waveform)

    # Plot the waveform
    plt.figure(figsize=(10, 6))  # Set the size of the plot
    plt.plot(waveform/max_val, color='blue', linestyle='-', linewidth=0.2)  # waveform and its window
    plt.plot(waveform_win/max_val, color='red', linestyle='-', linewidth=0.2)
    plt.savefig('waveform.png', dpi=300)  # Saves the plot as a PNG file
    plt.show()
    return waveform_win

def envelope_detection(waveform_win):
    analytic_signal = hilbert(waveform_win)
    envelope = np.abs(analytic_signal)
    # Compute and test the envelope function
    # envelope = envelope_detection(waveform_win)
    return envelope

def preProcessData(waveform, alpha=0.1, noise_length=300):
    # Apply Tukey window
    waveform_win = tukey_window(waveform, alpha, noise_length)
    # Test the pre-processing function 
    envelope = envelope_detection(waveform_win)
    return envelope

def createImagingGrid(dx, Lx):
    Nx = round(Lx / dx)
    x_vec = np.arange(0, Nx) * dx - np.mean(np.arange(0, Nx) * dx)
    X, Y = np.meshgrid(x_vec, x_vec)
    return X, Y

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
    return int(time * sample_frequency)

# Assuming you have a time value in seconds and the sample frequency
time = 0.001  # Replace with your time value
sample_frequency = 10e6  # Replace with your sample frequency

sample_index = time_to_sample_index(time, sample_frequency)
print(f"Sample Index: {sample_index}")

