import cptac
import cptac.utils as ut
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('agg')
import seaborn as sns
import argparse

cptac.list_datasets()

parser = argparse.ArgumentParser(description='Calculate two gene correlation')  # 创建一个解析对象
parser.add_argument('gene_1', type=str, help='gene_1')  # 向该对象中添加你要关注的命令行参数和选项
parser.add_argument('gene_2', type=str, help='gene_2')
args = parser.parse_args()


en = cptac.Endometrial()
proteomics = pd.DataFrame(en.get_proteomics())
tumorProt = pd.DataFrame(en.join_metadata_to_omics(metadata_df_name="clinical", omics_df_name="proteomics",
                                      metadata_cols='Proteomics_Tumor_Normal'))
tumor_pro_data = tumorProt[tumorProt.Proteomics_Tumor_Normal == 'Tumor']

gene_cor1=tumor_pro_data.A1BG_proteomics
gene_cor2=tumor_pro_data.EGFR_proteomics
pearson_correlation_array= stats.pearsonr(gene_cor1,gene_cor2)

sns.set(style="darkgrid")
plot = sns.regplot(x=gene_cor1, y=gene_cor2)
plot.set(xlabel='A1BG', ylabel='EGFR',
         title='gene correlation for the A1BG&EGFR gene')
matplotlib.pyplot.savefig('gene_correlation')
print(pearson_correlation_array)