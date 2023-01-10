## Genome-wide STR Truth Set for Tool Benchmarking and Development 

Short tandem repeat (STR) expansions are associated with over 50 monogenic diseases [[Depienne 2021](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8205997/)] as well as common diseases such as autism [[Trost 2020](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9348607/)] [[Mitra 2021](https://www.nature.com/articles/s41586-020-03078-7)]. Over the past 5 years, improvements in STR genotyping tools such as [ExpansionHunter](https://github.com/Illumina/ExpansionHunter) and [GangSTR](https://github.com/gymreklab/GangSTR) have generated new interest in studying STRs using short read sequencing data. 

However, one persistant challenge with designing and scaling up STR analyses is the scarcity of publicly available high-quality truth data (ie. samples with known STR expansions) that can be used for:
1. comparing tools
2. evaluatating tool accuracy beyond the ~50 known disease-associated loci
3. further tool development, including genotype quality filters

In this blog post, I share a new genome-wide STR truth set that partially addresses this challenge. It is based on the Synthetic Diploid Bechmark (SynDip) [[Li 2018](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6341484/)] and contains accurate genotypes for ~150,000 STR variants in a single human sample (CHM1-CHM13). The PCR-free genome sequencing data for this sample is publicly available from the [Short Read Archive (SRA)](https://trace.ncbi.nlm.nih.gov/Traces/?view=run_browser&acc=ERR1341796&display=data-access) and also from the Broad Institute - including both [genome data](https://console.cloud.google.com/storage/browser/broad-public-datasets/CHM1_CHM13_WGS2) and [exome data](https://console.cloud.google.com/storage/browser/broad-public-datasets/CHM1_CHM13_WES).

I apply this truth set to evaluate widely-used STR calling tools - ExpansionHunter, GangSTR, HipSTR and ExpansionHunter Denovo, and also use it to explore relevant questions about STRs in general such as:
- what is the distribution of STR variants in the human genome (ie. motif sizes, lengths, percent multiallelic, etc.)?
- how well do widely-used catalogs of STR loci capture these variants?
- how many STR variants are novel (ie. have a motif or repeat locus not present in the hg38 reference genome)?

**Key Findings**

Some of the most interesting and/or surprising results from the truth set analysis are listed below. These are based on a survey of all STR variants in a single human genome of european ancestry - the CHM1-CHM13 synthetic diploid sample from [[Li 2018](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6341484/)]. They can be considered as findings from an n=1 case study. 

- An individual's genome differs from the reference at ~150,000 STR loci, but 98% of these alleles differ by less than 30bp. On average, only several thousand STR loci differ from the reference by more than 30bp.
- 99.6% of STR variants occured at STR loci in the reference genome. Only 521 STR variants had novel motifs that were entirely different from the adjacent motifs or refence sequence context.
- ExpansionHunter has better accuracy than GangSTR or HipSTR across the entire range of STR allele sizes.
- widely-used STR catalogs would miss 35% to 40% of the STR variants in the truth set. To capture more than 95% of STR variants, we recommend using a different catalog that contains 2.8 million STR loci. 
- pLI gene constraint is useful but insufficient for identifing genes that are intolerant of STR variation.

*NOTE*: STRs are traditionally defined as repeating motifs that are between 1 to 6bp long. For this truth set I exclude 1bp (homopolymer) repeats since they are uniquely error-prone, but include motifs longer than 6bp so that users can decide whether to include these in their analyses.

---

### Defining the STR truth set

To generate an STR truth set, I started with the Synthetic Diploid Benchmark (SynDip) [[Li 2018](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6341484/)] which is a unique dataset that uses haploid PacBio assemblies to identify all variants in the CHM1-CHM13 synthetic diploid sample. Because these variants are based on alignments of haploid assemblies (rather than individual reads) to the reference genome, the SynDip genotypes are more reliable than those produced by short-read or even ordinary long-read pipelines. 

Of the 4.1 million high-confidence variants in the [SynDip VCF](https://github.com/lh3/CHM-eval), 259k (6.3%) are insertions and 249k (6.1%) are deletions. To create the STR truth set, I filtered these insertions and deletions to the subset that represent STR expansions or contractions by following these steps:

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
  
This variant passes the thresholds for length ≥ 9bp and repeat count ≥ 3, so **we add it to STR truth set**.

----

### Validation

The SynDip benchmark is based on samples from two individuals: CHM1 and CHM13. One of them (CHM13) is also the basis of the new [telomere-to-telomere](https://www.genome.gov/about-genomics/telomere-to-telomere) (T2T) reference genome, so it's possible to validate most STR variants in the truth set by checking that at least one allele matches the T2T reference sequence.

<table>
   <tr>
      <th> </th>
      <th>Validation Step</th>
      <th nowrap># of Variants<br />That Failed</th>
      <th nowrap align="right">% Failed</th>
   </tr>
   <tr>
      <td><i>1</i></td>
      <td>Lift over STR variant to the T2T reference</td>
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
      <td><i>4</i></td>
      <td>Check if the variant position changed due to hg38 ⇒ T2T ⇒ hg38 liftover</td>
      <td nowrap align="right">0</td>
      <td nowrap align="right">0 %</td>
   </tr>

</table>

Overall, of the 86,028 STRs that could be validated <sup>‡</sup> against T2T, 84,183 (97.9%) passed this validation, underscoring the accuracy and relevance of this truth set. 

‡ *NOTE*: STR contractions that failed hg38 ⇒ T2T liftover due to an  “IndelStraddlesMultipleIntevals” error were included in the truth set without these validation steps as I consider this to be a technical issue with liftover rather than a problem with genotype accuracy. This applies to 60,590 (77%) of STR contractions.


---
### Results:

The resulting STR truth set contains:

- **144,773 STR variants**  
- **175,372 STR alleles**   

The size distribution of these alleles is as follows:

<img width=500 src="https://user-images.githubusercontent.com/6240170/200637637-32348eff-13bc-4c10-9cbb-c52304709859.png">

Here, the x-axis represents the STR allele size in CHM1-CHM13 minus the number of repeats at that locus in the hg38 reference genome. The distribution is symmetric around 0 - which is as expected since there's no reason for STRs in hg38 to be systematically larger or smaller than repeats in random individuals from the  population (ie. CHM1 and CHM13). To take it a step further, this symmetry provides further support for the truth set's accuracy since it rules out systematic bias toward expansions or contractions in the pipeline that produced the SynDip Benchmark. 

If I plot the same distribution but with size in base pairs rather than # of repeats on the x-axis, it looks like:

<img width=500 src="https://user-images.githubusercontent.com/6240170/201500475-561acf00-3b52-43b6-9a27-b1846ce76ddd.png">

To summarize, only 3,037 STR alleles (1.7%) differ by more than 30bp from the reference genome, and only 849 (0.5%) differ by more than 60bp. Although there are many STR variants, the overwhelming majority add or subtract only a few repeats. 

We can also look at the prevalence of STR variants with different motifs and compare it to the distribution of pure STR repeats in hg38 (found using [TandemRepeatFinder](https://github.com/Benson-Genomics-Lab/TRF)):

<div nowrap align=center>
<img width=400 src="https://user-images.githubusercontent.com/6240170/200649782-9c128fa7-fe46-4593-bb54-5e42bb546217.png">
<img width="148" alt="image" src="https://user-images.githubusercontent.com/6240170/200648659-7b827c97-b95d-4713-947c-bca349cf36c4.png">
<img width=400 src="https://user-images.githubusercontent.com/6240170/200649509-d8a1fd0d-4dbc-4e4b-9ab4-82eb9566b5cb.png">
</div>

Here the motifs are sorted by how common they are in hg38. 
Although the 2 distributions are roughly similar, some motifs clearly have more STR variants than others. 

30,599 out of 144,773 (21%) STR variants are multiallelic (ie. have 2 non-reference alleles), reflecting the high mutation rates of STR loci.

<div align=center>
<img width=850 src="https://user-images.githubusercontent.com/6240170/200898063-bcdfdfe6-1496-4997-b95d-192f83e08ceb.png">
</div>

Finally, we can also ask - for STR variants in the truth set, how large are the corresponding loci in the hg38 reference genome? 
and also, if a locus has many repeats in the reference genome, is it more likely to be expanded or contracted in CHM1-CHM13?  
These plots address those questions:

<img width=615 src="https://user-images.githubusercontent.com/6240170/204148709-ab45e9b2-e808-4daa-a089-107b3139811b.png">



Unsurprisingly, truth set variants at loci where the reference sequence contains relatively few repeats are more likely to be expanded, while loci that have many repeats in the reference are more likely to be contracted in the truth set. 


### Genomic regions

How are truth set STR variants distributed across various annotated regions of the genome?

3,121 out of 144,773 (2.2%) STR variants overlap segmental duplications (SegDups) in hg38:

<div align=center>
<img width=850 src="https://user-images.githubusercontent.com/6240170/200898172-0d04bc7c-269c-402b-b3c6-e1b2e6d86df6.png">
</div>
  

STRs overlap transcripts from [Gencode v42](https://www.gencodegenes.org/human/release_42.html) and [MANE v1](https://www.ncbi.nlm.nih.gov/refseq/MANE/) as follows:

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

If we filter out STRs that are intergenic, intronic or overlap non-coding exons, and look only at the small subset that overlap either promoters, UTRs or coding regions (CDS), the histogram looks like:
<div align=left>
<img width=500 src="https://user-images.githubusercontent.com/6240170/200899334-703e84af-0b10-4c4c-9bb6-fa80efa8cf22.png">
</div>

This shows that nearly all - 198 out of 203 (97.5%) - of the STR alleles in coding regions have motif sizes that are multiples of 3bp.  
As for the 5 loci that don't fit this pattern, 3 have very large motifs - larger than 50bp, 1 is an out-of-frame expansion of the rare "GC" dinucleotide motif, and 1 is an expansion of a 5bp "GGGGC" motif that adds 3 additional repeats relative to the reference and so does not introduce a frameshift. 

We can also look at whether the 203 coding STR alleles fall within LoF or missense constrained genes and compare this to the gene constraint of the 25 known disease-associated loci that are within coding regions. 

![image](https://user-images.githubusercontent.com/6240170/202306770-ad9d07b8-159d-49a4-930d-ad0e72deae4e.png)

From this, we see that disease-associated STRs are much more likely to be in constrained genes, implying that both missense and LoF constraint computed from SNVs is also relevant for STRs. On the other hand, just because a gene is constrained doesn't mean that in-frame STR variants in that gene cause disease since many of the truth set STRs fall in highly constrained genes.

Another way to look at this is to see whether larger STR variants are less likely to be in constrained genes. This might not be enough data to say, but at least for larger expansions, pLI is more likely to be near 0. Here, each dot represents a coding STR allele in the truth set, and contractions relative to the reference are negative on the y-axis:
![image](https://user-images.githubusercontent.com/6240170/202331857-f5cf777c-37d5-4342-b3c7-60aab7e096a5.png)



#### Novel STR loci

Unlike variant calling tools for SNVs and structural variants which take only read alignments (bam or cram) as input, nearly all STR genotyping tools besides [ExpansionHunterDenovo](https://github.com/Illumina/ExpansionHunterDenovo) and [STRling](https://github.com/quinlan-lab/STRling) require users to also provide the exact boundaries and motifs of the STR loci to genotype. For example, to genotype the Huntington's Disease locus, a user must specify the reference coordinates "chr4:3074876-3074933" and motif "CAG". The implicit assumption of these algorithms is that all STRs a user might want to genotype are also present in the reference genome - meaning that STR variants look like:

<img width="452" alt="image" src="https://user-images.githubusercontent.com/6240170/200219094-78f3ad2f-bcba-4412-a5cb-098e8f6b56a8.png">

rather than 

<img width="450" alt="image" src="https://user-images.githubusercontent.com/6240170/200219024-2464a379-b1b9-4569-ba3d-d6a47583c357.png">


The truth set allows us to check the degree to which this assumption is valid. It turns out that it is almost 100%:

- 144,158 out of 144,773 (99.6%) of STR variants in CHM1-CHM13 match repeats found in hg38 immediately to the left or right of the variant. Only 521 variants are novel STRs, and they are all intergenic (based on Gencode v42).

This suggests that, for samples like CHM1-CHM13 that have European ancestry, nearly all true STR variants can be found by using a large enough STR catalog generated from the reference genome. 


#### Limitations of existing STR catalogs

An important question for any genome-wide STR analysis using tools like ExpansionHunter or GangSTR is which STR catalog to genotype. 

The truth set allows us to ask: for a given catalog, how many CHM1-CHM13 STR variants would be missed because they occur at loci that are not in the catalog? 

Here I compare several widely-used catalogs and approaches:
<table>
   <tr>
      <th></th>
      <th>Catalog Name</th>
      <th>How It Was Created</th>
      <th nowrap>Catalog Size:<br /># of STR Loci</th>
      <th nowrap># of Truth Set Variants<br/>Missed By Catalog</th>
      <th nowrap>% Missed</th>
   </tr>
   <tr>
      <td>1</td>
      <td><a href="https://github.com/Illumina/RepeatCatalogs/blob/master/docs/str_generation.md">Illumina catalog</a></td>
      <td>Identifying STRs that are polymorphic in 2,504 individuals from the 1000 genomes project.</td>
      <td nowrap align="right">174,300</td>
      <td nowrap align="right">53,137 out of 144,773</td>
      <td nowrap align="right">36.7%</td>      
   </tr>
   <tr>
      <td rowspan=2>2</td>
      <td><a href="https://github.com/gymreklab/GangSTR#gangstr-reference-files">GangSTR v13 loci</a></td>
      <td rowspan=2>Running <a href="https://github.com/Benson-Genomics-Lab/TRF">TandemRepeatFinder</a> (TRF) on the reference genome 
         using a mismatch penalty = 5 and an indel penalty = 17. Loci had to <b>span at least 12bp</b> in the hg38 reference genome. Multiple additional filters and post-processing steps were applied as described in [<a href="https://academic.oup.com/nar/article/47/15/e90/5518310?login=true">Mousavi 2019</a>].</td>
      <td nowrap align="right">832,380</td>
      <td nowrap align="right">79,397 out of 144,773</td>
      <td nowrap align="right">54.8%</td>      
   </tr>
   <tr>
      <td><a href="https://github.com/gymreklab/GangSTR#gangstr-reference-files">GangSTR v17 loci</a></td>
      <td nowrap align="right">1,340,266</td>
      <td nowrap align="right">59,462 out of 144,773</td>
      <td nowrap align="right">41.1%</td>
   </tr>
   <tr>
      <td>3</td>
      <td nowrap><a href="https://github.com/bw2/bw2.github.io/blob/master/2022-05-06-STR-truth-set.md#extra-sections">Pure Repeats Catalog</a></td>
      <td>Running <a href="https://github.com/Benson-Genomics-Lab/TRF">TandemRepeatFinder</a> (TRF) with very large mismatch and indel penalties to find all pure repeats that <b>span at least 6bp</b> in the hg38 reference genome</td>
      <td nowrap align="right">4,722,859</td>
      <td nowrap align="right">5,434 out of 144,773</td>
      <td nowrap align="right">3.8%</td>      
   </tr>
   <tr>
      <td>4</td>
      <td nowrap><a href="https://github.com/bw2/bw2.github.io/blob/master/2022-05-06-STR-truth-set.md#extra-sections">Pure Repeats Catalog<br/>Subset ≥ 9bp</a></td>
      <td>Running <a href="https://github.com/Benson-Genomics-Lab/TRF">TandemRepeatFinder</a> (TRF) with very large mismatch and indel penalties to find all pure repeats that <b>span at least 9bp</b> in the hg38 reference genome</td>
      <td nowrap align="right">2,805,842</td>
      <td nowrap align="right">6,787 out of 144,773</td>
      <td nowrap align="right">4.7%</td>      
   </tr>
   <tr>
      <td>5</td>
      <td nowrap><a href="https://github.com/bw2/bw2.github.io/blob/master/2022-05-06-STR-truth-set.md#extra-sections">Pure Repeats Catalog<br/>Subset ≥ 12bp</a></td>
      <td>Running <a href="https://github.com/Benson-Genomics-Lab/TRF">TandemRepeatFinder</a> (TRF) with very large mismatch and indel penalties to find all pure repeats that <b>span at least 12bp</b> in the hg38 reference genome</td>
      <td nowrap align="right">1,343,313</td>
      <td nowrap align="right">11,474 out of 144,773</td>
      <td nowrap align="right">7.9%</td>      
   </tr>
   <tr>
      <td>6</td>
      <td nowrap><a href="https://github.com/bw2/bw2.github.io/blob/master/2022-05-06-STR-truth-set.md#extra-sections">Pure Repeats Catalog<br/>Subset ≥ 15bp</a></td>
      <td>Running <a href="https://github.com/Benson-Genomics-Lab/TRF">TandemRepeatFinder</a> (TRF) with very large mismatch and indel penalties to find all pure repeats that <b>span at least 15bp</b> in the hg38 reference genome</td>
      <td nowrap align="right">702,486</td>
      <td nowrap align="right">22,830 out of 144,773</td>
      <td nowrap align="right">15.8%</td>      
   </tr>
</table>


One takeaway is that, if we want to capture more than 95% of STR variants using a TRF-derived catalog, we need to genotype more than 2.8M loci genome-wide in each individual. 

This takeaway is based on the entire truth set - but does is it still true for larger loci - for example the 89,622 (62%) of loci where the reference locus spans at least 24bp? Yes - both the GangSTR and Illumina catalogs would miss 30% to 45% of these variants.

What about loci with relatively large expansions? Arguably these are the loci we're most interested in. If you filter the truth set to the 1,702 (1%) of STR expansions that add 10 or more repeats to the reference repeat count, the percenages of missed loci remain large - with 30% missed by the GangSTR v17 catalog and 45% missed by the Illumina catalog. The 19/20xTCT expansion @ [chr1:18341013-18341042](https://tgg-viewer.broadinstitute.org/#locus=chr1:18341013-18341042&show=~(~'bed~'gtf~'vcf~'alignment)&selectedRows=~(Tool*20Results~(~)~Mappability*20Tracks~(~)~Truth*20Set~(~'Truth*20Set*20BED~'Truth*20Set*20VCF)~CHM1-CHM13~(~'SynDip*20full*20truth*20set*20VCF)~Other*20STR*20Catalogs~(~'Illumina*20Catalog~'GangSTR*20v17*20catalog))&selectedSamples=~()&order=~(~'Truth*20Set*20BED*20~'SynDip*20full*20truth*20set*20VCF*20vcf~'Truth*20Set*20VCF*20vcf~'Illumina*20Catalog*20~'GangSTR*20v17*20catalog*20~'Refseq*20Genes)&sjOptions=~(bounceHeightBasedOn~'random~colorBy~'isAnnotatedJunction~colorByNumReadsThreshold~5~hideAnnotated~false~hideUnannotated~false~labelAnnotatedJunction~false~labelAnnotatedJunctionValue~'*20*5bA*5d~labelMotif~false~labelMultiMappedReadCount~false~labelTotalReadCount~false~labelUniqueReadCount~true~maxFractionMultiMappedReads~1~minSplicedAlignmentOverhang~0~minTotalReads~1~minUniquelyMappedReads~0~showOnlyMinusStrand~false~showOnlyPlusStrand~false~thicknessBasedOn~'numUniqueReads~trackHeight~170~minJunctionEndsVisible~1~labelWithInParen~null~labelWith~'totalReadCount)&vcfOptions=~(displayMode~'EXPANDED)&bamOptions=~(alignmentShading~'strand~showSoftClips~true~trackHeight~400~viewAsPairs~true~showInsertionText~true~showDeletionText~true)&gcnvOptions=~(trackHeight~200~trackMin~0~trackMax~5~autoscale~false~onlyHandleClicksForHighlightedSamples~true)&settingsUrl=~'https*3a*2f*2fstr-truth-set.storage.googleapis.com*2fhg38*2ftgg-viewer-config.json*3fnocache17) is one example truth set variant that's missed by both the GangSTR v17 and the Illumina catalogs. 

---
### Tool comparisons

Using the truth set to compare accuracy of existing STR callers requires us to first define what we mean by accuracy. 
For other variant types such as SNVs and InDels, the definition is relatively straight-forward - a tool will either call a variant or not, and then it might get the zygosity right or wrong, but that's about it. These metrics are also important for STRs, but the additional aspect of number of repeats introduces a lot more nuance. For example, for a given STR locus, a tool may get the number of repeats exactly right, or it may be off by +/-1, or off by many repeats. It might even call an expansion where the true genotype is a contraction. To avoid getting bogged down in finding the right definition, we can begin with the simplest definition and build from there. 

Also, to keep the analysis manageable, we focus on several widely-used tools - ExpansionHunter, GangSTR and HipSTR, and later also look at ExpansionHunterDenovo.

#### Exact accuracy

The simplest definition of STR calling accuracy is - how many genotypes did a tool get exactly right? ie. what fraction of called allele sizes exactly match the corresponding allele size in the truth set. When we run ExpansionHunter, GangSTR and HipSTR on the 139,244 (96%) truth set loci that have 2bp to 6bp motifs and that are present in the reference genome, we find that accuracy varies as follows: 

<table>
   <tr>
      <th>Tool</th>
      <th>Accuracy @ 40x <br />genome coverage</th>
      <th>Accuracy @ 20x <br />genome coverage</th>
      <th>Accuracy @ 10x <br />genome coverage</th>
      <th>Accuracy @ 5x  <br />genome coverage</th>
   </tr>
   <tr>
      <td nowrap>ExpansionHunter v5</td>
      <td>92.6%</td>
      <td>90.9%</td>
      <td>83.3%</td>
      <td>0.1%</td>
   </tr>
   <tr>
      <td nowrap>GangSTR v2.5</td>
      <td>91.0%</td>
      <td>87.1%</td>
      <td>76.1%</td>
      <td>53.5%</td>
   </tr>
   <tr>
      <td nowrap>HipSTR v0.6.2</td>
      <td>74.0%</td>
      <td>72.9%</td>
      <td>65.9%</td>
      <td>42.5%</td>
   </tr>
</table>

We can see that ExpansionHunter slightly outperforms GangSTR, and both tools outperform HipSTR. Unsurprisingly, accuracy decreases when the original data (which has 40x genome-wide coverage) is downsampled to lower read depths.


#### Exact accuracy by number of repeats

For most STR analyses, we care more about large expansions than about variants that only add or remove a few repeats. 
However, as we saw [previously](https://github.com/bw2/bw2.github.io/blob/master/2022-05-06-STR-truth-set.md#results), the overwhelming majority of truth set variants only differ from the reference genome by 1 or 2 repeats. This means the accuracy metric defined above is dominated by variants we don't care as much about. To improve on this, we can look at how accuracy varies across different true allele size bins. 

First though, a technical note about comparing STR genotypes. For a given locus, there are 5 numbers to consider - the number of repeats in the reference genome, the true size of the short allele and the long allele, and finally the short and long allele as called by the given tool. 
For the analyses below, the x-axis values come from comparing the true allele sizes to the number of repeats in the reference. Then, to determine tool accuracy at a locus, the true genotype as well as the tool's reported genotype can be split into a short allele and a long allele. The short alleles can be compared, and then, separately, the long alleles:

<img width="900" alt="image" src="https://user-images.githubusercontent.com/6240170/211456690-509a2d7d-177a-4986-b4ef-1cbda2e13e66.png">

The plots below are based on this approach, so each locus contributes 2 separate counts to the plot - one for the short alleles and one for the long alleles. 

Now, we can look at the fraction of alleles that each tool gets exactly right:

<div align="center"><img src="https://user-images.githubusercontent.com/6240170/210284643-9e99df88-3e18-4937-b12a-530dedfa0965.png" width=800></div>

This plot represents calls @ 40x coverage, and shows how accuracy drops for larger expansions (positive x-axis) but remains steady for contractions (negative x-axis), with ExpansionHunter retaining higher accuracy across all bins.

HipSTR shows poor accuracy largely because it refuses to call many loci, instead outputing the following error message: "Aborting genotyping of the locus as the sequence upstream/downstream of the repeat is too repetitive for accurate genotyping". If we take the loci where HipSTR has "No Call" and exclude them from the comparison for all tools, this discards 25,257 out of 139,244 (18.1%) truth set loci that have 2 to 6bp motifs, and the plot then looks like:

<div align="center"><img src="https://user-images.githubusercontent.com/6240170/211458163-14a24f96-cca9-4a52-9d42-a927cdefc898.png" width=800></div>

This shows that, even on the subset of loci that HipSTR can genotype, its accuracy is roughly the same as GangSTR's and worse than ExpansionHunter's. 

Next, we can look at how accuracy varies for different sequencing coverage depths, showing only ExpansionHunter and GangSTR for clarity:

<div align="center"><img src="https://user-images.githubusercontent.com/6240170/210285501-e10be5f6-847d-4c59-b88f-9009c02ce1a2.png" width=800></div>


#### Accuracy and error size

When a tool doesn't get the genotype exactly right, it matters whether it's off by 1 or by 20 repeats, and whether it tends to overestimate or underestimate the true genotype. This is especially important for rare disease cases where underestimating expansions can lead to missed diagnoses. We can use different colors to add information about the size and direction of errors:

<img src="https://user-images.githubusercontent.com/6240170/210287962-b90dda84-d988-4c69-af3d-8f2d05c37b2c.png" width="100%">

Here, green shows allele sizes that ExpansionHunter got exactly right and so represents the same fraction of calls as the plots in the previous section. Orange represents alleles that ExpansionHunter overestimated (with darker orange meaning a bigger overestimate), while blue represents alleles that ExpansionHunter underestimated (with darker blues representing larger errors). Additional colors include gray for the few loci where ExpansionHunter didn't produce a genotype (such as due to insufficient coverage), red represents the loci that ExpansionHunter called as homozygous reference and so entirely missed the variant, brown is where ExpansionHunter incorrectly called an allele as being heterozygous reference, and teal is for alleles where ExpansionHunter called a contraction but the true allele size was an expansion or vice versa.
The plot shows that ExpansionHunter errs in both directions - overestimating some expansions and underestimating others.   

We can compare this to other tools:

<img src="https://user-images.githubusercontent.com/6240170/210287979-4753df79-81a7-446c-9fd2-34abe2bcda4b.png" width="100%">
<img src="https://user-images.githubusercontent.com/6240170/210287997-8c837077-f169-400e-986b-e81bacd50e45.png" width="100%">

This shows that both GangSTR and HipSTR underestimate (blue) or entirely miss (red) more expansions than ExpansionHunter. 


#### Exome data

Since exome sequencing data is available for the CHM1-CHM13 sample, we can check what fraction of the truth set can be called in an exome. To exclude off-target regions that accidentally got some read coverage, we prefilter loci to exclude those that are intergenic, intronic or in promoters (based on Gencode v42 annotations), and also exclude loci where neither ExpansionHunter nor GangSTR produced a genotype.

<img src="https://user-images.githubusercontent.com/6240170/210300290-a6df46f2-66c2-44d2-b99c-28aa6dcc4393.png" width="100%">
<img src="https://user-images.githubusercontent.com/6240170/210300313-4c698feb-d5ee-45e1-964f-0817ec9ed161.png" width="100%">

As exepcted, exome data only allows us to call 1,766 of the 139,244 (1.3%) truth set loci with 2 to 6bp motifs. Even for this small subset, more than half of the genotype calls are inaccurate. 


#### ExpansionHunterDenovo

TODO describe results

#### Interruptions

TODO describe results

#### Runtime and cost

TODO describe results

---
### Next Steps

The truth set and tool results provide an opportunity to identify features that distinguish
- STR loci that are variant in CHM1-CHM13 vs those that are not
- STR loci where tools produce accurate genotypes
- Filter false-positive STR genotypes

A key next step is to use the truth set to train classifiers for these categories.

---
### Extra Sections

---
**Extra Section 1:** Data availability and details

CHM1-CHM13-2 WGS read data is publicly available under run id ERR1341796: [[SRA](https://trace.ncbi.nlm.nih.gov/Traces/?view=run_browser&acc=ERR1341796&display=data-access)]  [[EBI](https://www.ebi.ac.uk/ena/browser/view/ERR1341796)].

CHM1-CHM13-2 WGS read data is also publicly available from the Broad Institute here: [genome data](https://console.cloud.google.com/storage/browser/broad-public-datasets/CHM1_CHM13_WGS2)

Details:
- Illumina HiSeq X Ten
- PCR-Free protocol
- Paired-end 151bp reads
- 40x Depth of Coverage

Further details are provided in [[Li 2018](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6341484/)].  

CHM1-CHM13 exome sequencing data is also available from the Broad Institute here: [exome data](https://console.cloud.google.com/storage/browser/broad-public-datasets/CHM1_CHM13_WES)

Details:
- Illumina HiSeq X Ten
- Paired-end 151bp reads
- 85x mean target coverage (based on Picard metrics).

---

**Extra Section 2:** Code and other data availability

The source code for all aspects of the truth set analysis is available at [https://github.com/broadinstitute/str-truth-set](https://github.com/broadinstitute/str-truth-set). It includes the following scripts:

* [tool_comparison/scripts/convert_truth_set_to_variant_catalogs.py](https://github.com/broadinstitute/str-truth-set/blob/main/tool_comparison/scripts/convert_truth_set_to_variant_catalogs.py) - a script that converts the truth set into ExpansionHunter and GangSTR input catalogs and also generates the set of true negative loci with a matching distribution of motif sizes. 

TODO describe other scripts here

To run ExpansionHunter, GangSTR, and HipSTR on this sample, I generated variant catalogs with
1) 144,251 positive loci. These are all the loci in the truth set (excluding the 521 that don't have matching repeats in the reference genome). They represent true positive variants.
2) 144,252 negative loci. These are repeat loci in hg38 that are not in the truth set (and therefore have a homozygous reference genotype). They represent true negatives. They were selected by taking the much larger set of all pure repeats in hg38 and selecting a random subset that has the same distribution of motif sizes as the set of positive loci. 

These variant catalogs and other files used in the analysis are publicly available in the [gs://str-truth-set](https://console.cloud.google.com/storage/browser/str-truth-set/hg38) Google Storage bucket. Many of the smaller files are also available on the [Releases page](https://github.com/broadinstitute/str-truth-set/releases) of the [str-truth-set github repo](https://github.com/broadinstitute/str-truth-set).

---

**Extra Section 3:** Genome-wide STR catalogs via TandemRepeatFinder

To generate a comprehensive catalog of pure repeats in hg38, I ran [TandemRepeatFinder](https://github.com/Benson-Genomics-Lab/TRF) with very large mismatch and indel penalties (=1000000) that basically disallow any mismatches or indels. I used a small Minscore value (=8) to include short stretches of repeats:

```
trf catalog.txt 2 1000000 1000000 80 10 8 2000 -ngs -d
```

I then post-processed the output to discard homopolymers and loci than contained fewer than 3 repeats of a motif. Also, I trimmed the loci so that the locus size was an exact multiple of the motif size. These are the results (filtered to different minimum locus size thresholds):


<table>
   <tr>
      <td nowrap><b>Catalog of Pure Repeats</b></td>
      <td nowrap><b># of STR Loci</b></td>
      <td nowrap><b>Download Link</b></td>
   </tr>
   <tr>
      <td nowrap>Pure repeats that <b>span at least 6bp</b> in hg38</td>
      <td nowrap align="right">4,722,859</td>
      <td nowrap><a href="https://storage.googleapis.com/str-truth-set/hg38/ref/other/repeat_specs_GRCh38_without_mismatches.sorted.trimmed.at_least_6bp.bed.gz">gs://str-truth-set/hg38/ref/other/repeat_specs_GRCh38_without_mismatches.sorted.trimmed.at_least_6bp.bed.gz</a></td>
   </tr>
   <tr>
      <td nowrap>Pure repeats that <b>span at least 9bp</b> in hg38</td>
      <td nowrap align="right">2,805,842</td>
      <td nowrap><a href="https://storage.googleapis.com/str-truth-set/hg38/ref/other/repeat_specs_GRCh38_without_mismatches.sorted.trimmed.at_least_9bp.bed.gz">gs://str-truth-set/hg38/ref/other/repeat_specs_GRCh38_without_mismatches.sorted.trimmed.at_least_9bp.bed.gz</a></td>
   </tr>
   <tr>
      <td nowrap>Pure repeats that <b>span at least 12bp</b> in hg38</td>
      <td nowrap align="right">1,343,313</td>
      <td nowrap><a href="https://storage.googleapis.com/str-truth-set/hg38/ref/other/repeat_specs_GRCh38_without_mismatches.sorted.trimmed.at_least_12bp.bed.gz">gs://str-truth-set/hg38/ref/other/repeat_specs_GRCh38_without_mismatches.sorted.trimmed.at_least_12bp.bed.gz</a></td>
   </tr>
   <tr>
      <td nowrap>Pure repeats that <b>span at least 15bp</b> in hg38</td>
      <td nowrap align="right">702,486</td>
      <td nowrap><a href="https://storage.googleapis.com/str-truth-set/hg38/ref/other/repeat_specs_GRCh38_without_mismatches.sorted.trimmed.at_least_15bp.bed.gz">gs://str-truth-set/hg38/ref/other/repeat_specs_GRCh38_without_mismatches.sorted.trimmed.at_least_15bp.bed.gz</a></td>
   </tr>
</table>


Although it wasn't used in the truth set analyses, I also generated a repeat catalog by running [TandemRepeatFinder](https://github.com/Benson-Genomics-Lab/TRF) with a more permissive mismatch penalty (=7) to capture some of the loci missed in the above catalog - such as known pathogenic loci that have interruptions in their reference repeat sequence. I kept the indel penalty very large (=1000000):

```
trf catalog.txt 2 7 1000000 80 10 8 2000 -ngs -d
```
As before, I post-processed the output to discard homopolymers and loci than contained fewer than 3 repeats of a motif. The resulting catalog is available here:

<table>
   <tr>
      <td nowrap><b>Catalog Allowing Mismatches</b></td>
      <td nowrap><b># of STR Loci</b></td>
      <td nowrap><b>Download Link</b></td>
   </tr>
   <tr>
      <td nowrap>Repeats that <b>span at least 6bp</b> in hg38</td>
      <td nowrap align="right">4,655,977</td>
      <td nowrap><a href="https://storage.googleapis.com/str-truth-set/hg38/ref/other/repeat_specs_GRCh38_allowing_mismatches.sorted.trimmed.at_least_6bp.bed.gz">gs://str-truth-set/hg38/ref/other/repeat_specs_GRCh38_allowing_mismatches.sorted.trimmed.at_least_6bp.bed.gz</a></td>
   </tr>
</table>

This catalog has fewer loci than the catalog of pure repeats because a number of adjacent pure repeat loci were merged into single loci once mismatches were allowed. 

---

**Extra Section 4:** A few words about the limitations of existing approaches to STR truth data:

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
**Extra Section 5**: The table below lists STR calling tools + the truth data used in their publications.

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

**Extra Section 6:** Synthetic Diploid Benchmark Overview

[[Li 2018](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6341484/)] produced a high-qaulity truth set based on [Huddleston 2017](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5411763/) haploid assemblies of two individuals - CHM1 and CHM13. 

To create the Synthetic Diploid Benchmark, [[Li 2018](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6341484/)] generated variant calls by:

1. Aligning each haploid assembly to GRCh37 or GRCh38 using minimap2
2. Converting the differences revealed by these alignments to variant calls directly from the CIGAR string. There was no need to run a separate variant calling tool downstream of the alignment step.

**Li et al. 2018 Figure 1:** Constructing the Syndip benchmark dataset. 

![image](https://user-images.githubusercontent.com/6240170/167907455-84baa96d-95ae-44bc-8471-c7769bd6474f.png)

This yielded 5,362,620 variants of which 4,148,586 were in high-confidence regions.

[[Li 2018](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6341484/)] used this data to evaluate SNV and INDEL calling tools, but it can also serve as a high-quality truth set for STRs, as well as tandem repeats (TRs) and structural variants (SVs).


