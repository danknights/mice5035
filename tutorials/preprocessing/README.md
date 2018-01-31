## MiCE 5992 Tutorial: QIIME Core diversity analyses

### Background
In this tutorial we will learn how to use the command line to
install the SHI7 preprocessing tool and use it to preprocess 16S and shotgun data.

### Setup
1. Connect to MSI
 Follow the steps in the [Getting Started Guide](../../README.md) to connect to MSI using SSH.

 When you first log in, you will be on the "login" node. You are not allowed to run computations on this node. Instead, you can get to an interactive node for running computations with this command:
 ```bash
    isub -n nodes=1:ppn=4 -m 8GB -w 02:00:00
 ```
 Note: if you ever receive an error saying that you have exceeded the available memory, you can increase to 16GB.
 You can also request 8 hours instead of two as follows:
 ```bash
    isub -n nodes=1:ppn=4 -m 16GB -w 08:00:00
 ```
2. Change to your official home directory
```bash
   cd
```

 List the contents of your home directory, if you are curious what's in there:
 ```bash
    ls
 ```
