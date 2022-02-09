## MiCE 5035 Tutorial: QIIME

### Background
QIIME is a comprehensive tool for doing microbiome analysis. This tutorial is just an introduction
to the QIIME tool to allow you to try running a few commands and viewing the output. QIIME2 provides 
more options for visualizations but performs mostly the same core analyses and has a steeper learning curve.

### Connect to an interactive computing node on MSI
- Follow the steps the [logging in guide](../../logging_in.md) to get connected to an interactive node on MSI.

### Follow the tutorial
1. make sure that you are in your home directory inside the MICE 5035 course directory (`/home/mice5035`), and not your default home directory if you have another one. As a reminder, the following command will list your current directory:
 ```bash
    pwd
 ```

2. Load software  
 Load all of the software "modules" that you will need.
 ```bash
    module load qiime/1.8.0
    module load bowtie2
 ```
 
3. Change in to the course repo and then into the directory for this tutorial. Ensure you have the latest files from the github repository with `git pull`.
 ```bash
    cd mice5035
    cd tutorials/02_qiime
    ls
    git pull
 ```

4. Find the sequencing data

Unzip the sequences file from the `globalgut` directory:
 ```bash
    unzip ../../data/globalgut/seqs.fna.zip
    ls
 ```

 Test how large the files are:
 ```bash
    du -hs *
 ```

 Peek at the first 10 lines of the file:
 ```bash
    head seqs.fna
 ```

 Count the number of lines, words, and characters in the file. How many sequences are in the file?
 ```bash
    wc seqs.fna
 ```

 How many unique samples are there?
 ```bash
    grep ">" seqs.fna | cut -f 1 -d "_" | sort | uniq | wc
    
 ```



5. Pick Operational Taxonomic Units (OTUs)  

 Find the closest match for each sequence in a reference database using NINJA-OPS.


 ```bash
    time python /home/knightsd/public/mice5035/NINJA-OPS-1.5.1/bin/ninja.py -i seqs.fna -o otus -p 4 -z -m normal
    ls otus
    
    # note: if something didn't work right and you need to remove a file, use "rm"
    rm file_to_remove.txt
    
    # if you need to remove a directory:
    rm -r directory_to_remove
 ```
 
 Get a nice summary of the OTU table, and inspect the first 20 lines using `head`:
 ```bash
    biom summarize_table -i otus/ninja_otutable.biom -o otus/stats.txt
    head -n 20 otus/stats.txt
 ```

 Make a text-based version of the OTU table and print out the first 10 rows (with `head`) and the first 5 columns (with `cut`):
 ```bash
    biom convert -i otus/ninja_otutable.biom -o otus/ninja_otutable.txt -b
    # note: for qiime 1.9.1 use --to-tsv instead of -b
    head otus/ninja_otutable.txt | cut -f 1-5
 ```
 
6. Calculate beta diversity

 ```bash
    beta_diversity.py -i otus/ninja_otutable.biom -o beta -m "unweighted_unifrac,weighted_unifrac,bray_curtis" -t /home/knightsd/public/mice5035/databases/97_otus.tree
 ```

7. Run principal coordinates analysis on beta diversity distances to collapse to 3 dimensions

 ```bash
    principal_coordinates.py -i beta/unweighted_unifrac_ninja_otutable.txt -o beta/unweighted_unifrac_ninja_otutable_pc.txt
 ```

8. Make the 3D interactive "Emperor" plot

 ```bash
    time make_emperor.py -i beta/unweighted_unifrac_ninja_otutable_pc.txt -m ../../data/globalgut/map.txt -o 3dplots
 ```

9. Move the files back from MSI to your computer using Filezilla  
 See instructions on [Getting Started Guide](../../README.md) to connect to MSI using Filezilla. Navigate to `/home/mice5035/yourusername/mice5035/tutorials/02_qiime/`. Then drag the `otus`, `beta`, and `3dplots` folders over to your laptop.
 
 ![Filezilla example](https://raw.githubusercontent.com/danknights/mice5992-2017/master/supporting_files/qiime_tutorial_FTP_screenshot.png "Filezilla example")


10. Now do it yourself on other data  
 There are dozens of studies with sequence files and mapping files in this directory:
 ```bash
    ls /home/knightsd/public/qiime_db/processed/
    ls /home/knightsd/public/qiime_db/processed/Bushman_enterotypes_cafe_study_1010_ref_13_8
 ```

 First make a new directory to work in and move into it:
 ```bash
    mkdir bonus
    cd bonus
 ```
 
  Now run OTU picking, Beta diversity, Principal Coordinates Analysis, and making the 3D plots on the "Bushman...cafe" study:
 ```bash
    python /home/knightsd/public/mice5035/NINJA-OPS-1.5.1/bin/ninja.py -i /home/knightsd/public/qiime_db/processed/Bushman_enterotypes_cafe_study_1010_ref_13_8/Bushman_enterotypes_cafe_study_1010_split_library_seqs.fna -o otus -p 4
    
    ...etc.
 ```
 
