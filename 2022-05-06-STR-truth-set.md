## Genome-wide STR Truth Set for Tool Benchmarking and Development 

Short tandem repeat (STR) expansions are associated with over 50 monogenic diseases [[Depienne 2021](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8205997/)] as well as common diseases such as autism [[Trost 2020](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9348607/)] [[Mitra 2021](https://www.nature.com/articles/s41586-020-03078-7)]. Improvements in STR genotyping tools like [ExpansionHunter](https://github.com/Illumina/ExpansionHunter) and [GangSTR](https://github.com/gymreklab/GangSTR) have generated new interest in studying STRs using short read sequencing data. 

One persistant challenge for the field is the scarcity of publicly available high-quality truth data (ie. samples with known STR expansions) that can be used for:
1. comparing STR genotyping tools 
2. evaluatating how a given tool's performance varies across different loci
3. developing additional tools such as genotype quality filters

Here, we describe a new genome-wide STR truth set based on the Synthetic Diploid Bechmark (SynDip) [[Li 2018](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6341484/)]. The result is ~145k accurate STR genotypes in a single human sample (CHM1-CHM13) with publicly available short-read sequencing data. 

In addition to tool evaluations, we can use this truth set to explore some interesting questions about STRs in general, such as:
- what is the distribution of STR variants in the human genome (ie. motif sizes, lengths, percent multiallelic, etc.)?
- how well do the existing catalogs of STR loci capture these variants?
- how many STR variants are novel relative to the hg38 reference (ie. different motif or locus)?
- can we predict which loci are more likely to be mutated based on their sequence and reference context?

*NOTE*: STRs are traditionally defined as repeating motifs that are between 1 to 6bp long. For this truth set we exclude 1bp (homopolymer) repeats since they are uniquely error-prone, but include motifs longer than 6bp, allowing users to decide whether to include these in their analyses.

---

### Defining the STR truth set

To generate an STR truth set, we start with the Synthetic Diploid Benchmark (SynDip) [[Li 2018](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6341484/)]. This unique dataset uses haploid PacBio assemblies to identify all variants in the CHM1-CHM13 synthetic diploid sample. Because these variants are based on alignments of haploid assemblies (rather than individual reads) to the reference genome, the SynDip variants are more reliable than those produced by short-read or even ordinary long-read pipelines. 

Of the 4.1 million high-confidence variants in the [SynDip VCF](https://github.com/lh3/CHM-eval), 259k (6.3%) are insertions and 249k (6.1%) are deletions. To create the STR truth set, we filter these insertions and deletions to the subset that represent STR expansions or contractions:

<table>
   <tr>
      <th> </th>
      <th>Filtering Step</th>
      <th nowrap># of Variants<br />That Passed</th>
      <th nowrap align="right">%</th>
   </tr>
   <tr>
      <td><i>1</i></td>
      <td>Start with high-confidence variants provided by the SynDip Benchmark</td>
      <td nowrap align="right">4,081,549</td>
      <td nowrap align="right">all</td>
   </tr>
   
   <tr>
      <td><i>2</i></td>
      <td>Keep only insertions and deletions</td>
      <td nowrap align="right">507,603</td>
      <td nowrap align="right">12.4 %</td>
   </tr>

   <tr>
      <td><i>3</i></td>
      <td>Identify the subset that are STR expansions or contractions (requiring that they have ≥ 3 repeats, span ≥ 9bp, are pure (ie. no interuptions), and have motif size ≥ 2bp)</td>
      <td nowrap align="right">146,618</td>
      <td nowrap align="right">3.6 %</td>
   </tr>

</table>

<br />

<img width="85" alt="image" src="https://user-images.githubusercontent.com/6240170/200182718-67b467b0-80a6-49ae-b147-56a8bb0cf655.png">

Let's say the SynDip truth set contains this insertion:   <img width="275" alt="image" src="https://user-images.githubusercontent.com/6240170/200183159-d42914b0-9636-4584-a593-dcb86463ff14.png">


Should we include it in the STR truth set?  

   *step 1*: find the minimal motif (**GGC**) in the inserted sequence (**GGCGGC**) by using brute force k-mer search similar to [STRling](https://www.biorxiv.org/content/10.1101/2021.11.18.469113v1).  
   *step 2*: check the reference context for additional **GGC** repeats immediately to the left or right of the variant:  

<p align="center"><img width="350" alt="image" src="https://user-images.githubusercontent.com/6240170/200182871-639e7282-07a1-4587-8592-453d68622383.png"></center></p>

Here, the reference contains 9 additional GGC repeats so the variant can be represented as having  
   
**9 x GGC repeats in the reference allele**  
**11 x GGC repeats in the alternate allele**   
  
This variant passes our thresholds for length ≥ 9bp and repeat count ≥ 3, so **we add it to STR truth set**.

----

### Validation

The SynDip benchmark is based on samples from two individuals: CHM1 and CHM13. One of them (CHM13) is also the basis of the new [telomere-to-telomere](https://www.genome.gov/about-genomics/telomere-to-telomere) (T2T) reference genome, so we can validate most STR variants by checking that at least one allele matches the T2T reference sequence.

*NOTE*: STR contractions that failed hg38 ⇒ T2T liftover due to an  “IndelStraddlesMultipleIntevals” error were included in the truth set without these validation steps since it was deemed to be a technical problem with liftover rather than an issue with the variant itself. This applies to 60,590 (77%) of STR contractions.

<table>
   <tr>
      <th> </th>
      <th>Validation Step</th>
      <th nowrap># of Variants<br />That Failed</th>
      <th nowrap align="right">% Failed</th>
   </tr>
   <tr>
      <td><i>1</i></td>
      <td>Liftover to the T2T reference</td>
      <td nowrap align="right">1,507</td>
      <td nowrap align="right">1.0 %</td>
   </tr>
   
   <tr>
      <td><i>2</i></td>
      <td>Check that one allele exactly matches the T2T reference sequence</td>
      <td nowrap align="right">295</td>
      <td nowrap align="right">0.2 %</td>
   </tr>

   <tr>
      <td><i>3</i></td>
      <td>Lift back over to hg38</td>
      <td nowrap align="right">43</td>
      <td nowrap align="right">0.03 %</td>
   </tr>
   
   <tr>
      <td><i>3</i></td>
      <td>Check if the variant position changed due to hg38 ⇒ T2T ⇒ hg38 liftover</td>
      <td nowrap align="right">0</td>
      <td nowrap align="right">0 %</td>
   </tr>

</table>

Overall, of the 86,028 STRs that could be validated against T2T, 84,183 (97.9%) passed this validation, underscoring the accuracy and relevance of this truth set. 

---
### Results:

The resulting STR truth set contains:

- **144,773 STR variants**  
- **175,372 STR alleles**   
 
If we take all alleles and plot the number of repeats in CHM1-CHM13 minus the number of repeats in hg38 at the same locus, the distribution is symmetrical around 0:

<img width=500 src="https://user-images.githubusercontent.com/6240170/200637637-32348eff-13bc-4c10-9cbb-c52304709859.png">


This distribution matches expectation since there's no reason that STRs in hg38 should be systematically larger or smaller than repeats in random individuals from the  population (ie. CHM1 and CHM13). To take it a step further, the degree to which this distribution is symetrical around 0 further supports the truth set's accuracy since it rules out systematic bias toward expansions or contractions in the pipeline that produced the SynDip Benchmark. 

If we plot the same distribution but with size in base pairs instead of # of repeats on the x-axis, we see:

<img width=500 src="https://user-images.githubusercontent.com/6240170/201500475-561acf00-3b52-43b6-9a27-b1846ce76ddd.png">

To summarize this another way, only 3,037 STR alleles (1.7%) are more than 30bp different from the size of the STR in the reference genome, and only 849 (0.5%) are more than 60bp different - meaning it might not be possible to genotype them using spanning reads alone.

We can also look at the prevalence of STR variants with different motifs and compare it to the distribution of pure STR repeats in hg38 (found using [TandemRepeatFinder](https://github.com/Benson-Genomics-Lab/TRF)):

<div nowrap align=center>
<img width=400 src="https://user-images.githubusercontent.com/6240170/200649782-9c128fa7-fe46-4593-bb54-5e42bb546217.png">
<img width="148" alt="image" src="https://user-images.githubusercontent.com/6240170/200648659-7b827c97-b95d-4713-947c-bca349cf36c4.png">
<img width=400 src="https://user-images.githubusercontent.com/6240170/200649509-d8a1fd0d-4dbc-4e4b-9ab4-82eb9566b5cb.png">
</div>

Here the motifs are sorted by how common they are in hg38. 
Although the 2 distributions are roughly similar, STR variants are clearly more likely for some motifs than for others. We examine this in more detail below. 


### Additional Summary Stats

30,599 out of 144,773 (21%) STR variants are multiallelic (ie. have 2 non-reference alleles).  
As we'll see, this can serve as a crude proxy for mutability:

<div align=center>
<img width=850 src="https://user-images.githubusercontent.com/6240170/200898063-bcdfdfe6-1496-4997-b95d-192f83e08ceb.png">
</div>


3,121 out of 144,773 (2.2%) STR variants overlap segmental duplications (SegDups) in hg38:

<div align=center>
<img width=850 src="https://user-images.githubusercontent.com/6240170/200898172-0d04bc7c-269c-402b-b3c6-e1b2e6d86df6.png">
</div>
  

We can also check where truth set STRs fall relative to Gencode v42 or MANE v1 gene annotations:

<table>
   <tr>
      <th rowspan=2>Gene Region</th>
      <th colspan=2>Gencode v42</th>
      <th></th>
      <th colspan=2>MANE v1</th>
   </tr><tr>
      <th># of STR variants</th>
      <th>%</th>
      <th></th>
      <th># of STR variants</th>
      <th>%</th>
   </tr><tr>
      <td>intron</td>
      <td align=right>98,772</td>
      <td align=right>56 %</td>
      <td></td>
      <td align=right>61,529</td>
      <td align=right>35 %</td>
   </tr><tr>
      <td>intergenic</td>
      <td align=right>70,236</td>
      <td align=right>40 %</td>
      <td></td>
      <td align=right>110,723</td>
      <td align=right>63 %</td>
   </tr><tr>
      <td>exon of a non-coding gene</td>
      <td align=right>2,094</td>
      <td align=right>1.2 %</td>
      <td></td>
      <td align=right>0</td>
      <td align=right>0 %</td>
   </tr><tr>
      <td>promoter</td>
      <td align=right>1,869</td>
      <td align=right>1.1 %</td>
      <td></td>
      <td align=right>1,214</td>
      <td align=right>0.8 %</td>
   </tr><tr>
      <td>3' UTR</td>
      <td align=right>1,667</td>
      <td align=right>1.0 %</td>
      <td></td>
      <td align=right>1,404</td>
      <td align=right>0.8 %</td>
   </tr><tr>
      <td>5' UTR</td>
      <td align=right>492</td>
      <td align=right>0.3 %</td>
      <td></td>
      <td align=right>299</td>
      <td align=right>0.2 %</td>
   </tr><tr>
      <td>coding region</td>
      <td align=right>242</td>
      <td align=right>0.1 %</td>
      <td></td>
      <td align=right>203</td>
      <td align=right>0.1 %</td>
   </tr>
</table>

*NOTE: promoters are defined as just a 1kb window upstream of the 5' start of any transcript*


Showing the MANE v1 proportions as a histogram stratified by motif sizes:
<div align=left>
<img width="500" alt="image" src="https://user-images.githubusercontent.com/6240170/202269863-abc40ef0-35c1-428a-8065-ccb37b29157c.png">
</div>

If we look only at the very small fraction of STRs that overlap either promoters, UTRs or coding regions, the histogram looks like:
<div align=left>
<img width=500 src="https://user-images.githubusercontent.com/6240170/200899334-703e84af-0b10-4c4c-9bb6-fa80efa8cf22.png">
</div>

This shows that nearly all - 198 out of 203 (97.5%) - of the STR alleles in coding regions have motif sizes that are multiples of 3bp.  
Of the 5 coding STRs that are not in this category, 3 have large (> 50bp) motifs, 1 is an out-of-frame expansion of the rare 2bp "GC" motif, and 1 is an expansion of a 5bp "GGGGC" motif that adds 3 additional repeats relative to the reference and so remains in-frame. 

We can also look at whether the 203 coding STR variants fall in LoF or missense constrained genes and compare this to the gene constraint of 25 coding  disease-associated STR loci. 

![image](https://user-images.githubusercontent.com/6240170/202306770-ad9d07b8-159d-49a4-930d-ad0e72deae4e.png)

From this, we can see that disease-associated STRs are much more likely to be in constrained genes, implying that both missense and LoF constraint computed from SNVs is also relevant for STRs. On the other hand, just because a gene is constrained doesn't mean that in-frame STR variants in that gene cause disease since many of the truth set STRs fall in high-constraint genes.

Another way to look at this is whether larger STR variants are less likely to be in constrained genes, and the answer is yes - at least based on pLI and STR expansions (but not contractions). Other metrics don't separate as well by STR size, implying that pLI is the most useful metric.
![image](https://user-images.githubusercontent.com/6240170/202331857-f5cf777c-37d5-4342-b3c7-60aab7e096a5.png)



#### Novel STR loci

Unlike variant calling tools for SNVs and structural variants which just take read alignments (bam or cram) as input, nearly all STR genotyping tools except [ExpansionHunterDenovo](https://github.com/Illumina/ExpansionHunterDenovo) and [STRling](https://github.com/quinlan-lab/STRling) require users to also specify the exact boundaries and motifs of the STR loci to genotype. For example, to genotype the Huntington's Disease locus, a user must specify the reference coordinates "chr4:3074876-3074933" and motif "CAG". The implicit assumption of these algorithms is that all STRs you might want to genotype are also present in the reference genome - meaning that STR variants look like:

<img width="452" alt="image" src="https://user-images.githubusercontent.com/6240170/200219094-78f3ad2f-bcba-4412-a5cb-098e8f6b56a8.png">

rather than 

<img width="450" alt="image" src="https://user-images.githubusercontent.com/6240170/200219024-2464a379-b1b9-4569-ba3d-d6a47583c357.png">


The truth set allows us to check the degree to which this assumption is valid. It turns out that it is:

- 144,158 out of 144,773 (99.6%) of STR variants in CHM1-CHM13 match repeats found in hg38 immediately to the left or right of the variant.  Only 521 variants are novel STRs. 

This suggests that, for samples like CHM1-CHM13 that have European ancestry, nearly all true STR variants can be found by using a large enough STR catalog generated from the reference genome. 

*NOTE*: The truth set doesn't include variants where a large inserted sequence contains more than one STR or an STR embedded in non-repetative sequence. Such variants, if they exist, are not counted in the stats above.


#### Limitations of existing STR catalogs

An important question for any genome-wide STR analysis using tools like ExpansionHunter or GangSTR is which STR catalog to genotype. 

The truth set allows us to ask: if we genotype all loci in a given catalog, how many CHM1-CHM13 STR variants are we guaranteed to miss because they fall outside this catalog? 

Here we compare several catalogs and approaches:
<table>
   <tr>
      <th></th>
      <th>Description</th>
      <th>Example</th>
      <th nowrap>Total # of<br />STR Loci</th>
      <th nowrap># of Variants<br/>Missed By Catalog</th>
      <th nowrap>% Missed</th>
   </tr>
   <tr>
      <td>1</td>
      <td>Identifying STRs that are polymorphic in population control samples</td>
      <td><a href="https://github.com/Illumina/RepeatCatalogs/blob/master/docs/str_generation.md">Illumina catalog</a></td>
      <td nowrap align="right">174,300</td>
      <td nowrap align="right">53,137 out of 144,773</td>
      <td nowrap align="right">36.7%</td>      
   </tr>
   <tr>
      <td rowspan=2>2</td>
      <td rowspan=2>Running <a href="https://github.com/Benson-Genomics-Lab/TRF">TandemRepeatFinder</a> (TRF) on the reference genome and doing a series of post-processing steps</td>
      <td><a href="https://github.com/gymreklab/GangSTR#gangstr-reference-files">GangSTR v13 reference</a></td>
      <td nowrap align="right">832,380</td>
      <td nowrap align="right">79,397 out of 144,773</td>
      <td nowrap align="right">54.8%</td>      
   </tr>
   <tr>
      <td><a href="https://github.com/gymreklab/GangSTR#gangstr-reference-files">GangSTR v17 reference</a></td>
      <td nowrap align="right">1,340,266</td>
      <td nowrap align="right">59,462 out of 144,773</td>
      <td nowrap align="right">41.1%</td>
   </tr>
   <tr>
      <td>3</td>
      <td>Running <a href="https://github.com/Benson-Genomics-Lab/TRF">TandemRepeatFinder</a> (TRF) with very large mismatch and indel penalties to find all pure repeats that <b>span at least 6bp</b> in the hg38 reference genome</td>
      <td> </td>
      <td nowrap align="right">4,880,610</td>
      <td nowrap align="right">5,423 out of 144,773</td>
      <td nowrap align="right">3.7%</td>      
   </tr>
   <tr>
      <td>4</td>
      <td>Running <a href="https://github.com/Benson-Genomics-Lab/TRF">TandemRepeatFinder</a> (TRF) with very large mismatch and indel penalties to find all pure repeats that <b>span at least 9bp</b> in the hg38 reference genome</td>
      <td> </td>
      <td nowrap align="right">2,805,842</td>
      <td nowrap align="right">6,787 out of 144,773</td>
      <td nowrap align="right">4.7%</td>      
   </tr>
   <tr>
      <td>4</td>
      <td>Running <a href="https://github.com/Benson-Genomics-Lab/TRF">TandemRepeatFinder</a> (TRF) with very large mismatch and indel penalties to find all pure repeats that <b>span at least 12bp</b> in the hg38 reference genome</td>
      <td> </td>
      <td nowrap align="right">1,343,313</td>
      <td nowrap align="right">11,474 out of 144,773</td>
      <td nowrap align="right">7.9%</td>      
   </tr>
   <tr>
      <td>4</td>
      <td>Running <a href="https://github.com/Benson-Genomics-Lab/TRF">TandemRepeatFinder</a> (TRF) with very large mismatch and indel penalties to find all pure repeats that <b>span at least 15bp</b> in the hg38 reference genome</td>
      <td> </td>
      <td nowrap align="right">702,486</td>
      <td nowrap align="right">22,830 out of 144,773</td>
      <td nowrap align="right">15.8%</td>      
   </tr>
</table>


One takeaway is that, if we aim to capture more than 95% of STR variants using a TRF-derived catalog, we need to genotype more than 2.8M loci genome-wide in each individual. 

---
### Tool Comparisons

We downloaded Illumina paired-end short read data for CHM1-CHM13 from [EBI] and realigned it to hg38 using bwa. Then, we generated an STR catalog for the 144,000 (99%) of loci that had adjacent matching repeats in the hg38 reference (ie. were not novel). 
We then ran ExpansionHunter, GangSTR, and HipSTR to genotype these loci while applying different downstream filters. We also ran STRling and ExpandionHunterDenovo, neither of which need an STR catalog.

Below are results from comparing these tools on different loci.


---
### Inference

The truth set and tool results provide an opportunity to identify features that can distinguish
- STR loci that are variant in CHM1-CHM13 vs those that are not
- STR loci where tools produce accurate genotypes vs those that are not
- How to filter low quality STR genotypes

---
### Extra Sections

---
**Extra Section 1:** A few words about the limitations of existing approaches to STR truth data:

1. **simulated STRs:** we can generate an unlimited number of STR examples with known genotypes by using a tool like [wgsim](https://github.com/lh3/wgsim). However, simulated data doesn't capture the full complexity of real sequencing data (eg. adjacent variants not present in the reference genome, GC bias, and other sequencing artifacts). 
2. **mendelian violations analysis:** trios can be used to check whether genotypes are consistant with Mendelian inheritance. However, This is informative about specificity but not sensitivity since a tool that misses all expansions will have zero mendelian violations. This produces a coarser  
   truth set since it's impossible to say whether any individual mendelian violation is error or truth - just that 
   overall, there should be no more than ~80 mendelian violations on average per trio (based on the estimated denovo rate for STR 
   variants [[Willems 2017](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5482724/?report=classic)]). Additionally, 
   mendelian violations are confounded by a tool's false-negative rate since a tool that consistently fails to detect 
   STR expansions at some loci will have fewer mendelian violations.
3. **PCR-validated pathogenic expansions:** A small number of WGS samples with PCR-validated STR expansions are publicly available - including 9 
   samples from [[Dashnow 2018](https://genomebiology.biomedcentral.com/articles/10.1186/s13059-018-1505-2)]. Typically only one locus is validated in        each sample, so there's too little data in this category to be useful for a genome-wide STR benchmark. Additionally, PCR and other related methods 
   often give only approximate expansion sizes (eg. "greater than 150 repeats"). This is sufficient for determining 
   pathogenicity but not for evaluating tool accuracy.   
4. **long read data:** This might be the ideal source of truth in the future, but currently suffers from a lack of well-validated STR calling tools. The most-recently published tool - Straglr [[Chiu 2021](https://genomebiology.biomedcentral.com/articles/10.1186/s13059-021-02447-3)] - reports 73% concordance between heterozygous STR expansions called from HiFi PacBio data vs truth data generated from the diploid assembly of HG00733 [[Kronenberg 2019](https://www.biorxiv.org/content/10.1101/327064v2.full)]. [[Chiu 2021](https://genomebiology.biomedcentral.com/articles/10.1186/s13059-021-02447-3)], [[Dashnow 2021](https://www.biorxiv.org/content/10.1101/2021.11.18.469113v1)] and other groups (unpublished) also raise concerns about diploid assemblies as a source of STR truth data since manual inspection of discordant loci often revealed that the assembly was not credible at those loci. 

----
**Extra Section 2**: The table below lists STR calling tools + the truth data used in their publications.

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
   </td>
</tr><tr>
   <td>GangSTR</td>
   <td>[<a href="https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6735967/">Mousavi 2019</a>]</td>
   <td>
   </td>
</tr><tr>
   <td>ExpansionHunter</td>
   <td>
      [<a href="https://genome.cshlp.org/content/early/2017/09/08/gr.225672.117">Dolzhenko 2017</a>],
      [<a href="https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6853681/">Dolzhenko 2019</a>]
   </td>
   <td>
   </td>
</tr><tr>
   <td>TredParse</td>
   <td>[<a href="https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5673627/">Tang 2017</a>]</td>
   <td>
   </td>
</tr><tr>
   <td>STRetch</td>
   <td>[<a href="https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6102892/">Dashnow 2018</a>]</td>
   <td>
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

The largest truth sets in this table are generated using diploid assemblies - as described in the Straglr paper [<a href="https://genomebiology.biomedcentral.com/articles/10.1186/s13059-021-02447-3">Chiu 2021</a>] - but the accuracy of these assemblies for STRs remains questionable. 

----
**Extra Section 3:** Synthetic Diploid Benchmark Overview

[[Li 2018](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6341484/)] produced a high-qaulity truth set based on [Huddleston 2017](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5411763/) haploid assemblies of two individuals - CHM1 and CHM13. 

To create the Synthetic Diploid Benchmark, [[Li 2018](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6341484/)] generated variant calls by:

1. Aligning each haploid assembly to GRCh37 or GRCh38 using minimap2
2. Converting the differences revealed by these alignments to variant calls directly from the CIGAR string. There was no need to run a separate variant calling tool downstream of the alignment step.

**Li et al. 2018 Figure 1:** Constructing the Syndip benchmark dataset. 

![image](https://user-images.githubusercontent.com/6240170/167907455-84baa96d-95ae-44bc-8471-c7769bd6474f.png)

This yielded 5,362,620 variants of which 4,148,586 were in high-confidence regions.

[[Li 2018](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6341484/)] used this data to evaluate SNV and INDEL calling tools, but it can also serve as a high-quality truth set for STRs, as well as tandem repeats (TRs) and structural variants (SVs).


