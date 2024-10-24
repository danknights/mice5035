## MiCE 5035 Tutorial: Data cleaning in R

### Background
This tutorial is an introduction to loading, filtering, and visualizing microbiome data in _R_.

### Requirements
You must have R and RStudio installed as described in the [Getting Started Guide](../../README.md).

### Tutorial

#### Open RStudio and start a new Project
Click the "Project" dropdown in the top right; In the resulting popup window, click "New Directory", "New Project", and then name the directory "Tutorials_04_05". You should place it in a folder on your computer where you know how to find it, and you know it will be backed up safely, with Google Drive, DropBox, or OneDrive, for example. If you are not using automatic backups to protect your work, please do so! The University of Minnesota provides [free storage on Google Drive](https://it.umn.edu/services-technologies/google-drive-desktop) using your University Google account.

#### Install some needed packages
Click in the bottom left window. This is the console where you can run R commands interactively. For this tutorial we will need the `car` package and the `vegan` package. Install the `vegan` package like this:
```bash
install.packages('vegan')
```
If that proceeds without errors, then install the `car` package:
```bash
install.packages('car')
```

#### Download and clean up the Immigration Microbiome Project data
We will download all of the output files from the [Immigration Microbiome Project code repository](https://github.com/knights-lab/IMP_analyses).

Create a new R file called `download_data.r`. On a Mac, you can do this with "File", "New File", "R Script". Windows should be similar. You should now have a blank text file open in the top left quadrant of the display. Paste these commands into the file, then click the "Source" above the file to run all of them. Note that we transposed the OTU table and taxon tables so that the samples are in the rows, and the features are in the columns. Also note: the `<-` is an assignment operator. It stores the output of the command on the right in the variable on the left.
```bash
map <- read.delim(url('https://raw.githubusercontent.com/knights-lab/IMP_analyses/master/data/map.txt?raw=true'),row=1)
otus <- t(read.delim(url('https://github.com/knights-lab/IMP_analyses/blob/master/data/denovo/final_otu.txt?raw=true'),row=1))
alpha <- read.delim(url('https://raw.githubusercontent.com/knights-lab/IMP_analyses/master/data/denovo/alpha.txt?raw=true'),row=1)
beta_uuf <- read.delim(url('https://raw.githubusercontent.com/knights-lab/IMP_analyses/master/data/denovo/unweighted_unifrac_dm.txt?raw=true'),row=1)
beta_wuf <- read.delim(url('https://raw.githubusercontent.com/knights-lab/IMP_analyses/master/data/denovo/weighted_unifrac_dm.txt?raw=true'),row=1)
phylum <- t(read.delim(url('https://github.com/knights-lab/IMP_analyses/blob/master/data/denovo/taxatable_L2.txt?raw=true'),row=1))
genus <- t(read.delim(url('https://github.com/knights-lab/IMP_analyses/blob/master/data/denovo/taxatable_L6.txt?raw=true'),row=1))
```

Each of these objects is now a data table with samples in rows. Think spreadsheet or matrix. The beta diversity tables also have samples in the columns, of course. We can inspect each table by clicking "Environment" in the top right panel, and then click on the object.

#### Exercises
Answer these questions about the data tables:
1. How many samples are there?
2. How many OTUs (hint: you can run `dim(otus)` to get the dimensions)?
3. How many distinct genera (hint: you can run `dim(genus)` to get the dimensions)?
4. Are there any _continuous_ (not categorical) variables in the mapping file (metadata) that you expect to be related to the microbiome?

The bottom left quadrant is the console. When you enter a command, _R_ evaluates the command and prints the result. We can use the console to run commands that we don't need to save permanently in our source file.

We can access an individual element in a table with square brackets `[]`. For example, this prints the relative abundance of the 9th genus in the 10th sample:
```bash
genus[10,9]
```

We can also access a arange of elements in a table by passing in a vector of numerical indices, or a vector of TRUE/FALSE values. For example, this prints the first 3 rows and first 6 columns of the map table. The `1:6` expression is shorthand for 1, 2, 3, 4, 5, 6. 
```bash
map[1:3,1:6]
```

<!--
..and this prints the first 3 rows and columns 1, 2, 3, and 6. The `c()` function concatenates individual values (the TRUE's and FALSE's) into a vector:
```bash
map[1:3,c(TRUE, TRUE, TRUE, FALSE, FALSE, TRUE)]
```
-->

There is another important and convenient way that we can access data in a table. R allows tables to have row names and column names, and these can be used to access data. For example, if we want to print out the `Sample.Group` column in the `map` table, there are two different ways:
```bash
map$Sample.Group
map[,"Sample.Group"]
```

Before we continue, we need to "clean up" the data in a few ways:
1. Remove longitudinal samples from the metadata table (`map`)
2. Ensure that all of the tables have the same samples in the same order
3. Shorten the column names in the genus and phylum table for clarity
4. Make a new column "Generation" that shows only Thai/1st/2nd/Control
5. Save the refined tables to your local hard drive.

To read about how we do these steps in detail, for future reference, click [here](detailed_cleaning.md). For now, you can just paste the commands into your `download_data.r` file, and execute:

```bash
# Remove logitudinal samples (those with Sample.Order > 1)
keep.ix <- is.na(map$Sample.Order) | map$Sample.Order==1
map <- map[keep.ix,]

# Ensure each table has the same sample IDs (rownames)
common.sampleIDs <- intersect(rownames(map),rownames(otus))
map <- map[common.sampleIDs,]
otus <- otus[common.sampleIDs,]
alpha <- alpha[common.sampleIDs,]
beta_uuf <- beta_uuf[common.sampleIDs,common.sampleIDs]
beta_wuf <- beta_wuf[common.sampleIDs,common.sampleIDs]
genus <- genus[common.sampleIDs,]
phylum <- phylum[common.sampleIDs,]

# Shorten the taxonomy names
colnames(genus) <- sapply(strsplit(colnames(genus),";"),function(xx) xx[length(xx)])
colnames(phylum) <- sapply(strsplit(colnames(phylum),";"),function(xx) xx[length(xx)])

# Make a new "Generation" column that shows Thai/1st/2nd/Control
map$Generation <- "Thai" # fill with Thai to start
map$Generation[map$Sample.Group == "Karen1st" | map$Sample.Group == "Hmong1st"] <- "1stGen"
map$Generation[map$Sample.Group == "Hmong2nd"] <- "2ndGen"
map$Generation[map$Sample.Group == "Control"] <- "Control"
map$Generation <- factor(map$Generation, levels=c('Thai','1stGen','2ndGen','Control'))

# Save the tables to your local hard drive
write.table(map,'map.txt',quote=F,col.names=TRUE,row.names=TRUE,sep="\t")
write.table(otus,'otu_table.txt',quote=F,col.names=TRUE,row.names=TRUE,sep="\t")
write.table(alpha,'alpha.txt',quote=F,col.names=TRUE,row.names=TRUE,sep="\t")
write.table(beta_uuf,'beta_uuf.txt',quote=F,col.names=TRUE,row.names=TRUE,sep="\t")
write.table(beta_wuf,'beta_wuf.txt',quote=F,col.names=TRUE,row.names=TRUE,sep="\t")
write.table(genus,'genus.txt',quote=F,col.names=TRUE,row.names=TRUE,sep="\t")
write.table(phylum,'phylum.txt',quote=F,col.names=TRUE,row.names=TRUE,sep="\t")
```

Continue to [tutorial 5](../05_visualization_in_R).

