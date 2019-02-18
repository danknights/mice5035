## MiCE 5992 Tutorial: QIIME

### Background
QIIME is a comprehensive tool for doing microbiome analysis. This tutorial is just an introduction
to the QIIME tool to allow you to try running a few commands and viewing the output.

### Setup
1. Connect to MSI  
 Follow the steps in the [Getting Started Guide](../../README.md) to connect to MSI using SSH.

 When you first log in, you will be on the "login" node. You are not allowed to run computations on this node. Instead, you can get to an interactive node for running computations with this command:
 ```bash
    isub -n nodes=1:ppn=4 -m 8GB -w 02:00:00
 ```
 This command might take a minute or two because you are waiting in line for an availabe computer node. The `nodes=1:ppn=4` means one computer node with 4 processors. The `-m 8GB` means you need 8GB of RAM, and the `-w 02:00:00` means you want up to 2 hours of time to work before you get kicked off.

 Then make sure that you are in the course directory, and not your home directory. The following command will list your current directory:
 ```bash
    pwd
 ```
 The current directory should be /home/mice5992/yourusername.
2. Load software  
 Load all of the software "modules" that you will need.
 ```bash
    module load qiime/1.9.1
    module load bowtie2
 ```
 
3. Get the data  
 Download the course repository to your folder on MSI:
 ```bash
    git clone https://github.com/danknights/mice5992-2017.git
 ```

 Then change directories into the course repository folder that you downloaded:
 ```bash
    cd mice5992-2017
 ```
 List the contents of the directory:
 ```bash
    ls
 ```

 Move to the `data` directory:
 ```bash
    cd data
 ```

 Move to the `globalgut` directory:
 ```bash
    cd globalgut
 ```

 Unzip the sequences file; list the directory contents before and after:
 ```bash
    ls
    unzip seqs.fna.zip
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

 Move up two directories, then down to the `qiime` directory in the `tutorials` directory:
 ```bash
    cd ..
    cd ..
    cd tutorials
    cd qiime
 ```
 
3. Pick Operational Taxonomic Units (OTUs)  
 Find the closest match for each sequence in a reference database using NINJA-OPS.

 ```bash
    time python /home/mice5992/shared/NINJA-OPS-1.5.1/bin/ninja.py -i ../../data/globalgut/seqs.fna -o otus -p 4 -z
    ls otus
 ```
 
 Get a nice summary of the OTU table, and inspect the first 20 lines using `head`:
 ```bash
    biom summarize_table -i otus/ninja_otutable.biom -o otus/stats.txt
    head -n 20 otus/stats.txt
 ```

 Make a text-based version of the OTU table and print out the first 10 rows (with `head`) and the first 5 columns (with `cut`):
 ```bash
    biom convert -i otus/ninja_otutable.biom -o otus/ninja_otutable.txt --to-tsv
    head otus/ninja_otutable.txt | cut -f 1-5
 ```
 
4. Calculate beta diversity

 ```bash
    beta_diversity.py -i otus/ninja_otutable.biom -o beta -m "unweighted_unifrac,weighted_unifrac,bray_curtis" -t /home/mice5992/shared/97_otus.tree
 ```

5. Run principal coordinates analysis on beta diversity distances to collapse to 3 dimensions

 ```bash
    principal_coordinates.py -i beta/unweighted_unifrac_ninja_otutable.txt -o beta/unweighted_unifrac_ninja_otutable_pc.txt
 ```

6. Make the 3D interactive "Emperor" plot

 ```bash
    time make_emperor.py -i beta/unweighted_unifrac_ninja_otutable_pc.txt -m ../../data/globalgut/map.txt -o 3dplots
 ```

7. Move the files back from MSI to your computer using Filezilla  
 See instructions on [Getting Started Guide](../../README.md) to connect to MSI using Filezilla. Navigate to `/home/mice5992/yourusername/mice5992-2017/tutorials/qiime/`. Then drag the `otus`, `beta`, and `3dplots` folders over to your laptop.
 
 ![Filezilla example](https://raw.githubusercontent.com/danknights/mice5992-2017/master/supporting_files/qiime_tutorial_FTP_screenshot.png "Filezilla example")


8. Now do it yourself on other data  
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
    python /home/mice5992/shared/NINJA-OPS-1.5.1/bin/ninja.py -i /home/knightsd/public/qiime_db/processed/Bushman_enterotypes_cafe_study_1010_ref_13_8/Bushman_enterotypes_cafe_study_1010_split_library_seqs.fna -o otus -p 4
    
    etc.
 ```
 
