# UG-Research-Project
## Overview
This project focuses on utilising full-waveform inversion imaging data and recomputes it into reflection imgaing data, designed to be used in Breast Cancer Ultrasound Image Acquisition, using an OpenSource Scanner. This project has been developed as part of my undergraduate studies at University College London under the Biomedical Ultrasound Research Group.

## Installation
Follow these steps to set up the project locally:
### Clone the repository:
git clone https://github.com/Emiree123/UG-Research-Project.git
### Navigate into the project directory:
cd UG-Research-Project
### Install the required dependencies:
This project does not require any dependencies to function, unless you wish to check the work and understand how the algorithm works. You will only need the dataset file of full-waveform images in order to see a recomputed reflection imaging data image. You may want to install Anaconda and Jupyter Notebooks.
Optional libraries: 
pip install scipy.io
pip install os
pip install matplotlib
pip install numpy

### Running the repository
You will need the following files: 
ultrasound_reflection_file = 'data/ultrasound_reflection_data.mat'
ideal_element_positions_file = 'data/ideal_element_positions.mat'
kidney_data_file = 'data/25-01-2024-Open-UST-Kidney3-data.h5' # This can be any data file, i.e a breast, heart, kidney file, any organ
You will also need a h5 file of the organ in order to combine it with your post-processed image to see best results. You can run it through the composite.ipynb file in order to see the final result.


# Notes to self: 
Install Anaconda, jupyter notebooks
git branch: check current branch
git checkout -b feat_name: create new branch for new feature
git checkout banch_name: change branch to branch_name
git push origin feat_goodbye_world: push feature branch to github website (after commiting)

 ## To pull
 git checkout main
 git remote update: download changes from github website (but don't activate them yet)
 git pull origin main: pull (activate) the recent changes
 
 ## commiting changes
 git add . (all the files that have been changed)
 git commit -m "commit message" (description of the change that was made)
 git push --set-upstream origin week11 -> 'week11'  is simply the branch name

## Sync functions and scripts:
    "jupyter.runStartupCommands": [
        "%load_ext autoreload", "%autoreload 2"
    ]
