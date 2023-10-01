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

## Run actual quality filtering with SHI7
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

# run shi7 on IMP 16S data, located here:
# /home/knightsd/public/imp-16s-shallow/
time python3 /home/knightsd/public/shi7/shi7.py -i /home/knightsd/public/imp/16s-shallow/ -o 16s-output

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

# now run shi7 on the paired-end wgs data, allowing stitching, keep separate fastq files
# located here:  /home/mice5035/
python3 /home/knightsd/public/shi7/shi7.py -i /home/knightsd/public/imp/wgs-shallow -o wgs-output --combine_fasta False --convert_fasta False

# list contents of output folder
ls wgs-output

# print top 10 lines of the first output fastq (.fq) file 
head wgs-output/CS.079.S37.001.fa.fq

# examine the log file as above
# less lets you scroll up and down in a file without editing
less wgs-output/shi7.log

# exit from less by typing “q”
q

# Now run paired-end wgs data, no stitching (use a different output folder!)
# keep separate fastq files
time python3 /home/knightsd/public/shi7/shi7.py -i /home/knightsd/public/imp/wgs-shallow -o wgs-output-no-stitch --combine_fasta False --convert_fasta False --flash False

# use the log file to answer these questions:
# How long were the average reads in each sample?
# How many bases were trimmed from the left and right of each read?
```

### Additional exercises
```bash
# Read the SHI7 help output (shi7.py -h) for instructions

# 1. paired-end wgs data, no stitching, produce separate fasta (not fastq) files
# print out the first sequence of the first R1 fasta file. How long is it?

# 2. run on paired-end wgs data and do not trim by quality
# How long were the average reads in each sample?
# How many bases were trimmed from the left and right of each read?

# 3. run on paired-end data and decrease the minimum quality score for trimming
# How long were the average reads in each sample?
# How many bases were trimmed from the left and right of each read?
```

### Appendix
Note: when sequence data come off the Illumina sequencer they have a bunch of extra text in the filenames. Instead of `Sample1_R1.fastq`, samples are named `Sample1_Sxxx_R1_001.fastq` where `Sxxx` might have 1, 2, or 3 digits after the `S`. This text is annoying because it makes your sample IDs not match with your metadata file, so you have to get rid of it somehow. One way is to just rename the files, using a command like this:
```bash
for f in *.fastq.gz; do echo $f; mv $f "$(echo "${f}" | sed 's/_S[0-9][0-9]*_R\([1-2]\)_001/_R\1/')"; done
```
