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

#### TR Truth Set analysis

To test this script and evaluate how adjacent loci affect ExpansionHunter accuracy, I used the TR truth set from 
[Insights from a genome-wide truth set of tandem repeat variation by Ben Weisburd, Grace Tiao, Heidi L. Rehm
bioRxiv 2023.05.05.539588](https://www.biorxiv.org/content/10.1101/2023.05.05.539588v1). 

This truth set contains 146,640 TR loci that are polymorphic in the CHM1-CHM13 synthetic diploid sample. 

First, I ran the `add_adjacent_loci_to_expansion_hunter_catalog` on the ExpansionHunter catalog for these 146,640 loci, and using the reference TR catalog 
```gs://str-truth-set/hg38/ref/other/repeat_specs_GRCh38_without_mismatches.including_homopolymers.sorted.at_least_9bp.bed.gz```
which contains 4,484,369 pure TR loci detected in hg38 by TandemRepeatFinder.

```
python3 -u -m str_analysis.add_adjacent_loci_to_expansion_hunter_catalog \
	--source-of-adjacent-loci ./ref/other/repeat_specs_GRCh38_without_mismatches.including_homopolymers.sorted.at_least_9bp.bed.gz \
	--ref-fasta ./ref/hg38.fa \
    --max-distance-between-adjacent-repeats 10 \
	--add-extra-fields \
    truth_set_variant_catalog.json
```


**Pros and Cons**
- can genotype multiple loci together and use REViewer to see phased visualizations


