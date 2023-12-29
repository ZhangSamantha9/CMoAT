import os

import pandas as pd
from scipy import stats
import cptac.utils as ut
import seaborn as sns

from cmoa.libs import cptac_data as cd
from .analysis_task_base import AnalysisTaskBase, PreprocessError, ProcessError


class CorrelationHeatmapTask(AnalysisTaskBase):

    def __init__(self, cancer: str, gene1: str, gene2: str, gene3:str, gene4:str, gene5:str, gene6:str, gene7:str) -> None:
        super().__init__()
        self.cancer_name = cancer
        self.gene1_name = gene1
        self.gene2_name = gene2
        self.gene3_name = gene3
        self.gene4_name = gene4
        self.gene5_name = gene5
        self.gene6_name = gene6
        self.gene7_name = gene7

    def preprocess(self):

        cancer_dataset = cd.load_cancer(self.cancer_name)
        if not cancer_dataset:
            raise PreprocessError(f'cancer dataset [{self.cancer_name}] load failure.')

        cancer_raw_data = cancer_dataset.multi_join(
            {'umich proteomics': [self.gene1_name, self.gene2_name,self.gene3_name,self.gene4_name,self.gene5_name,self.gene6_name,self.gene7_name]}
        )
        cancer_raw_data = pd.DataFrame(
            ut.reduce_multiindex(
                df=cancer_raw_data,
                levels_to_drop="Database_ID"
            ))

        tail = '_umich_proteomics'
        self.gene1_pro_name = self.gene1_name + tail
        self.gene2_pro_name = self.gene2_name + tail
        self.gene3_pro_name = self.gene3_name + tail
        self.gene4_pro_name = self.gene4_name + tail
        self.gene5_pro_name = self.gene5_name + tail
        self.gene6_pro_name = self.gene6_name + tail
        self.gene7_pro_name = self.gene7_name + tail


        # cancer_raw_data.to_excel('cancer_raw_data.xlsx')
        if self.gene1_pro_name not in cancer_raw_data.columns:
            raise ProcessError(f'Gene [{self.gene1_pro_name}] not in dataframe')
        if self.gene2_pro_name not in cancer_raw_data.columns:
            raise ProcessError(f'Gene [{self.gene2_pro_name}] not in dataframe')
        if self.gene3_pro_name not in cancer_raw_data.columns:
            raise ProcessError(f'Gene [{self.gene3_pro_name}] not in dataframe')
        if self.gene4_pro_name not in cancer_raw_data.columns:
            raise ProcessError(f'Gene [{self.gene4_pro_name}] not in dataframe')
        if self.gene5_pro_name not in cancer_raw_data.columns:
            raise ProcessError(f'Gene [{self.gene5_pro_name}] not in dataframe')
        if self.gene6_pro_name not in cancer_raw_data.columns:
            raise ProcessError(f'Gene [{self.gene6_pro_name}] not in dataframe')
        if self.gene7_pro_name not in cancer_raw_data.columns:
            raise ProcessError(f'Gene [{self.gene7_pro_name}] not in dataframe')


        cancer_raw_data = cancer_raw_data.loc[:, ~cancer_raw_data.columns.duplicated()]
        is_tumor = [not lable.endswith('.N') for lable in cancer_raw_data.index]
        self.preprocess_data = cancer_raw_data.loc[is_tumor, :]
        # self.preprocess_data.to_excel('preprocess_data.xlsx')

    def process(self) -> None:

        genes_series = self.preprocess_data.replace('NaN', float('nan')).dropna()
        genes_series = genes_series.loc[:, ~genes_series.columns.duplicated()]
        correlation_matrix = genes_series.corrwith(genes_series[self.gene1_pro_name])
        print(correlation_matrix)


    def plot(self):
        correlation_df = pd.DataFrame(correlation_matrix, columns=['Correlation'])
        # 绘制相关性热图
        sns.heatmap(correlation_df, annot=True, cmap='coolwarm', fmt=".2f")
        plt.title('Correlation Heatmap')
        plt.show()
        # p_value = '{:.4e}'.format(stats.pearsonr(self.gene1_modified, self.gene2_modified).pvalue)
        # R = '{:.6f}'.format(stats.pearsonr(self.gene1_modified, self.gene2_modified).statistic)
        # print("GeneA和GeneB的相关性：", R)
        # print("p-value：", p_value)

        sns.set(style="darkgrid")
        plot = sns.regplot(x=self.gene1_modified, y=self.gene2_modified)
        plot.set(xlabel=self.gene1_name, ylabel=self.gene2_name,
                 title=f'{self.cancer_name} protein expression correlation for {self.gene1_name} and {self.gene2_name}\nR = {R} p-value = {p_value}')

        figPath = os.path.join(os.getcwd(),
                               f'{self.cancer_name}_{self.gene1_name} and {self.gene2_name} correlation.png')
        plot.get_figure().savefig(figPath)

        if (os.path.exists(figPath)):
            self.figPath = figPath
        else:
            raise ProcessError(f'Could not save figer at {figPath}')

        @property
        def result(self):
            return self.figPath

