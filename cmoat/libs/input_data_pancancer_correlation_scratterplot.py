import pandas as pd
from scipy import stats

import seaborn as sns
import os

# 从Excel文件中读取数据
excel_file1 = 'D:\\doc\\progress\\request_analysis\\result\\20240105Muc1\\ERBB3_pancan.csv'
excel_file2='D:\\doc\\progress\\request_analysis\\result\\20240105Muc1\\MUC1_pancan.csv'# 替换为你的Excel文件路径
cancer_df1 = pd.read_csv(excel_file1)
cancer_df2=pd.read_csv(excel_file2)
merged_df = pd.merge(cancer_df1, cancer_df2, on='id', how='outer')

# 打印DataFrame
merged_df.set_index("id", inplace=True)
print(merged_df)
merged_df.to_excel('merged_df.xlsx')

gene1_name='ERBB3'
gene2_name='MUC1'
cancer_name='pancancer'

# 将 'NA' 替换为 NaN
cancer_df = merged_df.replace('NA', float('NaN'))
genes_series = cancer_df.dropna()
genes_series = genes_series.loc[:, ~genes_series.columns.duplicated()]
print(genes_series)
# Delete 'Dataset_x' and 'Group_y' columns
genes_series = genes_series.drop(['Dataset_x', 'Group_y'], axis=1)
# Filter rows where 'Group_x' is 'Tumor'
genes_series = genes_series[genes_series['Group_x'] == 'Tumor']
genes_series['Dataset_y']=genes_series['Dataset_y'].str.replace('_.*','',regex=True)
genes_series['Dataset_y']=genes_series['Dataset_y'].str.replace('PDAC','PDA')
genes_series=genes_series.rename(columns={'Dataset_y':'cancer'})
# genes_series = genes_series[genes_series['cancer'] == cancer_name]
genes_series.to_excel('genes_series.xlsx')
gene1_modified = genes_series[gene1_name]
gene2_modified = genes_series[gene2_name]
print(gene1_modified, gene2_modified, type(gene1_modified))
 # 计算填充后的DataFrame中基因"A"和基因"B"之间的相关性
p_value = '{:.4e}'.format(stats.spearmanr(gene1_modified, gene2_modified).pvalue)
R = '{:.6f}'.format(stats.spearmanr(gene1_modified, gene2_modified).statistic)
print("GeneA和GeneB的相关性：", R)
print("p-value：", p_value)

sns.set(style="darkgrid")
plot = sns.scatterplot(x=gene1_modified, y=gene2_modified,hue='cancer',data=genes_series,edgecolor='none')
plot.set(xlabel=gene1_name, ylabel=gene2_name,
         title=f'{cancer_name} protein expression correlation for {gene1_name} and {gene2_name}\nR = {R} p-value = {p_value}')
# Set axis limits
plot.set_xlim(-4, 4)
plot.set_ylim(-10, 5)
plot.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

figPath = os.path.join(os.getcwd(), f'{cancer_name}_{gene1_name} and {gene2_name} correlation.png')
plot.get_figure().savefig(figPath,bbox_inches='tight', pad_inches=0.1)

if (os.path.exists(figPath)):
    figPath = figPath
else:
    raise (f'Could not save figer at {figPath}')