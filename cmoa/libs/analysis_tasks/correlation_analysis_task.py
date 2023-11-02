import os

import pandas as pd
from scipy import stats
import cptac.utils as ut
import seaborn as sns



from cmoa.libs import cptac_data as cd
from .analysis_task_base import AnalysisTaskBase, PreprocessError, ProcessError


class CorrelationAnalysisTask(AnalysisTaskBase):

    def __init__(self, cancer: str, gene1: str, gene2: str) -> None:
        super().__init__()
        self.cancer_name = cancer
        self.gene1_name = gene1
        self.gene2_name = gene2

    def preprocess(self):

        cancer_dataset = cd.load_cancer(self.cancer_name)
        if not cancer_dataset:
            raise PreprocessError(f'cancer dataset [{self.cancer_name}] load failure.')

        cancer_raw_data = cancer_dataset.join_metadata_to_omics(
            metadata_name='clinical',
            metadata_source='mssm',
            metadata_cols='type_of_analyzed_samples',
            omics_name='proteomics',
            omics_source='umich'
        )
        cancer_raw_data= cancer_raw_data.loc[:,~cancer_raw_data.columns.duplicated()]
        cancer_raw_data.to_excel('cancer_raw_data.xlsx')
        # if self.cancer_name!='Ucec':
        #     reduced_cancer_data = pd.DataFrame(
        #         ut.reduce_multiindex(
        #             df=cancer_raw_data,
        #             levels_to_drop='Database_ID',
        #             quiet=True
        #         ))
        # else:
        #     reduced_cancer_data=cancer_raw_data
        # TODO: 验证是否只需要返回Tumor类别
        self.preprocess_data = cancer_raw_data[cancer_raw_data['type_of_analyzed_samples_mssm_clinical'].notna()]
        self.preprocess_data.to_excel('self.preprocess_data.xlsx')

    
    def process(self) -> None:
        tail = '_umich_proteomics'
        gene1_proteomics_name = self.gene1_name + tail
        gene2_proteomics_name = self.gene2_name + tail

        if gene1_proteomics_name not in self.preprocess_data.columns:
             raise ProcessError(f'Gene [{gene1_proteomics_name}] not in dataframe')
        if gene2_proteomics_name not in self.preprocess_data.columns:
            raise ProcessError(f'Gene [{gene2_proteomics_name}] not in dataframe')


        # 检查基因"A"和基因"B"是否有缺失值
        gene1_series = self.preprocess_data[gene1_proteomics_name]
        gene2_series = self.preprocess_data[gene2_proteomics_name]
        print(gene2_series, gene1_series)
        genes_series = pd.merge(gene1_series, gene2_series, on='Patient_ID')
        print(genes_series)
        genes_series = genes_series.replace('NaN', float('nan')).dropna()
        genes_series = genes_series.loc[:, ~genes_series.columns.duplicated()]
        print(genes_series)
        self.gene1_modified = genes_series[gene1_proteomics_name]
        self.gene2_modified = genes_series[gene2_proteomics_name]

        print("填充后的DataFrame:")
        print(self.gene1_modified, self.gene2_modified, type(self.gene1_modified))
        # 计算填充后的DataFrame中基因"A"和基因"B"之间的相关性
    def plot(self):
        p_value = '{:.4e}'.format(stats.pearsonr(self.gene1_modified, self.gene2_modified).pvalue)
        R = '{:.6f}'.format(stats.pearsonr(self.gene1_modified, self.gene2_modified).statistic)
        print("GeneA和GeneB的相关性：", R)
        print("p-value：", p_value)

        sns.set(style="darkgrid")
        plot = sns.regplot(x=self.gene1_modified, y=self.gene2_modified)
        plot.set(xlabel=self.gene1_name, ylabel=self.gene2_name,
                title=f'{self.cancer_name} protein expression correlation for {self.gene1_name} and {self.gene2_name}\nR = {R} p-value = {p_value}')

        figPath = os.path.join(os.getcwd(), f'{self.gene1_name} and {self.gene2_name} correlation.png')
        plot.get_figure().savefig(figPath)

        if (os.path.exists(figPath)):
            self.figPath = figPath
        else:
            raise ProcessError(f'Could not save figer at {figPath}')

        @property
        def result(self):
            return self.figPath

