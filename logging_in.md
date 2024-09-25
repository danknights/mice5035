# Guide to logging in to MSI "manually" (not using OnDemand)
Warning: This is for advanced users only. Normally, you will use MSI's [on demand](https://ondemand.msi.umn.edu/pun/sys/dashboard) app for logging in, as described on the [getting started guide](README.md).

## How to log in to an interactive node on MSI
### Background
You will need to follow these steps once every time you want to get logged in to a new interactive node. 

### Connect to MSI
- Follow the steps in the [Getting Started Guide](README.md) to get SSH working on your computer. On a Mac this means opening the Terminal app. On Windows this means either using the "Command Prompt," or if SSH doesn't work in your Windows Command Prompt, then using the software called Putty.

- SSH to an MSI login node (skip this step if you are using Putty) (Replace `yourusername` with your actual username):

```bash
ssh yourusername@login.msi.umn.edu 
```

### Launch and connect to an interactive computing node
- When you first log in to mesabi, you will be on a "login" node. You are not allowed to run computations on this node. Instead, you can launch an interactive node for running computations with this command:

 ```bash
srun -N 1 --ntasks-per-node=2 --mem-per-cpu=8gb -t 02:00:00 -p interactive --pty bash
 ```

This may take a while to finish running. It will log you directly in to the interactive node. Often you can see that this has happened because the start of the line in the terminal will say something like "yourusername@cn0077" or "yourusename@acn001" and it will be different from what it was on the previous line. If in doubt, you can run `hostname` to print out the name of the node. Login nodes usually start with `login` or `ln`. 
