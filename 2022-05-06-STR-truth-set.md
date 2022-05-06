## CHM1_CHM13 Data as an STR Truthset for Tool Benchmarking and Development 

There has been much progress over the past 10 years in the development of STR genotyping tools for short read whole-genome sequencing (WGS) data. 
However, there's still room for improvement, and new tools continue to be developed which aim to close the current gap in accuracy and compute costs between STR genotyping tools and tools for other variant classes like SNVs and InDels.

A high-quality truthset of WGS samples with known STR expansions or contractions is key to comparing existing tools and for further tool development. 

To date, STR truth data has come from:

1. **simulated STRs:** using a tool like wgsim, it's possible to simulate STR expansions or contractions at any STR locus 
   and generate an unlimited number of test cases. Benchmarking on simulated data is useful for setting 
   an upperbound on tool performance. If a tool doesn't work well on simuluated data, it almost certainly 
   will be even worse on real data. However, good performance is no guarantee of success since real data includes additional 
   challenges like GC bias, locus-specific variation not present in the reference genome, etc. which can 
   affect STR tool performance. 
2. **mendelian violations analysis:** large WGS datasets with trios are available, and can be used to compare the number of 
   mendelian violations produced by different STR calling tools or filtering strategies. This produces a somewhat coarse 
   truthset since it's impossible to say whether any individual mendelian violation is error or truth - just that 
   overall, there should be no more than ~80 mendelian violations on average per trio (TODO: source). Additionally 
   mendelian violations are confounded by a tool's false-negative rate - a tool that consistently misses STR expansions at 
   difficult-to-call loci will produce fewer mendelian violations.
3. **PCR-validated pathogenic expansions:** there are several datasets with STR expansions that have been validated by PCR 
   or other gold-standard methods. The main downside is that only 10 samples (each with 1 STR expansion) are publicly available 
   and larger datasets are private or otherwise difficult to access (TODO: source). Additionally, PCR or other such truth data is 
   not ideal because large STR expansions are often approximate (eg. greater than 150 repeats). This is sufficient for determining 
   pathogenicity, but complicates evaluation and development of more accurate tools.   
4. **long read data:** although this would seem like the ideal solution, STR calling from long read data is surprisingly challenging.

----
**CHM1_CHM13_2 Synthetic Diploid Benchmark as an STR Truthset**

[Li 2018](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6341484/) used haploid long-read assemblies. 
Although this is not HiFi data, the assemblies used additional error correction. 

----
**Pipeline for deriving high-quality STR genotypes from the CHM1_CHM13_2 Synthetic Diploid Benchmark**

[Li 2018](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6341484/) provide a set of variant calls (VCF) generated through a process that's very 
different from typical variant calling pipelines.  Instead of aligning individual PacBio reads to some reference and running a variant calling tool, 
the SynDip Bechmark performed haploid assembly of the long reads, aligned the assembled contigs to eachother using minimap, and then simply read off the differences between the 2 haploid assemblies. 

90% of these variants are SNVs, and 10% are indels. 

More specifically, the steps were as follows:


---





