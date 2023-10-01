# merges mpa-style kraken2 reports into a single tab-delimited table
# uses file names as sample names, everything before the last "."
# tried many different scripts from various packages and none worked.
# scans file once to 
# usage:
# python kraken2otu.py report1 report2 ... output-dir

import sys
import os
from collections import defaultdict

files = sys.argv[:-1]
outdir = sys.argv[-1]
if not os.path.exists(outdir):
    os.makedirs(outdir)

taxa = set() # set of all observed taxa
samples = {} # each sample ID will map to a dict of taxa:count

for fname in files:
    sampleID = os.path.basename(fname)
    sampleID = '.'.join(sampleID.split('.')[:-1])
                        
    counts = defaultdict(int)
    with open(fname,'r') as f:
        for line in f:
            line.replace(' ','_')
            words = line.strip().split()
            print(words)
            taxon = words[0].strip()
            count = words[1].strip()
            counts[taxon] = count
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
    f.write('Taxon\t' + '\t'.join(sampleIDs) + '\n')

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
    elif "|d__" in taxon:
        f = f1
    f.write(taxon)
    for sample in sampleIDs:
        f.write('\t' + str(samples[sampleID][taxon]))
    f.write('\n')
