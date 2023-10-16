import os

import pandas as pd
from scipy import stats
import cptac.utils as ut
import seaborn as sns
from sklearn.impute import KNNImputer
import numpy as np


from cmoa.libs import cptac_data as cd
from .analysis_task_base import AnalysisTaskBase, PreprocessError, ProcessError


class CorrelationAnalysisTask(AnalysisTaskBase):

    def __init__(self, cancer: str, gene1: str, gene2: str) -> None:
        super().__init__()
        self.cancer_name = cancer
        self.gene1_name = gene1
        self.gene2_name = gene2

    def preprocess(self):

        cancer_dataset = cd.load_dataset(self.cancer_name)
        if not cancer_dataset:
            raise PreprocessError(f'cancer dataset [{self.cancer_name}] load failure.')

        cancer_raw_data = cancer_dataset.join_metadata_to_omics(
            metadata_df_name='clinical',
            omics_df_name='proteomics',
            metadata_cols='Sample_Tumor_Normal'
        )

        reduced_cancer_data = pd.DataFrame(
            ut.reduce_multiindex(
                df=cancer_raw_data,
                levels_to_drop='Database_ID',
                quiet=True
            ))

        # TODO: 验证是否只需要返回Tumor类别
        self.preprocess_data = reduced_cancer_data[reduced_cancer_data.Sample_Tumor_Normal == 'Tumor']
        print(self.preprocess_data)

    
    def process(self) -> None:
        tail = '_proteomics'
        gene1_proteomics_name = self.gene1_name + tail
        gene2_proteomics_name = self.gene2_name + tail

        if gene1_proteomics_name not in self.preprocess_data.columns:
             raise ProcessError(f'Gene [{gene1_proteomics_name}] not in dataframe')
        if gene2_proteomics_name not in self.preprocess_data.columns:
            raise ProcessError(f'Gene [{gene2_proteomics_name}] not in dataframe')
        
        gene1_series = self.preprocess_data[gene1_proteomics_name]
        gene2_series = self.preprocess_data[gene2_proteomics_name]

        # 检查基因"A"和基因"B"是否有缺失值
        if gene1_series.isnull().any() or gene2_series.isnull().any():
            # 使用K近邻填充缺失值
            print(gene1_series, gene2_series, gene1_series.ndim, type(gene1_series))
            gene1_series.to_excel('gene1_data.xlsx', index=False)
            gene2_series.to_excel('gene2_data.xlsx', index=False)
            gene1_modified=gene1_series.replace('NA', float('NaN'))
            gene2_modified=gene2_series.replace('NA', float('NaN'))
            # 打印填充后的DataFrame
            print("填充后的DataFrame:")
            print(gene1_modified, gene2_modified, type(gene1_modified))
            # 计算填充后的DataFrame中基因"A"和基因"B"之间的相关性
            p_value = '{:.4e}'.format(stats.pearsonr(gene1_modified, gene2_modified).pvalue)
            R = '{:.6f}'.format(stats.pearsonr(gene1_modified, gene2_modified).statistic)
            print("GeneA和GeneB的相关性：", R)
            print("p-value：", p_value)
        else:
            # 直接进行相关性分析
            gene1_modified = gene1_series
            gene2_modified = gene2_series
            print(gene1_modified, gene2_modified)
            p_value = '{:.4e}'.format(stats.pearsonr(gene1_modified, gene2_modified).pvalue)
            R = '{:.6f}'.format(stats.pearsonr(gene1_modified, gene2_modified).statistic)

            print("ProteinA和ProteinB的相关性：", R)
            print("p-value：", p_value)

        # pearsonr_result = stats.pearsonr(gene1_series, gene2_series)
        # r_value = '{:.6f}'.format(pearsonr_result.statistic)
        # p_value = '{:.4e}'.format(pearsonr_result.pvalue)

        sns.set(style="darkgrid")
        plot = sns.regplot(x=gene1_series, y=gene2_series)
        plot.set(xlabel=self.gene1_name, ylabel=self.gene2_name,
                title=f'{self.cancer_name} protein expression correlation for {self.gene1_name} and {self.gene2_name}\nR = {R} p-value = {p_value}')

        figPath = os.path.join(os.getcwd(), 'correlation.png')
        plot.get_figure().savefig(figPath)

        if (os.path.exists(figPath)):
            self.figPath = figPath
        else:
            raise ProcessError(f'Could not save figer at {figPath}')

        @property
        def result(self):
            return self.figPath

