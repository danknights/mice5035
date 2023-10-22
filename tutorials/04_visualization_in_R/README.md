## MiCE 5035 Tutorial: Data cleaning and visualization in R

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

#### Exercise
Answer these questions about the data tables:
1. How many samples are there?
2. How many OTUs?
3. How many distinct genera?
4. Are there any _continuous_ (not categorical) variables in the mapping file (metadata) that you expect to be related to the microbiome?

The bottom left quadrant is the console. When you enter a command, _R_ evaluates the command and prints the result. We can use the console to run commands that we don't need to save permanently in our source file.

We can access an individual element in a table with square brackets `[]`. For example, this prints the relative abundance of the 9th genus in the 10th sample:
```bash
genus[10,9]
```

We can also access a arange of elements in a table by passing in a vector of numerical indices, or a vector of TRUE/FALSE values. For example, this prints the first 3 rows and first 6 columns of the map table...
```bash
map[1:3,1:6]
```

..and this prints the first 3 rows and columns 1, 2, 3, and 6. The `c()` function concatenates individual values (the TRUE's and FALSE's) into a vector:
```bash
map[1:3,c(TRUE, TRUE, TRUE, FALSE, FALSE, TRUE)]
```

Before we continue, we need to remove the longitudinal subjects from all of the tables. These are subjects that have `NA` or `1` in the "Sample.Order" column in the mapping file. Note: the `|` means "or" and it makes keep.ix TRUE for every row where either the value is `NA` or `1`. Paste this command into your source file. You can type command-Return (Mac) or control-Return (Windows) to run each single line immediately in the terminal. 
```bash
keep.ix <- is.na(map$Sample.Order) | map$Sample.Order==1
map <- map[keep.ix,]
```

We will now make sure that each table has the same samples in the exact same order. This is a critical step that you must do before analyzing almost any data set! Paste these into your source file and then execute them. 
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

Note that the taxonomy names are long and hard to read. Let's shorten them. You don't need to understand how this command works at this point. Paste these into your source file and then execute them. 
```bash
colnames(genus) <- sapply(strsplit(colnames(genus),";"),function(xx) xx[length(xx)])
colnames(phylum) <- sapply(strsplit(colnames(phylum),";"),function(xx) xx[length(xx)])
```

Let's make a new column that is just "Generation" (Thai/1st/2nd/Control). The `|` in `map$Sample.Group == "Karen1st" | map$Sample.Group == "HmongThai"` is a logical "OR" operator. It makes the statement TRUE for every row in the mapping table where Sample.Group is "Karen1st" or "HmongThai", and FALSE otherwise. Paste these into your source file and then execute them. 
```bash
map$Generation <- "Thai" # fill with Thai to start
map$Generation[map$Sample.Group == "Karen1st" | map$Sample.Group == "HmongThai"] <- "1stGen"
map$Generation[map$Sample.Group == "Hmong2nd"] <- "2ndGen"
map$Generation[map$Sample.Group == "Control"] <- "Control"
map$Generation <- factor(map$Generation, levels=c('Thai','1stGen','2ndGen','Control'))
```

Finally, we will save these tables as text files on your computer so that you don't have to download them again later. Paste these into your source file and then execute them. 
```bash
write.table(map,'map.txt',quote=F,col.names=TRUE,row.names=TRUE,sep="\t")
write.table(otus,'otu_table.txt',quote=F,col.names=TRUE,row.names=TRUE,sep="\t")
write.table(alpha,'alpha.txt',quote=F,col.names=TRUE,row.names=TRUE,sep="\t")
write.table(beta_uuf,'beta_uuf.txt',quote=F,col.names=TRUE,row.names=TRUE,sep="\t")
write.table(beta_wuf,'beta_wuf.txt',quote=F,col.names=TRUE,row.names=TRUE,sep="\t")
write.table(genus,'genus.txt',quote=F,col.names=TRUE,row.names=TRUE,sep="\t")
write.table(phylum,'phylum.txt',quote=F,col.names=TRUE,row.names=TRUE,sep="\t")
```

#### Make a Beta diversity plot
Create a new R source file and call it, `tutorial_04.r`.

Load in the two packages that we installed at the start of the tutorial. It's a good practice to load these at the top of your source file, so that you know right away if you have the required packages installed. Paste these into your source file and execute them. 
```bash
library('car')
library('vegan')
```

We will begin by loading in the data tables, even though technically they are still loaded into R from the downloading step above. This way when we run this file alone, it will load the data properly. Paste these into your source file, and execute them. 
```bash
map <- read.delim(map,'map.txt')
otus <- read.delim(otus,'otu_table.txt',check=F)
alpha <- read.delim(alpha,'alpha.txt')
beta_uuf <- read.delim(beta_uuf,'beta_uuf.txt')
beta_wuf <- read.delim(beta_wuf,'beta_wuf.txt')
genus <- read.delim(genus,'genus.txt')
phylum <- read.delim(phylum,'phylum.txt')
```


5. Add colors to the groups

6. Add ellipses to the groups

7. Make a histogram of alpha diversity values

8. Make a boxplot of alpha diversity values colored by group

9. Subset; visualize only a subset of samples

