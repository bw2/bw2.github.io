ExpansionHunter has a unique feature where, for each locus, users can optionally specify any adjacent STR loci, and ExpansionHunter will genotype both the main locus and these adjacent loci together. For example, for the Huntington's disease locus, rather than just specifying the CAG repeat as in:
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

To understand how specifying adjacent loci affects ExpansionHunter performance, I wrote a script that adds adjacent loci to existing STR catalogs. It takes any ExpansionHunter variant catalog (such as the Illumina [catalog of 174k polymorphic loci](https://github.com/Illumina/RepeatCatalogs)) as well as a catalog of all STRs in the reference genome (such as those produced by running TandemRepeatFinder) and outputs a new catalog after adding adjacent repeats that are within a user-defined distance from the original locus. This script is called `add_adjacent_loci_to_expansion_hunter_catalog` and is available in the [str_analysis](https://github.com/broadinstitute/str-analysis) repo:

```
usage: add_adjacent_loci_to_expansion_hunter_catalog.py [-h] --ref-fasta REF_FASTA [-d MAX_DISTANCE_BETWEEN_ADJACENT_REPEATS]
                                                        [--max-overlap-between-adjacent-repeats MAX_OVERLAP_BETWEEN_ADJACENT_REPEATS]
                                                        [--max-total-adjacent-region-size MAX_TOTAL_ADJACENT_REGION_SIZE]
                                                        --source-of-adjacent-loci SOURCE_OF_ADJACENT_LOCI [--add-extra-info-to-locus-id]
                                                        [--add-extra-fields] [--output-dir OUTPUT_DIR] [-o OUTPUT_CATALOG]
                                                        input_catalog_paths [input_catalog_paths ...]

positional arguments:
  input_catalog_paths   ExpansionHunter catalog json file path. If more than one catalog path is specified, the catalogs will be processed
                        sequentially, and the output catalog arg will be used as an output filename suffix.

optional arguments:
  -h, --help            show this help message and exit
  --ref-fasta REF_FASTA
                        Reference fasta path
  -d MAX_DISTANCE_BETWEEN_ADJACENT_REPEATS, --max-distance-between-adjacent-repeats MAX_DISTANCE_BETWEEN_ADJACENT_REPEATS
                        Loci no more than this many base pairs from each other will be combined into a single locus, including any non-
                        repetitive bases between them
  --max-overlap-between-adjacent-repeats MAX_OVERLAP_BETWEEN_ADJACENT_REPEATS
                        TandemRepeatFinder sometimes outputs loci that overlap by a few base pairs. For ExpansionHunter catalogs that are
                        based on TandemRepeatFinder output, this controls how slightly overlapping loci are combined
  --max-total-adjacent-region-size MAX_TOTAL_ADJACENT_REGION_SIZE
                        The maximum size of the region spanning all adjacent repeats that we will load from the adjacent loci bed file
  --source-of-adjacent-loci SOURCE_OF_ADJACENT_LOCI
                        The local or Google Storage (gs://) path of a .bed file that specifies repeat intervals in the reference genome. It
                        should have 0-based coordinates and the name field (column 4) should contain the repeat motif. This can be a large
                        catalog of loci generated using TandemRepeatFinder. This .bed file will be used as the source for adjacent loci.
  --add-extra-info-to-locus-id
                        Add info about adjacent loci to the locus id in the output variant catalog. This will include the number of adjacent
                        loci and the max distance between them.
  --add-extra-fields    Add extra fields to each locus in the output variant catalog that record the number of base pairs between any adjacent
                        loci and the main locus in an easy-to-parse format
  --output-dir OUTPUT_DIR
                        Output directory. If not specified, the input catalog's directory will be used.
  -o OUTPUT_CATALOG, --output-catalog OUTPUT_CATALOG
                        Path where to write the output catalog. If not specified, it will be based on the input catalog path
```

### TR Truth Set analysis

To test this script and evaluate how adjacent loci affect ExpansionHunter accuracy, I used the TR truth set from 
[Insights from a genome-wide truth set of tandem repeat variation by Ben Weisburd, Grace Tiao, Heidi L. Rehm
bioRxiv 2023.05.05.539588](https://www.biorxiv.org/content/10.1101/2023.05.05.539588v1). 

This truth set contains 146,640 TR loci that are polymorphic in the CHM1-CHM13 synthetic diploid sample. 

First, I ran `add_adjacent_loci_to_expansion_hunter_catalog` on the ExpansionHunter catalog for these 146,640 truth set loci.  
For the reference TR catalog, I used 
```
gs://str-truth-set/hg38/ref/other/repeat_specs_GRCh38_without_mismatches.including_homopolymers.sorted.at_least_9bp.bed.gz
```
which contains 4,484,369 pure TR loci detected in hg38 by TandemRepeatFinder.  
Also, I set `max-distance-between-adjacent-repeats = 10` because I found little difference in performance when I increased this arg. 
The full command line was:
```
python3 -u -m str_analysis.add_adjacent_loci_to_expansion_hunter_catalog \
	--source-of-adjacent-loci ./ref/other/repeat_specs_GRCh38_without_mismatches.including_homopolymers.sorted.at_least_9bp.bed.gz \
	--ref-fasta ./ref/hg38.fa \
        --max-distance-between-adjacent-repeats 10 \
	--add-extra-fields \
    truth_set_variant_catalog.json
```

#### Stats on adjacent loci

```
 48,391 out of 146,318 loci (33.1%) were found to have 1 or more adjacent repeats
```

The distances between these adjacent loci were distributed as follows:
```
  35,837 out of   68,991 spacers (51.9%) had     0bp spacer
   8,273 out of   68,991 spacers (12.0%) had     1bp spacer
   3,452 out of   68,991 spacers ( 5.0%) had     2bp spacer
   3,852 out of   68,991 spacers ( 5.6%) had     3bp spacer
   2,791 out of   68,991 spacers ( 4.0%) had     4bp spacer
   3,164 out of   68,991 spacers ( 4.6%) had     5bp spacer
   2,349 out of   68,991 spacers ( 3.4%) had     6bp spacer
   2,732 out of   68,991 spacers ( 4.0%) had     7bp spacer
   2,093 out of   68,991 spacers ( 3.0%) had     8bp spacer
   2,527 out of   68,991 spacers ( 3.7%) had     9bp spacer
   1,921 out of   68,991 spacers ( 2.8%) had    10bp spacer
```

The most common configuration was a pair of adjacent loci (the main locus + a newly added adjacent locus) with different motifs. The other configurations were as follows:
```
  26,360 out of  215,309 reference regions (12.2%) had adjacent repeats count:   2 reference regions with different motifs
   7,949 out of  215,309 reference regions ( 3.7%) had adjacent repeats count:   2 reference regions with same motif
   9,460 out of  215,309 reference regions ( 4.4%) had adjacent repeats count:   3 reference regions with different motifs
     219 out of  215,309 reference regions ( 0.1%) had adjacent repeats count:   3 reference regions with same motif
   2,961 out of  215,309 reference regions ( 1.4%) had adjacent repeats count:   4 reference regions with different motifs
       8 out of  215,309 reference regions ( 0.0%) had adjacent repeats count:   4 reference regions with same motif
     955 out of  215,309 reference regions ( 0.4%) had adjacent repeats count:   5 reference regions with different motifs
     333 out of  215,309 reference regions ( 0.2%) had adjacent repeats count:   6 reference regions with different motifs
     105 out of  215,309 reference regions ( 0.0%) had adjacent repeats count:   7 reference regions with different motifs
      30 out of  215,309 reference regions ( 0.0%) had adjacent repeats count:   8 reference regions with different motifs
       7 out of  215,309 reference regions ( 0.0%) had adjacent repeats count:   9 reference regions with different motifs
       4 out of  215,309 reference regions ( 0.0%) had adjacent repeats count:  10 reference regions with different motifs
```

#### ExpansionHunter performance with vs. without specifying adjacent loci 

To evaluate how ExpansionHunter performance changed when specifying adjacent loci, I first selected the 48,391 (33%) of loci where at least 1 adjacent repeat was added by 
the `add_adjacent_loci_to_expansion_hunter_catalog` script. Then, I ran ExpansionHunter on these loci first with and then without specifying the adjacent loci. 

```
 40,127 out of 48,042 (83.5%) loci had the same exact genotype with vs. without using adjacent loci
```

I then checked ExpansionHunter accuracy as measured by concordance with the true genotypes from the Synthetic Diploid Benchmark:

<img width="836" alt="image" src="https://github.com/bw2/bw2.github.io/assets/6240170/167255dc-3f5d-431f-b878-09aa8fdaac63">

The blue line represents the calls with adjacent loci, and is slightly lower - indiciating that including adjacent loci leads to **slightly reduced** accuracy overall. 

To look a this is more detail, we can compare the per-locus genotyping errors when running ExpansionHunter with vs. without adjacent loci. 
Here genotyping error at a locus is measured as the total difference between the true allele size and ExpansionHunter's estimated allele size for allele1 + allele2.

```
40,423 out of 48,042 (84.1%) loci:  genotype error didn't change when running ExpansionHunter with vs. without adjacent loci.
---
3,622 out of 48,042 ( 7.5%) loci: allele1 + allele2 genotype error decreased by at least 1 repeats when using adjacent loci.
3,995 out of 48,042 ( 8.3%) loci: allele1 + allele2 genotype error INCREASED by at least 1 repeats when using adjacent loci.
---
2,375 out of 48,042 ( 4.9%) loci: allele1 + allele2 genotype error decreased by at least 2 repeats when using adjacent loci.
2,113 out of 48,042 ( 4.4%) loci: allele1 + allele2 genotype error INCREASED by at least 2 repeats when using adjacent loci.
---
1,881 out of 48,042 ( 3.9%) loci: allele1 + allele2 genotype error decreased by at least 3 repeats when using adjacent loci.
1,258 out of 48,042 ( 2.6%) loci: allele1 + allele2 genotype error INCREASED by at least 3 repeats when using adjacent loci.
---
1,644 out of 48,042 ( 3.4%) loci: allele1 + allele2 genotype error decreased by at least 4 repeats when using adjacent loci.
  974 out of 48,042 ( 2.0%) loci: allele1 + allele2 genotype error INCREASED by at least 4 repeats when using adjacent loci.
---
1,434 out of 48,042 ( 3.0%) loci: allele1 + allele2 genotype error decreased by at least 5 repeats when using adjacent loci.
  777 out of 48,042 ( 1.6%) loci: allele1 + allele2 genotype error INCREASED by at least 5 repeats when using adjacent loci.
```

These proportions between the number of loci where errors increased vs. decreased stay approximately the same even when I prefilter to alleles that have the highest genotype 
quality scores (Q > 0.8) in all cases (ie. when called with and without adjacent repeats).


### Conclusions

- Adding adjacent loci significantly improves performance for ~4% of loci and significantly degrades performance for ~2% of loci. 
- For ~85% of loci, adding adjacent loci has no effect on the results.
- Based on this, it makes sense to add adjacent loci only for a small subset of loci and only after confirming that this improves accuracy.
- Since REViewer can phase reads across adjacent loci, they can also be useful for loci where phased genotypes are of interest. 


