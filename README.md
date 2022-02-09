# MiCE 5035 Getting Started Guide

To set up your MSI account for using QIIME, please follow these steps:

### Connect to MSI with SSH

**Windows users**
  * Option 1: open the command prompt by searching for "command prompt" in the bottom left. Then follow the instructions for Mac users below.
  * Option 2: only if option 1 does not work, use a program called "Putty" instead, as follows:
    * Install "Putty" by downloading this file and running the installer:
https://www.ssh.com/academy/ssh/putty/windows/install
    * Open the Putty application
    * Under the "Hostname" field, enter `login.msi.umn.edu`
    * Under "Port", enter `22`
    * For "Connection type" click "SSH"
    * Click "Open"
    * Enter your MSI username and password
    * You should now be connected.


**Mac/Linux users**

  * Open the "Terminal" application. On a Mac you can click the search button (magnifying glass) and type "Terminal" to find the application.

### Get logged in to an interactive computing node
  * Follow the steps in the [logging in guide](logging_in.md). 

 
**Troubleshooting**
  * If you have trouble connecting, try filling out the MSI user agreement here: https://www.msi.umn.edu/user-agreement.
  * Make sure you are on the UofM network or eduroam network. Otherwise, MSI will probably block your computer from connecting. To get around this you can also use a UofM VPN, instructions for installing which are below.

### Run the setup command
Copy this command, paste it into your terminal, and press "return"

Run this additional command. It's OK to get two "File exists" errors:
```bash
mkdir ~/.config; mkdir ~/.config/matplotlib; echo "backend: agg" >> ~/.config/matplotlib/matplotlibrc
```

### Run a test script

`module load qiime/1.8.0` (Load QIIME software)

`print_qiime_config.py` (Test that QIIME is working).


This should print out some details about your QIIME configuration and should not return any errors. If so, you are now ready to use MSI and QIIME.

### Clone/download the course code repository to your home directory
```
cd /home/mice5035/<yourusername>
git clone https://github.com/danknights/mice5035.git
```

### Install Filezilla to transfer files to/from MSI
Download and install Filezilla from here: https://filezilla-project.org/download.php?type=client

Instructions for connecting to MSI can be found here (Step 4): http://gabedev.com/3004/software_guide/

Thanks to Gabe Al-Ghalith for these instructions!

### Get a VPN working
MSI won't let you connect directly unless you are on campus. To access your files from home, you will need to set up a VPN (Virtual Private Network). Note: You usually only need to do this if you want to work from off campus. Most of the time when you are on campus you will be able to connect to MSI without a VPN.

Follow instructions from the university's IT website to install a VPN: https://it.umn.edu/services-technologies/virtual-private-network-vpn

### Install R and R studio on your computer 
You do not have to use R but we will demonstrate its capabilities during class. You can optionally install it if you want to follow along and get a light introduction to it.

Instructions for installing R can be found here: https://mirror.las.iastate.edu/CRAN/

Instructions for installing RStudio can be found here: https://www.rstudio.com/

