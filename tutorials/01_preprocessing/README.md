## MiCE 5035 Tutorial: Preprocessing

### Background
In this tutorial we will learn how to use the command line to
install the SHI7 preprocessing tool and use it to preprocess 16S and shotgun data.

### Connect to MSI
- Follow the steps in the [Getting Started Guide](../../README.md) to connect to MSI using SSH. On a Mac this means opening the Terminal app and using SSH. On Windows this means either using the "Command Prompt" or SSH doesn't work in your Windows Command Prompt, then using Putty to connect.

- When you first log in, you will be on the "login" node. You are not allowed to run computations on this node. Instead, you can get to an interactive node for running computations with this command:
 ```bash
ssh mesabi
qsub -I -l "nodes=1:ppn=4,mem=16gb,walltime=02:00:00" -m p -q interactive
 ```

This may take a while to finish running. It will eventually print out a line like, `salloc: Granted job allocation`. This means that MSI has allocated a node for you to use. Now you just need to find out the name of that node so that you can connect to it. To find the name of your new node, run this:

`squeue -u <your username>`, using your username in place of `<your username>`. In the last column of the output is the name of the node that you want to connect to. It will usually look something like, `cn0123`.

Now you must connect to that node:

`ssh cn0123` (Do not use `cn0123`; replace that with your node name).

### First time only: Download and install SHI7

```bash
# change into your course “home” directory
cd /home/mice5035/<yourusername>

# list the contents of this directory, just for fun
ls

# print out the “path” to this directory, just for fun
pwd

# make a new directory (aka folder) for your programs (binaries)
mkdir bin

# make sure it got created
ls

# change into the “bin” directory
cd bin

# download the shi7 installation folder
wget https://github.com/knights-lab/shi7/releases/download/v0.9.9/shi7_0.9.9_linux_release.zip

# unzip it (but don’t type the whole filename; type “shi” then hit <tab> to auto-complete.
# always do that!)
unzip shi7_0.9.9_linux_release.zip

# remove the unneeded zip file
rm shi7_0.9.9_linux_release.zip

# tell the operating system where to find the shi7 programs next time you log in
# by adding the path to this directory to your system “PATH” variable
# we will send the following text to your ".bash_profile" file in 
# your official home directory. This will be loaded every time you log in in 
# the future. You do not need to run this command again the next time you log in.

# BE SURE TO FILL IN YOUR USERNAME where it says "<username>".
echo "PATH=\$PATH:/home/mice5035/<username>/bin/shi7-1.0.3" >> ~/.bash_profile; source ~/.bash_profile

# test that shi7.py runs
shi7.py -h

# change back to your course directory
cd /home/mice5035/<yourusername>

# get the course repository, if you have not yet done this.
git clone https://github.com/danknights/mice5035.git
```


### Using SHI7 to preprocess sequencing data

```bash
# change to your course directory if you are not already there.
cd /home/mice5035/<yourusername>

# change into course repository directory that you cloned from git (above).
# the change to this tutorial directory
cd mice5035
cd tutorials
cd 01_preprocessing

# load python2 for SHI7 (not necessary for everyone, but seems to work universally)
module load python2

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
# located here:  /home/mice5035/public/preprocessing/wgs-paired/fastq
shi7.py -i /home/mice5035/public/preprocessing/wgs-paired/fastq -o wgs-paired-output

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
time shi7.py -i /home/mice5035/public/preprocessing/wgs-paired/fastq -o wgs-paired-no-stitching --flash False

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

