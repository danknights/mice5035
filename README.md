# MiCE 5035 Getting Started Guide

To set up your MSI account for using QIIME, please follow these steps:

### Get your login info for MSI

  * Click on this link: https://www.msi.umn.edu/user-agreement. After you agree to the user agreement you will get your login information. 
  * If you already have MSI access, log in using your normal username and password, but then change into the course directory with this command:
  ```bash
  cd /home/mice5035/<your username>
  ```

### Connect to MSI with SSH

**Windows users**
  * First option: open the command prompt by searching for "command prompt" in the bottom left. Then follow the instructions for Mac users below. If that does not work, use Putty instead:
    * Visual instructions can be found here: http://gabedev.com/3004/software_guide/ (Step 3)
    * Alternatively, follow these instructions:
    * Install "Putty" by downloading this file and running the installer:
https://the.earth.li/~sgtatham/putty/latest/w64/putty-64bit-0.73-installer.msi
    * Open the Putty application
    * Under the "Hostname" field, enter `login.msi.umn.edu`
    * Under "Port", enter `22`
    * For "Connection type" click "SSH"
    * Click "Open"
    * Enter your MSI username and password
    * You should now be connected.


**Mac/Linux users**

  * Open the "Terminal" application. On a Mac you can click the search button (magnifying glass) and type "Terminal" to find the application.
  * Enter this command into the terminal, using your username in place of `yourusername`:

`ssh yourusername@login.msi.umn.edu`
 
 * Enter your password
  * You should now be connected.

### Run the setup command
Copy this command, paste it into your terminal, and press "return"

Run this additional command. It's OK to get two "File exists" errors:
```bash
mkdir ~/.config; mkdir ~/.config/matplotlib; echo "backend: agg" >> ~/.config/matplotlib/matplotlibrc
```

### Run a test script
Run the following commands on the MSI terminal:

`ssh mesabi`

`qsub -I /home/mice5035/public/isub-16gb-2h.pbs`

`module load qiime/1.8.0`

`print_qiime_config.py`


This should print out some details about your QIIME configuration and should not return any errors. If so, you are now ready to use MSI and QIIME.

### Clone/download the course code repository to your home directory
```
cd
git clone https://github.com/danknights/mice5035.git
```

### Install Filezilla to transfer files to/from MSI
Download and install Filezilla from here: https://filezilla-project.org/download.php?type=client

Instructions for connecting to MSI can be found here (Step 4): http://gabedev.com/3004/software_guide/

Thanks to Gabe Al-Ghalith for these instructions!

### Get a VPN working
MSI won't let you connect directly unless you are on campus. To access your files from home, you will need to set up a VPN (Virtual Private Network). 

Windows users see step 7 in Gabe's instructions here: http://gabedev.com/3004/software_guide/

Mac users try the "Native Client for MAC using IPSec" instructions here: https://it.umn.edu/downloads-guides-install-ipsec-native

If those don't work, see more options here: https://it.umn.edu/downloads-guides

### Install R and R studio on your computer 
Instructions for installing R can be found here (Steps 1 and 2): http://gabedev.com/3004/software_guide/
Instructions for installing RStudio can be found here: https://www.rstudio.com/

