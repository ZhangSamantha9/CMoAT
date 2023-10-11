import pandas as pd
from scipy import stats
import numpy as np


# 从Excel文件中读取数据
excel_file = 'C:\\Users\\126614\\Documents\\project\\TE\\progress\\meetings\\colon\\cptac_colon_normal_tumor_trans.xlsx'  # 替换为你的Excel文件路径
tumorProt = pd.read_excel(excel_file,index_col=0)
# 打印DataFrame
print(tumorProt)


#Retrieve boolean array of true values
tumor_bool = tumorProt['Sample_Tumor_Normal'] == "Tumor"
normal_bool = tumorProt['Sample_Tumor_Normal'] != "Tumor"
print(tumor_bool)
#Use boolean array to select for appropriate patients
tumor = tumorProt[tumor_bool]
normal = tumorProt[normal_bool]
print(tumor)
#Create array variables to hold the significant genes for each partition
tumor_genes = []
normal_genes = []
#Grab the genes of interest, ignoring the MSI column in the dataframe
genes = tumor.columns[1:]
print(genes)
#Correct alpha level for multiple testing by dividing the standard .05 by the number of genes to be analyzed
threshold = .05 / len(genes)
#Perform Welch's t-test(different variances) on each gene between the two groups
for gene in genes:
    tumor_gene_abundance = tumor[gene]
    normal_gene_abundance = normal[gene]
    pvalue = stats.ttest_ind(tumor_gene_abundance, normal_gene_abundance, equal_var=False,nan_policy='omit').pvalue
    tumor_gene_abundance_median=np.nanmedian(tumor_gene_abundance)
    normal_gene_abundance_median=np.nanmedian(normal_gene_abundance)
    print(tumor_gene_abundance_median, normal_gene_abundance_median)
    middle_dif= tumor_gene_abundance_median-normal_gene_abundance_median
    log2_middle_dif=np.log2(middle_dif)

    #If the P-value is significant, determine which partition is more highly expressed
    if pvalue < threshold:
         if tumor_gene_abundance.mean() > normal_gene_abundance.mean():
             # tumor_genes.append(gene[0].split("_")[0])
             row=(gene,pvalue,log2_middle_dif)
             tumor_genes.append(row)
         elif normal_gene_abundance.mean() > tumor_gene_abundance.mean():
             normal_genes.append(gene)
# #Optional check of number of genes in each partition
print("Proteomics Tumor Genes:", len(tumor_genes))
print("Proteomics Normal Genes:", len(normal_genes))

# 将 rcc_expression 转换为 DataFrame
df = pd.DataFrame(tumor_genes, columns=["Gene", "P-value","Fold_change"])

# 指定要保存的 Excel 文件名
excel_filename = "colon_expression_results.xlsx"

# 将 DataFrame 写入 Excel 文件
df.to_excel(excel_filename, index=False)

print(f"数据已保存到 {excel_filename}")

