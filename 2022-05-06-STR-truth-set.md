## Genome-wide STR Truth Set for Tool Benchmarking and Development 

Short tandem repeat (STR) expansions are associated with over 50 monogenic rare diseases [[Depienne 2021](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8205997/)] as well as common diseases such as autism [[Trost 2020](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9348607/)] [[Mitra 2021](https://www.nature.com/articles/s41586-020-03078-7)]. Improvements in STR genotyping tools like ExpansionHunter and GangSTR are generating new interest in studying STRs using short read sequencing data. 

High-quality STR truth data is needed both for:
1. comparing the existing STR genotyping tools 
2. comparing the accuracy of a single tool across different STR loci
3. developing new tools such as post-genotype filters
 
This post describes a new genome-wide truth set that has accurate genotypes for ~150k STR variants in a single human sample (CHM1-CHM13) derived from the Synthetic Diploid Benchmark [[Li 2018](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6341484/)].

In addition to tool evaluations, this dataset allows us to explore a few interesting questions related to STRs in general:
- what is the distribution of STR variants in the human genome (ie. motif sizes, lengths, percent multiallelic, etc.)?
- how many STR variants are novel relative to the hg38 human reference genome (ie. different motif or locus)?
- can we predict which loci are more likely to be mutated based on their sequence and reference context?

-------


<!-- close the current gap in accuracy and compute costs between STR genotyping tools and tools for other variant classes like SNVs and InDels. --> 

To date, STR truth data has come from:

1. **simulated STRs:** using a tool like wgsim, it's possible to simulate STR expansions or contractions at any STR locus 
   and generate an unlimited number of test cases. Benchmarking on simulated data can be useful for setting 
   an upperbound on tool performance. However, simulated data lacks some of the complexities of real data like GC bias, 
   adjacent variants not present in the reference genome, etc. so a tools performance on real-world data can be significantly worse. 
2. **mendelian violations analysis:** large WGS datasets with trios are available, and can be used to compare the number of 
   mendelian violations produced by different STR calling tools or filtering strategies. This produces a coarser  
   truthset since it's impossible to say whether any individual mendelian violation is error or truth - just that 
   overall, there should be no more than ~80 mendelian violations on average per trio (based on the estimated denovo rate for STR 
   variants [[Willems 2017](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5482724/?report=classic)]). Additionally, 
   mendelian violations are confounded by a tool's false-negative rate since a tool that consistently fails to detect 
   STR expansions at some loci will have fewer mendelian violations.
3. **PCR-validated pathogenic expansions:** A small number of WGS samples with PCR-validated STR expansions are publicly available - including 9         
   samples from [[Dashnow 2018](https://genomebiology.biomedcentral.com/articles/10.1186/s13059-018-1505-2)]. Typically only one locus is validated in        each sample, so there's too little data in this category to be useful for a genome-wide STR benchmark. Additionally, PCR and other related methods 
   often give only approximate expansion sizes (eg. "greater than 150 repeats"). This is sufficient for determining 
   pathogenicity but not for evaluating tool accuracy.   
4. **long read data:** This might be the ideal source of truth in the future, but currently suffers from a lack of well-validated STR calling tools. The most-recently published tool - Straglr [[Chiu 2021](https://genomebiology.biomedcentral.com/articles/10.1186/s13059-021-02447-3)] - reports 73% concordance between heterozygous STR expansions called from HiFi PacBio data vs truth data generated from the diploid assembly of HG00733 [[Kronenberg 2019](https://www.biorxiv.org/content/10.1101/327064v2.full)]. [[Chiu 2021](https://genomebiology.biomedcentral.com/articles/10.1186/s13059-021-02447-3)], [[Dashnow 2021](https://www.biorxiv.org/content/10.1101/2021.11.18.469113v1)] and other groups (unpublished) also raise concerns about diploid assemblies as a source of STR truth data since manual inspection of discordant loci often revealed that the assembly was not credible at those loci. 

The table below lists STR calling tools + the truth data used in their publications:  

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
         <li>4 WGS samples with HTT, 3 WGS samples with FMR1</li>
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
   <td>
      <ul>
         <li>Long read data from Plasmids with engineered expansions of 4 motifs (CAG, CAA, GGGGCC, and iCCTG)</li>
         <li>3 WGS samples with ATXN10 expansions</li>
         <li>NA12878 short-read calls at known pathogenic loci</li>
      </ul>
   </td>
</tr><tr>
   <td>RepeatHMM</td>
   <td>[<a href="https://doi.org/10.1186/s13073-017-0456-7">Liu 2017</a>]</td>
   <td>
      <ul>
         <li>20 WGS samples with ATXN3, 3 WGS samples with ATXN10 expansions</li>
         <li>NA12878 short-read calls at known pathogenic loci</li>
      </ul>
   </td>
</tr><tr>
   <td rowspan="100">Short Read</td>
   <td>STRling</td>
   <td>[<a href="https://www.biorxiv.org/content/10.1101/2021.11.18.469113v1">Dashnow 2021</a>]</td>
   <td>
      <ul>
         <li>134 WGS samples with expansions at 14 known pathogenic STR loci</li>
         <li>Diploid assemblies of Ashkenazi trio using HiFi PacBio. Assembled using PacBio Improved Phased Assembler (IPA), aligned to GRCh38 using pbmm2, variant calling using bcftools mpileup</li>
      </ul>
   </td>
</tr><tr>
   <td>adVNTR</td>
   <td>
      [<a href="https://genome.cshlp.org/content/28/11/1709.full">Bakhtiari 2018</a>], 
      [<a href="https://www.nature.com/articles/s41467-021-22206-z">Bakhtiari 2020</a>]</td>
   <td>
      <ul>
         <li>91 WGS samples with confirmed HTT, FXN, DMPK, or FMR1 expansions</li>
      </ul>
   </td>
</tr><tr>
   <td>ExpansionHunterDenovo</td>
   <td>[<a href="https://genomebiology.biomedcentral.com/articles/10.1186/s13059-020-02017-z">Dolzhenko 2020</a>]</td>
   <td>
      <ul>
         <li>91 WGS samples with confirmed HTT, FXN, DMPK, or FMR1 expansions</li>
      </ul>
   </td>
</tr><tr>
   <td>GangSTR</td>
   <td>[<a href="https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6735967/">Mousavi 2019</a>]</td>
   <td>
      <ul>
         <li></li>
      </ul>
   </td>
</tr><tr>
   <td>ExpansionHunter</td>
   <td>
      [<a href="https://genome.cshlp.org/content/early/2017/09/08/gr.225672.117">Dolzhenko 2017</a>],
      [<a href="https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6853681/">Dolzhenko 2019</a>]
   </td>
   <td>
      <ul>
         <li></li>
      </ul>
   </td>
</tr><tr>
   <td>TredParse</td>
   <td>[<a href="https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5673627/">Tang 2017</a>]</td>
   <td>
      <ul>
         <li></li>
      </ul>
   </td>
</tr><tr>
   <td>STRetch</td>
   <td>[<a href="https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6102892/">Dashnow 2018</a>]</td>
   <td>
      <ul>
         <li></li>
      </ul>
   </td>
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

*NOTE:* [Table 1](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8351082#Tab1) in [[Rajan-Babu 2021](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8351082/)] provides additional comparisons of many of these tools. 

The largest truthsets in this table are generated using diploid assemblies - as described in the Straglr paper - but the accuracy of these assemblies for STRs remains questionable. 

Can we improve on this?

----
**CHM1_CHM13_2 Synthetic Diploid Benchmark as an STR Truthset**

[[Li 2018](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6341484/)] produced a high-qaulity truthset based on [Huddleston 2017](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5411763/) haploid assemblies of two individuals - CHM1 and CHM13. 

To create the Synthetic Diploid Benchmark, [[Li 2018](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6341484/)] generated variant calls by:

1. Aligning each haploid assembly to GRCh37 or GRCh38 using minimap2
2. Converting the differences revealed by these alignments to variant calls. 

**Li et al. 2018 Figure 1:** Constructing the Syndip benchmark dataset. 

![image](https://user-images.githubusercontent.com/6240170/167907455-84baa96d-95ae-44bc-8471-c7769bd6474f.png)

This yielded 5,362,620 variants of which 4,148,586 were in high-confidence regions:
``` 
   3585549  ( 86.4%) SNV
    286568  (  6.9%) INS
    276469  (  6.7%) DEL
```

Although [[Li 2018](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6341484/)] used this data to evaluate SNV and INDEL calling tools, it can also serve as a high-quality SV and STR truthset since: 

1. haploid assembly is more accurate than diploid assembly
2. one of the two samples - CHM13 - is the basis of the new telomere-to-telomere (t2t) reference assembly, so we can further validate STR variants by lifting them over to t2tv2.0 and checking that at least one allele is concordant with the t2t reference.

---
**Part 1: Check All CHM1_CHM13_2 Variants For Concordance with The CHM13 T2T Reference Genome Assembly**

Below are the steps and how many variants pass each step:

<br />

<table class="ui striped table">
<tr>
   <th>Step</th>
   <th>Description</th>
   <th>Variants Filtered</th>
   <th>% Filtered</th>
   <th>Variants Remaining</th>
   <th>% Remaining</th>
</tr><tr>
   <td>#1 </td>
   <td>Start with all high-confidence, normal (ACGT) variants</td>
   <td></td>
   <td></td>
   <td>4,129,390</td>
   <td>100%</td>
</tr><tr>
   <td>#2 </td>
   <td>Liftover variants to t2t-v2.0 reference genome (CHM13) using gatk LiftoverVcf. <br />
      <br/>
      These are the reasons variants failed this step: 
      <ul>
        <li>190,474 IndelStraddlesMultipleIntevals (these are all deletions)</li> 
        <li> 23,158 NoTarget </li>
        <li>10,297 MismatchedRefAllele </li>
      </ul>
   </td>
   <td>223,929</td>
   <td>5.4%</td>
   <td>3,905,448</td>
   <td>94.6%</td>
</tr><tr>
   <td>#3 </td>
   <td>Since all valid variants should have at least 1 allele that matches the CHM13 T22 reference, filter out variants that are HOM-ALT after liftover: 
      <ul>
         <li>1026 (0.03%) SNVs</li>
         <li>338 (0.01%) insertions</li>
      </ul>
   </td>
   <td>1,364</td>
   <td>0.0%</td>
   <td>3,904,084</td>
   <td>94.5%</td>
</tr><tr>
   <td>#4 </td>
   <td>Liftover variants from t2t-v2.0 back to GRCh38 using gatk LiftoverVcf. </td>
   <td>253</td>
   <td>0.0%</td>
   <td>3,903,831</td>
   <td>94.5%</td>
</tr><tr>
   <td>#5</td>
   <td>Restore the 190,474 deletions that were dropped in the 1st liftover (GRCh38 => CHM13) due to IndelStraddlesMultipleIntevals. I'm assuming this is an artifact of the liftover chain files and not a sufficient reason to discard these variants.</td>
   <td></td>
   <td></td>
   <td>4,094,305</td>
   <td>99.2%</td>
</tr>
</table>

---

**Part 2: Filter CHM1_CHM13_2 Variants To STR Variants**

To identify the INDELs that are actually STR variants, process each INDEL to:
1. check if the inserted or deleted sequence is made up of some k-mer that covers at least 90% of the variant bases. 
2. if yes, treat this k-mer as the STR repeat unit. Otherwise, treat the entire variant sequence as the repeat unit to allow detection of STR expansions or contractions that differ from the reference by only 1 repeat. 
3. check the reference genome flanking sequence (immediately to the left and right of the variant) for additional repeats with the same repeat unit.

Keep variants that have:
 - at least 3 repeats of some motif in the variant + flanking sequences.
 - the total repeat size is 9bp or longer.

This is approach is implemented in the [filter_vcf_to_STR_variants.py](https://github.com/broadinstitute/str-analysis/blob/main/str_analysis/filter_vcf_to_STR_variants.py) script. 

Limitations:  
  * The current approach doesn't properly handle interruptions in the repeat sequence and will miss most STR variants that include interuptions. 
  A future version of filter_vcf_to_STR_variants.py can avoid this limitation by integrating the TandemRepeatFinder [Benson 1999] algorithm.
 

Results:
```
Run filter_vcf_to_STR_variants.py --min-fraction-of-variant-covered-by-repeat 0.9 
on all 4,094,305 variants in high-confidence regions.

This yields 180,471 TOTAL STR variants (4.4%)

Expansions vs. Contractions:
      89,633  ( 49.7%) STR DEL
      90,838  ( 50.3%) STR INS


Motif Sizes:
     106,969  ( 59.3%) STR motif size = 2 bp
      14,884  (  8.2%) STR motif size = 3 bp
      40,423  ( 22.4%) STR motif size = 4 bp
       9,802  (  5.4%) STR motif size = 5 bp
       2,667  (  1.5%) STR motif size = 6 bp
         802  (  0.4%) STR motif size = 7 bp
         565  (  0.3%) STR motif size = 8 bp
       4,359  (  2.4%) STR motif size = 9+ bp

Repeat Sizes (# of repeats):
      94,148  ( 52.2%) STR delta 1 repeat
      34,703  ( 19.2%) STR delta = 2 repeats
      17,762  (  9.8%) STR delta = 3 repeats
      10,413  (  5.8%) STR delta = 4 repeats
       6,811  (  3.8%) STR delta = 5 repeats
       4,435  (  2.5%) STR delta = 6 repeats
       3,043  (  1.7%) STR delta = 7 repeats
       2,123  (  1.2%) STR delta = 8 repeats
       7,033  (  3.9%) STR delta = 9+ repeats
  
Repeat Sizes (# of base pairs):
     173,749  ( 96.3%) STR size 0-25bp    *
       5,010  (  2.8%) STR size 25-50bp   *
         775  (  0.4%) STR size 50-75bp   *
         255  (  0.1%) STR size 75-100bp  
         157  (  0.1%) STR size 100-125bp
         112  (  0.1%) STR size 125-150bp
          76  (  0.0%) STR size 150-175bp
          70  (  0.0%) STR size 175-200bp
          51  (  0.0%) STR size 200-225bp
          45  (  0.0%) STR size 225-250bp
          29  (  0.0%) STR size 250-275bp
          19  (  0.0%) STR size 275-300bp
          16  (  0.0%) STR size 300-325bp
          11  (  0.0%) STR size 325-350bp
          17  (  0.0%) STR size 350-375bp
          15  (  0.0%) STR size 375-400bp
           5  (  0.0%) STR size 400-425bp
          13  (  0.0%) STR size 425-450bp
           9  (  0.0%) STR size 450-475bp
          11  (  0.0%) STR size 475-500bp
          26  (  0.0%) STR size 500+bp
     
HOM vs. HET:
     39,492  ( 21.9%) genotype are homozygous

de-novo:
       1,015  (  0.6%) STRs with no matching repeat in the left or right reference genome flanking sequence

```

Switching to `--min-fraction-of-variant-covered-by-repeat 1.0` doesn't significantly change the results:

```
Run filter_vcf_to_STR_variants.py --min-fraction-of-variant-covered-by-repeat 1.0 
on all 4,094,305 variants in high-confidence regions.

This yields 177,826 TOTAL STR variants (4.3%)

Expansions vs. Contractions:
      89,188  ( 50.2%) STR DEL
      88,638  ( 49.8%) STR INS
 
Motif Sizes:
     105,483  ( 59.3%) STR motif size 2 bp
      14,759  (  8.3%) STR motif size 3 bp
      39,751  ( 22.4%) STR motif size 4 bp
       9,597  (  5.4%) STR motif size 5 bp
       2,598  (  1.5%) STR motif size 6 bp
         728  (  0.4%) STR motif size 7 bp
         547  (  0.3%) STR motif size 8 bp
       4,363  (  2.5%) STR motif size 9+ bp

Repeat Sizes (# of repeats):
      94,238  ( 53.0%) STR delta 1 repeats
      34,697  ( 19.5%) STR delta 2 repeats
      17,499  (  9.8%) STR delta 3 repeats
      10,298  (  5.8%) STR delta 4 repeats
       6,540  (  3.7%) STR delta 5 repeats
       4,257  (  2.4%) STR delta 6 repeats
       2,887  (  1.6%) STR delta 7 repeats
       2,008  (  1.1%) STR delta 8 repeats
       5,402  (  3.0%) STR delta 9+ repeats
    
Repeat Sizes (# of base pairs):
     172,447  ( 97.0%) STR size 0-25bp
       4,036  (  2.3%) STR size 25-50bp
         641  (  0.4%) STR size 50-75bp
         236  (  0.1%) STR size 75-100bp
         134  (  0.1%) STR size 100-125bp
          87  (  0.0%) STR size 125-150bp
          57  (  0.0%) STR size 150-175bp
          37  (  0.0%) STR size 175-200bp
          32  (  0.0%) STR size 200-225bp
          27  (  0.0%) STR size 225-250bp
          18  (  0.0%) STR size 250-275bp
          13  (  0.0%) STR size 275-300bp
           3  (  0.0%) STR size 300-325bp
           6  (  0.0%) STR size 325-350bp
          11  (  0.0%) STR size 350-375bp
           7  (  0.0%) STR size 375-400bp
           3  (  0.0%) STR size 400-425bp
           9  (  0.0%) STR size 425-450bp
           5  (  0.0%) STR size 450-475bp
           3  (  0.0%) STR size 475-500bp
          14  (  0.0%) STR size 500+bp
     
HOM vs. HET:
      39,341  ( 22.1%) genotype are homozygous

de-novo:
         663  (  0.4%) STRs with no matching repeat in the left or right reference genome flanking sequence

```

---





