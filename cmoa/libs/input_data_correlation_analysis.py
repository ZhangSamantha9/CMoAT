import pandas as pd

# 从Excel文件中读取数据
excel_file = 'C:\\Users\\126614\\Documents\\project\\TE\\progress\\meetings\\Lung\\rawdata\\CPTAC-LSCC__proteome_TUMOR.cct.xlsx'  # 替换为你的Excel文件路径
df = pd.read_excel(excel_file)
# 打印DataFrame
print(df)


# 将 'NA' 替换为 NaN
df = df.replace('NA', float('NaN'))

# 将"AAR2"列与其他列计算相关性
correlation = df.corr(method='spearman')['CEACAM6']
correlation.to_excel('LSCC_correlation.xlsx', index=True)  # 设置index为True以包括行索引

print(f"相关性矩阵已保存到 LSCC_correlation.xlsx")

