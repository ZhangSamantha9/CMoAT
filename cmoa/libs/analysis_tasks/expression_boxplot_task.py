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
        self.gene=gene

    def preprocess(self) :


        cancer_dataset=cd.load_cancer(self.cancer_name)
        if not cancer_dataset:
            raise PreprocessError(f'cancer dataset [{self.cancer_name}] load failure.')

        cancer_raw_data=cancer_dataset.join_metadata_to_omics(
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
        self.preprocess_data=reduced_cancer_data
        self.normal_preprocess_data = reduced_cancer_data[reduced_cancer_data.Sample_Tumor_Normal == 'Normal']
        self.tumor_preprocess_data = reduced_cancer_data[reduced_cancer_data.Sample_Tumor_Normal == 'Tumor']

        print('data done')



    def process(self) -> None:
        tail= '_proteomics'
        gene_proteomics_name = self.gene +tail
        print(gene_proteomics_name)

        if gene_proteomics_name not in self.preprocess_data.column:
            raise PreprocessError(f'Gene[{gene_proteomics_name}] not in dataframe')
        print('0')

        tumor_normal_label = "Sample_Tumor_Normal"
        self.preprocess_data[tumor_normal_label].unique()
        print('1')
        # gene_normal = self.preprocess_data.Sample_Tumor_Normal =='Normal'
        # gene_tumor = self.preprocess_data.Sample_Tumor_Normal =='Tumor'

        p_value= scipy.stats.ttest_ind(self.normal_preprocess_data, self.tumor_preprocess_data).pvalue
        print(p_value)
        boxplot=sns.boxplot(x=tumor_normal_label, y=self.gene, data=self.preprocess_data, showfliers=False,
                    order=["Tumor", "Normal"])
        boxplot = sns.stripplot(x=tumor_normal_label, y=self.gene, data=self.preprocess_data, color='.3',
                      order=["Tumor", "Normal"])
        boxplot.set(title=f'{self.cancer_name} protein expression for {self.gene} ')
        #\np - value = {p_value}
        figPath = os.path.join(os.getcwd(),'expression_boxplot')
        print('figure done')
        boxplot.get_figure().savefig(figPath)

        if (os.path.exists(figPath)):
            self.figPath = figPath
        else:
            raise ProcessError(f'Could not save figer at {figPath}')


        @property
        def result(self):
            return self.figPath