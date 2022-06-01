
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


