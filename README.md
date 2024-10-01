# UG-Research-Project
## Overview
This project focuses on utilising full-waveform inversion imaging data and recomputes it into reflection imgaing data, designed to be used in Breast Cancer Ultrasound Image Acquisition, using an OpenSource Scanner. This project has been developed as part of my undergraduate studies at University College London under the Biomedical Ultrasound Research Group.

## Installation
Follow these steps to set up the project locally:

Clone the repository:
bash
Copy code
git clone https://github.com/Emiree123/UG-Research-Project.git
Navigate into the project directory:
bash
Copy code
cd UG-Research-Project
Install the required dependencies:
bash
Copy code
pip install -r requirements.txt
Ensure you have [mention any additional tools or software] set up before proceeding.



Notes to self: 
Install Anaconda, jupyter notebooks
git branch: check current branch
git checkout -b feat_name: create new branch for new feature
git checkout banch_name: change branch to branch_name
git push origin feat_goodbye_world: push feature branch to github website (after commiting)

 ## To pull
 git checkout main
 git remote update: download changes from github website (but don't activate them yet)
 git pull origin main: pull (activate) the recent changes
 
 ##commiting changes
git add . (all the files that have been changed)
git commit -m "commit message" (description of the change that was made)

git push --set-upstream origin week11 -> 'week11'  is simply the branch name



## Sync functions and scripts:
    "jupyter.runStartupCommands": [
        "%load_ext autoreload", "%autoreload 2"
    ]
