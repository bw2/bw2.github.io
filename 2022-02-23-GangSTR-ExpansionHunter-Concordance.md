ExpansionHunter [[Dolzhenko 2019](https://academic.oup.com/bioinformatics/article/35/22/4754/5499079)] and GangSTR [[Mousavi 2019](https://pubmed.ncbi.nlm.nih.gov/31194863/)] 
are widely used tools for genotyping short tandem repeats (STRs) in whole genome sequencing (WGS) data. They can genotype both small and large STR expansions 
(shorter or longer than the standard 150bp Illumina read length) and rely on very similar types of evidence in the WGS data do so:

* Spanning reads (called "Encolsing" reads in the GangSTR paper)
* Fragment length (called "Spanning" reads in the GangSTR paper. Only GangSTR uses this type of evidence.)
* Flanking reads 
* Fully repetitive reads (called In-repeat Reads (IRRs) in the ExpansionHunter paper)

These evidence classes are illustrated in the ExpansionHunter and GangSTR papers as follows:

----
**Fig. 1** from ExpansionHunter [[Dolzhenko 2017](https://pubmed.ncbi.nlm.nih.gov/28887402/)]:  

![1895f01](https://user-images.githubusercontent.com/6240170/155419124-8881e97c-b2dc-4144-8a06-22c45c26f697.jpg)

  
----
**Fig. 1** from GangSTR [[Mousavi 2019](https://pubmed.ncbi.nlm.nih.gov/31194863/)]:  

![gkz501fig1](https://user-images.githubusercontent.com/6240170/155419204-b661a670-f2e8-4535-bbe2-f0d03f577363.jpg)

----

