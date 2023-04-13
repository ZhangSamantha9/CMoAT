import cptac
import cptac.utils as ut
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

matplotlib.use('agg')

# 导入数据库并把他们存到字典中）
CANCER_DATA_DIC = {
    'Luad': cptac.Luad,
    'Endometrial': cptac.Endometrial,
    'Brca': cptac.Brca,
    'Ccrcc': cptac.Ccrcc,
    'Colon': cptac.Colon,
    'Gbm': cptac.Gbm,
    'Hnscc': cptac.Hnscc,
    'Lscc': cptac.Lscc,
    'Ovarian': cptac.Ovarian,
    'Pdac': cptac.Pdac,
    'UcecConf': cptac.UcecConf,
    'GbmConf': cptac.GbmConf
}


# 定义处理癌症数据的函数，如果找到癌症数据，则处理之。否则打印没找到
def get_cancer_data(cancer_name):
    print("receive parameters: ", cancer_name)

    if CANCER_DATA_DIC.__contains__(cancer_name):
        return cancer_data_preprocess(CANCER_DATA_DIC[cancer_name]())
    else:
        print(cancer_name, 'is not in the dictionary')


# 癌症数据处理过程：将临床数据与表达数据合成一个，再舍去多重索引，最后挑选肿瘤组织的数据
def cancer_data_preprocess(cancer):
    cancer_row_data = cancer.join_metadata_to_omics(metadata_df_name="clinical", omics_df_name="proteomics",
                                                    metadata_cols='Sample_Tumor_Normal')
    reduced_cancer_data = pd.DataFrame(
        ut.reduce_multiindex(df=cancer_row_data, levels_to_drop="Database_ID", quiet=True))
    cancer_data = reduced_cancer_data[reduced_cancer_data.Sample_Tumor_Normal == 'Tumor']
    return cancer_data


# 绘制相关性曲线
def gene_correlation_curve(gene1, gene2, cancer_data_analysis):
    print("receive parameters:", gene1, gene2)
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

    gene1_data = cancer_data_analysis[gene1_proteomics_name]
    print('data for gene 1 done')
    gene2_data = cancer_data_analysis[gene2_proteomics_name]
    print('data for gene 2 done')

    # 计算相关性系数r和p_value，相关性系数R保留6位小数
    R = '{:.6f}'.format(stats.pearsonr(gene1_data, gene2_data).statistic)
    p_value = '{:.4e}'.format(stats.pearsonr(gene1_data, gene2_data).pvalue)

    # 画图设置
    sns.set(style="darkgrid")
    plot = sns.regplot(x=gene1_data, y=gene2_data)
    plot.set(xlabel=gene1, ylabel=gene2,
             title='Gene correlation for ' + gene1 + ' and ' + gene2 + "\n" + 'R = ' + R + '  p-value = ' + p_value)
    # plt.text(1,1,pearson_correlation_array)
    matplotlib.pyplot.savefig('gene_correlation')
    print('Figure done')
