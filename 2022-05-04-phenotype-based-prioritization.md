## Benchmarking LIRICAL for Phenotype-based Gene Prioritization In Rare Diseaes Cases

LIRICAL [[Robinson 2020](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7477017/)] is a phenotype-based gene & variant prioritization tool.

Lets say an individual has symptoms described by these 7 HPO terms:

- Hearing impairment ([HP:0000365](https://hpo.jax.org/app/browse/term/HP:0000365))  
- Autism ([HP:0000717](https://hpo.jax.org/app/browse/term/HP:0000717))
- Seizure ([HP:0001250](https://hpo.jax.org/app/browse/term/HP:0001250))
- Global developmental delay ([HP:0001263](https://hpo.jax.org/app/browse/term/HP:0001263))
- Gastrointestinal dysmotility ([HP:0002579](https://hpo.jax.org/app/browse/term/HP:0002579))
- Short stature ([HP:0004322](https://hpo.jax.org/app/browse/term/HP:0004322))
- Supraventricular tachycardia ([HP:0004755](https://hpo.jax.org/app/browse/term/HP:0004755))

The LIRICAL algorithm takes these as input along with the individual's variant call file (from WGS or WES) and outputs a list of candidate diagnoses, 
their post-test probabilities, and visualizations showing which of the individual's HPO terms support or contradict each candidate.

For the above example, LIRICAL outputs:

<img width="1000" alt="LIRICAL output screenshot" src="https://user-images.githubusercontent.com/6240170/166859374-128a44d3-6590-44e4-ba95-279bfa2fada9.png">

Clinical geneticists that previously evaluated this case without using LIRICAL came to the conclusion that variants in the KMT2C gene explain 
this patient's phenotype. 

To evaluate LIRICAL performance, I ran it on 75 previously-solved rare disease cases from the [Rare Genomes Project](https://raregenomes.org/). 

- 59 cases: solved with a known gene-disease association. 
- 2 cases: solved with a gene that was previously associated with a different disease phenotype. 
- 14 cases: solved with a gene not previously associated with a disease. 

LIRICAL correctly identified the correct gene in 65 out of the 75 cases (87%), and in 42 out of 75 cases (56%) the correct gene was in the top 3.

<i><u><b>NOTE</b></u>:  By default, LIRICAL uses gnomAD v2 allele frequencies (AFs) when analyzing variants. In order to take advantage of gnomAD v3.1 AFs, the analysis described here is based on first prefiltering the variant call files (VCFs) to gnomAD v3.1 POPMAX AF < 1% before passing them to LIRICAL.</i>

<br />
This histogram show how often LIRICAL ranked the correct gene in the top 5, between 6-10, and >10th in the list, colored by inheritance mode. 
The x-axis represents # of cases: <br /> 
  
<br />
<img width="1000" alt="LIRICAL correct gene rank by inheritance mode" src="https://user-images.githubusercontent.com/6240170/169574825-3e719744-07fe-4e0e-afc6-29c856436c27.png">


Another way to look at this is - for the 65 cases where LIRICAL found the correct gene, what was that gene's rank in the 
list and it's post-test probability:

<img width="750" alt="Plot post-test probability vs LIRICAL rank" src="https://user-images.githubusercontent.com/6240170/166860896-d35babad-a1a5-4d20-a9b4-cc3f58dc8045.png">

To summarize this plot, in 49 out of 75 cases (65%) the correct result was among the top 5 hits and for 36 out of 75 (48%) it also had a post-test probability between 1% and 100%. On the other hand, for 15 cases (20%) the correct result was below 5th in the list and had a post-test probability near 0. Then, for another 10 cases (13%), the correct result was not in the list at all. 

**Conclusion:** LIRICAL shows relatively high sensitivity in finding the causal genes for rare disease cases from [RGP](https://raregenomes.org/). 

---

**How many genes would someone need to look through for a typical case?**

From the above plot, a conservative approach would be to only consider the top 5 results (x-axis cutoff) and only if they have a post-test probability (PTP) of 1% or higher (y-axis cutoff). This would give 3 results (or more percisely, 2.53 results) to look at on average, with 24% of cases having 5 or more results with PTP > 1%:

<img width="500" alt="histogram: % of RGP cases that have 0, 1, 2, 3, 4, or 5 LIRICAL results with PTP > 1 and rank <= 5" src="https://user-images.githubusercontent.com/6240170/169594097-7f9caeee-824c-4baf-b5d4-0992dfc70c56.png">

**Conclusion:**  3 genes per case when using cutoffs that would yield ~50% sensitivity.

---

**What is the false-positive rate?**

The above plot shows that, although LIRICAL reports the correct gene as #1 in the list in 23 out of 75 cases (31%), most of the time the 
correct gene is further down in the list. All genes above the correct gene can be considered false positives. With conservative thresholds of only looking at the top 5 results and only when they have a post-test probability (PTP) of 1% or higher, analysts would need to look at ~2 false-positive genes per case on average.

Another way to look into this and also test how much LIRICAL performance depends on variants vs. phenotype match is to rerun the same tests, but substitute in variants from completely unrelated healthy individuals sequenced as part of the same cohort. I did this 5x for each of the 75 solved cases above (=> 375 test runs). Unsurprisingly, this caused LIRICAL accuracy to drop to esssentially 0: only 10 out of the 375 LIRICAL reports (3%) still included the correct gene, and only 3 of these were in the top 5 and had a post-test probability > 1%.

However, in 260 out of 375 tests (70%) LIRICAL still reported at least one result with a post-test probability > 1%:

<!-- img width="429" alt="image" src="https://user-images.githubusercontent.com/6240170/166864705-af5f4943-d41e-4416-967d-e6f16183c85a.png" -->
<img width="500" alt="histogram: % of RGP cases that had 0, 1, 2, 3, 4, or 5 false-positive LIRICAL results with PTP > 1 and rank <= 5" src="https://user-images.githubusercontent.com/6240170/166866744-55f075b5-08e5-4999-bbec-8bde066add03.png">

This again shows that, even with conservative thresholds of top-5 and PTP > 1%, a user should expect to see on average 2 false-positive results per case. 

**Conclusion:**  At least 2 genes per case.

---

**Can LIRICAL performance be improved further?**

Yes - through additional prefiltering. For the tests above, I prefiltered each individual's variants to exclude those that are common in the general popualation (keeping only variants with gnomAD v3 PopMax AF < 0.01). Applying this prefilter didn't change the number of true positive results, but improved their average rank from 7.6 to 5.9.
Adding further prefiltering - such as by inheritance mode for cases where parents' DNA is available will almost certainly improve results further. 

---

References:

1. Robinson PN, Ravanmehr V, Jacobsen JOB, et al. Interpretable Clinical Genomics with a Likelihood Ratio Paradigm. Am J Hum Genet. 2020;107(3):403-417. [doi:10.1016/j.ajhg.2020.06.021](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7477017/)
2. Yuan X, Wang J, Dai B, et al. Evaluation of phenotype-driven gene prioritization methods for Mendelian diseases. Brief Bioinform. 2022;23(2):bbac019. [doi:10.1093/bib/bbac019](https://pubmed.ncbi.nlm.nih.gov/35134823/)



