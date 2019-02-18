## MiCE 5992 Tutorial: QIIME Core diversity analyses

### Background
In this tutorial we will learn how to run all standard QIIME analyses including alpha diversity, beta diversity, and significance testing.
We will use a QIIME parameters file to tweak the settings.

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
2. Load software  
 Load all of the software "modules" that you will need.
 ```bash
    module load qiime/1.9.1
    module load bowtie2
 ```

3. Go to the tutorial directory
 Change to your personal course directory if you are not already there:
 ```bash
    /home/mice5992/<yourusername>
 ```

 List the contents of your home directory, if you are curious what's in there:
 ```bash
    ls
 ```

 Then change directories into the course repository folder that you downloaded:
 ```bash
    cd mice5992-2017
 ```

4. Update the directory 
 The following command will "pull" (download) any updates to the online repository to your local filesystem on MSI:
 ```bash
    git pull
 ```

 Then change directories into the new tutorial folder:
 ```bash
    cd tutorials
    cd corediv
 ```

 List the contents of the directory:
 ```bash
    ls
 ```
 You should see a file `parameters.txt`. Print the contents of this file to the screen with `cat`:
 
 ```bash
    cat parameters.txt
 ```

### Analysis
4. Pick Operational Taxonomic Units (OTUs) again
 Find the closest match for each sequence in a reference database using NINJA-OPS.

 ```bash
    time python /home/mice5992/shared/NINJA-OPS-1.5.1/bin/ninja.py -i ../../data/globalgut/seqs.fna -o otus -p 4 -z
    ls otus
 ```
 Note that we added `-z`. What does this do? Run the same command with `-h` to find out.
 
 Get a nice summary of the OTU table, and inspect the first 20 lines using `head`:
 ```bash
    biom summarize_table -i otus/ninja_otutable.biom -o otus/stats.txt
    head -n 20 otus/stats.txt
 ```
 
 From this summary you should be able to answer these questions:
  - How many unique OTUs (taxonomic groups) are there?
  - How many samples?
  - How many total sequences matched the database overall?
  - How many sequences matched the database in the lowest coverage sample?

 To view more of this file, you can scroll up and down inside it with `less otus/stats.txt`.
 However, you will need to quit `less` by typing `q` before you do anything else.

5. Drop rare OTUs, drop samples with < 500 sequences
 ```bash
    filter_otus_from_otu_table.py -i otus/ninja_otutable.biom -o otus/ninja_otutable_s10.biom -s 10
    filter_samples_from_otu_table.py -n 500 -i otus/ninja_otutable_s10.biom -o otus/ninja_otutable_s10_min500.biom
 ```

5. Make taxonomy stacked bar plots
 First read the usage instructions for the `summarize_taxa_through_plots.py` command with `-h`:
 ```bash
    summarize_taxa_through_plots.py -h
 ```
 
 What does this command do?
 
 Compare the default settings with the tweaked settings in `parameters.txt`. What are we changing by using `parameters.txt`?
 
 Now run the command `summarize_taxa_through_plots.py`:

 ```bash
    summarize_taxa_through_plots.py -i otus/ninja_otutable_s10_min500.biom -p parameters.txt -v -o taxaplots/
 ```
 **Note:** if you get an error from any QIIME script saying that the output directory already exists, then you can usually rerun the command with ` -f` at the end to force it to overwrite the existing directory. If that doesn't work, then remove the offending directory with `rm -rf <name of the directory>`.

6. Make beta diversity plots

 ```bash
    beta_diversity_through_plots.py -i otus/ninja_otutable_s10_min500.biom -m ../../data/globalgut/map.txt -o betaplots -p parameters.txt -t /home/mice5992/shared/97_otus.tree -v 
 ```
 
7.  Run alpha diversity analysis and make plots of rarefaction curves.

 ```bash
    alpha_rarefaction.py -i otus/ninja_otutable_s10_min500.biom --min_rare_depth 100 --max_rare_depth 500 --num_steps 3 -o alphaplots -m ../../data/globalgut/map.txt -v -p parameters.txt -t /home/mice5992/shared/97_otus.tree
 ```

8. Move the files back from MSI to your computer using Filezilla  
 See instructions on [Getting Started Guide](../../README.md) to connect to MSI using Filezilla. Navigate to `/home/mice5992/<yourusername>/mice5992-2017/tutorials/corediv/`. Drag the `betaplots`, `taxaplots`, and `alphaplots` folders to your computer.
 
9. Repeat using other data  
 Choose one of the many studies with sequence files and mapping files in this directory:
 ```bash
    ls /home/knightsd/public/qiime_db/processed/
    ls /home/knightsd/public/qiime_db/processed/Bushman_enterotypes_cafe_study_1010_ref_13_8
 ```
 **Note:** If you choose a very large data set you will run out of memory or time. You may need to log out of the interactive node with "control-D" and rerun `isub` requesting more RAM and/or more time:

 ```bash
    isub -n nodes=1:ppn=4 -m 16GB -w 08:00:00
 ```

 Then on MSI make a new directory to work in and move into it:
 ```bash
    mkdir bonus
    cd bonus
 ```
 
  Now run OTU picking, and the core diversity analyses above:
 ```bash
    python /home/mice5992/shared/NINJA-OPS-1.5.1/bin/ninja.py -i /home/knightsd/public/qiime_db/processed/Bushman_enterotypes_cafe_study_1010_ref_13_8/Bushman_enterotypes_cafe_study_1010_split_library_seqs.fna -o otus -p 4
    
    etc.
 ```

 After you finish running all core diversity analyses on the other data set, use Filezilla/FTP to move the outputs over to your computer. Also move the mapping file for that data set over to your computer, and open with Excel (or Google Sheets). Can you find a category that is interesting to run comparisons against? Use this information when examining the core diversity analyses on that study.
