## Creating a catalog for genotyping genome-wide STR variants 

Most existing tandem repeat (TR) genotyping tools - including ExpansionHunter, GangSTR, PopSTR, HipSTR, and others - require the user to specify a catalog with the exact reference coordinates and motifs of each TR locus to genotype. Defining this input catalog is a key step in any genome-wide analysis since TR variants occurring outside of the specified loci are guaranteed to be excluded from the resulting callset and downstream analyses. 

[[Willems 2014](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4216929/)], one of the first studies to perform a genome-wide TR analysis using Illumina short read sequencing data, put considerable effort into defining an appropriate catalog, as described in their [Results section](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4216929/#sec-1title) and [Supplementary Materials](https://genome.cshlp.org/content/24/11/1894/suppl/DC1) which are copy-pasted below. One limitation of their analysis was that it was based only on the hg19 reference. 

Data from the Human Pangenome Research Consortium (HPRC) as well as other studies such as T2T-YAO from [[He 2023](https://www.biorxiv.org/content/10.1101/2023.07.17.549286v1)] and the [Illumina catalog by Qiu, Dolzhenko, et al.](https://github.com/Illumina/RepeatCatalogs) which contains 174k STR loci that are polymorphic within 1kGP.


The many genome-wide TR analyses published since then have often used different catalogs. 

<hr />
<p align="center"><kbd><img width="798" alt="image" src="https://github.com/bw2/bw2.github.io/assets/6240170/1f3cbc71-36b1-4c9e-9c57-7cf47763b3eb"></kbd></p>


<p align="center"><kbd>
<img width="798" alt="supplementary text" src="https://github.com/bw2/bw2.github.io/assets/6240170/a492bf1a-f56d-4923-a465-75226ceec7f0">
</kbd></p>
