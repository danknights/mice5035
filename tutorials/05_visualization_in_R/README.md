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

But this is not quite what we want. We want to use a different symbol for each sample group. We can do this by listing the symbols we want in the order of the groups that we gave to R above ('KarenThai', 'Karen1st', 'HmongThai', 'Hmong1st', 'Hmong2nd', 'Control'). Then we use the square brackets `[]` to select the right symbol for each sample by using the `Sample.Group` column as the indices. How does this work? It works because when you use a factor in R (categorical variable) in a place where numbers are expected (like in the indices in a table), R automatically converts the categories to numbers, based on the order of the categories for that factor. So in our case, every entry of 'KarenThai' will be converted to `1`, every entry of 'Karen1st' will be converted to `2`, and so on. Let's start with the symbols 1, 2, 3, 4, 5, 6 for the 6 groups. We will also add a legend using the `legend` command that shows which symbol belongs to which group. The `cex` parameter makes the font slightly smaller in the legend. Edit the commands in your source file and run them again.
```bash
plot(pc[,1],pc[,2],pch=c(1, 2, 3, 4, 5, 6)[map$Sample.Group])
legend('topleft',levels(map$Sample.Group),pch=c(1,2,3,4,5,6), cex=.75)
```

OK it's still very hard to see any patterns. Let's add some colors. We can do this with the `col` parameter. It will work the same way as the `pch` parameter. We just need to pass in a list (vector) of 5 colors, and use `map$Sample.Group` to provide the indices that pick the right color for each point. We will store the list of five colors in a variable called `GROUP.COLORS`. Edit the commandS in your source file and run them again.
```bash
GROUP.COLORS <- c("#A300FF",  "#A300FF", "#00A696","#00A696", "#FE42AD", "#2E1915")
```

#### Exercise

- Modify your `plot` command by adding the `col` parameter with the `GROUP.COLORS` variable, in a similar manner to how we used the `pch` above, so that your points are colored. If you're not sure how to do this, look carefully at how we set `pch` to be 1, 2, 3, 4, 5, or 6, according to the `map$Sample.Group` categories. Here you want to set `col` to be the 6 colors we just stored in `GROUP.COLORS`, also according to the `map$Sample.Group` categories.
- Modify your code to add the colors to the legend. Don't forget that you can search the web for examples!
- It would be nice to use hollow points for the 1st gen samples, and solid points for the others, since the 1st gen samples are spread across the plot. Search the web for "R plot symbols" to find other options for `pch`. Can you make choose different symbols to make your plot look exactly like this one? Also notice that the axes are labeled "PC1" and "PC2". Search the web to find out how to change the axis labels in an R plot, and modify your code accordingly.

<img src="../../supporting_files/Tutorial05-final-beta-diversity-plot.png" width="600" />

  

### Add ellipses
Let's add some ellipses to show the 2D center and standard deviation of the points in each group.
```bash
dataEllipse(x=pc[,1], y=pc[,2], groups=map$Sample.Group,plot.points=FALSE,levels=0.68,robust=TRUE,col=GROUP.COLORS,segments=100)
```

7. Make a histogram of alpha diversity values

8. Make a boxplot of alpha diversity values colored by group

9. Subset; visualize only a subset of samples

