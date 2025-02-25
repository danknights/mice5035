## MiCE 5035 Tutorial: WGS feature extraction

### Background
This tutorial is an introduction to extracting taxonomic features from shotgun sequencing data, and 
performing alpha diversity and beta diversity analysis. We will use the Kraken tool to annotate the data.

### Connect to an interactive computing node on MSI
- If needed, follow the steps the [getting started guide](../../README.md) to get connected to an interactive node on MSI.

### Tutorial

1. Load software
   
 Load all of the software "modules" that you will need.
 ```bash
    module load qiime/1.9.1_centos7
    module load kraken
    module load bowtie2
    module load python/3.6.3
 ```
 
2. Navigate to the correct directory

Change directory in to the course repo and then into the directory for this tutorial. Ensure you have the latest files from the github repository with `git pull`.
Make sure that you are in your home directory. As a reminder, the following command will list your current directory:
 ```bash
    pwd
 ```
 ```bash
    cd mice5035
    cd tutorials/03_wgs_feature_extraction
    ls
    git pull
 ```

Let's set up a folder for our analysis of WGS taxa with the Kraken tool, so that we can keep our files organized.
 ```bash
    mkdir wgs-kraken
 ```

Change directory to the `wgs-kraken` directory
```bash
cd wgs-kraken
```
Run preprocessing on the raw data to get trimmed, filtered, stitched output sequences, in separate files, if you have not already done this in Tutorial 01.
```bash
# make sure you ran "module load python/3.6.3" as indicated above
time python3 /home/knightsd/public/shi7/shi7.py -i /home/knightsd/public/imp/wgs-shallow -o wgs-output --combine_fasta False

# Note: if the output files have an extra ".fa" in their names,
# then run this to rename the files:
for f in wgs-output/*.fa.fna; do mv $f wgs-output/`basename $f .fa.fna`.fna; done
```

Then create a subdirectory for the kraken raw output tables.
```bash
mkdir kraken-out
```

3. Run Kraken

Run Kraken on each input file. We will use a `for` loop for this so that we don't have to enter each file manually.
```bash
# loop through every .fna file. Run kraken2 on it.
for f in wgs-output/*.fna; do echo $f; time kraken2 --db /home/knightsd/public/minikraken2_v1_8GB --use-mpa-style --output tmp --report kraken-out/`basename $f .fna`.txt --use-names $f; done
```

Note: we could also run it on each file manually like this:
```bash
# just an example of running kraken2 on one individual file:
kraken2 --db /home/knightsd/public/minikraken2_v1_8GB --use-mpa-style --output tmp --report kraken-out/SAMPLE_ID.txt --use-names wgs-output/SAMPLE_ID.fna
```

4. Merge the separate Kraken outputs to taxon tables

This requires a custom script. A thorough search of the internet led to three failed attempts to use other software tools to do this.

```bash
# Now we have a single output file per sample;
# we can merge these using the script kraken2table.py in this repo:
wget https://raw.githubusercontent.com/danknights/mice5035/master/scripts/kraken2table.py -O kraken2table.py
python kraken2table.py kraken-out/*.txt taxon_tables
```

5. Convert each taxonomy table to biom format

This is only if you want to perform beta diversity and alpha diversity analysis using QIIME; can also do those steps in R. 

```bash
for f in taxon_tables/*.txt; do echo $f; biom convert -i $f --to-json -o `dirname $f`/`basename $f .txt`.biom --process-obs-metadata taxonomy; done
```

6. Continue with core diversity analyses
Alpha and beta diversity analysis can now be performed as in [Tutorial 2](../02_16s_feature_extraction), but with the species-level taxon tables as the input biom files. There will be a few differences:
- Be sure to check the sequencing depths after creating the summary of the OTU (species) table to choose an appropriate rarefaction depth before you run rarefaction. Note: if you have a very small number of samples, you should try to include all of them when you choose the rarefaction depth. Samples below the rarefaction depth would be discarded.
- You don't need to run `summarize_taxa.py` to create taxon-level tables, because you already have them from Kraken.
- When you run `filter_otus_from_otu_table.py`, change the minimum number of samples for an OTU from 4 to 2 or an appropriate number based on how many samples you have.
- There are no tree files, so no phylogenetic diversity measures. When you run `alpha_diversity.py`, don't include a tree, and remove the "PD_whole_tree" from the list of metrics. When you run `beta_diversity.py`, remove the two "UniFrac" metrics. When you run `principal_coordinates.py`, and `make_emperor.py`, use "binary_jaccard" distance instead of "unweighted_unifrac" and "bray_curtis" instead of "weighted_unifrac", as follows.
- Warning: Do not simply copy and paste these commands! You may need to modify them for them to work. Please read the comments and run one command at a time.

First, check the depths of the samples to choose a rarefaction depth:

```bash
biom summarize-table -i taxon_tables/taxa_table_L7.biom -o stats.txt
less stats.txt
```

Let's assume we chose 10,000 sequences as the rarefaction depth. In practice this would be much higher for deep shotgun data. 

```bash
# Rarefaction, choose an appropriate depth based on the stats of the biom table
# DO NOT PASTE this command without editing the rarefaction depth
single_rarefaction.py -i taxon_tables/taxa_table_L7.biom -d 10000 -o taxon_tables/taxa_table_L7_rarefied.biom

# filter species in < 10 samples
# Note: change the 10 to something appropriate for your
# number of samples
filter_otus_from_otu_table.py -i taxon_tables/taxa_table_L7_rarefied.biom -o taxon_tables/taxa_table_L7_final.biom -s 10

# convert the final taxon table back to text format to load into R
# Note: this file have an extra "comment" at the top, so in R
# you will have to load with t(read.delim("taxa_table_L7_final.txt", row.names=1, skip=1))
# Also note that these files have taxa in the _rows_ so, you have to transpose in R with t()
biom convert -i taxon_tables/taxa_table_L7_final.biom -o taxon_tables/taxa_table_L7_final.txt --to-tsv --table-type "Taxon table"

# run alpha and beta diversity analysis without tree-based metrics
alpha_diversity.py -m "chao1,observed_otus,shannon" -i taxon_tables/taxa_table_L7_final.biom -o alpha-diversity.txt
beta_diversity.py -i taxon_tables/taxa_table_L7_final.biom -o beta -m "bray_curtis,binary_jaccard"

# Optionally run principal coordinates and 3D plots
# can also do this in R as in Tutorial 5
principal_coordinates.py -i beta/bray_curtis_taxa_table_L7_final.txt -o beta/bray_curtis_taxa_table_L7_final_pc.txt
principal_coordinates.py -i beta/binary_jaccard_taxa_table_L7_final.txt -o beta/binary_jaccard_taxa_table_L7_final_pc.txt

# replace the mapping file with the mapping file for your study
make_emperor.py -i beta/bray_curtis_taxa_table_L7_final_pc.txt -m ../../../data/imp/map.txt -o 3dplots-bray-curtis
make_emperor.py -i beta/binary_jaccard_taxa_table_L7_final_pc.txt -m ../../../data/imp/map.txt -o 3dplots-binary-jaccard
```

Then repeat the processing with the other taxonomic levels like genus (level 6) or phylum (level 2) as needed. 



