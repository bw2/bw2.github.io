## List of public-facing projects

### Tandem Repeats

- **[trexplorer.broadinstitute.org](https://trexplorer.broadinstitute.org)**: An online portal for exploring and visualizing tandem repeats (TRs) genome-wide. It enables searching, sorting, and exporting TRs based on a wide range of annotations including population allele frequencies from short-read and long-read datasets, genic and chromosomal regions, published TR functions (expression, splicing, ...), association study results, and many others. [[code](https://github.com/broadinstitute/TRExplorer)] [[publication](https://pubmed.ncbi.nlm.nih.gov/42025159/)]
- **[trexplorer-catalog](https://github.com/broadinstitute/trexplorer-catalog/blob/main/README.md)**: TR catalog and variation clusters for genome-wide analyses and population databases. [[code](https://github.com/broadinstitute/trexplorer-catalog)] [[publication](https://pubmed.ncbi.nlm.nih.gov/42025159/)]
- **[ExpansionHunter (bw2 fork)](https://github.com/bw2/ExpansionHunter/blob/master/README.md)**: A fork of [Illumina/ExpansionHunter](https://github.com/Illumina/ExpansionHunter) that adds substantial new features and optimizations including optimized-streaming mode, motif composition analysis, allele quality scores, and others. [[code](https://github.com/bw2/ExpansionHunter)]
- **[str-truth-set](https://github.com/broadinstitute/str-truth-set/blob/main/README.md)**: Genome-wide TR truth set based on the Synthetic Diploid Benchmark (Li et al. 2018). [[code](https://github.com/broadinstitute/str-truth-set)] [[publication](https://pubmed.ncbi.nlm.nih.gov/37214979/)]
- **[str-truth-set-v2](https://github.com/broadinstitute/str-truth-set-v2/blob/main/README.md)**: v2.0 of the TR truth set (now based on 321 haplotype-resolved assemblies), along with a [tool benchmark viewer](https://broadinstitute.github.io/str-truth-set-v2/tool_comparison_viewer.html). [[code](https://github.com/broadinstitute/str-truth-set-v2)]
- **[TRails](https://github.com/broadinstitute/TRails/blob/main/README.md)**: A local, interactive app for prioritizing tandem repeat outlier expansions in rare disease callsets. [[code](https://github.com/broadinstitute/TRails)]
- **[colab-repeat-finder](https://github.com/broadinstitute/colab-repeat-finder/blob/main/README.md)**: A tool for finding perfect repeats in the reference genome that span more than M base pairs and/or N repeats. [[code](https://github.com/broadinstitute/colab-repeat-finder)]
- **[StrPileups](https://broadinstitute.github.io/StrPileups/)**: ExpansionHunter genotypes, REViewer read visualizations, and PCR truth data for 133 individuals at 14 known pathogenic STR loci. [[code](https://github.com/broadinstitute/StrPileups)] [[publication](https://pubmed.ncbi.nlm.nih.gov/35948990/)]
- **[str-analysis](https://github.com/broadinstitute/str-analysis/blob/main/README.md)**: Scripts and utilities for analyzing tandem repeats. [[code](https://github.com/broadinstitute/str-analysis)]

### Rare Disease

- **[sma-finder](https://github.com/broadinstitute/sma-finder/blob/main/README.md)**: A tool for diagnosing spinal muscular atrophy (SMA) in exome, genome, or targeted sequencing data. [[code](https://github.com/broadinstitute/sma-finder)] [[publication](https://pubmed.ncbi.nlm.nih.gov/39670433/)]
- **[seqr.broadinstitute.org](https://seqr.broadinstitute.org)**: Web-based interactive analysis and variant prioritization tool for rare disease genomic datasets including genomes, exomes, and RNA-seq. [[code](https://github.com/broadinstitute/seqr)] [[publication](https://pubmed.ncbi.nlm.nih.gov/35266241/)]
- **[spliceailookup.broadinstitute.org](https://spliceailookup.broadinstitute.org)**: Website for running SpliceAI, Pangolin, and SAI-10k prediction models on variants of interest, visualizing results, while also checking other variant effect predictor scores. [[code](https://github.com/broadinstitute/SpliceAI-lookup)]
- **[genelookup.broadinstitute.org](https://genelookup.broadinstitute.org)**: Website that aggregates information about gene-disease relationships from OMIM, ClinGen, PanelApp UK, and over 10 other sources, provides an AI summary of the phenotype, and makes the information easier to search, compare, and export. [[code](https://github.com/broadinstitute/gene-lookup)]
- **[tgg-viewer.broadinstitute.org](https://tgg-viewer.broadinstitute.org)**: Web app for visualizing splice junctions, copy number variation, and other sequencing data using IGV.js. [[code](https://github.com/broadinstitute/tgg-viewer)]
- **[phenotype-driven-analysis](https://github.com/broadinstitute/phenotype-driven-analysis/blob/main/README.md)**: Pipeline for phenotype-driven analysis of rare disease cases using the LIRICAL tool. [[code](https://github.com/broadinstitute/phenotype-driven-analysis)]

### Genomics

- **[gnomad.broadinstitute.org](https://gnomad.broadinstitute.org)**: Genome Aggregation Database browser. Includes [gnomad-readviz](https://github.com/broadinstitute/gnomad-readviz): scripts that precompute the mini-BAMs and other files behind gnomAD's read visualization feature. [[code](https://github.com/broadinstitute/gnomad-browser)] [[publication](https://pubmed.ncbi.nlm.nih.gov/32461654/)]
- **[liftover.broadinstitute.org](https://liftover.broadinstitute.org)**: A user-friendly genomic liftover interface for variants, positions, or intervals. [[code](https://github.com/broadinstitute/liftover)]

### General Software

- **[ConfigArgParse](https://github.com/bw2/ConfigArgParse/blob/master/README.md)**: Drop-in replacement for Python's argparse that adds support for config files and environment variables. [[code](https://github.com/bw2/ConfigArgParse)]
- **[flipbook](https://github.com/broadinstitute/flipbook/blob/main/README.md)**: Quickly flip through images in a local directory and record notes or answer questions about each one. [[code](https://github.com/broadinstitute/flipbook)] [[publication](https://pubmed.ncbi.nlm.nih.gov/35948990/)]
- **[step-pipeline](https://github.com/bw2/step-pipeline/blob/main/README.md)**: A thin wrapper around Hail Batch that adds features like skipping steps whose output files already exist, more options for localizing files, and notifications when a pipeline finishes. [[code](https://github.com/bw2/step-pipeline)]

### AI Coding Agents

- **[agent-command-tab](https://github.com/bw2/agent-command-tab/blob/main/README.md)**: A macOS menu bar app that lists the iTerm2 and tmux tabs where AI coding agents (Claude Code, Codex CLI, and others) are running, and shows what each one is doing. [[code](https://github.com/bw2/agent-command-tab)]
- **[claude-code-review-skill](https://github.com/bw2/claude-code-review-skill/blob/main/README.md)**: Claude Code skill that runs code review with Opus and Sonnet (plus, optionally, Google Antigravity), with blind peer validation and confidence-scored findings. [[code](https://github.com/bw2/claude-code-review-skill)]
- **[claude-code-session-recall](https://github.com/bw2/claude-code-session-recall/blob/main/README.md)**: Claude Code skill that searches and summarizes recent Claude Code sessions for the current directory. [[code](https://github.com/bw2/claude-code-session-recall)]
- **[claude-error-patterns](https://github.com/bw2/claude-error-patterns/blob/main/README.md)**: Claude Code plugin that analyzes session logs for recurring error patterns and wheel-spinning loops. [[code](https://github.com/bw2/claude-error-patterns)]
