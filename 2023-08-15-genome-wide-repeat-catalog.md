## Creating a catalog for genotyping tandem repeat variants genome-wide

Most existing tandem repeat (TR) genotyping tools - including ExpansionHunter, GangSTR, PopSTR, HipSTR, and others - require the user to provide a catalog that specifies the exact reference coordinates and motifs of each TR locus to genotype. Defining this input catalog is a key step in any genome-wide analysis since TR variants occurring outside of the specified loci are guaranteed to be missing from the resulting callset and downstream analysis. 

In one of the first genome-wide analyses performed using short read sequencing data - [[Willems 2014](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4216929/)] - the authors put considerable effort into defining an appropriate catalog. 

They describe their analysis in the [Results section](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4216929/#sec-1title) and [Supplementary Materials](https://genome.cshlp.org/content/24/11/1894/suppl/DC1) as follows:

<img width="789" alt="image" src="https://github.com/bw2/bw2.github.io/assets/6240170/551766bc-bcc0-4bbd-a651-bff3effdab53">


The many genome-wide TR analyses published since then have often used different catalogs. 

