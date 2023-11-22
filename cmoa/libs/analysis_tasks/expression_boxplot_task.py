import os


import pandas as pd
import scipy.stats
import seaborn as sns
import cptac.utils as ut

from cmoa.libs import cptac_data as cd
from .analysis_task_base import AnalysisTaskBase, PreprocessError, ProcessError

class ExpressionBoxplotTask(AnalysisTaskBase):


    def __init__ (self,cancer:str,gene:str)-> None:
        super().__init__()
        self.cancer_name=cancer
        self.gene_name=gene

    def preprocess(self) :

        cancer_dataset=cd.load_cancer(self.cancer_name)
        if not cancer_dataset:
            raise PreprocessError(f'cancer dataset [{self.cancer_name}] load failure.')

        cancer_raw_data = cancer_dataset.multi_join(
            {'umich proteomics': [self.gene_name]}
        )
        reduced_cancer_data= pd.DataFrame(
            ut.reduce_multiindex(
                df=cancer_raw_data,
                levels_to_drop="Database_ID"
            ))
        tail = '_umich_proteomics'
        self.gene_pro_name = self.gene_name + tail
        if self.gene_pro_name not in reduced_cancer_data.columns:
             raise ProcessError(f'Gene [{self.gene_pro_name}] not in dataframe')
        reduced_cancer_data= reduced_cancer_data.loc[:, ~reduced_cancer_data.columns.duplicated()]
        self.preprocess_data=reduced_cancer_data


    def process(self) -> None:
        is_tumor = [not lable.endswith('.N') for lable in self.preprocess_data.index]
        is_normal = [lable.endswith('.N') for lable in self.preprocess_data.index]
        self.normal_preprocess_data = self.preprocess_data.loc[is_normal, :]
        self.tumor_preprocess_data = self.preprocess_data.loc[is_tumor, :]
        self.preprocess_data['Sample_Type'] = 'Normal'
        self.preprocess_data.loc[is_tumor, 'Sample_Type'] = 'Tumor'

        print(self.preprocess_data,self.tumor_preprocess_data)
        self.p_value = scipy.stats.ttest_ind(self.normal_preprocess_data, self.tumor_preprocess_data).pvalue
        print(self.p_value)


    def plot(self):
        tumor_normal_label = "Sample_Type"
        self.preprocess_data[tumor_normal_label].unique()
        boxplot=sns.boxplot(x=tumor_normal_label, y=self.preprocess_data[self.gene_pro_name], data=self.preprocess_data, showfliers=False,
                    order=["Tumor", "Normal"])
        boxplot = sns.stripplot(x=tumor_normal_label, y=self.preprocess_data[self.gene_pro_name], data=self.preprocess_data, color='.3',
                      order=["Tumor", "Normal"])
        boxplot.set(title=f'{self.cancer_name} protein expression boxplot for {self.gene_name} \np-value = {self.p_value}')
        figPath = os.path.join(os.getcwd(),f'{self.cancer_name}_{self.gene_name}_expression_boxplot.png')
        print('figure done')
        boxplot.get_figure().savefig(figPath)

        if (os.path.exists(figPath)):
            self.figPath = figPath
        else:
            raise ProcessError(f'Could not save figer at {figPath}')


        @property
        def result(self):
            return self.figPath