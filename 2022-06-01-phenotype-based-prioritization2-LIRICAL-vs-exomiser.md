## LIRICAL vs Exomiser Phenotype-based Prioritization In 75 Rare Diseaes Cases

The [previous blog post](https://github.com/bw2/bw2.github.io/blob/master/2022-05-04-phenotype-based-prioritization.md) evaluated [LIRICAL](https://pubmed.ncbi.nlm.nih.gov/32755546/)
 on 75 previously solved phenotypically-heterogeneous cases from the [Rare Genomes Project](https://raregenomes.org/) (RGP). This blog post compares
[LIRICAL](https://pubmed.ncbi.nlm.nih.gov/32755546/) to [Exomiser](https://www.nature.com/articles/nprot.2015.124) on the same set of cases and finds that:
1. Exomiser and LIRICAL top-5 accuracy is identical (65%), but LIRICAL has better top-3 accuracy (56%) than Exomiser (49%). 
2. Exomiser and LIRICAL ranks are NOT well correlated (R<sup>2</sup>=0.05) and rare disease pipelines should consider top hits from both tools.

Exomiser [[Smedley, Robinson 2015](https://www.nature.com/articles/nprot.2015.124)] has been widely used for phenotype-based prioritzation 
in rare disease cases. Five years after publishing Exomiser, the same authors created 
LIRICAL [[Robinson, Smedley 2020](https://pubmed.ncbi.nlm.nih.gov/32755546/)] to provide users a way to tell whether the highest-ranked hits in a given case are low confidence and not worth evaluating. Unfortunately, based on the analysis in my [previous blog post](https://github.com/bw2/bw2.github.io/blob/master/2022-05-04-phenotype-based-prioritization.md), 
this feature doesn't currently work well, and users are better off ignoring LIRICAL's post-test probability (except to check that it's > 0).
Just looking at the 3 top-ranked hits (or however many you have time for) provides better accuracy than thresholding on the post-test probability.

---

**LIRICAL vs Exomiser comparison in [Robinson 2020]**  

The LIRICAL paper [[Robinson 2020](https://pubmed.ncbi.nlm.nih.gov/32755546/)] compared performance on 116 previously-solved singleton cases from the 100,000 Genomes Project.

**Fig. 4** shows Exomiser slightly out-performing LIRICAL:

<img alt="[Robinson 2020] Figure 4" src="https://user-images.githubusercontent.com/6240170/171466464-0a5a72e0-44d0-47a2-b512-61812f4b6641.png" width=500 />

"Considering the 89 diagnoses where Exomiser was not utilized, Exomiser prioritized 57/89 (64%) in first place compared to 51/89 (57%) for LIRICAL."

---

**LIRICAL vs Exomiser on 75 cases from the Rare Genomes Project**

These distributions show the rank that each tool assigns to the correct gene in 75 RGP cases: 

<img width="800" alt="LIRICAL and Exomiser rank distributions" src="https://user-images.githubusercontent.com/6240170/171470046-0a114cbd-215d-404f-b526-d7f80d085d83.png">

To summarize these plots, both Exomiser and LIRICAL rank the correct gene among the top-5 results for 49 out of 75 (65%) of cases, so top-5 performance is identical. 
Performance varies for other cut-offs:

<table class="ui striped center aligned table">
  <tr><th>Top-k results</th><th>Exomiser: correct genes</th><th>LIRICAL: correct genes</th></tr>
  <tr><td>top 5</td><td>49 out of 75 (65%)</td><td>49 out of 75 (65%)</td></tr>
  <tr><td>top 4</td><td>46 out of 75 (61%)</td><td>45 out of 75 (60%)</td></tr>
  <tr><td>top 3</td><td>37 out of 75 (49%)</td><td>42 out of 75 (56%)</td></tr>
  <tr><td>top 2</td><td>30 out of 75 (40%)</td><td>40 out of 75 (53%)</td></tr>
  <tr><td>top 1</td><td>12 out of 75 (16%)</td><td>29 out of 75 (39%)</td></tr>
</table>

Also, the median and mean ranks of the correct gene differ between the 2 tools:

<table class="ui striped center aligned table">
  <tr><th></th><th>Exomiser</th><th>LIRICAL</th></tr>
  <tr>
    <td>Median rank of correct gene</td>
    <td>4 *</td>
    <td>2 *</td>
  </tr>
  <tr>
    <td>Mean rank of correct gene</td>
    <td>19 *</td>
    <td>33 *</td>
  </tr>
</table>

<i>*</i> For cases where the correct gene wasn't detected by a tool at all , its rank was arbitrarily set = 200 before calculating the median and mean


---

**LIRICAL and Exomiser prioritize different genes**

Interestingly, LIRICAL and Exomiser ranks aren't well correlated (R<sup>2</sup> is 0.05) as this plot shows. Here rank=200 is a special value that 
means the correct gene wasn't included at all in the results from that tool.  

<img width="850" alt="image" src="https://user-images.githubusercontent.com/6240170/171471200-b78706fe-a26a-4eea-880d-5599523d45eb.png">

To summarize this plot:

<table class="ui striped center aligned table">
  <tr><th>Correct Genes in Top-5</th><th>Quadrant</th></tr>
  <tr><td>38 out of 75 (50%)</td><td>bottom-left: Both Exomiser and LIRICAL</td></tr>
  <tr><td>11 out of 75 (15%)</td><td>upper-left: Exomiser but not LIRICAL</td></tr>
  <tr><td>11 out of 75 (15%)</td><td>bottom-right: LIRICAL but not Exomiser</td></tr>
  <tr><td>15 out of 75 (20%)</td><td>upper-right: Neither tool's top-5</td></tr>
</table>


**Conclusion**: 

Let's say users have time to evaluate 10 genes per case. They would get better sensitivity by evaluating 
top-5 from Exomiser and top-5 from LIRICAL instead of the top-10 results from one of the tools. 
In either case, users evaluating 75 cases would be looking at 750 total genes, but with top-5 results from Exomiser & LIRICAL this set 
would include 60 correct genes, while with top-10 results from only one tool it would include only 54 correct genes.
  

---

**What explains the low concordance between LIRICAL and Exomiser?**

It's like due to how they handle phenotype prioritization. Exomiser uses model organism data (mouse & zebra fish) in addition to OMIM gene-disease associations. It also uses protein-protein interactions to check phenotype match scores of adjacent genes. All of these are combined into an Exomiser phenotype match score which is then combined with a variant pathogenicity score to get the final combined "exomiser score". 
LIRICAL computes variant pathogenicity scores the same way as Exomiser (reusing its code and reference data), but does it's own thing for phenotypes - using only OMIM data and computing a post-test probability. 
Spot-checking one of the cases where Exomiser ranked the correct gene as #1 and LIRICAL ranked it as #5: 
2 out of the 4 false-positive LIRICAL genes weren't in the Exomiser results at all, and 2 were quite far down in the list.

Interestingly, the number of HPO terms does not significantly differentiate the tools. Here rank=200 is again a special value that 
means the correct gene wasn't included at all in the results from that tool.  

<img width="850" alt="image" src="https://user-images.githubusercontent.com/6240170/171486870-6b25d874-a250-405b-984b-6bc289c16dfc.png">

