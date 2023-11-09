import pandas as pd
from scipy import stats

import seaborn as sns
import os

# 从Excel文件中读取数据
excel_file = 'D:\\doc\\data\\Ov\\OV_tumor.xlsx'  # 替换为你的Excel文件路径
cancer_df = pd.read_excel(excel_file)
# 打印DataFrame
cancer_df.set_index("patiens", inplace=True)
cancer_df=cancer_df.T
print(cancer_df)


# 将 'NA' 替换为 NaN
cancer_df = cancer_df.replace('NA', float('NaN'))
gene1_name = 'MUC1'
gene2_name = 'EGFR'
cancer_name='Ov'

if gene1_name not in cancer_df.columns:
    raise (f'Gene [{gene1_name}] not in dataframe')
if gene2_name not in cancer_df.columns:
    raise (f'Gene [{gene2_name}] not in dataframe')



genes_series = cancer_df[[gene1_name,gene2_name]]
print(genes_series)
genes_series = genes_series.dropna()
genes_series = genes_series.loc[:, ~genes_series.columns.duplicated()]
print(genes_series)
gene1_modified = genes_series[gene1_name]
gene2_modified = genes_series[gene2_name]
print("填充后的DataFrame:")
print(gene1_modified, gene2_modified, type(gene1_modified))
 # 计算填充后的DataFrame中基因"A"和基因"B"之间的相关性
p_value = '{:.4e}'.format(stats.pearsonr(gene1_modified, gene2_modified).pvalue)
R = '{:.6f}'.format(stats.pearsonr(gene1_modified, gene2_modified).statistic)
print("GeneA和GeneB的相关性：", R)
print("p-value：", p_value)

sns.set(style="darkgrid")
plot = sns.regplot(x=gene1_modified, y=gene2_modified)
plot.set(xlabel=gene1_name, ylabel=gene2_name,
         title=f'{cancer_name} protein expression correlation for {gene1_name} and {gene2_name}\nR = {R} p-value = {p_value}')

figPath = os.path.join(os.getcwd(), f'{cancer_name}_{gene1_name} and {gene2_name} correlation.png')
plot.get_figure().savefig(figPath)

if (os.path.exists(figPath)):
    figPath = figPath
else:
    raise (f'Could not save figer at {figPath}')