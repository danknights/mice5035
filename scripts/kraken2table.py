# merges mpa-style kraken2 reports into a single tab-delimited table
# uses file names as sample names, everything before the last "."
# tried many different scripts from various packages and none worked.
# 
# Note: assumes kraken output taxonomy is pipe | separated
# usage:
# python kraken2otu.py report1 report2 ... output-dir

import sys
import os
from collections import defaultdict
import re

# will be used to replace multiple spaces
import re
_RE_COMBINE_WHITESPACE = re.compile(r" +")


files = sys.argv[1:-1]
outdir = sys.argv[-1]
if not os.path.exists(outdir):
    os.makedirs(outdir)

taxa = set() # set of all observed taxa
samples = {} # each sample ID will map to a dict of taxa:count

for fname in files:
    sampleID = os.path.basename(fname)
    sampleID = os.path.splitext(sampleID)[0]
    # remove .fa at end if present
    if sampleID.endswith('.fa'):
        sampleID = sampleID[:-3]
        
    # Regular expression pattern to match the .S***.001 part
    pattern = re.compile(r'\.S\d+\.001')

    # Process filename and modify it if pattern is detected
    if pattern.search(sampleID):
        sampleID= re.sub(pattern, '', sampleID)

    print(sampleID)
    
    # sampleID = '.'.join(sampleID.split('.')[:-1])
                        
    counts = defaultdict(int)
    with open(fname,'r') as f:
        for line in f:
            line = _RE_COMBINE_WHITESPACE.sub("_", line).strip() # replace multispaces
            words = line.strip().split()
            taxon = words[0].strip()
            count = words[1].strip()
            counts[taxon] = int(count)
            taxa.add(taxon)
    samples[sampleID] = counts

taxa = sorted(list(taxa))
sampleIDs = sorted(list(samples.keys()))
                    
# open seven output files
f1 = open(os.path.join(outdir,'taxa_table_L1.txt'),'w')
f2 = open(os.path.join(outdir,'taxa_table_L2.txt'),'w')
f3 = open(os.path.join(outdir,'taxa_table_L3.txt'),'w')
f4 = open(os.path.join(outdir,'taxa_table_L4.txt'),'w')
f5 = open(os.path.join(outdir,'taxa_table_L5.txt'),'w')
f6 = open(os.path.join(outdir,'taxa_table_L6.txt'),'w')
f7 = open(os.path.join(outdir,'taxa_table_L7.txt'),'w')
files = [f1, f2, f3, f4, f5, f6, f7]
for f in files:
    f.write('Taxon\t' + '\t'.join(sampleIDs) + '\t' + 'taxonomy\n')

for taxon in taxa:
    if "|s__" in taxon:
        f = f7
    elif "|g__" in taxon:
        f = f6
    elif "|f__" in taxon:
        f = f5
    elif "|o__" in taxon:
        f = f4
    elif "|c__" in taxon:
        f = f3
    elif "|p__" in taxon:
        f = f2
    else:
        f = f1
    # check that taxon is nonzero
    maxcount = 0
    for sampleID in sampleIDs:
        if samples[sampleID][taxon] > maxcount:
            maxcount = samples[sampleID][taxon]
    taxonomy_string = taxon.replace('|','; ')
    if maxcount > 0:
        f.write(taxon)
        for sampleID in sampleIDs:
            f.write('\t' + str(samples[sampleID][taxon]))
        f.write('\t' + taxonomy_string)
        f.write('\n')
