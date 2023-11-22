import os


import pandas as pd
import scipy.stats
import seaborn as sns
import cptac.utils as ut

from cmoa.libs import cptac_data as cd
from .analysis_task_base import AnalysisTaskBase, PreprocessError, ProcessError

class MutiExpressionBoxplotTask(AnalysisTaskBase):

    def __init__ (self,gene:str)-> None:
        super().__init__()
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