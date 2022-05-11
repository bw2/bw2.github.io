## CHM1_CHM13 Data as an STR Truthset for Tool Benchmarking and Development 

STR genotyping tools for short read whole-genome sequencing (WGS) data have improved significantly over the past 10 
years. However, additional improvements in computational cost and accuracy may be possible, and new tools continue to be developed.
A high-quality STR truthset is important for these efforts - both for comparing existing tools and for focusing future tool development.

<!-- close the current gap in accuracy and compute costs between STR genotyping tools and tools for other variant classes like SNVs and InDels. --> 

To date, STR truth data has come from:

1. **simulated STRs:** using a tool like wgsim, it's possible to simulate STR expansions or contractions at any STR locus 
   and generate an unlimited number of test cases. Benchmarking on simulated data can be useful for setting 
   an upperbound on tool performance. However, simulated data lacks some of the complexities of real data like GC bias, 
   adjacent variants not present in the reference genome, etc. so real-world performance can be significantly worse. 
2. **mendelian violations analysis:** large WGS datasets with trios are available, and can be used to compare the number of 
   mendelian violations produced by different STR calling tools or filtering strategies. This produces a coarser  
   truthset since it's impossible to say whether any individual mendelian violation is error or truth - just that 
   overall, there should be no more than ~80 mendelian violations on average per trio (based on the estimated denovo rate for STR 
   variants [[Willems 2017](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5482724/?report=classic)]). Additionally, 
   mendelian violations are confounded by a tool's false-negative rate since a tool that consistently fails to detect 
   STR expansions at some loci will produce fewer mendelian violations.
3. **PCR-validated pathogenic expansions:** A small number of WGS samples with PCR-validated STR expansions are publicly available - including the 10        samples from [[Dashnow 2018](https://genomebiology.biomedcentral.com/articles/10.1186/s13059-018-1505-2)]. Typically only one locus is validated in        each sample, so there's too little data in this category to be useful for a genome-wide STR benchmark. Additionally, PCR and other related methods 
   often give only approximate expansion sizes (eg. "greater than 150 repeats"). This is sufficient for determining 
   pathogenicity but not for evaluating tool accuracy.   
4. **long read data:** This may be the ideal source of truth data in the future, but currently suffers from a lack of well-validated accurate tools for      calling STR expansions. The most recent published tool - Straglr - reports only ~70% concordance between long read STR calls and truth data generated    from a diploid assembly of HG00733 [[Chiu 2021](https://genomebiology.biomedcentral.com/articles/10.1186/s13059-021-02447-3)].


This table lists STR calling tools + the benchmarking data used in their publications:  

<br />
<table class="ui striped table">
<tr>
   <th>Data Type</th>
   <th>Tool Name</th>
   <th>Paper</th>
   <th>Data Used For Benchmarking</th>
</tr><tr>
   <td rowspan="3">Long Read</td>
   <td>Straglr</td>
   <td>[<a href="https://genomebiology.biomedcentral.com/articles/10.1186/s13059-021-02447-3">Chiu 2021</a>]</td>
   <td>
      <ul>
         <li>Simulated data using <a href="https://academic.oup.com/gigascience/article/6/4/gix010/3051934">NanoSim</a></li>
         <li>4 patients with HTT, 3 patients with FMR1</li>
         <li>Phased diploid assembly of HG00733 based on PacBio CLR + HiC data from [<a href="https://www.biorxiv.org/content/10.1101/327064v2.full">Kronenberg 2019</a>]
            <ul>
               <li>215,894 STR loci</li>
               <li>2,992 expansions were 200bp to 4,000bp</li>
               <li>418 HET expansions with >= 100bp difference between long and short allele</li>
            </ul>
         </li>
      </ul>
   </td>
</tr><tr>
   <td>tandem-genotypes </td>
   <td>[<a href="https://doi.org/10.1186/s13059-019-1667-6">Mitsuhashi 2019</a>]</td>
   <td></td>
</tr><tr>
   <td>RepeatHMM</td>
   <td>[<a href="https://doi.org/10.1186/s13073-017-0456-7">Liu 2017</a>]</td>
   <td>
      <ul>
         <li>20 patients with ATXN3 expansions</li>
         <li>3 patients with ATXN10 expansions</li>
         <li>NA12878 short-read calls as truth (40 loci)</li>
      </ul>
   </td>
</tr><tr>
   <td rowspan="100">Short Read</td>
   <td>STRling</td>
   <td>[<a href="https://www.biorxiv.org/content/10.1101/2021.11.18.469113v1">Dashnow 2021</a>]</td>
   <td></td>
</tr><tr>
   <td>ExpansionHunterDenovo</td>
   <td>[<a href="https://genomebiology.biomedcentral.com/articles/10.1186/s13059-020-02017-z">Dolzhenko 2020</a>]</td>
   <td></td>
</tr><tr>
   <td>GangSTR</td>
   <td>[<a href="https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6735967/">Mousavi 2019</a>]</td>
   <td></td>
</tr><tr>
   <td>ExpansionHunter</td>
   <td>[<a href="https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6853681/">Dolzhenko 2019</a>]</td>
   <td></td>
</tr><tr>
   <td>TredParse</td>
   <td>[<a href="https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5673627/">Tang 2017</a>]</td>
   <td></td>
</tr><tr>
   <td>STRetch</td>
   <td>[<a href="https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6102892/">Dashnow 2018</a>]</td>
   <td></td>
</tr><tr>
   <td>HipSTR</td>
   <td>[<a href="https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5482724/">Willems 2017</a>]</td>
   <td></td>
</tr><tr>
   <td>PopSTR2</td>
   <td>[<a href="https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7141861/">Kristmundsdottir 2020</a>]</td>
   <td></td>
</tr><tr>
   <td>LobSTR</td>
   <td>[<a href="https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3371701/">Gymrek 2012</a>]</td>
   <td></td>
</tr><tr>
   <td>ExSTRa</td>
   <td>[<a href="https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6288141/">Tankard 2018</a>]</td>
   <td></td>
</tr><tr>
   <td>TRhist</td>
   <td>[<a href="https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3957077/">Doi 2014</a>]</td>
   <td></td>
</tr><tr>
   <td>SuperSTR</td>
   <td>[<a href="https://www.biorxiv.org/content/10.1101/2021.04.05.438449v2">Fearnley 2021</a>]</td>
   <td></td>
</tr>
</table>

<br />

*NOTE:* [Table 1](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8351082#Tab1) in [[Rajan-Babu 2021](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8351082/)] provides additional comparisons for many of these tools. 


----
**CHM1_CHM13_2 Synthetic Diploid Benchmark as an STR Truthset**

To create the Synthetic Diploid Benchmark, [[Li 2018](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6341484/)] generated variant calls by:

1. Taking the 2 haploid assemblies of PacBio data from [Huddleston 2017](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5411763/). These are the CHM1 and CHM13 hydatidiform mole cell lines.
2. Using PCR-free WGS data to error correct the PacBio assemblies
3. Using minimap2 to align each haploid assembly to GRCh37 or GRCh38
4. Generating a VCF of all differences (ie. variants) between CHM1/CHM13 and GRCh37 or GRCh38. 

**Li et al. 2018 Figure 1:** Constructing the Syndip benchmark dataset. 

![image](https://user-images.githubusercontent.com/6240170/167907455-84baa96d-95ae-44bc-8471-c7769bd6474f.png)

This yielded 5,362,620 variants of which 4,148,586 are in high-confidence regions. Some details:
``` 
    276469  (  6.7%) DEL
    286568  (  6.9%) INS
   3585549  ( 86.4%) SNV

   1236613  ( 29.8%) genotype: 0|1
   1245185  ( 30.0%) genotype: 1|0
   1532879  ( 36.9%) genotype: 1|1
```

---
**Steps to convert this to an STR truthset:**

<br />

<table class="ui striped table">
<tr>
   <th>Step #</th>
   <th>Description</th>
   <th>Variants Dropped</th>
   <th>% Lost</th>
   <th>Variants Remaining</th>
   <th>% Remaining</th>
</tr><tr>
   <td>1 </td>
   <td>Start with all high-confidence, normal (ACGT) variants</td>
   <td></td>
   <td></td>
   <td>4,129,390</td>
   <td>100%</td>
</tr><tr>
   <td>2 </td>
   <td>Liftover variants to t2t-v2.0 reference genome (CHM13) using gatk LiftoverVcf. Reasons for failure: 
      <ul>
        <li>190,474 IndelStraddlesMultipleIntevals </li> 
        <li> 23,158 NoTarget </li>
        <li>10,297 MismatchedRefAllele </li>
      </ul>
   </td>
   <td>223,929</td>
   <td>5.4%</td>
   <td>3,905,448</td>
   <td>94.6%</td>
</tr>
</table>


---





