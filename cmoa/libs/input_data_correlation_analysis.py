import pandas as pd

# 从Excel文件中读取数据
excel_file = 'D:\\doc\\data\\TCGA\\PRAD\\TCGA_PRAD_RSEM_log2.xlsx'  # 替换为你的Excel文件路径
df = pd.read_excel(excel_file,index_col=0)

df=df.T
# 打印DataFrame
print(df)

# 将 'NA' 替换为 NaN
df = df.replace('NA', float('NaN'))
#
# # 将"AAR2"列与其他列计算相关性
correlation = df.corr(method='spearman')['SLC39A6']
correlation.to_excel('PRAD_SLC39A6_correlation.xlsx', index=True)  # 设置index为True以包括行索引
#
# print(f"相关性矩阵已保存到 Pda_correlation.xlsx")

