import cptac
import cptac.utils as ut
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('agg')
import seaborn as sns

CANCER_DATA_DIC = {'Luad':cptac.Luad(), 'Endometrial': cptac.Endometrial()}


def user_cancer_name(cancer_name):
    print("receive parameters: ", cancer_name)

    if CANCER_DATA_DIC.__contains__(cancer_name):
        return clean_dataframe(CANCER_DATA_DIC[cancer_name])
    else:
        print(cancer_name, 'is not in the dictionary')

    # if cancer_name == 'Endometrial' or cancer_name== 'endometrial':
    #     print("analysis endometrial")
    #     tumor_pro_data = clean_dataframe(CANCER_DATA_DIC['Endometrial'])
    #     return tumor_pro_data
    # elif cancer_name == 'luad' or cancer_name== 'Luad':
    #     print("analysis luad")
    #     tumor_pro_data = clean_dataframe(CANCER_DATA_DIC['Luad'])
    #     return tumor_pro_data


def clean_dataframe(cancer):
    #proteomics = cancer.get_proteomics()
    # proteomics.to_csv('test.csv')
    tumorProt = cancer.join_metadata_to_omics(metadata_df_name="clinical", omics_df_name="proteomics",
                                                         metadata_cols='Sample_Tumor_Normal')
    reduced_tumor_prot = pd.DataFrame(ut.reduce_multiindex(df=tumorProt, levels_to_drop="Database_ID"))
    tumor_pro_data = reduced_tumor_prot [reduced_tumor_prot.Sample_Tumor_Normal == 'Tumor']
    # tumor_pro_data.to_csv('test.csv')
    return tumor_pro_data

def gene_correlation(gene1,gene2,tumor_pro_data):
    print("receive parameters:", gene1, gene2)

    tumor_colums = tumor_pro_data.columns

    tail = '_proteomics'

    a=f'is {gene1} in list: {gene1 in tumor_colums}'
    b=f'is {gene2} in list: {gene2 in tumor_colums}'
    c=f'is {gene2} in list: {(gene2+tail) in tumor_colums}'


    if gene1 in tumor_pro_data.columns:
        return gene1
    else:
        print("No data for gene 1 is found")
    if gene2 in tumor_pro_data.columns:
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



