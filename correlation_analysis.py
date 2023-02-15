import cptac
import cptac.utils as ut
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('agg')
import seaborn as sns

cancer_data = {'Luad':cptac.Luad(), 'Endometrial': cptac.Endometrial()}


def user_cancername(cancername):
    print("receive parameters:",cancername)
    if cancername == 'Endometrial' or cancername=='endometrial':
        print("analysis endometrial")
        tumor_pro_data = gene_date(cancer_data['Endometrial'])
    elif cancername == 'luad' or cancername=='Luad':
        print("analysis luad")
        tumor_pro_data = gene_date(cancer_data['Luad'])


def gene_date(cancer):
    proteomics = pd.DataFrame(cancer.get_proteomics())
    tumorProt = pd.DataFrame(cancer.join_metadata_to_omics(metadata_df_name="clinical", omics_df_name="proteomics",
                                                         metadata_cols='Sample_Tumor_Normal'))
    tumor_pro_data = tumorProt[tumorProt.Sample_Tumor_Normal == 'Tumor']
    tumor_pro_data.to_csv('test.csv')
    return tumor_pro_data

# def correlation_curve(gene1,gene2):
#     tumor_pro_data=user_cancername("Endometrial")

# def user_genes(gene1,gene2):
#     print("receive parameters",gene1,gene2)
#     for gene1_proteomics in gene_date():
#         if gene1_proteomics in gene_date().column:
#             gene1 = gene1_proteomics
#     for gene2_proteomics in gene_date():
#         if gene2_proteomics in gene_date().column:
#             gene1 = gene2_proteomics
#     pearson_correlation_array = stats.pearsonr(gene1, gene2)
#     sns.set(style="darkgrid")
#     plot = sns.regplot(x=gene1, y=gene2)
#     plot.set(xlabel='A1BG', ylabel='EGFR',
#          title='gene correlation')
#     matplotlib.pyplot.savefig('gene_correlation')
#     print(pearson_correlation_array)



