# MiCE 5035 Getting Started Guide

To set up your MSI account for using QIIME, please follow these steps:

### Connect to MSI with SSH

**Windows users**
  * First option: open the command prompt by searching for "command prompt" in the bottom left. Then follow the instructions for Mac users below. If that does not work, use Putty instead:
    * Visual instructions can be found here: http://gabedev.com/3004/software_guide/ (Step 3)
    * Alternatively, follow these instructions:
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
  * Enter this command into the terminal, using your username in place of `yourusername`:

`ssh yourusername@login.msi.umn.edu`
 
 * Enter your password
  * You should now be connected.

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
Run the following commands on the MSI terminal:

`ssh mesabi`

`qsub -I -l "nodes=1:ppn=4,mem=16gb,walltime=02:00:00" -m p`

This will print out a few lines containing something like, `salloc: Nodes cn0123 are ready for job.` This tells you the name of the node to which you need to connect. In this case, the node name is `cn0123`, but you will have a different node. Now you must connect to that node:

`ssh cn0123` (Replace with your node name).

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

