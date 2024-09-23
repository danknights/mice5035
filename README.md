# MiCE 5035 Getting Started Guide

To set up your MSI account for using the supercomputer, please follow these steps:

### Connect to MSI login node using "OnDemand":
* Control-click (Windows) or Command-click (Mac) here to open the MSI OnDemand dashboard in a new tab: https://ondemand.msi.umn.edu/pun/sys/dashboard
* Click Files > Home Directory to view your files
* Click Clusters > Agate Shell Access to open a terminal with command-line access to a login node.

### Launch and connect to an interactive computing node
- When you first log in to MSI, you will be on a "login" node. You are not allowed to run computations on this node. Instead, you can launch an interactive node for running computations with this command:

 ```bash
srun -N 1 --ntasks-per-node=2 --mem-per-cpu=8gb -t 02:00:00 -p interactive --pty bash
 ```

This may take a while to finish running. It will log you directly in to the interactive node. Often you can see that this has happened because the start of the line in the terminal will say something like "yourusername@cn0077" or "yourusename@acn001" and it will be different from what it was on the previous line. If in doubt, you can run `hostname` to print out the name of the node. Login nodes usually start with `ahl` or `login` or `ln`. 

### One-time setup
If this is the FIRST TIME you have connected to MSI in this class, follow the [one-time setup instructions](one_time_setup.md).

**Troubleshooting**
  * If you have trouble connecting, try filling out the MSI user agreement here: https://www.msi.umn.edu/user-agreement.
  * Make sure you are on campus, connected to the the UofM network or eduroam network. Otherwise, MSI will block your computer from connecting. To get around this, you can also use a [University of Minnesota VPN](https://it.umn.edu/services-technologies/virtual-private-network-vpn). 
### Get logged in to an interactive computing node
 

### Log out
When you are done using MSI, log out with `exit`, or you can type _control-D_. You may have to enter this several times if you are logged in to a special node or cluster.
