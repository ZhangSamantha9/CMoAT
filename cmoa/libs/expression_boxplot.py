import matplotlib
import pandas as pd
import numpy as np
import scipy.stats
import statsmodels.stats.multitest
import matplotlib.pyplot as plt
import seaborn as sns
import math
import cptac
import cptac.utils as ut


lu = cptac.Luad()

#Join attribute with acetylation dataframe
clinical_and_proteomics = lu.join_metadata_to_omics(metadata_df_name="clinical", omics_df_name="proteomics",
                                                     metadata_cols='Sample_Tumor_Normal')

# Use the cptac.utils.reduce_multiindex function to combine the
# multiple column levels, so it's easier to graph our data
clinical_and_proteomics = pd.DataFrame(ut.reduce_multiindex(df=clinical_and_proteomics, levels_to_drop="Database_ID", quiet=True))
clinical_attribute = "Sample_Tumor_Normal"
#Show possible variations of Histologic_type
clinical_and_proteomics[clinical_attribute].unique()
#Make dataframes with only endometrioid and only serous data in order to compare
tumor = clinical_and_proteomics.loc[clinical_and_proteomics[clinical_attribute] == "Tumor"]
normal = clinical_and_proteomics.loc[clinical_and_proteomics[clinical_attribute] == "Normal"]
#Here is where we set the NaN values to "Non_Tumor"
# clinical_and_proteomics[[clinical_attribute]] = clinical_and_proteomics[[clinical_attribute]].fillna(value="Non_Tumor")

df=pd.read_excel("C:\\Users\\126614\\PycharmProjects\\GEPIA_batch_processing\\CI部提报靶点的GEPIA生信分析_单次跨膜蛋白_protein\\single_transmembrane_protein_list_protein.xlsx")
genes=df['gene_name']
plt.clf()
for graphing_gene in genes:
    graphing_gene += '_proteomics'
    print(graphing_gene,'_',scipy.stats.ttest_ind(tumor[graphing_gene], normal[graphing_gene]).pvalue)
    sns.boxplot(x=clinical_attribute, y=graphing_gene, data=clinical_and_proteomics, showfliers=False,
                order=["Tumor", "Normal"])
    sns.stripplot(x=clinical_attribute, y=graphing_gene, data=clinical_and_proteomics, color='.3',
                  order=["Tumor", "Normal"])
    matplotlib.pyplot.savefig(graphing_gene)
    plt.clf()