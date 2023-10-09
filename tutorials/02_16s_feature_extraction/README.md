## MiCE 5035 Tutorial: 16s feature extraction

### Background
This tutorial is an introduction to extracting taxonomic features from 16S sequencing data, and 
performing alpha diversity and beta diversity analysis. 

Some of this tutorial uses QIIME 1.9.1 to perform basic analysis. QIIME2 provides 
more options for visualizations but performs mostly the same core analyses and has a steeper learning curve.

### Connect to an interactive computing node on MSI
- Follow the steps the [logging in guide](../../logging_in.md) to get connected to an interactive node on MSI.

### Tutorial

1. Load software  
 Load all of the software "modules" that you will need.
 ```bash
    module load qiime/1.9.1_centos7
    module load bowtie2
 ```
 
2. Navigate to the correct directory
Make sure that you are in your home directory inside the MICE 5035 course directory (`/home/mice5035`), and not your default home directory if you have another one. As a reminder, the following command will list your current directory:
 ```bash
    pwd
 ```

Change directory in to the course repo and then into the directory for this tutorial. Ensure you have the latest files from the github repository with `git pull`.
 ```bash
    cd mice5035
    cd tutorials/02_16s_feature_extraction
    ls
    git pull
 ```

Let's set up two folders for our analyses: closed-ref 16S OTUs, and de novo 16S OTUs, so that we can keep our files organized.
 ```bash
    mkdir 16s-closed-ref
    mkdir 16s-de-novo
 ```

Change directory into the 16s-closed-ref directory.
```bash
    cd 16s-closed-ref
 ```

3. Examine the sequencing data
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

4. Pick Operational Taxonomic Units (OTUs) (Closed-reference)
 We will start with closed-reference OTU picking. This means we will find the closest match for each sequence in a reference database using NINJA-OPS. We can also use the QIIME `pick_closed_reference_otus.py` workflow script, but NINJA-OPS is faster.

Note: The default reference database is Greengenes version 13_8, which is now 10 years old. There is a newer Greengenes database, but there is no publicly shared clustered version (OTUs picked on the reference database), only the raw database, which as 20m+ sequences. [Silva](https://www.arb-silva.de/) has alternative 16S databases clustered at the 99% level, but they do not make it easy to download a pre-built phylogeny for their representative sequences. NCBI has a nice alternative in the [RefSeq targeted locus project](https://www.ncbi.nlm.nih.gov/refseq/targetedloci/), but again, no phylogeny is provided. Therefore, for ease of use, we are using the old Greengenes 97% representative sequences and phylogeny.

 ```bash
    python /home/knightsd/public/mice5035/NINJA-OPS-1.5.1/bin/ninja.py -i ../../01_preprocessing/16s-output/combined_seqs.fna -o otus -p 4 -z -m normal
    ls otus

    # rename the output table so that it is consistent with other QIIME commands
    mv otus/ninja_otutable.biom otus/otu_table.biom
 ```
 
 Make a text-based version of the OTU table and print out the first 10 rows (with `head`) and the first 10 columns (with `cut`):
 ```bash
    biom convert -i otus/otu_table.biom -o otus/otu_table.txt --to-tsv

    head otus/otu_table.txt | cut -f 1-10
 ```

 Get a nice summary of the OTU table, and inspect the first 30 lines using `head`. Can you find a good depth cutoff for rarefaction?
 ```bash
    biom summarize-table -i otus/otu_table.biom -o otus/stats.txt
    head -n 30 otus/stats.txt
 ```

 5. Rarefy and filter the OTU table
 We will subsample the observations in each sample so that they have the same effective sequencing depth. This controls for differences in alpha diversity and beta diversity that might show up as artifacts if one group of samples had much higher depth than another. We will use a depth of 140 chosen by inspecting the `stats.txt` file above. In a full data set, this would be much higher.

 ```bash
    single_rarefaction.py -i otus/otu_table.biom -d 140 -o otus/otu_table_rarefied.biom
 ```

 Remove OTUs not present in at least 4 samples (in practice we might choose 10% or 25% of all samples).
 ```bash
   filter_otus_from_otu_table.py -i otus/otu_table_rarefied.biom -o otus/otu_table_final.biom -s 4
 ```

6. Collapse OTUs at different taxonomic levels for later taxonomic analysis
```bash
summarize_taxa.py -i otus/otu_table_final.biom -o taxon_tables --level 2,3,4,5,6,7
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
    make_emperor.py -i beta/weighted_unifrac_otu_table_final_pc.txt -m ../../../data/imp/map.txt -o 3dplots-weighted-unifrac
 ```

11. Move the files back from MSI to your computer using Filezilla  
 See instructions on [Getting Started Guide](../../README.md) to connect to MSI using Filezilla. Navigate to `/home/mice5035/yourusername/mice5035/tutorials/02_16s_feature_extraction/`. Then drag the `alpha-diversity.txt` file and `beta`, `otus`, and `taxon_tables` folders over to your local computer.
 
 ![Filezilla example](https://raw.githubusercontent.com/danknights/mice5992-2017/master/supporting_files/qiime_tutorial_FTP_screenshot.png "Filezilla example")

We now have all of the basic features and tables that we will want to use for statistical testing: OTU tables, taxonomy tables, alpha diversity analysis, and beta diversity analyses.

## Repeat with de-novo OTU picking

First, change directory to the `16s-de-novo` directory
```bash
cd ..
cd 16s-de-novo
```

To pick de novo OTUs:
```bash
   # This will take around 5 minutes
   pick_de_novo_otus.py -i ../../01_preprocessing/16s-output/combined_seqs.fna -o otus -O 4 -v -a
```

Then proceed with steps 5-11 above.

Note: you will need to use the de novo tree `otus/rep_set.tre` rather than the reference tree in the beta diversity step. 

Note: we will use the same rarefaction depth (140) as in the closed-reference analysis above. In practice, you would run `biom summarize-table` to get summary statistics about the OTU table, and then you would use that output to choose an appropriate rarefaction depth. 

```bash
biom summarize-table -i otus/otu_table.biom -o otus/stats.txt
biom convert -i otus/otu_table.biom -o otus/otu_table.txt --to-tsv
single_rarefaction.py -i otus/otu_table.biom -d 140 -o otus/otu_table_rarefied.biom
filter_otus_from_otu_table.py -i otus/otu_table_rarefied.biom -o otus/otu_table_final.biom -s 4
summarize_taxa.py -i otus/otu_table_final.biom -o taxon_tables --level 2,3,4,5,6,7
alpha_diversity.py -m "chao1,observed_otus,shannon,PD_whole_tree" -i otus/otu_table_final.biom -t otus/rep_set.tre -o alpha-diversity.txt
beta_diversity.py -i otus/otu_table_final.biom -o beta -m "unweighted_unifrac,weighted_unifrac,bray_curtis,binary_jaccard" -t otus/rep_set.tre
principal_coordinates.py -i beta/weighted_unifrac_otu_table_final.txt -o beta/weighted_unifrac_otu_table_final_pc.txt
make_emperor.py -i beta/weighted_unifrac_otu_table_final_pc.txt -m ../../../data/imp/map.txt -o 3dplots-weighted-unifrac
```

 ### Additional exercises
1. Explore the options for the `pick_de_novo_otus.py` by running it with `-h`. Change one parameter setting, and send the output to a new folder. Then examine the output OTU table and describe the differences from the original de-novo table. If possible, explain why changing that parameter changed the OTU table in that way.

2. Run Dada2 or Kraken on the input data, as follows:
   
Dada2 can be run on the 16s data to pick amplicon sequence variants (ASVs) using QIIME2 as follows.

The raw sequence data need to be imported into QIIME2. There are various approaches to importing data, but an easy one is just to have all of one's fastq files in the following file format: `sampleID_1_L001_R1_001.fastq.gz` or `sampleID_1_L001_R2_001.fastq.gz`. If one has files with this format: `Sample1_Sxxx_R1_001.fastq`, one can modify these to the correct format with:
```bash
# Don't run this -- just for future reference
# for f in *.fastq.gz; do echo $f; mv $f "$(echo "${f}" | sed 's/_S[0-9][0-9]*_R\([1-2]\)/_1_L001_R\1/')"; done
```

There is already a version of the 16s data with the files in the correct format in the folder `/home/knightsd/public/imp/16s-shallow-for-dada2`. Therefore we can move ahead with importing the data, and running dada2 using QIIME2.

```bash
# Unload the QIIME 1.9 module, and load the QIIME2 module:
module unload qiime/1.9.1_centos7
module load qiime2

# Make a new directory for Dada2 analysis and change into it
cd ..
mkdir 16s-dada2
cd 16s-dada2

# Import the data
qiime tools import --input-path /home/knightsd/public/imp/16s-shallow-for-dada2/  --output-path seqs.qza --type 'SampleData[PairedEndSequencesWithQuality]' --input-format CasavaOneEightSingleLanePerSampleDirFmt

# then run Dada2
# Need to choose the start position/truncation length for the forward and reverse reads
# Below we have 5 and 200 for each
# these were chosen by running fastqc on the raw data and then viewing the
# resulting HTML files in a browser.
# This will take around 5 minutes on the shallow data.
qiime dada2 denoise-paired --i-demultiplexed-seqs seqs.qza --p-n-threads 0 --p-trim-left-f 5 --p-trim-left-r 5 --p-trunc-len-f 200 --p-trunc-len-r 200 --o-representative-sequences rep-seqs-dada2.qza --o-table table-dada2.qza --o-denoising-stats stats-dada2.qza

# Summarize the depths of the table and use them to choose a rarefaction depth
qiime feature-table summarize --i-table table-dada2.qza --o-visualization table-dada2.qzv
qiime tools export --input-path table-dada2.qzv --output-path table-viz-export
# inspect the sample-frequency-detail.csv file to see depths
# 175 seems like a reasonable rarefaction depth
tail -n 30 table-viz-export/sample-frequency-detail.csv

# Build tree
qiime phylogeny align-to-tree-mafft-fasttree --i-sequences rep-seqs-dada2.qza --o-alignment aligned-rep-seqs.qza --o-masked-alignment masked-aligned-rep-seqs.qza --o-tree unrooted-tree.qza --o-rooted-tree rooted-tree.qza --output-dir tree

# Run core diversity analysis
# Note: this has a very low rarefaction depth (300) set!
# that is for tutorial purposes only. Need to determine the
# appropriate depth by summarizing the otu table as shown above.
qiime diversity core-metrics-phylogenetic --i-phylogeny rooted-tree.qza --i-table table-dada2.qza --p-sampling-depth 175 --m-metadata-file ../../../data/imp/map.txt --output-dir core-metrics-results

# export the OTU table and convert to tab-delimited format. Rename for convenience.
qiime tools export --input-path table-dada2.qza --output-path otus
mv otus/feature-table.biom otus/otu_table.biom

# export the tree in case we need it later
qiime tools export --input-path rooted-tree.qza --output-path rooted-tree-export

# Now that we have the OTU table and tree, switch to QIIME 1, proceed as above
module unload qiime2
module load qiime/1.9.1_centos7

biom summarize-table -i otus/otu_table.biom -o otus/stats.txt
biom convert -i otus/otu_table.biom -o otus/otu_table.txt --to-tsv
single_rarefaction.py -i otus/otu_table.biom -d 175 -o otus/otu_table_rarefied.biom
filter_otus_from_otu_table.py -i otus/otu_table_rarefied.biom -o otus/otu_table_final.biom -s 4
alpha_diversity.py -m "chao1,observed_otus,shannon,PD_whole_tree" -i otus/otu_table_final.biom -t rooted-tree-export/tree.nwk-o alpha-diversity.txt
beta_diversity.py -i otus/otu_table_final.biom -o beta -m "unweighted_unifrac,weighted_unifrac,bray_curtis,binary_jaccard" -t rooted-tree-export/tree.nwk
principal_coordinates.py -i beta/weighted_unifrac_otu_table_final.txt -o beta/weighted_unifrac_otu_table_final_pc.txt
make_emperor.py -i beta/weighted_unifrac_otu_table_final_pc.txt -m ../../../data/imp/map.txt -o 3dplots-weighted-unifrac
```

Kraken2 and Bracken can be run on the _16S_ data (paper here)[https://microbiomejournal.biomedcentral.com/articles/10.1186/s40168-020-00900-2]. For reference, here is how.
```bash
# download SILVA database from Ben Langmead
# https://benlangmead.github.io/aws-indexes/k2
# Specifically, [SILVA v138 99% ID](https://genome-idx.s3.amazonaws.com/kraken/16S_Silva138_20200326.tgz)
# is already located here: /home/knightsd/public/kraken/16s/silva/16S_SILVA138_k2db

# load modules
module load kraken
module load bracken

# make and enter sub-directory
mkdir 16s-kraken
cd 16s-kraken

# generate stitched, trimmed, per-sample FASTQ files with SHI7
python3 /home/knightsd/public/shi7/shi7.py -i /home/knightsd/public/imp/16s-shallow/ -o 16s-output-fastq-sep --convert_fasta False --combine_fasta False
# unfortunately we have an extra ".fa" in each sample name; remove with this
for f in 16s-output-fastq-sep/*.fq; do echo $f; mv $f "$(echo "${f}" | sed 's/.fa.fq/.fq/')"; done

# Run kraken on each per-sample FASTQ files
mkdir kraken-out
mkdir bracken-out
for f in 16s-output-fastq-sep/*.fq; do
  echo $f;
  sampleid=`basename $f .fq`;
  kraken2 --db /home/knightsd/public/kraken/16s/silva/16S_SILVA138_k2db --threads 4 --report kraken-out/${sampleid}.kreport2 $f > kraken-out/${sampleid}.kreport2
  bracken -d /home/knightsd/public/kraken/16s/silva/16S_SILVA138_k2db -i kraken-out/${sampleid}.kreport2 -o bracken-out/${sampleid}.bracken -w bracken-out/${sampleid}.bracken.kreport2 -r 250 -l G;
done

# the "bracken.kreport2" output files in the bracken-out folder then need to be converted to mpa format (Metaphlan format?).
# We can do this with a script from https://github.com/jenniferlu717/KrakenTools
wget https://github.com/jenniferlu717/KrakenTools/raw/master/kreport2mpa.py
for f in bracken-out/*.bracken.kreport2; do python kreport2mpa.py -r $f -o bracken-out/`basename $f .bracken.kreport2`.mpa; done

# then we need to merge all of the mpa files into one table, with sampleIDs as the column headers.
# we will use our own script for this
python ../../../scripts/kraken2table.py bracken-out/*.mpa taxon_tables

# Finally, convert taxon tables to biom format for use instead of OTU table in QIIME
for f in taxon_tables/*.txt; do echo $f; biom convert -i $f --to-json -o `dirname $f`/`basename $f .txt`.biom --process-obs-metadata taxonomy; done

```

### Random tip on deleting files    
Note: In bash/unix, if something didn't work right and you need to remove a file, use "rm"
```bash
   rm file_to_remove.txt
    
   # if you need to remove a directory:
   rm -r directory_to_remove
```

### Next: Tutorial 3
When you are finished, move on to [Tutorial 03, WGS Feature Extraction](../03_wgs_feature_extraction)
