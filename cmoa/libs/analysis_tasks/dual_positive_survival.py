import os

import cptac.utils as ut
import pandas as pd
import numpy as np
from lifelines import KaplanMeierFitter

from cmoa.libs import cptac_data as cd
from .analysis_task_base import AnalysisTaskBase, PreprocessError, ProcessError


class DualSurvivalAnalysisTask(AnalysisTaskBase):

    def __init__(self, cancer: str, gene1: str, gene2: str) -> None:
        super().__init__()
        self.cancer_name = cancer
        self.gene1_name = gene1
        self.gene2_name = gene2

    def preprocess(self):

        cancer_dataset = cd.load_dataset(self.cancer_name)
        if not cancer_dataset:
            raise PreprocessError(
                f'cancer dataset [{self.cancer_name}] load failure.')
        else:
            self.cancer_dataset = cancer_dataset


    def process(self) -> None:

        clinical = self.cancer_dataset.get_clinical()
        cols = list(clinical.columns)
        tail = '_proteomics'



        follow_up = self.cancer_dataset.get_followup()

        clinical.to_excel('clinical.xlsx')
        follow_up.to_excel('follow_up.xlsx')

        cancer_raw_data = self.cancer_dataset.join_metadata_to_omics(
            metadata_df_name="clinical",
            omics_df_name="proteomics",
            omics_genes=[self.gene1_name,self.gene2_name],
            quiet=True
        )
        # 删除重复列名的列
        # cancer_raw_data=cancer_raw_data.loc[:, ~cancer_raw_data.columns.duplicated()]
        # print(cancer_raw_data)
        # cancer_raw_data = cancer_raw_data.iloc[:, :17]
        cancer_raw_data.to_excel('cancer_raw_data.xlsx')
        omics_gene1 = self.gene1_name+tail
        omics_gene2 = self.gene2_name+tail
        if omics_gene1 not in cancer_raw_data.columns:
            raise ProcessError(f'Gene [{omics_gene1}] not in dataframe')
        if omics_gene2 not in cancer_raw_data.columns:
            raise ProcessError(f'Gene [{omics_gene2}] not in dataframe')

        follow_up = follow_up.rename({'PPID': 'Patient_ID'}, axis='columns')

        print('1')

        reduced_cancer_data= pd.DataFrame(
            ut.reduce_multiindex(
                df=cancer_raw_data,
                levels_to_drop="Database_ID"
            ))
        
        print('2')


        clin_prot_follow1 = pd.merge(
            reduced_cancer_data, follow_up, on="Patient_ID")
        clin_prot_follow1.to_excel('clin_prot_follow1.xlsx')
        
        print('3')
        columns_to_focus_on = ['Vital Status',
                               'Path Diag to Last Contact(Day)',
                               'Path Diag to Death(days)']

        

        columns_to_focus_on.append(omics_gene1)
        print('4')
        columns_to_focus_on.append(omics_gene2)
        print('5')
        focus_group = clin_prot_follow1[columns_to_focus_on].copy()
        
        focus_group = focus_group.copy()
        print('6')
    

        focus_group['Vital Status'] = focus_group['Vital Status'].replace(
            'Living', False)
        focus_group['Vital Status'] = focus_group['Vital Status'].replace(
            'Deceased', True)
        focus_group['Vital Status'] = focus_group['Vital Status'].astype(
            'bool')
        

        cols = ['Path Diag to Last Contact(Day)', 'Path Diag to Death(days)']
        focus_group.to_excel('focus_group.xlsx')
        focus_group = focus_group.assign(
            Days_Until_Last_Contact_Or_Death=focus_group[cols].sum(1)).drop(columns=cols)
        # focus_group = focus_group.iloc[:, 1:4]
        focus_group.to_excel('focus_group.xlsx')
        print('7')
        lower_25_filter = (focus_group[omics_gene1] <= focus_group[omics_gene1].quantile(.25))\
            & (focus_group[omics_gene2] <= focus_group[omics_gene2].quantile(.25))
        upper_25_filter = (focus_group[omics_gene1] >= focus_group[omics_gene1].quantile(.75)) \
            & (focus_group[omics_gene2] >= focus_group[omics_gene2].quantile(.75))


        focus_group[omics_gene1] = np.where(
            lower_25_filter, "Lower_25%", focus_group[omics_gene1])
        focus_group[omics_gene1] = np.where(
            upper_25_filter, "Upper_75%", focus_group[omics_gene1])
        focus_group[omics_gene1] = np.where(
            ~lower_25_filter & ~upper_25_filter, "Middle_50%", focus_group[omics_gene1])

        focus_group[omics_gene2] = np.where(
            lower_25_filter, "Lower_25%", focus_group[omics_gene2])
        focus_group[omics_gene2] = np.where(
            upper_25_filter, "Upper_75%", focus_group[omics_gene2])
        focus_group[omics_gene2] = np.where(~lower_25_filter & ~upper_25_filter, "Middle_50%",
                                                      focus_group[omics_gene2])
        df_clean = focus_group.dropna(axis=0, how='any').copy()
        df_clean.to_excel('df_clean.xlsx')
        # df2_clean = focus_group2.dropna(axis=0, how='any').copy()

        kmf = KaplanMeierFitter()
        T = df_clean['Days_Until_Last_Contact_Or_Death']
        E = df_clean['Vital Status']
        groups = df_clean[omics_gene1]
        ix = (groups == 'Lower_25%')
        kmf.fit(T[~ix], E[~ix], label='Upper_75%')
        plot = kmf.plot_survival_function(loc=slice(0., 1100.))

        kmf.fit(T[ix], E[ix], label='Lower_25%')
        plot = kmf.plot_survival_function(ax=plot, loc=slice(0., 1100.))
        figPath = os.path.join(os.getcwd(
        ), f'[{omics_gene1}] and [{omics_gene2}] survival of [{self.cancer_name}].png')
        plot.get_figure().savefig(figPath)

        if (os.path.exists(figPath)):
            self.figPath = figPath
        else:
            raise ProcessError(f'Could not save figer at {figPath}')

        @property
        def result(self):
            return self.figPath
