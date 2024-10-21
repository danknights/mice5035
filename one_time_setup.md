# One-time setup instructions 
Follow these instructions _one time_ at the beginning of the semester.

### Set some default parameters
This setup script performs the following actions: (1) Set a parameter `backend:agg` that lets the popular Python-based visualization software `matplotlib` work; (2) tell the operating system where to find executables for the SHI7 tool.

Copy this command, paste it into your terminal, and press "return". It's OK to get a "File exists" error:
```bash
bash /home/knightsd/public/mice5035/mice5035_setup.sh
```

###
### Run a test script

`module load qiime/1.9.1_centos7` (Load the "QIIME" software)

`print_qiime_config.py` (to test that this package is working).

This should print out some details about your system configuration and should not return any errors. If so, you are now ready to use MSI and all of the bioinformatics packages they have available.


### Clone/download the course code repository to your home directory
```
# make sure you are in your home directory
cd

# download a copy of this repo to your directory
git clone https://github.com/danknights/mice5035.git
```

### Install R and R Studio on your computer 
We will be using R and R Studio in this class.

Instructions for installing R can be found here: https://mirror.las.iastate.edu/CRAN/

Instructions for installing RStudio can be found here: [https://www.rstudio.com/](https://posit.co/downloads/)

More detailed instructions can be found [here](https://www.r-bloggers.com/2020/08/tutorial-getting-started-with-r-and-rstudio/).
