# MiCE 5992 Getting Started Guide

To set up your MSI account for using QIIME, please follow these steps:

### Get your login info for MSI

  * Click on this link: https://www.msi.umn.edu/user-agreement. After you agree to the user agreement you will get your login information. 

### Connect to MSI with SSH

**Windows users**

  * Install "Putty" by downloading this file and running the installer:
https://the.earth.li/~sgtatham/putty/latest/x86/putty-0.67-installer.msi
  * Open the Putty application
  * Under the "Hostname" field, enter `login.msi.umn.edu`
  * Under "Port", enter `22`
  * For "Connection type" click "SSH"
  * Click "Open"
  * Enter your MSI username and password
  * You should now be connected.
  * Visual instructions can be found here: http://www.fastcomet.com/tutorials/getting-started/putty#connect and here: http://gabedev.com/3004/software_guide/ (Step 3)

**Mac/Linux users**

  * Open the "Terminal" application. On a Mac you can click the search button (magnifying glass) and type "Terminal" to find the application.
  * Enter this command into the terminal, using your username in place of `yourusername`:

`ssh yourusername@login.msi.umn.edu`
 
 * Enter your password
  * You should now be connected.

### Run the setup command
Copy this command, paste it into your terminal, and press "return"

`wget -O setup.sh z.umn.edu/5992setup && chmod +x setup.sh && ./setup.sh`

Run this additional command. It's OK to get two "File exists" errors:
```bash
    mkdir ~/.config; mkdir ~/.config/matplotlib; echo "backend: agg" >> ~/.config/matplotlib/matplotlibrc
```

### Run a test script
Run the following commands on the MSI terminal:

`isub`

`module load qiime/1.8.0`

`print_qiime_config.py`


This should print out some details about your QIIME configuration and should not return any errors. If so, you are now ready to use MSI and QIIME.

### Install Filezilla to transfer files to/from MSI
Download and install Filezilla from here: https://filezilla-project.org/download.php?type=client

Instructions for connecting to MSI can be found here (Step 4): http://gabedev.com/3004/software_guide/

Thanks to Gabe Al-Ghalith for these instructions!

### Get a VPN working
MSI won't let you connect directly unless you are on campus. To access your files from home, you will need to set up a VPN (Virtual Private Network). 

Windows users see step 7 in Gabe's instructions here: http://gabedev.com/3004/software_guide/

Mac users try the "Native Client for MAC using IPSec" instructions here: https://it.umn.edu/downloads-guides-install-ipsec-native

If those don't work, see more options here: https://it.umn.edu/downloads-guides
