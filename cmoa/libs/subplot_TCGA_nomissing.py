import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
from io import StringIO
import os


gene_name='VEGFA'
cancer_name='pancaner'
# plt.style.use('_mpl-gallery')
url_normals = 'http://firebrowse.org/api/v1/Analyses/mRNASeq/Quartiles?format=csv&gene=VEGFA&protocol=RSEM&sample_type=normals'
normals_response = requests.get(url_normals)
normals_df = pd.read_csv(StringIO(normals_response.text),index_col=0)
# normals_df.drop('outliers', axis=1)
url_tumors = 'http://firebrowse.org/api/v1/Analyses/mRNASeq/Quartiles?format=csv&gene=VEGFA&protocol=RSEM&sample_type=tumors'
tumors_response = requests.get(url_tumors)
tumors_df = pd.read_csv(StringIO(tumors_response.text))
merged_df = pd.merge(normals_df, tumors_df, on='cohort', how='outer')
merged_df.to_excel('a.xlsx')
merged_df= merged_df.dropna()

# Define plot data using column names
tumors_plot_data = [
    [row['low_bound_y'], row['q1_y'], row['median_y'], row['q3_y'], row['high_bound_y']] for _, row in merged_df.iterrows()
]

normals_plot_data = [
    [row['low_bound_x'], row['q1_x'], row['median_x'], row['q3_x'], row['high_bound_x']] for _, row in merged_df.iterrows()
]


tumors_outliers = [row['outliers_y'] for _, row in merged_df.iterrows()]
normals_outliers = [row['outliers_x'] for _, row in merged_df.iterrows()]
tumors_labels = [row['cohort'] for _, row in merged_df.iterrows()]
normals_labels = [row['cohort'] for _, row in merged_df.iterrows()]

tumors_labels = merged_df['cohort'].tolist()

# 定义盒图的位置
tumors_positions = np.arange(1, len(tumors_plot_data) * 2, step=2)
normals_positions = tumors_positions + 1  # 为正常盒图的x坐标添加一个小偏移量
plt.figure(figsize=(12, 6))
# 创建盒图
bplot1=plt.boxplot(tumors_plot_data, positions=tumors_positions, showfliers=True, boxprops={'color': 'red'},patch_artist=True)
bplot2=plt.boxplot(normals_plot_data, positions=normals_positions, showfliers=True, boxprops={'color': 'blue'},patch_artist=True)
# fill with colors
# 为正常盒图设置填充颜色
colors = ['pink','lightblue']
for patch in bplot1['boxes']:
    patch.set_facecolor(colors[0])
for patch in bplot2['boxes']:
    patch.set_facecolor(colors[1])

# 设置x轴刻度和标签
tick_positions = (tumors_positions + normals_positions) / 2
plt.xticks(tick_positions, merged_df['cohort'].tolist(), rotation=60)
plt.ylabel(f'{gene_name}_RSEM')
plt.ylim(-2,20 )

plt.title(f'Boxplot for {gene_name} expression in {cancer_name} - Tumors vs Normals')

# 保存图像到指定路径
save_path =os.path.join(os.getcwd(), f'{cancer_name}_{gene_name} expression_TCGA.png')
plt.savefig(save_path, bbox_inches='tight')

# 显示图像
plt.show()

