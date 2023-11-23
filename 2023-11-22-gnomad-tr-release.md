## Updating the disease-associated TR callset in gnomAD

### Defining the locus catalog

The latest variant catalogs for known disease-associated TR loci in ExpansionHunter format are available @
- [variant_catalog_without_offtargets.GRCh38.json](https://github.com/broadinstitute/str-analysis/blob/main/str_analysis/variant_catalogs/variant_catalog_without_offtargets.GRCh38.json)
- [variant_catalog_with_offtargets.GRCh38.json](https://github.com/broadinstitute/str-analysis/blob/main/str_analysis/variant_catalogs/variant_catalog_with_offtargets.GRCh38.json)

There are five new loci based on recent publications or bioRxiv preprints:
```
ABCD3  (Oculopharyngodistal myopathy when >= 124 x GCC repeats)
FGF14  (Spinocerebellar ataxia when >= 250 x AAG repeats)
THAP11 (Spinocerebellar ataxia when >= 45 x CAG repeats)
RILPL1 (Oculopharyngodistal myopathy when >= 139 x GGC repeats)
ZFHX3  (Spinocerebellar ataxia when  >= 46 x GCC repeats)
```
Also, there are 7 new loci that have not been directly/confidently linked to monogenic disease, but have been
published as candidate disease loci (eg. AFF3), or included in published lists of pathogenic loci - most recently by [[English 2023](https://www.biorxiv.org/content/10.1101/2023.10.29.564632v1.full)] @ https://zenodo.org/records/8329210
```
AFF3 
C11ORF80
CBL
FRA10AC1
NOTCH2NLA
TMEM185A
ZNF713
```

To define adjacent repeat regions for these loci where relevant, I ran: 
```
python3 -u -m str_analysis.add_adjacent_loci_to_expansion_hunter_catalog \
    --ref-fasta hg38.fa \
    --max-distance-between-adjacent-repeats 6 \
    --max-adjacent-repeats 2 \
    --source-of-adjacent-loci  str-truth-set/ref/other/repeat_specs_GRCh38_without_mismatches.including_homopolymers.sorted.at_least_6bp.bed.gz \
    variant_catalog_without_offtargets.GRCh38.json \
    -x ATXN2 -x PABPN1 -x TCF4 -x AFF2 -x AR -x SAMD12 -x DAB1 -x DMD
```
For more details on adjacent repeats, see [2023-07-31-adjacent-repeats-in-expansion-hunter-catalogs](https://bw2.github.io/2023-07-31-adjacent-repeats-in-expansion-hunter-catalogs.html).

Also, to add off-target regions I used the [str_analysis.add_offtarget_regions](https://github.com/broadinstitute/str-analysis/tree/main) script. 


### Locus QC

To estimate ExpansionHunter genotyping error rates at these locus, I ran a mendelian violations analysis using 
510 trios from internal cohorts with high-quality PCR-free WGS data. 


### Sample QC 

For this release, added publicly-available HGDP samples and filtered out 
- PCR+ samples
- samples with 100bp reads





