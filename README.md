This project utilises full-waveform inversion imaging data and recomputes it into reflection imaging data, designed to be used in Breast Cancer Ultrasound Image Acquisition, using an OpenSource Scanner.

# UG-Research-Project



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
