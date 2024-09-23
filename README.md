# MiCE 5035 Getting Started Guide

To set up your MSI account for using the supercomputer, please follow these steps:

### Connect to MSI login node using "OnDemand":
* Control-click (Windows) or Command-click (Mac) here to open the MSI OnDemand dashboard in a new tab: https://ondemand.msi.umn.edu/pun/sys/dashboard
* Click Files > Home Directory to view your files
* Click Clusters > Agate Shell Access to open a terminal with command-line access to a login node.

**Troubleshooting**
  * If you have trouble connecting, try filling out the MSI user agreement here: https://www.msi.umn.edu/user-agreement.
  * Make sure you are on campus, connected to the the UofM network or eduroam network. Otherwise, MSI will block your computer from connecting. To get around this, you can also use a [University of Minnesota VPN](https://it.umn.edu/services-technologies/virtual-private-network-vpn). 
### Get logged in to an interactive computing node
  * Follow the steps in the [logging in guide](logging_in.md). 

 

### Set some default parameters
This setup script performs the following actions: (1) Set a parameter `backend:agg` that lets the QIIME 1.9 data visualization software `matplotlib` work; (2) tell the operating system where to find executables for the SHI7 tool.

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
cd /home/mice5035/<yourusername>
git clone https://github.com/danknights/mice5035.git
```

### Log out
When you are done using MSI, log out with `exit`. You may have to enter this several times if you are logged in to a special node or cluster.


### Install R and R studio on your computer 
You do not have to use R but we will demonstrate its capabilities during class. You can optionally install it if you want to follow along and get a light introduction to it.

Instructions for installing R can be found here: https://mirror.las.iastate.edu/CRAN/

Instructions for installing RStudio can be found here: https://www.rstudio.com/

