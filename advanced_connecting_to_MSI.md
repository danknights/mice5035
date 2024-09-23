### Connect to MSI using SSH and your own terminal program
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


### Transfer files to/from MSI using an FTP program instead of OnDemand
Download and install Filezilla from here: https://filezilla-project.org/download.php?type=client

Instructions for connecting to MSI can be found here: https://www.msi.umn.edu/support/faq/how-do-i-use-filezilla-transfer-data. You have to set up a new "site" (meaning server) with an interactive login, so that you can use DUO to log in.
