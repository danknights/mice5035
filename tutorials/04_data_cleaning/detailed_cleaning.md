## MiCE 5035 Tutorial: Detailed Data cleaning in R

We will assume the raw IMP data tables have been loaded as shown at the top of [Tutorial 4](README.md).

Before we continue, we need to remove the longitudinal samples from all of the tables. These are subjects that have `NA` or `1` in the "Sample.Order" column in the mapping file. Note: the `|` means "or" and it makes `keep.ix` `TRUE` for every row where either the value is `NA` or `1`. Paste this command into your source file. You can type command-Return (Mac) or control-Return (Windows) to run each single line immediately in the terminal. 
```bash
# Remove logitudinal samples (those with Sample.Order > 1)
keep.ix <- is.na(map$Sample.Order) | map$Sample.Order==1
map <- map[keep.ix,]
```

We will now make sure that each table has the same samples in the exact same order. This is a critical step that you must do before analyzing almost any data set! Paste these into your source file and then execute them. 
```bash
# Ensure each table has the same sample IDs (rownames)
common.sampleIDs <- intersect(rownames(map),rownames(otus))
map <- map[common.sampleIDs,]
otus <- otus[common.sampleIDs,]
alpha <- alpha[common.sampleIDs,]
beta_uuf <- beta_uuf[common.sampleIDs,common.sampleIDs]
beta_wuf <- beta_wuf[common.sampleIDs,common.sampleIDs]
genus <- genus[common.sampleIDs,]
phylum <- phylum[common.sampleIDs,]
```
#### Exercise
- How many samples are left (you can check the map table or other tables)?
  
Note that the taxonomy names are long and hard to read. Let's shorten them. You don't need to understand how this command works at this point. Paste these into your source file and then execute them. 
```bash
# Shorten the taxonomy names
colnames(genus) <- sapply(strsplit(colnames(genus),";"),function(xx) xx[length(xx)])
colnames(phylum) <- sapply(strsplit(colnames(phylum),";"),function(xx) xx[length(xx)])
```

Let's make a new column that is just "Generation" (Thai/1st/2nd/Control). The `|` in `map$Sample.Group == "Karen1st" | map$Sample.Group == "Hmong1st"` is a logical "OR" operator. It makes the statement TRUE for every row in the mapping table where Sample.Group is "Karen1st" or "Hmong1st", and FALSE otherwise. Paste these into your source file and then execute them. 
```bash
# Make a new "Generation" column that shows Thai/1st/2nd/Control
map$Generation <- "Thai" # fill with Thai to start
map$Generation[map$Sample.Group == "Karen1st" | map$Sample.Group == "Hmong1st"] <- "1stGen"
map$Generation[map$Sample.Group == "Hmong2nd"] <- "2ndGen"
map$Generation[map$Sample.Group == "Control"] <- "Control"
map$Generation <- factor(map$Generation, levels=c('Thai','1stGen','2ndGen','Control'))
```

Finally, we will save these tables as text files on your computer so that you don't have to download them again later. Paste these into your source file and then execute them. 
```bash
# Save the tables to your local hard drive
write.table(map,'map.txt',quote=F,col.names=TRUE,row.names=TRUE,sep="\t")
write.table(otus,'otu_table.txt',quote=F,col.names=TRUE,row.names=TRUE,sep="\t")
write.table(alpha,'alpha.txt',quote=F,col.names=TRUE,row.names=TRUE,sep="\t")
write.table(beta_uuf,'beta_uuf.txt',quote=F,col.names=TRUE,row.names=TRUE,sep="\t")
write.table(beta_wuf,'beta_wuf.txt',quote=F,col.names=TRUE,row.names=TRUE,sep="\t")
write.table(genus,'genus.txt',quote=F,col.names=TRUE,row.names=TRUE,sep="\t")
write.table(phylum,'phylum.txt',quote=F,col.names=TRUE,row.names=TRUE,sep="\t")
```
