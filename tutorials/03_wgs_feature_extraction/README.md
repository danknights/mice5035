## MiCE 5035 Tutorial: WGS feature extraction

### Background
This tutorial is an introduction to extracting taxonomic features from shotgun sequencing data, and 
performing alpha diversity and beta diversity analysis. We will use the Kraken tool to annotate the data.

### Connect to an interactive computing node on MSI
- Follow the steps the [logging in guide](../../logging_in.md) to get connected to an interactive node on MSI.

### Tutorial

1. Load software  
 Load all of the software "modules" that you will need.
 ```bash
    module load qiime/1.9.1_centos7
    module load bowtie2
    module load kraken
 ```
 
2. Navigate to the correct directory
Change directory in to the course repo and then into the directory for this tutorial. Ensure you have the latest files from the github repository with `git pull`.
Make sure that you are in your home directory inside the MICE 5035 course directory (`/home/mice5035`), and not your default home directory if you have another one. As a reminder, the following command will list your current directory:
 ```bash
    pwd
 ```
 ```bash
    cd mice5035
    cd tutorials/02_qiime
    ls
    git pull
 ```

Let's set up a folder for our analysis of WGS taxa with the Kraken tool, so that we can keep our files organized.
 ```bash
    mkdir wgs-kraken
 ```

Change directory to the `wgs-kraken` directory
```bash
cd ..
cd wgs-kraken
```

Then create a subdirectory for the kraken raw output tables.
```bash
mkdir kraken-output
```

3. Run Kraken.
Run Kraken on each input file. If we had many input files, we would write a `for` loop for this so that we didn't have to enter each file manually.

```bash
kraken2 --db /home/knightsd/public/minikraken2_v1_8GB --use-mpa-style --output tmp --report kraken/CS.079.txt --use-names ../../01_preprocessing/wgs-output/CS.079.S37.001.fa.fna
kraken2 --db /home/knightsd/public/minikraken2_v1_8GB --use-mpa-style --output tmp --report kraken/CS.145.txt --use-names  ../../01_preprocessing/wgs-output/CS.145.S1.001.fa.fna
kraken2 --db /home/knightsd/public/minikraken2_v1_8GB --use-mpa-style --output tmp --report kraken/CS.146.txt --use-names  ../../01_preprocessing/wgs-output/CS.146.S12.001.fa.fna 
kraken2 --db /home/knightsd/public/minikraken2_v1_8GB --use-mpa-style --output tmp --report kraken/CS.165.txt --use-names  ../../01_preprocessing/wgs-output/CS.165.S59.001.fa.fna 
kraken2 --db /home/knightsd/public/minikraken2_v1_8GB --use-mpa-style --output tmp --report kraken/CS.166.txt --use-names  ../../01_preprocessing/wgs-output/CS.165.S59.001.fa.fna 
kraken2 --db /home/knightsd/public/minikraken2_v1_8GB --use-mpa-style --output tmp --report kraken/CS.222.txt --use-names  ../../01_preprocessing/wgs-output/CS.222.S15.001.fa.fna
kraken2 --db /home/knightsd/public/minikraken2_v1_8GB --use-mpa-style --output tmp --report kraken/T.CS.008.txt --use-names  ../../01_preprocessing/wgs-output/T.CS.008.S40.001.fa.fna
kraken2 --db /home/knightsd/public/minikraken2_v1_8GB --use-mpa-style --output tmp --report kraken/T.CS.018.txt --use-names  ../../01_preprocessing/wgs-output/T.CS.018.S17.001.fa.fna
kraken2 --db /home/knightsd/public/minikraken2_v1_8GB --use-mpa-style --output tmp --report kraken/T.CS.030.txt --use-names  ../../01_preprocessing/wgs-output/T.CS.030.S84.001.fa.fna
```

4. Merge the separate Kraken outputs to taxon tables
This requires a custom script. A thorough search of the internet led to three failed attempts to use other software tools to do this.

```bash
# Now we have a single output file per sample;
# we can merge these using the script kraken2table.py in this repo:
python ../../../scripts/kraken2table.py kraken/*.txt taxon_tables
```

5. Convert each taxonomy table to biom format to perform beta diversity and alpha diversity analysis.
```bash
for f in taxon_tables/*.txt; do echo $f; biom convert -i $f --to-json -o `dirname $f`/`basename $f .txt`.biom --process-obs-metadata taxonomy; done
```

6. Continue with core diversity analyses
Alpha and beta diversity analysis can now be performed as in [Tutorial 2](../02_16s_feature_extraction), but with the taxon tables as the input biom files, without tree files, and without phylogenetic diversity measures.


