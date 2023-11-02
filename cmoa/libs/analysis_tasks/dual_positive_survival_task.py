import os

import cptac.utils as ut
import pandas as pd
import numpy as np
from lifelines import KaplanMeierFitter
from lifelines.statistics import logrank_test

from cmoa.libs import cptac_data as cd
from .analysis_task_base import AnalysisTaskBase, PreprocessError, ProcessError


class DualSurvivalAnalysisTask(AnalysisTaskBase):

    def __init__(self, cancer: str, gene1: str, gene2: str) -> None:
        super().__init__()
        self.cancer_name = cancer
        self.gene1_name = gene1
        self.gene2_name = gene2

    def preprocess(self):

        cancer_dataset = cd.load_cancer(self.cancer_name)
        if not cancer_dataset:
            raise PreprocessError(
                f'cancer dataset [{self.cancer_name}] load failure.')
        else:
            self.cancer_dataset = cancer_dataset

    def process(self) :

        clinical = self.cancer_dataset.get_clinical("mssm")
        # cols = list(clinical.columns)
        tail = '_proteomics'

        follow_up = self.cancer_dataset.get_followup("mssm")

        clinical.to_excel('clinical.xlsx')
        follow_up.to_excel('follow_up.xlsx')


        cancer_raw_data = self.cancer_dataset.multi_join({
            "mssm clinical": '',
            "umich proteomics": [self.gene1_name, self.gene2_name],
        })

        cancer_raw_data.to_excel('cancer_raw_data.xlsx')
        self.omics_gene1 = self.gene1_name+'_umich'+tail
        omics_gene2 = self.gene2_name+'_umich'+tail
        if self.omics_gene1 not in cancer_raw_data.columns:
            raise ProcessError(f'Gene [{self.omics_gene1}] not in dataframe')
        if omics_gene2 not in cancer_raw_data.columns:
            raise ProcessError(f'Gene [{omics_gene2}] not in dataframe')

        follow_up = follow_up.rename({'PPID': 'Patient_ID'}, axis='columns')

        reduced_cancer_data = pd.DataFrame(
            ut.reduce_multiindex(
                df=cancer_raw_data,
                levels_to_drop="Database_ID"
            ))


        reduced_cancer_data= reduced_cancer_data.loc[:, ~reduced_cancer_data.columns.duplicated()]
        reduced_cancer_data = reduced_cancer_data.dropna(subset=['type_of_analyzed_samples_mssm_clinical'])

        reduced_cancer_data = reduced_cancer_data[reduced_cancer_data['type_of_analyzed_samples_mssm_clinical'] != 'Normal']
        reduced_cancer_data.to_excel('reduce_data.xlsx')
        clin_prot_follow= pd.merge(
            reduced_cancer_data, follow_up, on="Patient_ID")
        clin_prot_follow.to_excel('clin_prot_follow1.xlsx')

        self.vital_status='vital_status_at_date_of_last_contact'
        date_of_last_contact='number_of_days_from_date_of_initial_pathologic_diagnosis_to_date_of_last_contact'
        date_of_death='number_of_days_from_date_of_initial_pathologic_diagnosis_to_date_of_death'
        columns_to_focus_on = [
            self.vital_status,
            date_of_last_contact,
            date_of_death,
            self.omics_gene1,omics_gene2]

        focus_group = clin_prot_follow[columns_to_focus_on].copy()

        focus_group = focus_group.copy()

        focus_group[self.vital_status] = focus_group[self.vital_status].replace(
            'Living', False)
        focus_group[self.vital_status] = focus_group[self.vital_status].replace(
            'Deceased', True)
        focus_group[self.vital_status] = focus_group[self.vital_status].astype(
            'bool')

        cols = [date_of_last_contact,date_of_death]
        # focus_group.to_excel('focus_group.xlsx')
        focus_group = ((focus_group.assign(
            Days_Until_Last_Contact_Or_Death=focus_group[cols].sum(1)).drop(columns=cols)))
        focus_group=focus_group.loc[:, ~focus_group.columns.duplicated()]
        focus_group.to_excel('focus_group.xlsx')

        lower_25_filter = (focus_group[self.omics_gene1] <= focus_group[self.omics_gene1].quantile(.25))\
            & (focus_group[omics_gene2] <= focus_group[omics_gene2].quantile(.25))
        upper_25_filter = (focus_group[self.omics_gene1] >= focus_group[self.omics_gene1].quantile(.75)) \
            & (focus_group[omics_gene2] >= focus_group[omics_gene2].quantile(.75))

        focus_group[self.omics_gene1] = np.where(
            lower_25_filter, "Lower_25%", focus_group[self.omics_gene1])
        focus_group[self.omics_gene1] = np.where(
            upper_25_filter, "Upper_75%", focus_group[self.omics_gene1])
        focus_group[self.omics_gene1] = np.where(
            ~lower_25_filter & ~upper_25_filter, "Middle_50%", focus_group[self.omics_gene1])

        self.df_clean = focus_group.dropna(axis=0, how='any').copy()
        self.df_clean = self.df_clean[self.df_clean["Days_Until_Last_Contact_Or_Death"] >0]
        self.df_clean.to_excel('self.df_clean.xlsx')
    def plot(self):
        # return  self.df_clean
        kmf = KaplanMeierFitter()
        T = self.df_clean['Days_Until_Last_Contact_Or_Death']
        E = self.df_clean[self.vital_status]
        groups = self.df_clean[self.omics_gene1]
        ix = (groups == 'Lower_25%')
        kmf.fit(T[~ix], E[~ix], label='Upper_75%')
        median_survival_time_upper = kmf.median_survival_time_
        plot = kmf.plot_survival_function(loc=slice(0., 1200.))

        kmf.fit(T[ix], E[ix], label='Lower_25%')
        median_survival_time_lower = kmf.median_survival_time_
        print(f"Median Survival Time (Upper 75%): {median_survival_time_upper}")
        print(f"Median Survival Time (Lower 25%): {median_survival_time_lower}")
        # 执行 Log-rank 检验
        results = logrank_test(T[~ix], T[ix], event_observed_A=E[~ix], event_observed_B=E[ix])

        # 获取 Log-rank 检验的统计信息
        test_statistic = results.test_statistic
        p_value = results.p_value

        # 打印 Log-rank 检验的结果
        print("Log-rank test statistic:", test_statistic)
        print("P-value:", p_value)
        plot = kmf.plot_survival_function(ax=plot, loc=slice(0., 1200.))
        plot.set(ylabel='percent survival',
                 title=f'{self.gene1_name} and {self.gene2_name} survival of {self.cancer_name}')
        plot.legend(loc='lower left')
        figPath = os.path.join(os.getcwd(), f'{self.gene1_name} and {self.gene2_name} survival of {self.cancer_name}.png')
        plot.get_figure().savefig(figPath)

        if (os.path.exists(figPath)):
            self.figPath = figPath
        else:
            raise ProcessError(f'Could not save figure at {figPath}')

        @property
        def result(self):
            return self.figPath
