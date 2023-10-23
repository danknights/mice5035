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
First, tell R to show sample groups in a certain order. The column "Sample.Group" is what's called a "factor". This is just a categorical variable. R automatically detected that it was a categorical variable when it loaded the mapping file. R also keeps track of what order it should use to display the categories in plots. By default, it used alphabetical order, but we want to use a different order that makes sense for our visualizations. we can fix this by telling our that it is a factor and telling it the order of the levels, or categories, in the factor. Paste this into your source file and execute it. 
```bash
map$Sample.Group <- factor(map$Sample.Group,levels=c('KarenThai','Karen1st','HmongThai','Hmong1st','Hmong2nd','Control'))
```

Before we can make the beta diversity plot, we have to perform principal coordinates analysis. In R, this is known as _classical multidimensional scaling_, or `cmdscale`. Then we simply call `plot` and give it the first two dimensions of the principal coordinates analysis. Paste these into your file and execute them.
```bash
pc <- cmdscale(beta_uuf)
plot(pc[,1],pc[,2])
```

Did it work? This is horrible! It's a complete blob. There are no colors or groups at all. Or are there? Let us start by changing the plot symbols and adding a legend. We can do this with the `pch` parameter. If we set `pch` to `3`, we get a different symbol. Edit the `plot` command in your file and execute it again.
```bash
pc <- cmdscale(beta_uuf)
plot(pc[,1],pc[,2],pch=3)
```

But this is not what we want. We want to use a different symbol for each sample group. We can do this by listing the symbols we want in the order of the groups that we gave to R above ('KarenThai', 'Karen1st', 'HmongThai', 'Hmong1st', 'Hmong2nd', 'Control'). Then we use the square brackets `[]` to select the right symbol for each sample by using the `Sample.Group` column as the indices. How does this work? It works because when you use a factor in R (categorical variable) in a place where numbers are expected (like in the indices in a table), R automatically converts the categories to numbers, based on the order of the categories for that factor. So in our case, every entry of 'KarenThai' will be converted to `1`, every entry of 'Karen1st' will be converted to `2`, and so on. Let's start with the symbols 1, 2, 3, 4, 5. Edit the command in your source file and run it again.
```bash
plot(pc[,1],pc[,2],pch=pch=c(1, 2, 3, 4 ,5)[map$Sample.Group])
```


5. Add colors to the groups

6. Add ellipses to the groups

7. Make a histogram of alpha diversity values

8. Make a boxplot of alpha diversity values colored by group

9. Subset; visualize only a subset of samples

