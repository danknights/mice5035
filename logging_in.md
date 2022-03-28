## How to log in to an interactive node on MSI

### Background
You will need to follow these steps once every time you want to get logged in to a new interactive node. 

### Connect to MSI
- Follow the steps in the [Getting Started Guide](README.md) to get SSH working on your computer. On a Mac this means opening the Terminal app. On Windows this means either using the "Command Prompt," or if SSH doesn't work in your Windows Command Prompt, then using the software called Putty.

- SSH to an MSI login node (skip this step if you are using Putty):
`ssh yourusername@login.msi.umn.edu`. Replace `yourusername` with your actual username.

### Connect to the Mesabi cluster
- SSH from the login node to the "mesabi" cluster:

`ssh mesabi` (you may have to enter your password).

### Launch and connect to an interactive computing node
- When you first log in to mesabi, you will be on a "login" node. You are not allowed to run computations on this node. Instead, you can launch an interactive node for running computations with this command:

 ```bash
srun -N 1 --ntasks-per-node=2 --mem-per-cpu=2gb -t 02:00:00 -p interactive --pty bash
 ```

This may take a while to finish running. It will usually log you directly in to the interactive node. You can see that this has happened because the start of the line in the terminal will say something like "yourusername@cn0077" and it will be different from what it was on the previous line. If in doubt, you can run `hostname` to print out the name of the node. Login nodes usually start with `login` or `ln`. If you are still on the login node, you just need to find out the name of the new interactive node so that you can connect to it. To find the name of your new interactive node, run this:

`squeue -u <your username>`, using your username in place of `<your username>`.

In the last column of the output is the name of the node that you want to connect to. It will usually look something like, `cn0123`. Now you must connect to that node:

`ssh cn0123` (Do not use `cn0123`; replace that with your node name).
