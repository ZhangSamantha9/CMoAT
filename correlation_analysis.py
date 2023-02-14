import cptac
import cptac.utils as ut
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('agg')
import seaborn as sns
def user_cancername(cancername):
    print("receive parameters:",cancername)
    if cancername == 'Endometrial' or cancername=='endometrial':
        # print("go end")
        # en = cptac.Endometrial()
        # proteomics = pd.DataFrame(en.get_proteomics())
        # tumorProt = pd.DataFrame(en.join_metadata_to_omics(metadata_df_name="clinical", omics_df_name="proteomics",
        #                                                    metadata_cols='Proteomics_Tumor_Normal'))
        # tumor_pro_data = tumorProt[tumorProt.Proteomics_Tumor_Normal == 'Tumor']
        print("go end")
        proteomics, tumorProt, tumor_pro_data = gene_date(cptac.Endometrial())
        print(proteomics)
        print(tumorProt)

    elif cancername == 'luad' or cancername=='Luad':
        # Luad = cptac.Luad()
        # proteomics = pd.DataFrame(Luad.get_proteomics())
        # tumorProt = pd.DataFrame(Luad.join_metadata_to_omics(metadata_df_name="clinical", omics_df_name="proteomics",
        #                                                    metadata_cols='Proteomics_Tumor_Normal'))
        # tumor_pro_data = tumorProt[tumorProt.Proteomics_Tumor_Normal == 'Tumor']
        print("go luad")
        proteomics, tumorProt, tumor_pro_data = gene_date(cptac.Luad())
        print(proteomics)
        print(tumorProt)

def gene_date(cancer):
    proteomics = pd.DataFrame(cancer.get_proteomics())
    tumorProt = pd.DataFrame(cancer.join_metadata_to_omics(metadata_df_name="clinical", omics_df_name="proteomics",
                                                         metadata_cols='Sample_Tumor_Normal'))
    tumor_pro_data = tumorProt[tumorProt.Proteomics_Tumor_Normal == 'Tumor']

    return proteomics, tumorProt, tumor_pro_data

# def user_gene1(gene1):
#     print("receive parameters",gene1)
#     gene1 == globals('tumor_pro_data')['gene1']

# gene_cor1=tumor_pro_data.A1BG_proteomics
# gene_cor2=tumor_pro_data.EGFR_proteomics
# pearson_correlation_array= stats.pearsonr(gene_cor1,gene_cor2)
#
# sns.set(style="darkgrid")
# plot = sns.regplot(x=gene_cor1, y=gene_cor2)
# plot.set(xlabel='A1BG', ylabel='EGFR',
#          title='gene correlation for the A1BG&EGFR gene')
# matplotlib.pyplot.savefig('gene_correlation')
# print(pearson_correlation_array)
