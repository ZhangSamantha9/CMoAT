import pandas as pd
import scipy.stats

import seaborn as sns
import os

# 从Excel文件中读取数据
excel_file = 'D:\\doc\\progress\\request_analysis\\result\\20240105Muc1\\EGFR_pancan.csv'

cancer_df = pd.read_csv(excel_file)

cancer_df.set_index("id", inplace=True)
gene_name='EGFR'
cancer_name='GBM'

genes_series = cancer_df
genes_series['Dataset']=genes_series['Dataset'].str.replace('_.*','',regex=True)

genes_series = genes_series.loc[genes_series['Dataset'] == cancer_name]
tumor = genes_series.loc[genes_series['Group'] == "Tumor"]
normal = genes_series.loc[genes_series['Group'] == "Normal"]

p_value = scipy.stats.ttest_ind(tumor[gene_name],normal[gene_name]).pvalue
tumor_normal_label = "Group"
genes_series[tumor_normal_label].unique()
boxplot=sns.boxplot(x=tumor_normal_label, y=genes_series[gene_name], data=genes_series, showfliers=False,
                    order=["Tumor", "Normal"])
boxplot = sns.stripplot(x=tumor_normal_label, y=genes_series[gene_name], data=genes_series, color='.3',
                      order=["Tumor", "Normal"])
boxplot.set(title=f'{cancer_name} protein expression boxplot for {gene_name} \np-value = {p_value}')
figPath = os.path.join(os.getcwd(),f'{cancer_name}_{gene_name}_expression_boxplot.png')
print('figure done')
boxplot.get_figure().savefig(figPath)
if (os.path.exists(figPath)):
    figPath = figPath
else:
    raise (f'Could not save figer at {figPath}')