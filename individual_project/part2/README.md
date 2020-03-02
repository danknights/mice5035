## MiCE 5035 Project 1 Part 2

### Background
This is a short tutorial on how to get started on your individual project. Please show all work, including all commands run, by entering them into the [Individual Project part 2 worksheet](https://docs.google.com/document/d/14bqCKIMScBCUOqWTcrd2xEoX9UGQZpCJRdo0r3grK8U/edit?usp=sharing).

### Setup
1. Connect to MSI  
 Follow the steps in the [Getting Started Guide](../../README.md) to connect to MSI using SSH.

 When you first log in, you will be on the "login" node. You are not allowed to run computations on this node. Instead, you can get to an interactive node for running computations with this command:
 ```bash
    ssh mesabi
    qsub -I -l "nodes=1:ppn=4,mem=16gb,walltime=02:00:00" -m p
 ```

2. Load software  
 Load all of the software "modules" that you will need.
 ```bash
    module load qiime/1.8.0
    module load bowtie2
 ```
 
3. Go to the tutorial directory
 Change to your personal tutorial directory:
 ```bash
    cd /home/mice5035/<yourusername>/mice5035/individual_project/part2
 ```

4. Update the directory 
 The following command will "pull" (download) any updates to the online repository to your local filesystem on MSI:
 ```bash
    git pull
 ```

 If you receive an error stating that you have local changes preventing this from working, then try running this:

 ```bash
    git fetch --all
    git reset --hard origin/master
 ```

5. Locate your personal project files. The mapping files for the project are in the folder `mapping_files`; the DNA sequences are in `seqs_subset.fna.zip`

### Analysis
4. Now proceed with the core diversity analyses and a/b testing using the tools you
 learned in the [Core diversity tutorial](../../tutorials/03_corediv) and the [A/B testing tutorial](../../tutorials/04_abtesting)

 **Note:** you should copy the mapping file over to your computer using FTP so that you can inspect it before proceeding.
 
### Bonus 
One point each. Follow instructions in the following online [QIIME Tutorials](http://qiime.org/tutorials/index.html):
  1. [Making distance boxplots](http://qiime.org/tutorials/creating_distance_comparison_plots.html). Note: this is only for discrete variables. You may want to edit the mapping file in Excel to shorten the names of the variables. Otherwise the boxplots will not be legible.
  2. [Running supervised learning](http://qiime.org/tutorials/running_supervised_learning.html).
  3. Performing [Procrustes analysis](http://qiime.org/tutorials/procrustes_analysis.html) to compare unweighted UniFrac distances to weighted UniFrac distances.
