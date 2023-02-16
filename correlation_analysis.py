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
    proteomics = cancer.get_proteomics()
    proteomics = pd.DataFrame(ut.reduce_multiindex(df=proteomics, levels_to_drop="Database_ID"))
    # proteomics.to_csv('test.csv')
    tumorProt = pd.DataFrame(cancer.join_metadata_to_omics(metadata_df_name="clinical", omics_df_name="proteomics",
                                                         metadata_cols='Sample_Tumor_Normal'))
    tumor_pro_data = tumorProt[tumorProt.Sample_Tumor_Normal == 'Tumor']
    # tumor_pro_data.to_csv('test.csv')
    return tumor_pro_data

tumor_pro_data=user_cancername()

def gene_correlation(gene1,gene2):
    print("receive parameters:", gene1, gene2)
    if gene1 in tumor_pro_data.column:
        return gene1
    else:
        print("No data for gene 1 is found")
    if gene2 in tumor_pro_data.column:
        return gene2
    else:
        print("No data for gene 2 is found")
    pearson_correlation_array = stats.pearsonr(gene1, gene2)
    sns.set(style="darkgrid")
    plot = sns.regplot(x=gene1, y=gene2)
    plot.set(xlabel=gene1.column, ylabel=gene2.column,
         title='gene correlation')
    matplotlib.pyplot.savefig('gene_correlation')
    print(pearson_correlation_array)



