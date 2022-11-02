# Immigration Microbiome Project data, obtained with these commands:

# load data
map <- read.delim(url('https://raw.githubusercontent.com/knights-lab/IMP_analyses/master/data/map.txt'),row=1)
alpha <- read.delim(url('https://raw.githubusercontent.com/knights-lab/IMP_analyses/master/data/denovo/alpha.txt'),row=1)
taxa <- t(read.delim(url('https://github.com/knights-lab/IMP_analyses/blob/master/data/refbased/taxatable_L6.txt?raw=true'),row=1))

# drop the longitudinal subjects
map <- map[map$Sub.Study != "L",]

# get rows the same
common.rownames <- rownames(map)
common.rownames <- intersect(rownames(taxa), common.rownames)
common.rownames <- intersect(rownames(alpha), common.rownames)
map <- map[common.rownames,]
alpha <- alpha[common.rownames,]
taxa <- taxa[common.rownames,]

# check out taxa; colnames are awkward, let's shorten
colnames(taxa) <- sapply(strsplit(colnames(taxa),";"),function(xx) xx[length(xx)])

# drop taxa not present in at least 10% of samples
taxa <- taxa[,colMeans(taxa > 0) >= 0.1]

# let's tell R to show sample groups in a certain order
map$Sample.Group <- factor(map$Sample.Group,levels=c('KarenThai','Karen1st','HmongThai','Hmong1st','Hmong2nd','Control'))

# let's make a new column that is just "generation"
map$Generation <- "Thai" # fill with Thai to start
map$Generation[map$Sample.Group == "Karen1st" | map$Sample.Group == "HmongThai"] <- "1stGen"
map$Generation[map$Sample.Group == "Hmong2nd"] <- "2ndGen"
map$Generation[map$Sample.Group == "Control"] <- "Control"
map$Generation <- factor(map$Generation, levels=c('Thai','1stGen','2ndGen','Control'))

# save these
write.table(map,'map.txt',quote=F,col.names=TRUE,row.names=TRUE,sep="\t")
write.table(alpha,'alpha.txt',quote=F,col.names=TRUE,row.names=TRUE,sep="\t")
write.table(taxa,'taxa.txt',quote=F,col.names=TRUE,row.names=TRUE,sep="\t")
