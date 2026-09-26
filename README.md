# Variant Calling Project

Optimisation of somatic Single Nucleotide Variant (SNV) calling across different algorithms using a robust machine learning approach

### Project Objective

Accurately identifying somatic mutations from sequencing data possess significant challenges due to various factors, such as tumor heterogeneity, sequencing artefacts, and low allele frequencies [[1]](https://pubmed.ncbi.nlm.nih.gov/30649191/).

Therefore, the objective of this project is to develop a supervised machine learning model that improves the accuracy of SNV detections, combining the results of four existing variant callers: Mutect2, Freebayes, VarDict, and VarScan [[2]](https://www.biorxiv.org/content/10.1101/861054v1), [[3]](https://arxiv.org/abs/1207.3907), [[4]](https://pubmed.ncbi.nlm.nih.gov/27060149/), [[5]](https://ohiostate.elsevierpure.com/en/publications/varscan-variant-detection-in-massively-parallel-sequencing-of-ind/).

### Methodology

#### Datasets

Real tumour datasets `real1`, `real2` and synthetic tumour datasets `syn1` to `syn5` were given. But for the purpose of this documentation, only the synthetic datasets' results and their evaluation metrics are shown.

The synthetic datasets were obtained from the [ICGC-TCGA DREAM Somatic Mutation Calling Challenge.](https://www.synapse.org/Synapse:syn312572/wiki/62018)

#### Feature extraction from each VCF file

Features extracted by a parser that was written in R, and then used in the Random Forest classifier model.

| Feature | What it explains |
|---|---|
| `Chr` | Chromosome the candidate variant is located on |
| `START_POS_REF` / `END_POS_REF` | Genomic start/end coordinates of the reference allele at that site |
| `REF` | Reference (wild-type) base at that position |
| `ALT` | Alternate (variant) base called at that position |
| `REF_MFVdVs` / `ALT_MFVdVs` | Reference/alternate alleles as reported jointly across all four callers (Mutect2, FreeBayes, VarScan, VarDict), used to reconcile consistent allele calls before merging |
| `Sample_Name` | Name of each tumour dataset |
| `FILTER_*` (one per caller) | Whether that caller's own quality filter marked the call as PASS (1) or filtered out (0) |
| `m2_MQ` | Mutect2's mapping quality (MQ) score for reads supporting the call |
| `m2_TLOD` | Mutect2's Tumor LOD score — log-odds that the site is a genuine somatic variant rather than noise |
| `m2_MQRankSum` | Mutect2's Mapping Quality Rank Sum statistic, comparing read quality between reference- and alt-supporting reads |
| `f_MQM` | FreeBayes' mean mapping quality of reads supporting the alternate allele |
| `f_MQMR` | FreeBayes' mean mapping quality of reads supporting the reference allele |
| `vs_SPV` | VarScan's somatic p-value — statistical confidence the variant is somatic rather than germline or noise |
| `vd_MSI` | VarDict's microsatellite instability score at the site |
| `pred_mut` / `true_mut` | The model's predicted label vs. the ground-truth label for whether the site is a real mutation |

#### Data preprocessing

The true mutation data was concatenated to the dataset, and preprocessing of the data was carried out:

- Non-SNV observations were filtered out
- `REF` and `ALT` columns were one-hot-encoded [[6]](https://www.researchgate.net/publication/353857384_A_Deep-Learned_Embedding_Technique_for_Categorical_Features_Encoding)
- 7 new columns `m2_MQ_null`, `m2_TLOD_null`, `m2_MQRankSum_null`, `f_MQMR_null`, `f_MQM_null`, `vs_SPV_null`,  `vd_MSI_null`, `vs_SSC_null`, and  `vd_SSF_null` were added to describe if the corresponding feature had a `NaN` value for an observation
- All `NaN` values were imputed (assigned) with the mean of the corresponding feature column
- 6 features `Chr`, `START_POS_REF`, `END_POS_REF`, `Sample_Name`, `REF_MFVdVs`, and `ALT_MFVdVs` were dropped. `REF_MFVdVs` and `ALT_MFVdVs` were dropped because they contained similar information to `REF` and `ALT`, and thus would not be useful in prediction

#### Hyperparameter tuning

Our initial model had very high F1 scores across the synthetic and real datasets, but had a low F1 score when used to predict the test dataset, which may be the case of overfitting due to the 100% inclusion of all datasets. To reduce overfitting, we used Grid Search Cross Validation to find the optimal hyperparameters.

We searched for `max_tree_depth` and `max_features` hyperparameters, with 5-fold CV and F1 as scoring metrics.

#### Random Forest Classifier model

We then used Random Forest Classifier model to predict the SNVs. Evaluation metrics are defined as precision, recall, and F1, based on the true positive, false positive, and false negative values.

#### Results

The resulting predictions formatted as `.csv` file, along with the evaluation metrics of only the synthetic datasets used are shown [here](https://variant-calling.streamlit.app/).

---

### Credits
This project is part of a bioinformatics module "Knowledge Discovery Methods in Bioinformatics" at NUS.

#### Team Anything
- Chew Zhen Yuan
- Eliza Soesanto
- Jessica Mary Listijo

### References
[1] W. Huang, Y. A. Guo, K. Muthukumar, P. Baruah, M. M. Chang, A. J. Skanderup, "SMuRF: portable and accurate ensemble prediction of somatic mutations," Bioinformatics, vol. 35, no. 17, pp. 3157-3159, Sep. 2019.

[2] D. Benjamin, T. Sato, K. Cibulskis, G. Getz, C. Stewart, and L. Lichtenstein, "Calling somatic SNVs and indels with Mutect2," BioRxiv, p. 861054, 2019.

[3] E. Garrison, G. Marth, "Haplotype-based variant detection from short-read sequencing," arXiv:1207.3907 [q-bio.GN], Jul. 2012.

[4] Z. Lai et al., "VarDict: a novel and versatile variant caller for next-generation sequencing in cancer research," Nucleic Acids Res., vol. 44, no. 11, pp. e108-e108, 2016.

[5] D. C. Koboldt et al., "VarScan: variant detection in massively parallel sequencing of individual and pooled samples," Bioinformatics, vol. 25, no. 17, pp. 2283-2285, 2009.

[6] M. K. Dahouda and I. Joe, "A deep-learned embedding technique for categorical features encoding," IEEE Access, vol. 9, pp. 114381-114391, 2021.
