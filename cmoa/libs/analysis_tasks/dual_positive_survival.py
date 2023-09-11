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

        print('cancer data')

    def process(self) -> None:

        clinical = self.cancer_dataset.get_clinical()
        cols = list(clinical.columns)
        tail = '_proteomics'
        omics_gene1 = self.gene1_name+tail
        omics_gene2 = self.gene2_name+tail

        print('00')
        follow_up = self.cancer_dataset.get_followup()
        print('000')
        clinical.to_excel('clinical.xlsx')
        follow_up.to_excel('follow_up.xlsx')
        print('1')
        cancer_raw_data1 = self.cancer_dataset.join_metadata_to_omics(
            metadata_df_name="clinical",
            omics_df_name="proteomics",
            metadata_cols=cols,
            omics_genes=omics_gene1,
            quiet=True
        )
        print('0')
        cancer_raw_data1 = cancer_raw_data1.iloc[:, :17]
        cancer_raw_data2 = self.cancer_dataset.join_metadata_to_omics(
            metadata_df_name="clinical",
            omics_df_name="proteomics",
            metadata_cols=cols,
            omics_genes=omics_gene2,
            quiet=True
        )
        cancer_raw_data2 = cancer_raw_data2.iloc[:, :17]
        if omics_gene1 not in cancer_raw_data1.column:
            raise ProcessError(f'Gene [{omics_gene1}] not in dataframe')
        if omics_gene2 not in cancer_raw_data2.column:
            raise ProcessError(f'Gene [{omics_gene2}] not in dataframe')

        follow_up = follow_up.rename({'PPID': 'Patient_ID'}, axis='columns')
        cancer_raw_data1.to_excel('cancer_raw_data1.xlsx')
        print('3')

        reduced_cancer_data1 = pd.DataFrame(
            ut.reduce_multiindex(
                df=cancer_raw_data1,
                levels_to_drop="Database_ID"
            ))
        # reduced_cancer_data1 = pd.DataFrame(cancer_raw_data1)

        reduced_cancer_data2 = pd.DataFrame(
            ut.reduce_multiindex(
                df=cancer_raw_data2,
                levels_to_drop="Database_ID"
            ))
        # reduced_cancer_data2 = pd.DataFrame(cancer_raw_data2)
        print('4')

        reduced_cancer_data2.to_excel('reduced_cancer_data2.xlsx')

        clin_prot_follow1 = pd.merge(
            reduced_cancer_data1, follow_up, on="Patient_ID")
        clin_prot_follow2 = pd.merge(
            reduced_cancer_data2, follow_up, on="Patient_ID")
        clin_prot_follow1.to_excel('clin_prot_follow1.xlsx')
        clin_prot_follow2.to_excel('clin_prot_follow2.xlsx')
        clin_prot_follow = pd.merge(clin_prot_follow1, clin_prot_follow2)
        clin_prot_follow.to_excel('clin_prot_follow.xlsx')
        print('5')
        columns_to_focus_on = ['Vital Status',
                               'Path Diag to Last Contact(Day)',
                               'Path Diag to Death(days)']

        tail = '_proteomics'
        gene1_proteomics_name = self.gene1_name+tail
        gene2_proteomics_name = self.gene2_name+tail

        columns_to_focus_on.append(gene1_proteomics_name)
        print('5.1')
        columns_to_focus_on.append(gene2_proteomics_name)
        print('5.2')
        focus_group = clin_prot_follow[columns_to_focus_on].copy()
        # focus_group2 = clin_prot_follow2[columns_to_focus_on].copy()
        focus_group = focus_group.copy()
        print('6')
        # focus_group2 = focus_group2.copy()

        focus_group['Vital Status'] = focus_group['Vital Status'].replace(
            'Living', False)
        focus_group['Vital Status'] = focus_group['Vital Status'].replace(
            'Deceased', True)
        focus_group['Vital Status'] = focus_group['Vital Status'].astype(
            'bool')
        # focus_group2['Vital Status'] = focus_group2['Vital Status'].replace('Living', False)
        # focus_group2['Vital Status'] = focus_group2['Vital Status'].replace('Deceased', True)
        # focus_group2['Vital Status'] = focus_group2['Vital Status'].astype('bool')

        cols = ['Path Diag to Last Contact(Day)', 'Path Diag to Death(days)']

        focus_group = focus_group.assign(
            Days_Until_Last_Contact_Or_Death=focus_group[cols].sum(1)).drop(cols, 1)
        # focus_group = focus_group.iloc[:, 1:4]
        focus_group.to_excel('focus_group.xlsx')
        print('2')
        lower_25_filter = (focus_group[gene1_proteomics_name] <= focus_group[gene1_proteomics_name].quantile(.25))\
            & (focus_group[gene2_proteomics_name] <= focus_group[gene2_proteomics_name].quantile(.25))
        upper_25_filter = (focus_group[gene1_proteomics_name] >= focus_group[gene1_proteomics_name].quantile(.75)) \
            & (focus_group[gene2_proteomics_name] >= focus_group[gene2_proteomics_name].quantile(.75))

        # focus_group2 = focus_group2.assign(Days_Until_Last_Contact_Or_Death=focus_group2[cols].sum(1)).drop(cols, 1)
        # lower_25_filter2 = focus_group2[gene2_proteomics_name] <= focus_group2[gene2_proteomics_name].quantile(.25)
        # upper_25_filter2 = focus_group2[gene2_proteomics_name] >= focus_group2[gene2_proteomics_name].quantile(.75)

        focus_group[gene1_proteomics_name] = np.where(
            lower_25_filter, "Lower_25%", focus_group[gene1_proteomics_name])
        focus_group[gene1_proteomics_name] = np.where(
            upper_25_filter, "Upper_75%", focus_group[gene1_proteomics_name])
        focus_group[gene1_proteomics_name] = np.where(
            ~lower_25_filter & ~upper_25_filter, "Middle_50%", focus_group[gene1_proteomics_name])

        focus_group[gene2_proteomics_name] = np.where(
            lower_25_filter, "Lower_25%", focus_group[gene2_proteomics_name])
        focus_group[gene2_proteomics_name] = np.where(
            upper_25_filter, "Upper_75%", focus_group[gene2_proteomics_name])
        focus_group[gene2_proteomics_name] = np.where(~lower_25_filter & ~upper_25_filter, "Middle_50%",
                                                      focus_group[gene2_proteomics_name])
        df_clean = focus_group.dropna(axis=0, how='any').copy()
        df_clean.to_excel('df_clean.xlsx')
        # df2_clean = focus_group2.dropna(axis=0, how='any').copy()

        kmf = KaplanMeierFitter()
        T = df_clean['Days_Until_Last_Contact_Or_Death']
        E = df_clean['Vital Status']
        groups = df_clean[gene1_proteomics_name]
        ix = (groups == 'Lower_25%')
        kmf.fit(T[~ix], E[~ix], label='Upper_75%')
        plot = kmf.plot_survival_function(loc=slice(0., 1100.))

        kmf.fit(T[ix], E[ix], label='Lower_25%')
        plot = kmf.plot_survival_function(ax=plot, loc=slice(0., 1100.))
        figPath = os.path.join(os.getcwd(
        ), f'[{gene1_proteomics_name}] and [{gene2_proteomics_name}] survival of [{self.cancer_name}].png')
        plot.get_figure().savefig(figPath)

        if (os.path.exists(figPath)):
            self.figPath = figPath
        else:
            raise ProcessError(f'Could not save figer at {figPath}')

        @property
        def result(self):
            return self.figPath
