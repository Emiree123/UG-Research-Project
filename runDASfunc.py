# Function containing all the preprossing data, and run the reconstruction
import numpy as np
import h5py
import scipy.io
import matplotlib.pyplot as plt
import vectorised_hf as vhf  # Assuming this module contains necessary functions

ultrasound_reflection_file = 'data/ultrasound_reflection_data.mat'
ideal_element_positions_file = 'data/ideal_element_positions.mat'
kidney_data_file = 'data/25-01-2024-Open-UST-Kidney3-data.h5'

def run_das_processing(ultrasound_reflection_file, ideal_element_positions_file, kidney_data_file):
    # Load ultrasound reflection data
    data = scipy.io.loadmat(ultrasound_reflection_file, variable_names=['elementPositions', 'samplingFrequency', 'soundSpeed'])
    elementPositions = data['elementPositions']
    samplingFrequency = data['samplingFrequency'][0][0]
    soundSpeed = data['soundSpeed'][0][0]

    # Load ideal element positions data
    data2 = scipy.io.loadmat(ideal_element_positions_file, variable_names=['angle_TxNorm_to_RxNorm'])
    angleMap = data2['angle_TxNorm_to_RxNorm']
    angleMask = angleMap > 110

    # Load the HDF5 file for kidney data
    with h5py.File(kidney_data_file, 'r') as file:
        rcvData = file['ustData'][:,:,:]

    # DAS processing code starts here
    nTx = 255
    nRx = 255
    nt = 2560
    dx = 0.0003
    Lx = 0.15
    Ntx, Nrx, Nt = rcvData.shape
    rcvData2D = rcvData.reshape(Ntx*Nrx, Nt)
    winData2D = vhf.tukey_vectorised(rcvData2D, alpha=0.1, noise_Length=300)
    test_env = vhf.envelope_detection(winData2D)

    Xp, Yp = vhf.createImagingVector(dx, Lx)
    Xd = elementPositions[:,0]
    Yd = elementPositions[:,1]

    Xd2D = Xd.reshape(-1,1)
    Xp2D = Xp.reshape(-1,1)
    Yd2D = Yd.reshape(-1,1)
    Yp2D = Yp.reshape(-1,1)
    Yd2DT = Yd2D.T
    Xd2dT = Xd2D.T

    distanceMap = vhf.calculateDistanceMap(Xd2dT, Yd2DT, Xp2D, Yp2D)
    timeMap = vhf.timeMap(distanceMap, soundSpeed)

    accumulator = 0
    total_iterations = nTx * nRx
    completed_iterations = 0
    envData3D = test_env.reshape(Ntx, Nrx, Nt)

    Nmodule = 16
    deltaTheta = 360/Nmodule
    moduleNormals = np.arange(0,360,deltaTheta)
    moduleNormals2 = moduleNormals.reshape(-1,1)
    moduleNormals2T =  moduleNormals2.T
    elementNormals = np.tile(moduleNormals2T,(Nmodule,1))
    elementNormals = elementNormals.flatten('F')
    sinvals = np.sin(elementNormals * np.pi / 180).reshape(-1,1)
    cosvals = np.cos(elementNormals * np.pi / 180).reshape(-1,1)
    elementNormalVec = np.concatenate([sinvals,cosvals],1)

    Npx = Xp.size
    angle_map = np.zeros((Npx, Ntx))
    for idx in range(Ntx):
        vector_map = elementPositions[idx,:] - np.concatenate([Xp2D, Yp2D], 1)
        z = np.sqrt(np.sum(vector_map**2, 1))
        z = z.reshape(-1,1)
        a = (vector_map / z).T
        y = elementNormalVec[idx,:].T
        y = y.reshape(-1,1)
        b = np.tile(y, (1, Npx))
        c = a[0,:]*b[0,:] + a[1,:]*b[1,:]
        c = c.reshape(-1,1).T
        d = np.arccos(c) * 180 / np.pi
        d = d.T
        d = np.squeeze(d)
        angle_map[:,idx] = d 
    accumulator = np.zeros_like(Xp2D, dtype='complex_')
    for Tx in range(nTx):
        for Rx in range(nRx):
            if angleMask[Tx, Rx]:
                T1 = timeMap[:, Tx]
                T2 = timeMap[:, Rx]
                total_time = T1 + T2
                sample_index = vhf.time_to_sample_index(total_time, samplingFrequency)
                sample_index = sample_index.astype(int)
                valid = np.logical_and(sample_index < nt-1, sample_index >= 0)
                extract = envData3D[Tx, Rx, sample_index[valid]]

                beamFactor = 1.09
                angleWeightingTx = np.abs(np.cos(beamFactor * angle_map[:, Tx] * np.pi / 180))
                angleWeightingRx = np.abs(np.cos(beamFactor * angle_map[:, Rx] * np.pi / 180))
                angleWeighting = angleWeightingTx * angleWeightingRx
                angleWeighting = angleWeighting[np.squeeze(valid)]
                extract = extract * angleWeighting
                accumulator[valid.T] = accumulator[valid.T] + extract

                completed_iterations += 1
                current_percentage = (completed_iterations / total_iterations) * 100
                print(f"Completed: {current_percentage:.2f}%", end='\r')

                x = int(np.sqrt(Npx))
                finalImage = np.abs(accumulator)
                finalImage = np.reshape(finalImage, (x, x))

                plt.figure()
                plt.imshow(finalImage, cmap='gray')
                plt.show()

                plt.figure()
                plt.imshow(20 * np.log10(finalImage), cmap='gray')
                plt.show()

    return finalImage, Xp, Yp