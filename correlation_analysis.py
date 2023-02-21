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


def get_cancer_data(cancer_name):
    print("receive parameters: ", cancer_name)

    if CANCER_DATA_DIC.__contains__(cancer_name):
        return cancer_data_preprocess(CANCER_DATA_DIC[cancer_name])
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


def cancer_data_preprocess(cancer):
    #proteomics = cancer.get_proteomics()
    # proteomics.to_csv('test.csv')
    cancer_row_data = cancer.join_metadata_to_omics(metadata_df_name="clinical", omics_df_name="proteomics",
                                                         metadata_cols='Sample_Tumor_Normal')
    reduced_cancer_data = pd.DataFrame(ut.reduce_multiindex(df=cancer_row_data, levels_to_drop="Database_ID",quiet=True))
    cancer_data = reduced_cancer_data [reduced_cancer_data.Sample_Tumor_Normal == 'Tumor']
    # tumor_pro_data.to_csv('test.csv')
    return cancer_data

def gene_correlation_curve(gene1, gene2, cancer_data_analysis):
    print("receive parameters:", gene1, gene2)

    tumor_colums = cancer_data_analysis.columns

    tail = '_proteomics'
    gene1_proteomics_name = gene1 + tail
    gene2_proteomics_name = gene2 + tail


    # a=f'is {gene1} in list: {gene1 in tumor_colums}'
    # b=f'is {gene2} in list: {gene2 in tumor_colums}'
    # c=f'is {gene2} in list: {(gene2+tail) in tumor_colums}'


    if gene1_proteomics_name in cancer_data_analysis.columns:
        print('gene 1 successfully matched')
    else:
        print("No data for gene 1 is found")

    if gene2_proteomics_name in cancer_data_analysis.columns:
        print('gene 2 successfully matched')
    else:
        print("No data for gene 2 is found")

    gene1_data = cancer_data_analysis[gene1_proteomics_name]
    print('data for gene 1 done')
    gene2_data = cancer_data_analysis[gene2_proteomics_name]
    print('data for gene 2 done')


    R = str(round(stats.pearsonr(gene1_data, gene2_data).statistic,6))
    p_value=str(stats.pearsonr(gene1_data, gene2_data).pvalue)
    sns.set(style="darkgrid")
    plot = sns.regplot(x=gene1_data, y=gene2_data)
    plot.set(xlabel=gene1, ylabel=gene2,
         title='Gene correlation for '+ gene1 +' and '+ gene2+"\n"+'R = '+R+'  p-value = '+p_value)
    # plt.text(1,1,pearson_correlation_array)
    matplotlib.pyplot.savefig('gene_correlation')
    print(R,p_value)



