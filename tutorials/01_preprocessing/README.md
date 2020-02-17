## MiCE 5035 Tutorial: Preprocessing

### Background
In this tutorial we will learn how to use the command line to
install the SHI7 preprocessing tool and use it to preprocess 16S and shotgun data.

### Connect to MSI
- Follow the steps in the [Getting Started Guide](../../README.md) to connect to MSI using SSH. On a Mac this means opening the Terminal app and using SSH. On Windows this means using Putty to connect.

- When you first log in, you will be on the "login" node. You are not allowed to run computations on this node. Instead, you can get to an interactive node for running computations with this command:
 ```bash
 isub -n nodes=1:ppn=4 -m 8GB -w 02:00:00
 ```

- Note: if you ever receive an error saying that you have exceeded the available memory, you can increase to 16GB.
 You can also request 8 hours instead of two as follows:
 ```bash
 isub -n nodes=1:ppn=4 -m 16GB -w 08:00:00
 ```

### Get used to navigating on the command line

```bash
# change into your “home” directory
cd

# list the contents of this directory
ls

# print out the “path” to this directory
pwd

# make a new directory (aka folder) for your programs (binaries)
mkdir bin

# make sure it got created
ls

# change into the “bin” directory
cd bin
```

### First time only: Download and install SHI7

```bash
# download the shi7 installation folder
wget https://github.com/knights-lab/shi7/releases/download/v0.9.9/shi7_0.9.9_linux_release.zip

# unzip it (but don’t type the whole filename; type “shi” then hit <tab> to auto-complete.
# always do that!)
unzip shi7_0.9.9_linux_release.zip

# remove the unneeded zip file
rm shi7_0.9.9_linux_release.zip

# tell the operating system where to find the shi7 programs next time you log in
# by adding the path to this directory to your system “PATH” variable

# find the current directory’s full path with “pwd”
pwd
# copy it (or memorize it)
# it should be something like /home/mice5035/<username>/bin
# or /home/<lab name>/<username>/bin

# change back to your home directory
cd 

# open the file in your home directory called “.bash_profile”
nano .bash_profile

# add the bin path to your “PATH”.
# make sure you use the exact path from 3 steps ago
export PATH=$PATH:/home/mice5035/<username>/bin 

# exit and save the file with control-x, then “y”, then “enter”.

# reload the .bash_profile file
# You will not need to do this next time you log in.
source ~/.bash_profile

# change back to your home directory
cd

# make sure you are using a current version of Python
module load python3

# test that shi7.py runs
shi7.py -h

# get the course repository, if you have not yet done this.
git clone https://github.com/danknights/mice5035.git
```


### Using SHI7 to preprocess sequencing data

```bash
# change into course repository directory
# the change to this tutorial directory
cd mice5035
cd tutorials
cd 01_preprocessing

# run shi7 on 16S data
shi7.py -i /home/knightsd/public/mice5035/preprocessing/16s/fastq -o 16s-output

# print top 10 lines of output FASTA (.fna) file 
# inspect combined_seqs file (cut -c 1-100 cuts out the first 100 characters of each line)
head 16s-output/combined_seqs.fna | cut -c 1-100

# examine the log file as above
# less lets you scroll up and down in a file without editing
# exit from less by typing “q”
less 16s-output/shi7.log

# use the log file to answer these questions:
# What fraction of reads was stitched in each sample?
# How many bases were trimmed from the left and right of each read?

# exit from less by typing “q”
q

# now run shi7 on the paired-end wgs data, allowing stitching
# located here:  /home/knightsd/public/mice5035/preprocessing/wgs-paired/fastq
shi7.py -i /home/knightsd/public/mice5035/preprocessing/wgs-paired/fastq -o wgs-paired-output

# list contents of output folder
ls wgs-paired-output

# print top 10 lines of output FASTA (.fna) file 
# inspect combined_seqs file (cut -c 1-100 cuts out the first 100 characters of each line)
head wgs-paired-output/combined_seqs.fna | cut -c 1-100

# examine the log file as above
# less lets you scroll up and down in a file without editing
less wgs-paired-output/shi7.log

# exit from less by typing “q”
q

# Now run paired-end wgs data, no stitching (use a different output folder!)
time shi7.py -i /home/knightsd/public/mice5035/preprocessing/wgs-paired/fastq -o wgs-paired-no-stitching --flash False

# use the log file to answer these questions:
# How long were the average reads in each sample?
# How many bases were trimmed from the left and right of each read?
```

### Additional exercises
```bash
# Read the SHI7 help output (shi7.py -h) for instructions

# 1. paired-end wgs data, no stitching, produce separate fasta files
# print out the first sequence of the first R1 fasta file. How long is it?

# 2. paired-end wgs data, no stitching, don't convert to fasta, produce separate fastq files
# print out the first sequence of the first R1 fastq file. How long is it?

# 3. run on single-end wgs data (need any special flags?)
# How long were the average reads in each sample?
# How many bases were trimmed from the left and right of each read?

# 4. run on single-end wgs data and do not trim by quality
# How long were the average reads in each sample?
# How many bases were trimmed from the left and right of each read?

# 5. run on single-end wgs data and decrease the minimum quality score for trimming
# How long were the average reads in each sample?
# How many bases were trimmed from the left and right of each read?

```

