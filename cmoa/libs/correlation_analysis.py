import cptac
import cptac.utils as ut
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from cptac import dataset
import os



# 癌症数据处理过程：将临床数据与表达数据合成一个，再舍去多重索引，最后挑选肿瘤组织的数据
def dataset_preprocess(cancer: dataset.Dataset):
    '''
    preprocess the cancer date from dateset to dataframe
    '''
    cancer_row_data = cancer.join_metadata_to_omics(metadata_df_name="clinical", omics_df_name="proteomics",
                                                    metadata_cols='Sample_Tumor_Normal')
    reduced_cancer_data=pd.DataFrame(cancer_row_data)
    # reduced_cancer_data = pd.DataFrame(
    #     ut.reduce_multiindex(df=cancer_row_data, levels_to_drop="Database_ID", quiet=True))
    cancer_data = reduced_cancer_data[reduced_cancer_data.Sample_Tumor_Normal == 'Tumor']
    return cancer_data


# 绘制相关性曲线
def draw_correlation_curve(gene1: str, gene2: str, cancer_data_analysis: pd.DataFrame):
    matplotlib.use('agg')

    print(f'Starting drawing correlation curve for {gene1} and {gene2}')
    tumor_colums = cancer_data_analysis.columns
    tail = '_proteomics'
    gene1_proteomics_name = gene1 + tail
    gene2_proteomics_name = gene2 + tail

    # 找gene1，gene2
    if gene1_proteomics_name in cancer_data_analysis.columns:
        print('gene 1 successfully matched')
    else:
        print("No data for gene 1 is found")
        return

    if gene2_proteomics_name in cancer_data_analysis.columns:
        print('gene 2 successfully matched')
    else:
        print("No data for gene 2 is found")
        return


    # 使用DataFrame.merge()方法进行合并
    # gene1_gene2_merge = gene1_data.to_frame().merge(gene2_data)
    # 打印合并后的DataFrame
    # print(gene1_gene2_merge)

    gene1_series = cancer_data_analysis[gene1_proteomics_name]
    gene2_series = cancer_data_analysis[gene2_proteomics_name]
    print(gene2_series, gene1_series)
    genes_series = pd.merge(gene1_series, gene2_series, on='Patient_ID')
    print(genes_series)
    genes_series = genes_series.replace('NaN', float('nan')).dropna()
    print(genes_series)
    gene1_modified = genes_series[gene1_proteomics_name]
    gene2_modified = genes_series[gene2_proteomics_name]
    print("填充后的DataFrame:")
    print(gene1_modified, gene2_modified, type(gene1_modified))
    # 计算填充后的DataFrame中基因"A"和基因"B"之间的相关性
    p_value = '{:.4e}'.format(stats.pearsonr(gene1_modified, gene2_modified).pvalue)
    R = '{:.6f}'.format(stats.pearsonr(gene1_modified, gene2_modified).statistic)
    print("GeneA和GeneB的相关性：", R)
    print("p-value：", p_value)


    # 画图设置
    sns.set(style="darkgrid")
    plot = sns.regplot(x=gene1_modified, y=gene2_modified)
    plot.set(xlabel=gene1, ylabel=gene2,
             title='Gene correlation for ' + gene1 + ' and ' + gene2 + "\n" + 'R = ' + R + '  p-value = ' + p_value)
    # plt.text(1,1,pearson_correlation_array)

    figPath = os.path.join(os.getcwd(), 'correlation.png')
    plt.savefig(figPath, format='png')

    if (os.path.exists(figPath)):
        print(f'Figure saved at {figPath}')
        return figPath
    else:
        print('Figure not saved')
        return None
