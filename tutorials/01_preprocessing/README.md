## MiCE 5035 Tutorial: Preprocessing

### Background
In this tutorial we will learn how to use the command line to
install the SHI7 preprocessing tool and use it to preprocess 16S and shotgun data.

### Connect to an interactive computing node on MSI
- Follow the steps the [logging in guide](../../logging_in.md) to get connected to an interactive node on MSI.

## Visualize sequence quality. 
### Run the fastqc program to visualize sequence quality
- Tell the OS where to find SHI7 executables
```bash
module load fastqc
fastqc -o 16s-fastqc /home/knightsd/public/mice5035/preprocessing/16s/fastq
```

### Transfer files and view in a web browser
- Use FileZilla or another FTP program to drag the entire `16-fastqc` folder to your computer Desktop or class folder. Open the folder, and open the first `html` file.
- When does the sequence quality begin to drop off? If you had to choose a single length at which to truncate the sequences (trim off the ends, what would it be)? A quality score of 30 or 35 or higher is usually considered good.
- Scroll down to view the table of overrepresented sequences. Copy and paste the first one in to [NCBI's BLAST tool](https://blast.ncbi.nlm.nih.gov/Blast.cgi). Does it look suspicious?

## Run actual quality filtering
### First time only using SHI7
- Tell the OS where to find SHI7 executables
```bash
echo "PATH=/home/knightsd/public/mice5035/shi7:$PATH" >> ~/.bash_profile
source ~/.bash_profile
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

# run shi7 on 16S data
python /home/knightsd/public/mice5035/shi7/shi7.py -i /home/knightsd/public/mice5035/preprocessing/16s/fastq -o 16s-output

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
python /home/knightsd/public/mice5035/shi7/shi7.py -i /home/mice5035/public/preprocessing/wgs-paired/fastq -o wgs-paired-output

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
python /home/knightsd/public/mice5035/shi7/shi7.py -i /home/mice5035/public/preprocessing/wgs-paired/fastq -o wgs-paired-no-stitching --flash False

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

