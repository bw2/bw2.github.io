ExpansionHunter has a unique feature where users can specify adjacent STR loci next to the main locus being genotyped, and ExpansionHunter will genotype both the main locus and these adjacent loci together. For example, for the Huntington's disease locus, rather than just specifying the CAG repeat as in:
```
{
    "LocusId": "HTT",
    "LocusStructure": "(CAG)*",
    "ReferenceRegion": "4:3074876-3074933",
    "VariantType": "Repeat",
}
```
the user can specify the adjacent CCG repeat (source: 
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

**Pros and Cons**
- can genotype multiple loci together and use REViewer to see phased visualizations


