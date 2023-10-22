## MiCE 5035 Tutorial: Data cleaning and visualization in R

### Background
This tutorial is an introduction to loading, filtering, and visualizing microbiome data in _R_.

### Requirements
You must have R and RStudio installed as described in the [Getting Started Guide](../../README.md).

### Tutorial

1. Open RStudio and start a new Project
Click the "Project" dropdown in the top right; In the resulting popup window, click "New Directory", "New Project", and then name the directory "Tutorials_04_05". You should place it in a folder on your computer where you know how to find it, and you know it will be backed up safely, with Google Drive, DropBox, or OneDrive, for example. If you are not using automatic backups to protect your work, please do so! The University of Minnesota provides [free storage on Google Drive](https://it.umn.edu/services-technologies/google-drive-desktop) using your University Google account.
 
2. Download and clean up the Immigration Microbiome Project data
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

#### Exercise
Answer these questions about the data tables:
1. How many samples are there?
2. How many OTUs?
3. How many distinct genera?
4. Are there any _continuous_ (not categorical) variables in the mapping file (metadata) that you expect to be related to the microbiome?

We need to remove the longitudinal subjects. These are subjects that have `NA` or `1` in the "Sample.Order" column in the mapping file. Note: the `|` means "or" and it makes keep.ix TRUE for every row where either the value is `NA` or `1`.
keep.ix <- is.na(map$Sample.Order) | map$Sample.Order==1
map <- droplevels(map[keep.ix,])

Make sure each table has the same samples in the exact same order. This is a critical step that you must do before analyzing almost any data set!
```bash
common.rownames <- rownames(map)
common.rownames <- intersect(rownames(otus), common.rownames)
common.rownames <- intersect(rownames(alpha), common.rownames)
map <- map[common.rownames,]
otus <- otus[common.rownames,]
alpha <- alpha[common.rownames,]
beta_uuf <- beta_uuf[common.rownames,common.rownames]
beta_wuf <- beta_wuf[common.rownames,common.rownames]
genus <- genus[common.rownames,]
phylum <- phylum[common.rownames,]
```

Note that the taxonomy names are long and hard to read. Let's shorten them. You don't need to understand how this command works.
```bash
colnames(genus) <- sapply(strsplit(colnames(genus),";"),function(xx) xx[length(xx)])
colnames(phylum) <- sapply(strsplit(colnames(phylum),";"),function(xx) xx[length(xx)])
```

Let's make a new column that is just "Generation" (Thai/1st/2nd/Control)
map$Generation <- "Thai" # fill with Thai to start
map$Generation[map$Sample.Group == "Karen1st" | map$Sample.Group == "HmongThai"] <- "1stGen"
map$Generation[map$Sample.Group == "Hmong2nd"] <- "2ndGen"
map$Generation[map$Sample.Group == "Control"] <- "Control"
map$Generation <- factor(map$Generation, levels=c('Thai','1stGen','2ndGen','Control'))

# save these
write.table(map,'map.txt',quote=F,col.names=TRUE,row.names=TRUE,sep="\t")
write.table(otus,'otu_table.txt',quote=F,col.names=TRUE,row.names=TRUE,sep="\t")
write.table(alpha,'alpha.txt',quote=F,col.names=TRUE,row.names=TRUE,sep="\t")
write.table(beta_uuf,'beta_uuf.txt',quote=F,col.names=TRUE,row.names=TRUE,sep="\t")
write.table(beta_wuf,'beta_wuf.txt',quote=F,col.names=TRUE,row.names=TRUE,sep="\t")
write.table(genus,'genus.txt',quote=F,col.names=TRUE,row.names=TRUE,sep="\t")
write.table(phylum,'phylum.txt',quote=F,col.names=TRUE,row.names=TRUE,sep="\t")



4. Make a Beta diversity plot

5. Add colors to the groups

6. Add ellipses to the groups

7. Make a histogram of alpha diversity values

8. Make a boxplot of alpha diversity values colored by group

9. Subset; visualize only a subset of samples

