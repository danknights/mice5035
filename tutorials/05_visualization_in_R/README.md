## MiCE 5035 Tutorial: Basic data visualization in R

### Background
This tutorial is an introduction to visualizing microbiome data in _R_.

### Requirements
You must have completed [Tutorial 4](../04_visualization_in_R).


#### Install some needed packages
Make sure you (stil) have open your Tutorials project. Create a new R source file and call it, `tutorial_05.r`. Click in the console window. For this tutorial we will need the car package and the vegan package. Install the vegan package like this:
```bash
install.packages('vegan')
```

If that proceeds without errors, then install the car package:
```bash
install.packages('car')
```

### Tutorial

#### Load the data
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

#### Make a Beta diversity plot


5. Add colors to the groups

6. Add ellipses to the groups

7. Make a histogram of alpha diversity values

8. Make a boxplot of alpha diversity values colored by group

9. Subset; visualize only a subset of samples

