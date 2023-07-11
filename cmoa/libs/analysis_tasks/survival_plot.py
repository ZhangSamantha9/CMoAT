import os

import pandas as pd
import cptac
import cptac.utils as ut
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from lifelines import KaplanMeierFitter

from cmoa.libs import cptac_data as cd
from .analysis_task_base import AnalysisTaskBase, PreprocessError, ProcessError

class SurvivalAnalysisTask(AnalysisTaskBase):

    def __init__(self, cancer: str, gene: str) -> None:
        super().__init__()
        self.cancer_name = cancer
        self.gene_name = gene


    def preprocess(self):

      cancer_dataset= cd.load_dataset(self.cancer_name)
      if not cancer_dataset :
          raise PreprocessError(f'cancer dataset [{self.cancer_name}] load failure. ')

      clinical = cancer_dataset.get_clinical()
      cols = list(clinical.columns)
      omics_gene = self.gene_name
      follow_up = cancer_dataset.get_followup()
      cancer_raw_data= cancer_dataset.join_metadata_to_omics(
          metadata_df_name="clinical",
          omics_df_name="proteomics",
          metadata_cols=cols,
          omics_genes=omics_gene,
          quiet=True
      )
      follow_up = follow_up.rename({'PPID': 'Patient_ID'}, axis='columns')
      reduced_cancer_data = pd.DataFrame(
          ut.reduce_multiindex(
              df=cancer_raw_data,
              levels_to_drop="Database_ID"
          ))
      self.clin_prot_follow = pd.merge(reduced_cancer_data, follow_up, on="Patient_ID")
      self.columns_to_focus_on = ['Vital Status',
                             'Path Diag to Last Contact(Day)',
                             'Path Diag to Death(days)']


    def process(self) -> None:
        tail= '_proteomics'
        gene_proteomics_name = self.gene_name+tail

        if gene_proteomics_name not in self.preprocess_data.column:
            raise ProcessError(f'Gene [{gene_proteomics_name}] not in dataframe')

        self.columns_to_focus_on.append(gene_proteomics_name)
        focus_group = self.clin_prot_follow[self.columns_to_focus_on].copy()

        focus_group = focus_group.copy()

        focus_group['Vital Status'] = focus_group['Vital Status'].replace('Living', False)
        focus_group['Vital Status'] = focus_group['Vital Status'].replace('Deceased', True)
        focus_group['Vital Status'] = focus_group['Vital Status'].astype('bool')

        cols = ['Path Diag to Last Contact(Day)', 'Path Diag to Death(days)']


        focus_group = focus_group.assign(Days_Until_Last_Contact_Or_Death=focus_group[cols].sum(1)).drop(cols, 1)
        lower_25_filter = focus_group[gene_proteomics_name] <= focus_group[gene_proteomics_name].quantile(.25)
        upper_25_filter = focus_group[gene_proteomics_name] >= focus_group[gene_proteomics_name].quantile(.75)

        focus_group[gene_proteomics_name] = np.where(lower_25_filter, "Lower_25%", focus_group[gene_proteomics_name])
        focus_group[gene_proteomics_name] = np.where(upper_25_filter, "Upper_75%", focus_group[gene_proteomics_name])
        focus_group[gene_proteomics_name] = np.where(~lower_25_filter & ~upper_25_filter, "Middle_50%", focus_group[gene_proteomics_name])
        df_clean = focus_group.dropna(axis=0, how='any').copy()

        kmf = KaplanMeierFitter()
        T = df_clean['Days_Until_Last_Contact_Or_Death']
        E = df_clean['Vital Status']
        groups = df_clean[gene_proteomics_name]
        ix = (groups == 'Lower_25%')
        kmf.fit(T[~ix], E[~ix], label='Upper_75%')
        plot = kmf.plot_survival_function(loc=slice(0., 1100.))

        kmf.fit(T[ix], E[ix], label='Lower_25%')
        plot = kmf.plot_survival_function(ax=plot, loc=slice(0., 1100.))
        figPath = os.path.join(os.getcwd(), f'[{gene_proteomics_name}] survival.png')
        plot.get_figure().savefig(figPath)

        if (os.path.exists(figPath)):
            self.figPath = figPath
        else:
            raise ProcessError(f'Could not save figer at {figPath}')

        @property
        def result(self):
            return self.figPath






