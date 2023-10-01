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
    biom summarize-table -i otus/ninja_otutable.biom -o otus/stats.txt
    head -n 20 otus/stats.txt
 ```

 Make a text-based version of the OTU table and print out the first 10 rows (with `head`) and the first 5 columns (with `cut`):
 ```bash
    biom convert -i otus/ninja_otutable.biom -o otus/ninja_otutable.txt --to-tsv

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


 ## Appendix
 
Kraken2 and Bracken can also be run on the 16S data. For reference, here is how.
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

Dada2 can be run using QIIME2 to pick amplicon sequence variants (ASVs).

Then the sequence data need to be imported into QIIME2. There are various approaches, but an easy one is just to have all of one's fastq files in the following file format: `sampleID_1_L001_R1_001.fastq.gz` or `sampleID_1_L001_R2_001.fastq.gz`. If one has files with this format: `Sample1_Sxxx_R1_001.fastq`, one can modify these to the correct format with:
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
mv core-metrics-results/faith_pd__export/alpha-diversity.tsv core-metrics-export/alpha/faith_pd_.tsv

mkdir core-metrics-export/beta
mv core-metrics-results/unweighted_unifrac_export/distance-matrix.tsv core-metrics-export/beta/unweighted_unifrac-distance-matrix.tsv
mv core-metrics-results/weighted_unifrac_export/distance-matrix.tsv core-metrics-export/beta/weighted_unifrac-distance-matrix.tsv
mv core-metrics-results/jaccard_export/distance-matrix.tsv core-metrics-export/beta/jaccard-distance-matrix.tsv
mv core-metrics-results/bray_curtis_export/distance-matrix.tsv core-metrics-export/beta/bray_curtis-distance-matrix.tsv
```

