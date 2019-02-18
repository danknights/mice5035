## MiCE 5992 Tutorial: A/B testing with QIIME

### Background
In this tutorial we will learn how to run tests for statistical significance of alpha diversity, beta diversity, and taxonomic profile using QIIME.

### Setup
1. Connect to MSI.
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

Then change directories into the course repository folder that you downloaded:
 ```bash
    cd mice5992-2017
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
 
 
 Then change directories into the new tutorial folder:
 ```bash
    cd tutorials
    cd abtesting
 ```

 List the contents of the directory:
 ```bash
    ls
 ```

 Install some needed packages in R. You only have to do this one time. First start `R`:

 ```bash
    R
 ```

 Then run the installation command and answer `y` to any questions.
 ```R
    install.packages(c('optparse','vegan','randomForest'),repo='http://cran.wustl.edu',dep=TRUE)
 ```

 Quit `R` with `q()`:
 
 ```R
    q()
 ```
 
 
## Overview
This tutorial folder already contains the folders `alphaplots`, `betaplots`, `taxaplots` that come from the [Core diversity tutorial](../corediv).

There are three types of statistical testing that we will be doing in QIIME: taxonomic profiles, beta diversity, and alpha diversity.

## Taxonomic profile significance.

The goal of these tests is to answer the question: Is any species statistically associated with a particular experimental variable?

There are three different types of experimental variables that matter for these tests, each with a different test in QIIME:

1. Discrete variable with two groups (in the example data, AGE_GROUP has two groups). Use QIIME script [`group_significance.py`](http://qiime.org/scripts/group_significance.html) with flag `-s mann_whitney_u`. This uses the [Mann-Whitney U test](https://en.wikipedia.org/wiki/Mann%E2%80%93Whitney_U_test), which is a non-parametric test for different means across two groups (like a t-test). The non-parametric test is most reliable for microbiome data due to the many different types of distributions taxa and genes can have across microbiomes.

 Run an example:

 ```bash
    group_significance.py -i taxaplots/ninja_otutable_s10_min500_L6.biom -m ../../data/globalgut/map.txt -c AGE_GROUP -o genus_age_group_significance.txt -s mann_whitney_u
 ```
 
 Print the top single most significant genus:
 
 ```bash
    head -n 2 genus_age_group_significance.txt
 ```
 
 Were any of the test significant? Use the third column, FDR_P.
 
 Is it higher or lower in adults? Use the last two columns.

2. Discrete variable with more than two groups (in the example data, COUNTRY has three groups). Use QIIME script [`group_significance.py`](http://qiime.org/scripts/group_significance.html) with the default method. Here the default method is the [Kruskal-Wallis test](https://en.wikipedia.org/wiki/Kruskal%E2%80%93Wallis_one-way_analysis_of_variance), which is a non-parametric test for different means across three or more groups (like an ANOVA). A non-parametric tests is most reliable for microbiome data due to the many different types of distributions taxa and genes can have across microbiomes.

 Run an example:

 ```bash
    group_significance.py -i taxaplots/ninja_otutable_s10_min500_L6.biom -m ../../data/globalgut/map.txt -c COUNTRY -o genus_country_group_significance.txt -s kruskal_wallis
```

 Print the top 5 most significant genus:
 
 ```bash
    head -n 6 genus_country_group_significance.txt
 ```


3. Continuous variable (in the example data, AGE is continuous). Use QIIME script [`observation_metadata_correlation.py`](http://qiime.org/scripts/observation_metadata_correlation.html) with flag `-s spearman`. Spearman correlation is a non-parametric test.

 Run an example:

 ```bash
    observation_metadata_correlation.py -i taxaplots/ninja_otutable_s10_min500_L6.biom -m ../../data/globalgut/map.txt -c AGE -o genus_age_significance.txt -s spearman
 ```

 Print the top 5 most significant genus:
 
 ```bash
    head -n 6 genus_age_significance.txt
 ```


## Beta diversity significance.

The goal of these tests is to answer the question: Is overall microbiome variation statistically associated with a particular experimental variable?

We can test the same three different types of experimental variables as follows, using the same script and method. Use QIIME script [`compare_categories.py`](http://qiime.org/scripts/compare_categories.html) with flag `-s adonis`. This uses the `adonis` test in `R` (http://cc.oulu.fi/~jarioksa/softhelp/vegan/html/adonis.html), which is a non-parametric test for different means across groups, or for association of beta diversity distances with a continuous variable.

 Run an example:

 ```bash
    compare_categories.py -i betaplots/unweighted_unifrac_dm.txt -m ../../data/globalgut/map.txt -c COUNTRY -o beta_country_significance --method adonis
    compare_categories.py -i betaplots/unweighted_unifrac_dm.txt -m ../../data/globalgut/map.txt -c AGE -o beta_age_significance --method adonis
    compare_categories.py -i betaplots/unweighted_unifrac_dm.txt -m ../../data/globalgut/map.txt -c AGE_GROUP -o beta_age_group_significance --method adonis
 ```
 
 Print the significance testing results. The p-value is at the top right under `Pr(>F)`:
 
 ```bash
    cat beta_age_group_significance/adonis_results.txt
 ```
 
 Was the result significant? What does this mean?
 

## Alpha diversity significance.

The goal of this test is to answer the question: Is microbiome biodiversity (i.e. diversity within a sample) statistically associated with a particular experimental variable?

QIIME only currently has the ability to handle discrete variable testing for alpha diversity. Use QIIME script [`compare_alpha_diversity.py`](http://qiime.org/scripts/compare_alpha_diversity.html) with flag `-t parametric`. This runs a standard [Student's t-test](https://en.wikipedia.org/wiki/Student's_t-test) for each pair of groups. Alpha diversity tends to be more normally distributed within groups than individual taxa, so a t-test is usually acceptable.

 Run an example:

 ```bash
    compare_alpha_diversity.py -i alphaplots/alpha_div_collated/PD_whole_tree.txt -m ../../data/globalgut/map.txt -c COUNTRY -o alpha_country_significance -t parametric
    compare_alpha_diversity.py -i alphaplots/alpha_div_collated/PD_whole_tree.txt -m ../../data/globalgut/map.txt -c AGE_GROUP -o alpha_age_group_significance -t parametric
 ```
 
 Print the significance testing results. The p-value is at the top right:
 
 ```bash
    cat alpha_country_significance/COUNTRY_stats.txt
 ```
 
 Is the USA significantly more or less diverse than Malawi? Use the Group 1 mean, Group 2 mean, and p-value columns. Does this make sense?


8. Move the files back from MSI to your computer using Filezilla  
 See instructions on [Getting Started Guide](../../README.md) to connect to MSI using Filezilla. Navigate to `/home/mice5992/<yourusername>/mice5992-2017/tutorials/abtesting/`. Drag the `alpha_country_significance`, `alpha_age_group_significance`, `beta_age_group_significance`, `beta_age_significance`, `beta_country_significance`, `genus_age_group_significance.txt`, `genus_age_significance.txt`,`genus_country_group_significance.txt`, files and folders to your computer. Open any text files that you want to view in Excel with right-click --> Open with --> Excel. If you don't have Excel, you can create a new Google Sheet on Google Drive, and then use File --> Import to import the text file as a spreadsheet.
 
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
 
  Now run OTU picking and the core diversity analyses:
 ```bash
    python /home/mice5992/shared/NINJA-OPS-1.5.1/bin/ninja.py -i /home/knightsd/public/qiime_db/processed/Bushman_enterotypes_cafe_study_1010_ref_13_8/Bushman_enterotypes_cafe_study_1010_split_library_seqs.fna -o otus -p 4
    
    etc.
 ```

 **Note:** You will need to specify the full file path to whatever files you are using. These will be very long. For example, in the ninja.py command above, the full path to the sequences file is `/home/knightsd/public/qiime_db/processed/Bushman_enterotypes_cafe_study_1010_ref_13_8/Bushman_enterotypes_cafe_study_1010_split_library_seqs.fna`. The full path to the mapping file (metadata table) for that study is `/home/knightsd/public/qiime_db/processed/Bushman_enterotypes_cafe_study_1010_ref_13_8/Bushman_enterotypes_cafe_study_1010_mapping_file.txt`. These are examples of _absolute paths_ that begin with a `/` and specify the full file path starting at the very top of the file system. 

 You can also use _relative paths_ when it is easier. For example, when you run the core diversity analyses you will need a parameters file for some scripts. If you are in a folder called `bonus` inside the `corediv` tutorial folder, you can pass `-p ../parameters.txt` to reach the parameters file in the directory above your current directory using a _relative path_. Alternatively, you can use an absolute path, which will look something like this: `/home/mice5992/<yourusername>/mice5992-2017/tutorials/corediv/parameters.txt`.

 After you have finished running all core diversity analyses on another data set, use Filezilla/FTP to move the outputs over to your computer. Also move the mapping file for that data set over to your computer, and open with Excel (or Google Sheets as described above). Use these visualizations to find a category that is interesting to run significance test againsts. Then proceed with significance testing using taxonomic profiles, alpha diversity profiles, and beta diversity profiles as described in this tutorial.

