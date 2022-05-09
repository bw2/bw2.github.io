## CHM1_CHM13 Data as an STR Truthset for Tool Benchmarking and Development 

STR genotyping tools for short read whole-genome sequencing (WGS) data have improved significantly over the past 10 
years. However, room for improvement remains, and new tools continue to be developed.
A high-quality truthset is important for comparing existing tools and for future tool development.

<!-- close the current gap in accuracy and compute costs between STR genotyping tools and tools for other variant classes like SNVs and InDels. --> 

To date, STR truth data has come from:

1. **simulated STRs:** using a tool like wgsim, it's possible to simulate STR expansions or contractions at any STR locus 
   and generate an unlimited number of test cases. Benchmarking on simulated data can be useful for setting 
   an upperbound on tool performance, but simulated data lacks some of the complexities of real data like GC bias, 
   adjacent variants not present in the reference genome, etc. 
2. **mendelian violations analysis:** large WGS datasets with trios are available, and can be used to compare the number of 
   mendelian violations produced by different STR calling tools or filtering strategies. This produces a somewhat coarse 
   truthset since it's impossible to say whether any individual mendelian violation is error or truth - just that 
   overall, there should be no more than ~80 mendelian violations on average per trio (TODO: source). Additionally, 
   mendelian violations are confounded by a tool's false-negative rate since a tool that consistently fails to detect 
   STR expansions at some loci will produce fewer mendelian violations.
3. **PCR-validated pathogenic expansions:** there are several datasets with STR expansions that have been validated by PCR 
   or other gold-standard methods. However, too few of these samples are available. Additionally, PCR or other such truth data is 
   often gives only approximate expansion sizes (eg. greater than 150 repeats). This is sufficient for determining 
   pathogenicity but complicates evaluation of tool accuracy.   
4. **long read data:** although this would seem like the ideal solution, STR calling from long read data is still challenging.
   The most recent published tool - Straglr - reports only ~70% concordance between long read STR calls and truth data 
   generated from a diploid assembly of HG.. [].

----

The table below lists STR calling tools and the benchmarking data used in their publications:

<table>
<tr>
   <th>Data Type</th>
   <th>Tool Name</th>
   <th>Paper</th>
   <th>Data Used For Benchmarking</th>
</tr><tr>
   <td rowspan="3">Long Read</td>
   <td>Straglr</td>
   <td>[<a href="https://genomebiology.biomedcentral.com/articles/10.1186/s13059-021-02447-3">Chiu 2021</a>]</td>
   <td></td>
</tr><tr>
   <td>tandem-genotypes </td>
   <td>[<a href="https://doi.org/10.1186/s13059-019-1667-6">Mitsuhashi 2019</a>]</td>
   <td></td>
</tr><tr>
   <td>RepeatHMM</td>
   <td>[<a href="https://doi.org/10.1186/s13073-017-0456-7">Liu 2017</a>]</td>
   <td></td>
</tr><tr>
   <td rowspan="100">Short Read</td>
   <td>STRling</td>
   <td></td>
   <td></td>
</tr><tr>
   <td>ExpansionHunterDenovo</td>
   <td></td>
   <td></td>
</tr><tr>
   <td>GangSTR</td>
   <td></td>
   <td></td>
</tr><tr>
   <td>ExpansionHunter</td>
   <td></td>
   <td></td>
</tr><tr>
   <td>TredParse</td>
   <td></td>
   <td></td>
</tr><tr>
   <td>STRetch</td>
   <td></td>
   <td></td>
</tr><tr>
   <td>HipSTR</td>
   <td></td>
   <td></td>
</tr><tr>
   <td>LobSTR</td>
   <td></td>
   <td></td>
</tr><tr>
   <td>PopSTR</td>
   <td></td>
   <td></td>
</tr><tr>
   <td>RepeatSeq</td>
   <td></td>
   <td></td>
</tr><tr>
   <td>ExSTRa</td>
   <td></td>
   <td></td>
</tr><tr>
   <td>TRhist</td>
   <td></td>
   <td></td>
</tr><tr>
   <td>SuperSTR</td>
   <td></td>
   <td></td>
</tr>
</table>

The following publications have compared STR calling tools:

[[Rajan-babu 2021](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8351082/)]

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





