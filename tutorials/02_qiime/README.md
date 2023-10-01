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
    module load qiime/1.9.1_centos7
    module load bowtie2
 ```
 
3. Change directory in to the course repo and then into the directory for this tutorial. Ensure you have the latest files from the github repository with `git pull`.
 ```bash
    cd mice5035
    cd tutorials/02_qiime
    ls
    git pull
 ```

Let's set up three folders for our analyses: closed-ref 16S OTUs, de novo 16S OTUs, and WGS taxa with the Kraken tool, so that we can keep our files organized.
 ```bash
    mkdir 16s-closed-ref
    mkdir 16s-de-novo
    mkdir wgs-kraken
 ```

Change directory into the 16s-closed-ref directory.
```bash
    cd 16s-closed-ref
 ```

4. Find the sequencing data
You should already have the post-qc sequencing data in the tutorial 01 directory. Check to see that it is there:
 ```bash
    ls ../../01_preprocessing/16s-output/
 ```

 Count the number of lines, words, and characters in the sequence file. How many sequences are in the file?
 ```bash
    wc ../../01_preprocessing/16s-output/combined_seqs.fna
 ```

 How many unique samples are there? Note: this involves a few bash scripting tricks: using pipe `|` to feed the output from one program to another; using `cut` to cut each line into fields based on a given delimiter ("_" in this case), etc.
 ```bash
    grep ">" ../../01_preprocessing/16s-output/combined_seqs.fna | cut -f 1 -d "_" | sort | uniq | wc
    
 ```

5. Pick Operational Taxonomic Units (OTUs)
### Closed-reference
 Find the closest match for each sequence in a reference database using NINJA-OPS. We can also use the QIIME `pick_closed_reference_otus.py` workflow script, but NINJA-OPS is faster.

 ```bash
    time python /home/knightsd/public/mice5035/NINJA-OPS-1.5.1/bin/ninja.py -i ../../01_preprocessing/16s-output/combined_seqs.fna -o otus -p 4 -z -m normal
    ls otus

    # rename the output table so that it is consistent with other QIIME commands
    mv otus/ninja_otutable.biom otus/otu_table.biom
 ```
 
 Make a text-based version of the OTU table and print out the first 10 rows (with `head`) and the first 5 columns (with `cut`):
 ```bash
    biom convert -i otus/otu_table.biom -o otus/otu_table.txt --to-tsv

    head otus/otu_table.txt | cut -f 1-5
 ```

 Get a nice summary of the OTU table, and inspect the first 30 lines using `head`. Can you find a good depth cutoff for rarefaction?
 ```bash
    biom summarize-table -i otus/otu_table.biom -o otus/stats.txt
    head -n 30 otus/stats.txt
 ```

 6. Rarefy and filter the OTU table
 We will subsample the observations in each sample so that they have the same effective sequencing depth. This controls for differences in alpha diversity and beta diversity that might show up as artifacts if one group of samples had much higher depth than another. We will use a depth of 140 chosen by inspecting the `stats.txt` file above. In a full data set, this would be much higher.

 ```bash
    single_rarefaction.py -i otus/otu_table.biom -d 140 -o otus/otu_table_rarefied.biom
 ```

 Remove OTUs not present in at least 4 samples (in practice we might choose 10% or 25% of all samples).
 ```bash
   filter_otus_from_otu_table.py -i otus/otu_table_rarefied.biom -o otus/otu_table_final.biom -s 4
 ```

Note: we may perform relative abundance filtering later when doing statistical testing. QIIME1 does not implemement this type of filter.

7. Calculate alpha diversity
```bash
   alpha_diversity.py -m "chao1,observed_otus,shannon,PD_whole_tree" -i otus/otu_table_final.biom -t /home/knightsd/public/gg_13_8_otus/trees/97_otus.tree -o alpha-diversity.txt
```

8. Calculate beta diversity

 ```bash
    beta_diversity.py -i otus/otu_table_final.biom -o beta -m "unweighted_unifrac,weighted_unifrac,bray_curtis,binary_jaccard" -t /home/knightsd/public/gg_13_8_otus/trees/97_otus.tree
 ```

9. Run principal coordinates analysis on beta diversity distances to collapse to 3 dimensions

 ```bash
    principal_coordinates.py -i beta/weighted_unifrac_otu_table_final.txt -o beta/weighted_unifrac_otu_table_final_pc.txt
 ```

10. Make the 3D interactive "Emperor" plot

 ```bash
    time make_emperor.py -i beta/weighted_unifrac_otu_table_final_pc.txt -m ../map.txt -o 3dplots-weighted-unifrac
 ```

11. Move the files back from MSI to your computer using Filezilla  
 See instructions on [Getting Started Guide](../../README.md) to connect to MSI using Filezilla. Navigate to `/home/mice5035/yourusername/mice5035/tutorials/02_qiime/`. Then drag the `otus`, `beta`, and `3dplots` folders over to your laptop.
 
 ![Filezilla example](https://raw.githubusercontent.com/danknights/mice5992-2017/master/supporting_files/qiime_tutorial_FTP_screenshot.png "Filezilla example")

## Repeat with de-novo OTU picking

First, change directory to the `otus-de-novo` directory
```bash
cd ..
cd otus-de-novo
```

To pick de novo OTUs:
```bash
   time pick_de_novo_otus.py -i ../../01_preprocessing/16s-output/combined_seqs.fna -o otus -O 4 -v -a
```
Then proceed with steps 6-11 above. Note that you will need to use the de novo tree `otus/rep_set.tre` rather than the reference tree in the beta diversity step:

```bash
biom convert -i otus/otu_table.biom -o otus/otu_table.txt --to-tsv
single_rarefaction.py -i otus/otu_table.biom -d 140 -o otus/otu_table_rarefied.biom
filter_otus_from_otu_table.py -i otus/otu_table_rarefied.biom -o otus/otu_table_final.biom -s 4
alpha_diversity.py -m "chao1,observed_otus,shannon,PD_whole_tree" -i otus/otu_table_final.biom -t otus/rep_set.tre -o alpha-diversity.txt
beta_diversity.py -i otus/otu_table_final.biom -o beta -m "unweighted_unifrac,weighted_unifrac,bray_curtis,binary_jaccard" -t otus/rep_set.tre
principal_coordinates.py -i beta/weighted_unifrac_otu_table_final.txt -o beta/weighted_unifrac_otu_table_final_pc.txt
time make_emperor.py -i beta/weighted_unifrac_otu_table_final_pc.txt -m ../map.txt -o 3dplots-weighted-unifrac
```

## Repeat with WGS data using Kraken to create a taxon table:

First, change directory to the `wgs-kraken` directory
```bash
cd ..
cd wgs-kraken
```

Load the Kraken module
```bash
module load kraken
```

Then create and enter a subdirectory for the kraken raw output tables.
```bash
mkdir kraken-output
cd kraken-output/
```

Run Kraken on each input file. In the future, we will write a `for` loop for this so that we don't have to enter each file manually.

```bash
kraken2 --db /home/knightsd/public/minikraken2_v1_8GB --use-mpa-style --output tmp --report CS.079.kreport2 -use-names ../../../01_preprocessing/wgs-output/CS.079.S37.001.fa.fna
kraken2 --db /home/knightsd/public/minikraken2_v1_8GB --use-mpa-style --output tmp --report CS.145.kreport2 -use-names  ../../../01_preprocessing/wgs-output/CS.145.S1.001.fa.fna
kraken2 --db /home/knightsd/public/minikraken2_v1_8GB --use-mpa-style --output tmp --report CS.146.kreport2 -use-names  ../../../01_preprocessing/wgs-output/CS.146.S12.001.fa.fna 
kraken2 --db /home/knightsd/public/minikraken2_v1_8GB --use-mpa-style --output tmp --report CS.165.kreport2 -use-names  ../../../01_preprocessing/wgs-output/CS.165.S59.001.fa.fna 
kraken2 --db /home/knightsd/public/minikraken2_v1_8GB --use-mpa-style --output tmp --report CS.166.kreport2 -use-names  ../../../01_preprocessing/wgs-output/CS.165.S59.001.fa.fna 
kraken2 --db /home/knightsd/public/minikraken2_v1_8GB --use-mpa-style --output tmp --report CS.222.kreport2 -use-names  ../../../01_preprocessing/wgs-output/CS.222.S15.001.fa.fna
kraken2 --db /home/knightsd/public/minikraken2_v1_8GB --use-mpa-style --output tmp --report T.CS.008.kreport2 -use-names  ../../../01_preprocessing/wgs-output/T.CS.008.S40.001.fa.fna
kraken2 --db /home/knightsd/public/minikraken2_v1_8GB --use-mpa-style --output tmp --report T.CS.018.kreport2 -use-names  ../../../01_preprocessing/wgs-output/T.CS.018.S17.001.fa.fna
kraken2 --db /home/knightsd/public/minikraken2_v1_8GB --use-mpa-style --output tmp --report T.CS.030.kreport2 -use-names  ../../../01_preprocessing/wgs-output/T.CS.030.S84.001.fa.fna
```

Merge the separate Kraken outputs to a single table
```bash
# Now we have a single output file per sample;
# we can merge these using a tool from metaphlan2.py
module load metaphlan2
merge_metaphlan_tables.py *.txt > merged.txt
```

 ## Appendix
 
Kraken2 and Bracken can also be run on the _16S_ data. For reference, here is how.
```bash
# download SILVA database from Ben Langmead
# https://benlangmead.github.io/aws-indexes/k2
# Specifically, [SILVA v138 99% ID](https://genome-idx.s3.amazonaws.com/kraken/16S_Silva138_20200326.tgz)
# is already located here: /home/knightsd/public/kraken/16s/silva/16S_SILVA138_k2db

# generate stitched, trimmed, per-sample FASTQ files with SHI7
python3 /home/knightsd/public/shi7/shi7.py -i /home/knightsd/public/imp-16s-shallow/ -o 16s-output-fastq-sep --convert_fasta False --combine_fasta False

# Run kraken on each per-sample FASTQ files
module load kraken
module load bracken
time kraken2 --db /home/knightsd/public/kraken/16s/silva/16S_SILVA138_k2db --threads 4 --report kraken/CS.126.kreport2 CS.126.fa.fq > kraken/CS.126.kraken2
bracken -d /home/knightsd/public/kraken/16s/silva/16S_SILVA138_k2db -i kraken/CS.126.kreport2 -o bracken/CS.126.bracken -w bracken/CS.126.bracken.kreport2 -r 250 -l G

# the data can then be compiled into a taxonomy table using this script: https://github.com/sipost1/kraken2OTUtable/blob/main/kraken2otu.py
```

Dada2 can be run on the 16s data to pick amplicon sequence variants (ASVs) using QIIME2 as follows. The sequence data need to be imported into QIIME2. There are various approaches, but an easy one is just to have all of one's fastq files in the following file format: `sampleID_1_L001_R1_001.fastq.gz` or `sampleID_1_L001_R2_001.fastq.gz`. If one has files with this format: `Sample1_Sxxx_R1_001.fastq`, one can modify these to the correct format with:
```bash
# Don't run this -- just for future reference
# for f in *.fastq.gz; do echo $f; mv $f "$(echo "${f}" | sed 's/_S[0-9][0-9]*_R\([1-2]\)/_1_L001_R\1/')"; done
```

There is already a version of the 16s data with the files in the correct format in the folder `/home/knightsd/public/imp/16s-shallow-for-dada2`. Therefore we can move ahead with importing the data, and running dada2 using QIIME2.

```bash
# Unload the QIIME 1.9 module, and load the QIIME2 module:
module unload qiime/1.9.1_centos7
module load qiime2

# Import the data
qiime tools import --input-path /home/knightsd/public/imp/16s-shallow-for-dada22/  --output-path seqs.qza --type 'SampleData[PairedEndSequencesWithQuality]' --input-format CasavaOneEightSingleLanePerSampleDirFmt

# then run Dada2
# Need to choose the start position/truncation length for the forward and reverse reads
# Below we have 5 and 200 for each
# these were chosen by running fastqc on the raw data and then viewing the
# resulting HTML files in a browser
time qiime dada2 denoise-paired --i-demultiplexed-seqs seqs.qza --p-n-threads 0 --p-trim-left-f 5 --p-trim-left-r 5 --p-trunc-len-f 200 --p-trunc-len-r 200 --o-representative-sequences rep-seqs-dada2.qza --o-table table-dada2.qza --o-denoising-stats stats-dada2.qza

# extract the otu table summary stats and view the depths file
# this is used to determine rarefaction depth later
# Note the lowest depths are at the bottom, hence we use "tail -n 30"
# Could also use less to view the whole file
time qiime tools extract --input-path table-dada2.qzv --output-path table-dada2
tail -n 30 table-dada2/*/data/sample-frequency-detail.csv

# Build tree
qiime phylogeny align-to-tree-mafft-fasttree --i-sequences rep-seqs-dada2.qza --o-alignment aligned-rep-seqs.qza --o-masked-alignment masked-aligned-rep-seqs.qza --o-tree unrooted-tree.qza --o-rooted-tree rooted-tree.qza --output-dir tree

# Run core diversity analysis
# Note: this has a very low rarefaction depth (300) set!
# that is for tutorial purposes only. Need to determine the
# appropriate depth by summarizing the otu table as shown above.
time qiime diversity core-metrics-phylogenetic --i-phylogeny rooted-tree.qza --i-table table-dada2.qza --p-sampling-depth 300 --m-metadata-file map.txt --output-dir core-metrics-results

# to get the data out in tab-delimited format (to read in to R, for example):
mkdir core-metrics-export

# export the OTU table and convert to tab-delimited format.
qiime tools export --input-path table-dada2.qza --output-path table
biom convert --to-tsv -i table/feature-table.biom -o core-metrics-export/otu-table.tsv
mv table/feature-table.biom core-metrics-export/otu-table.biom

# export the rarefied OTU table as well
qiime tools export --input-path core-metrics-results/rarefied_table.qza --output-path core-metrics-results/table_export
biom convert --to-tsv -i core-metrics-results/table_export/feature-table.biom -o core-metrics-export/otu-table-rarefied.tsv
mv core-metrics-results/table_export/feature-table.biom core-metrics-export/otu-table-rarefied.biom

# export each distance metric/diversity metric
qiime tools export --input-path core-metrics-results/shannon_vector.qza --output-path core-metrics-results/shannon_export
qiime tools export --input-path core-metrics-results/observed_otus_vector.qza --output-path core-metrics-results/observed_otus_export
qiime tools export --input-path core-metrics-results/faith_pd_vector.qza --output-path core-metrics-results/faith_pd__export
qiime tools export --input-path core-metrics-results/bray_curtis_distance_matrix.qza --output-path core-metrics-results/bray_curtis_export
qiime tools export --input-path core-metrics-results/jaccard_distance_matrix.qza --output-path core-metrics-results/jaccard_export
qiime tools export --input-path core-metrics-results/unweighted_unifrac_distance_matrix.qza --output-path core-metrics-results/unweighted_unifrac_export
qiime tools export --input-path core-metrics-results/weighted_unifrac_distance_matrix.qza --output-path core-metrics-results/weighted_unifrac_export

# move and rename each file to the core-metrics-export folder
mkdir core-metrics-export/alpha
mv core-metrics-results/shannon_export/alpha-diversity.tsv core-metrics-export/alpha/shannon.tsv
mv core-metrics-results/observed_otus_export/alpha-diversity.tsv core-metrics-export/alpha/observed_otus.tsv
mv core-metrics-results/faith_pd__export/alpha-diversity.tsv core-metrics-export/alpha/faith_pd.tsv

mkdir core-metrics-export/beta
mv core-metrics-results/unweighted_unifrac_export/distance-matrix.tsv core-metrics-export/beta/unweighted_unifrac-distance-matrix.tsv
mv core-metrics-results/weighted_unifrac_export/distance-matrix.tsv core-metrics-export/beta/weighted_unifrac-distance-matrix.tsv
mv core-metrics-results/jaccard_export/distance-matrix.tsv core-metrics-export/beta/jaccard-distance-matrix.tsv
mv core-metrics-results/bray_curtis_export/distance-matrix.tsv core-metrics-export/beta/bray_curtis-distance-matrix.tsv

# export the tree
qiime tools export --input-path rooted-tree.qza --output-path rooted-tree-export
mv rooted-tree-export/tree.nwk core-metrics-export/tree.nwk

# switch to QIIME 1, make 3d plot (although there are some buried in one of the .qza files of QIIME2)
principal_coordinates.py -i core-metrics-results/weighted_unifrac-distance-matrix.tsv -o core-metrics-results/weighted_unifrac_pc.txt
time make_emperor.py -i core-metrics-results/weighted_unifrac_pc.txt -m map.txt -o core-metrics-results/3dplots-weighted-unifrac
```

    
Note: In bash/unix, if something didn't work right and you need to remove a file, use "rm"
```bash
   rm file_to_remove.txt
    
   # if you need to remove a directory:
   rm -r directory_to_remove
```
