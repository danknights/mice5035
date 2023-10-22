## MiCE 5035 Tutorial: Data cleaning and visualization in R

### Background
This tutorial is an introduction to loading, filtering, and visualizing microbiome data in _R_.

### Requirements
You must have R and RStudio installed as described in the [Getting Started Guide](../../README.md).

### Tutorial

1. Open RStudio and start a new Project
Click the "Project" dropdown in the top right; In the resulting popup window, click "New Directory", "New Project", and then name the directory "Tutorials_04_05". You should place it in a folder on your computer where you know how to find it, and you know it will be backed up safely, with Google Drive, DropBox, or OneDrive, for example. If you are not using automatic backups to protect your work, please do so! The University of Minnesota provides [free storage on Google Drive](https://it.umn.edu/services-technologies/google-drive-desktop) using your University Google account.
 

2. Download and clean up the Immigration Microbiome Project data
We will download all of the output files from the [Immigration Microbiome Project code repository](https://github.com/knights-lab/IMP_analyses).

Create a new R file called `download_data.r`. On a Mac, you can find this with "File", "New File", "R Script". You should now have a blank text file open in the top left quadrant of the display. Paste these commands into the file, then click the "Source" above the file to run all of them.
```bash
map <- read.delim(url('https://raw.githubusercontent.com/knights-lab/IMP_analyses/master/data/map.txt?raw=true'),row=1)
otus <- t(read.delim(url('https://github.com/knights-lab/IMP_analyses/blob/master/data/denovo/final_otu.txt?raw=true'),row=1))
alpha <- read.delim(url('https://raw.githubusercontent.com/knights-lab/IMP_analyses/master/data/denovo/alpha.txt?raw=true'),row=1)
beta_uuf <- read.delim(url('https://raw.githubusercontent.com/knights-lab/IMP_analyses/master/data/denovo/unweighted_unifrac_dm.txt?raw=true'),row=1)
beta_wuf <- read.delim(url('https://raw.githubusercontent.com/knights-lab/IMP_analyses/master/data/denovo/weighted_unifrac_dm.txt?raw=true'),row=1)
phylum <- t(read.delim(url('https://github.com/knights-lab/IMP_analyses/blob/master/data/denovo/taxatable_L2.txt?raw=true'),row=1))
genus <- t(read.delim(url('https://github.com/knights-lab/IMP_analyses/blob/master/data/denovo/taxatable_L6.txt?raw=true'),row=1))
```


4. Make a Beta diversity plot

5. Add colors to the groups

6. Add ellipses to the groups

7. Make a histogram of alpha diversity values

8. Make a boxplot of alpha diversity values colored by group

9. Subset; visualize only a subset of samples

