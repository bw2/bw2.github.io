
The [previous blog post](https://github.com/bw2/bw2.github.io/blob/master/2022-05-04-phenotype-based-prioritization.md) evaluated [LIRICAL](https://pubmed.ncbi.nlm.nih.gov/32755546/)
performance on 75 previously solved phenotypically-heterogeneous cases from the [Rare Genomes Project](https://raregenomes.org/). Here, I compare
[LIRICAL](https://pubmed.ncbi.nlm.nih.gov/32755546/) to [Exomiser](https://www.nature.com/articles/nprot.2015.124) on the same set of cases and find that:
1. Exomiser performs slightly better than LIRICAL overall
2. Exomiser and LIRICAL ranks are NOT well correlated, so rare disease pipelines can benefit from evaluating the top hits of both tools

Exomiser [[Smedley, Robinson 2015](https://www.nature.com/articles/nprot.2015.124)] has been widely used for phenotype-based prioritzation 
in rare disease cases. Five years after publishing Exomiser, the same authors created 
LIRICAL [[Robinson, Smedley 2020](https://pubmed.ncbi.nlm.nih.gov/32755546/)] to give users a way to tell when the highest-ranked hits in a given case 
are low-confidence and not worth evaluating. Unfortunately, based on the analysis in my [previous blog post](https://github.com/bw2/bw2.github.io/blob/master/2022-05-04-phenotype-based-prioritization.md), 
this feature doesn't currently work well, and users are better off ignoring LIRICAL's post-test probability (except to check that it's > 0%).
Just looking at the 3 top-ranked hits (or however many you have time for) provides better accuracy than thresholding on the post-test probability.

---

**LIRICAL vs Exomiser comparison in [Robinson 2020]**  

The LIRICAL paper [[Robinson 2020](https://pubmed.ncbi.nlm.nih.gov/32755546/)] compared performance on 116 previously-solved singleton cases from the 100,000 Genomes Project.

**Fig. 4** shows Exomiser slightly out-performing LIRICAL:

<img alt="[Robinson 2020] Figure 4" src="https://user-images.githubusercontent.com/6240170/171466464-0a5a72e0-44d0-47a2-b512-61812f4b6641.png" width=500 />

"Considering the 89 diagnoses where Exomiser was not utilized, Exomiser prioritized 57/89 (64%) in first place compared to 51/89 (57%) for LIRICAL."

---


**LIRICAL vs Exomiser on 75 cases from the Rare Genomes Project**

These distributions show what rank each tool assigns to the correct gene in 75 RGP cases: 

<img width="800" alt="LIRICAL and Exomiser rank distributions" src="https://user-images.githubusercontent.com/6240170/171470046-0a114cbd-215d-404f-b526-d7f80d085d83.png">

Both Exomiser and LIRICAL rank the correct gene among the top-5 results for 49 out of 75 (65%) of cases.

Interestingly, LIRICAL and Exomiser ranks aren't well correlated (R^2 is 0.05) as this plot shows:

<img width="850" alt="image" src="https://user-images.githubusercontent.com/6240170/171471200-b78706fe-a26a-4eea-880d-5599523d45eb.png">


