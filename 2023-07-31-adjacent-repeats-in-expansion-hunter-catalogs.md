## How adjacent repeats in ExpansionHunter catalogs affect genotype quality

ExpansionHunter has a unique feature where, for each locus, users can optionally specify adjacent STR loci, and ExpansionHunter will genotype both the main locus and the adjacent loci together. For example, for the Huntington's disease locus, rather than just specifying the CAG repeat as in:
```
{
    "LocusId": "HTT",
    "LocusStructure": "(CAG)*",
    "ReferenceRegion": "4:3074876-3074933",
    "VariantType": "Repeat",
}
```
the user can also specify the adjacent CCG repeat (source: 
[the official ExpansionHunter catalog](https://github.com/Illumina/ExpansionHunter/blob/master/variant_catalog/grch38/variant_catalog.json#L458-L473)):
```
{
    "LocusId": "HTT",
    "LocusStructure": "(CAG)*CAACAG(CCG)*",
    "ReferenceRegion": [
        "4:3074876-3074933",
        "4:3074939-3074966"
    ],
    "VariantId": [
        "HTT",
        "HTT_CCG"
    ],
    "VariantType": [
        "Repeat",
        "Repeat"
    ]
}
```

To understand how specifying adjacent loci affects ExpansionHunter performance, I wrote a script that adds adjacent 
loci to existing STR catalogs. It takes any ExpansionHunter variant catalog (such as the 
Illumina [catalog of 174k polymorphic loci](https://github.com/Illumina/RepeatCatalogs)) as well as a catalog of all 
STRs in the reference genome (such as those produced by running TandemRepeatFinder) and outputs a new catalog after 
adding adjacent repeats that are within a user-defined distance from the original locus. This script is 
called `add_adjacent_loci_to_expansion_hunter_catalog` and is available in the 
[str_analysis](https://github.com/broadinstitute/str-analysis) repo.


### TR truth set analysis

To test this script and evaluate how adjacent loci affect ExpansionHunter accuracy, I used the TR truth set from 
[Insights from a genome-wide truth set of tandem repeat variation by Ben Weisburd, Grace Tiao, Heidi L. Rehm
bioRxiv 2023.05.05.539588](https://www.biorxiv.org/content/10.1101/2023.05.05.539588v1). 

This truth set contains 146,318 TR loci that are polymorphic in the CHM1-CHM13 synthetic diploid sample and also present in the hg38 reference.

I converted these to ExpansionHunter catalog format, and then  ran `add_adjacent_loci_to_expansion_hunter_catalog` on it. For the reference TR catalog argument, I used 
```
gs://str-truth-set/hg38/ref/other/repeat_specs_GRCh38_without_mismatches.including_homopolymers.sorted.at_least_9bp.bed.gz
```
which contains 4,484,369 pure TR loci detected in hg38 by TandemRepeatFinder.  
Also, I set the `--max-distance-between-adjacent-repeats` parameter to 50bp which is 1/3 the read length. 

The full command line was:
```
python3 -u -m str_analysis.add_adjacent_loci_to_expansion_hunter_catalog \
	--source-of-adjacent-loci ./ref/other/repeat_specs_GRCh38_without_mismatches.including_homopolymers.sorted.at_least_9bp.bed.gz \
	--ref-fasta ./ref/hg38.fa \
        --max-distance-between-adjacent-repeats 50 \
	--add-extra-fields \
    truth_set_variant_catalog.json
```

### Adjacent loci summary statistics

For the 146,318 polymorphic TR loci in CHM1-CHM13:

```
  67,003 out of 146,318 polymorphic loci (45.8%) were found to have 1 or more adjacent repeats
```

The distances between the adjacent loci were distributed as follows:
```
  39,850 out of  114,220 spacers ( 34.9%) had     0bp spacer
   8,772 out of  114,220 spacers (  7.7%) had     1bp spacer
   3,895 out of  114,220 spacers (  3.4%) had     2bp spacer
   4,240 out of  114,220 spacers (  3.7%) had     3bp spacer
   3,148 out of  114,220 spacers (  2.8%) had     4bp spacer
   3,481 out of  114,220 spacers (  3.0%) had     5bp spacer
   ...
   2,189 out of  114,220 spacers (  1.9%) had    10bp spacer
   ...
   1,952 out of  114,220 spacers (  1.7%) had    15bp spacer
   ...
   1,202 out of  114,220 spacers (  1.1%) had    20bp spacer
   ...
     687 out of  114,220 spacers (  0.6%) had    30bp spacer
   ...
     516 out of  114,220 spacers (  0.5%) had    40bp spacer
   ...
     393 out of  114,220 spacers (  0.3%) had    50bp spacer
```

The most common configuration was a pair of adjacent loci (the main locus + a newly added adjacent locus) with differing motifs - like the HTT locus example above. The other configurations were as follows:
```
  30,029 out of  260,538 reference regions ( 11.5%) had adjacent repeats count:   2 reference regions with different motifs
   9,907 out of  260,538 reference regions (  3.8%) had adjacent repeats count:   2 reference regions with same motif
  15,117 out of  260,538 reference regions (  5.8%) had adjacent repeats count:   3 reference regions with different motifs
     631 out of  260,538 reference regions (  0.2%) had adjacent repeats count:   3 reference regions with same motif
   6,286 out of  260,538 reference regions (  2.4%) had adjacent repeats count:   4 reference regions with different motifs
      74 out of  260,538 reference regions (  0.0%) had adjacent repeats count:   4 reference regions with same motif
   2,709 out of  260,538 reference regions (  1.0%) had adjacent repeats count:   5 reference regions with different motifs
       4 out of  260,538 reference regions (  0.0%) had adjacent repeats count:   5 reference regions with same motif
   1,281 out of  260,538 reference regions (  0.5%) had adjacent repeats count:   6 reference regions with different motifs
     556 out of  260,538 reference regions (  0.2%) had adjacent repeats count:   7 reference regions with different motifs
     247 out of  260,538 reference regions (  0.1%) had adjacent repeats count:   8 reference regions with different motifs
     100 out of  260,538 reference regions (  0.0%) had adjacent repeats count:   9 reference regions with different motifs
      43 out of  260,538 reference regions (  0.0%) had adjacent repeats count:  10 reference regions with different motifs
      14 out of  260,538 reference regions (  0.0%) had adjacent repeats count:  11 reference regions with different motifs
       2 out of  260,538 reference regions (  0.0%) had adjacent repeats count:  12 reference regions with different motifs
       2 out of  260,538 reference regions (  0.0%) had adjacent repeats count:  13 reference regions with different motifs
       1 out of  260,538 reference regions (  0.0%) had adjacent repeats count:  14 reference regions with different motifs
```

Unsurprisingly, if I went back and selected approximately the same number of non-polymorphic loci (145,429) from the hg38 reference so that they had the same distribution of motif sizes as the polymorphic loci, a smaller percentage of the non-polymorphic lcoi had adjacent repeats:

```
   49,862 out of 145,429 non-polymorphic loci (34.4%) were found to have 1 or more adjacent repeats
```

### ExpansionHunter results with vs. without specifying adjacent loci 

To see how ExpansionHunter performance changes when specifying adjacent loci, I followed these steps:
- selected the 66,523 (45.5%) of polymorphic loci that had ExpansionHunter calls and at least 1 adjacent repeat within 50bp of the main locus 
- generated 2 ExpansionHunter variant catalogs for these 66,523 loci: one that included adjacent repeats, and one that didn't
- looked at differences between ExpansionHunter calls with vs. without adjacent repeats

```
 57,854 out of 66,523 (87%) loci had the same exact genotype with vs. without specifying adjacent loci
```

To see how different distances (ie. spacer sizes) between adjacent repeats affected results, I selected subsets of 
loci where the adjacent repeats were closer together than a particular max distance, and checked
what fraction of them had the exact same ExpansionHunter genotype with vs. without specifying adjacent repeat(s):

```
Distance between adjacent repeats =   0bp: Genotype didn't change for 11,918 out of 15,083 (79.0%) loci
Distance between adjacent repeats <= 10bp: Genotype didn't change for 30,495 out of 36,224 (84.2%) loci
Distance between adjacent repeats <= 20bp: Genotype didn't change for 41,863 out of 48,928 (85.6%) loci
Distance between adjacent repeats <= 30bp: Genotype didn't change for 48,826 out of 56,669 (86.2%) loci
Distance between adjacent repeats <= 40bp: Genotype didn't change for 53,727 out of 62,035 (86.6%) loci
Distance between adjacent repeats <= 50bp: Genotype didn't change for 57,854 out of 66,523 (87.0%) loci
```

When plotted, this looks like:  

<img width="577" alt="image" src="https://github.com/bw2/bw2.github.io/assets/6240170/449ab132-da02-42aa-a574-52a9c3822345">

This suggests that there's not much point in setting `--max-distance-between-adjacent-repeats` to values larger than ~20bp.


### Concordance with truth set genotypes

I then checked ExpansionHunter accuracy as measured by concordance with the true genotypes from the Synthetic Diploid Benchmark:

<img width="836" alt="image" src="https://github.com/bw2/bw2.github.io/assets/6240170/167255dc-3f5d-431f-b878-09aa8fdaac63">

The blue line represents the calls with adjacent loci, and is slightly lower - suggesting that specifying adjacent loci **slightly reduced** concordance with the truth set. 

More detailed stats are below, where genotyping error at a locus is defined as the total difference between the true allele size and ExpansionHunter's estimated allele size for allele1 + allele2.

```
40,423 out of 48,042 (84.1%) loci: genotype error didn't change when running ExpansionHunter with vs. without adjacent loci.
---
1,881 out of 48,042 ( 3.9%) loci: allele1 + allele2 genotype error decreased by at least 3 repeats when using adjacent loci.
1,258 out of 48,042 ( 2.6%) loci: allele1 + allele2 genotype error INCREASED by at least 3 repeats when using adjacent loci.
---
1,434 out of 48,042 ( 3.0%) loci: allele1 + allele2 genotype error decreased by at least 5 repeats when using adjacent loci.
  777 out of 48,042 ( 1.6%) loci: allele1 + allele2 genotype error INCREASED by at least 5 repeats when using adjacent loci.
```

These proportions between the number of loci where errors increased vs. decreased stay approximately the same even when I prefilter to alleles that have the highest genotype 
quality scores (Q > 0.8), or those that only have trinucleotide motifs. 

### Manual review of read visualizations

I then looked at REViewer images for 100 loci where adding adjacent repeats changed the genotype by 3 or more repeats total. 
For this, I selected only pure repeat loci where adjacent repeats didn't have any spacers between them (since on initial review, it looked like these were the loci where genotype quality 
improved most clearly after the addition of adjacent repeats). 
At each locus, I compared two images: one from running ExpansionHunter with adjacent repeats specified, and one without adjacent repeats. 

The stats for these 100 loci were:

```
50 loci ended up with low quality genotypes both with and without repeats
36 loci had higher quality genotypes when adjacent repeats were specified
10 loci had lower quality genotypes when adjacent repeats were specified
 4 loci were amgibuous
```

For 20 of these loci, the true genotype from the STR truth set appeared to be incorrect - implying that loci where ExpansionHunter genotypes significantly differ with vs. without adjacent repeats are enriched for assembly errors or cell line mutations in the CHM1-CHM13 synthetic diploid. 

The 200 REViewer images for these 100 loci can be viewed here:  [[200 REViewer images](https://bw2.github.io/2023-07-31_adjacent_repeats_flipbook/)]

### Conclusions

- It's possible to find/add adjacent repeats for 30 to 50% of loci in any given STR catalog.
- Within those 30 to 50%, adjacent repeats only make a difference (ie. change ExpansionHunter's genotype) in 5 to 10% of polymorphic loci.
- In ~7% of loci, specifying adjacent repeats changed the ExpansionHunter genotype by 3 or more repeats.
- For these 7% of loci, introducing adjacent repeats improved the genotype quality for 36% of loci, and reduced the genotype quality in 10% of loci (based on manual review). For 50% of these loci, the genotype quality remained equally bad with and without adjacent repeats.
- When running `add_adjacent_loci_to_expansion_hunter_catalog.py`, 20 is a reasonable value for `--max-distance-between-adjacent-repeats`.


