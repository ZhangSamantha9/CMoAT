import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import cptac
import csv

# cptac.download(dataset="colon")
# colon=cptac.colon
# proteomics =colon.get_proteomics()
cptac.download(dataset="colon")
co = cptac.Colon()

co_expression=[]



#Join attribute with acetylation dataframe
tumorProt = co.join_metadata_to_omics(metadata_df_name="clinical", omics_df_name="proteomics",
                                      metadata_cols='Sample_Tumor_Normal')
#Retrieve boolean array of true values
tumor_bool = tumorProt['Sample_Tumor_Normal'] == "Tumor"
normal_bool = tumorProt['Sample_Tumor_Normal'] != "Tumor"
#Use boolean array to select for appropriate patients
tumor = tumorProt[tumor_bool]
normal = tumorProt[normal_bool]
#Create array variables to hold the significant genes for each partition
tumor_genes = []
normal_genes = []
#Grab the genes of interest, ignoring the MSI column in the dataframe
genes = tumor.columns[1:]
#Correct alpha level for multiple testing by dividing the standard .05 by the number of genes to be analyzed
threshold = .05 / len(genes)
#Perform Welch's t-test(different variances) on each gene between the two groups
for gene in genes:
    tumor_gene_abundance = tumor[gene]
    normal_gene_abundance = normal[gene]
    pvalue = stats.ttest_ind(tumor_gene_abundance, normal_gene_abundance, equal_var=False,nan_policy='omit').pvalue

    #If the P-value is significant, determine which partition is more highly expressed
    if pvalue < threshold:
         if tumor_gene_abundance.mean() > normal_gene_abundance.mean():
             tumor_genes.append(gene[0].split("_")[0])
             row=(gene[0].split("_")[0],pvalue)
             co_expression.append(row)
         elif normal_gene_abundance.mean() > tumor_gene_abundance.mean():
             normal_genes.append(gene[0].split("_")[0])
# #Optional check of number of genes in each partition
print("Proteomics Tumor Genes:", len(tumor_genes))
print("Proteomics Normal Genes:", len(normal_genes))
print(co_expression)
import pandas as pd

# 将 rcc_expression 转换为 DataFrame
df = pd.DataFrame(co_expression, columns=["Gene", "P-value"])

# 指定要保存的 Excel 文件名
excel_filename = "colon_expression_results.xlsx"

# 将 DataFrame 写入 Excel 文件
df.to_excel(excel_filename, index=False)

print(f"数据已保存到 {excel_filename}")
