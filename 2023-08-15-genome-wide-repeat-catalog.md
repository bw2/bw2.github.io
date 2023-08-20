## Creating a catalog for genotyping tandem repeat variants genome-wide

Most existing tandem repeat (TR) genotyping tools - including ExpansionHunter, GangSTR, PopSTR, HipSTR, and others - require the user to specify a catalog with the exact reference coordinates and motifs of each TR locus to genotype. Defining this input catalog is a key step in any genome-wide analysis since TR variants occurring outside of the specified loci are guaranteed to be missing from the resulting callset and downstream analyses. 

In [[Willems 2014](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4216929/)], one of the first studies to perform a genome-wide TR analysis using Illumina short read sequencing data, the authors put considerable effort into defining an appropriate catalog, as described in their [Results section](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4216929/#sec-1title) and [Supplementary Materials](https://genome.cshlp.org/content/24/11/1894/suppl/DC1):

<p align="center"><kbd><img width="798" alt="image" src="https://github.com/bw2/bw2.github.io/assets/6240170/1f3cbc71-36b1-4c9e-9c57-7cf47763b3eb"></kbd></p>



The many genome-wide TR analyses published since then have often used different catalogs. 

