import pandas as pd
import cptac
import cptac.utils as ut
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from lifelines import KaplanMeierFitter
matplotlib.use('agg')
from lifelines.statistics import multivariate_logrank_test

# import cptac.utils as ut
# cptac.download(dataset="Luad",version="latest")

df=pd.read_excel("C:\\Users\\126614\\PycharmProjects\\GEPIA_batch_processing\\CI部提报靶点的GEPIA生信分析_单次跨膜蛋白_protein\\single_transmembrane_protein_list_protein.xlsx")
genes=df['gene_name']
lu = cptac.Luad()
clinical = lu.get_clinical()
proteomics = lu.get_proteomics()
follow_up = lu.get_followup()
plt.clf()
# proteomics = lu.join_metadata_to_omics(metadata_df_name="clinical", omics_df_name="proteomics",
#                                                 metadata_cols='Sample_Tumor_Normal')
# reduced_proteomics = pd.DataFrame(ut.reduce_multiindex(df=proteomics, levels_to_drop="Database_ID", quiet=True))
# for gene in genes:
#     omics_gene = gene
#     omics_gene += '_proteomics'
#     all_lost_data=()
#     if omics_gene in reduced_proteomics.columns:
#         continue
#     else:
#         print(omics_gene)



for gene in genes:
    cols = list(clinical.columns)
    omics_gene = gene

    clinical_and_protein = lu.join_metadata_to_omics(metadata_df_name="clinical",
                                                 omics_df_name="proteomics",
                                                 metadata_cols=cols,
                                                 omics_genes=omics_gene,
                                                 quiet=True)

    clinical_and_protein = ut.reduce_multiindex(clinical_and_protein,
                                                levels_to_drop="Database_ID")

    follow_up = follow_up.rename({'PPID' : 'Patient_ID'}, axis='columns')
    clin_prot_follow = pd.merge(clinical_and_protein, follow_up, on = "Patient_ID")

    columns_to_focus_on = ['Vital Status',
                           'Path Diag to Last Contact(Day)',
                           'Path Diag to Death(days)']

    omics_gene += '_proteomics'
    columns_to_focus_on.append(omics_gene)

    focus_group = clin_prot_follow[columns_to_focus_on].copy()

    focus_group = focus_group.copy()

    focus_group['Vital Status'] = focus_group['Vital Status'].replace('Living', False)
    focus_group['Vital Status'] = focus_group['Vital Status'].replace('Deceased', True)
    focus_group['Vital Status'] = focus_group['Vital Status'].astype('bool')

    cols = ['Path Diag to Last Contact(Day)','Path Diag to Death(days)']
    focus_group = focus_group.assign(Days_Until_Last_Contact_Or_Death=focus_group[cols].sum(1)).drop(cols, 1)

    # if focus_group[omics_gene] == 'nan' :
    #     print(omics_gene +' data lost')
    #     continue
    # else:
    lower_25_filter = focus_group[omics_gene] <= focus_group[omics_gene].quantile(.25)
    upper_25_filter = focus_group[omics_gene] >= focus_group[omics_gene].quantile(.75)

    focus_group[omics_gene] = np.where(lower_25_filter, "Lower_25%", focus_group[omics_gene])
    focus_group[omics_gene] = np.where(upper_25_filter, "Upper_75%", focus_group[omics_gene])
    focus_group[omics_gene] = np.where(~lower_25_filter & ~upper_25_filter, "Middle_50%", focus_group[omics_gene])
    df_clean = focus_group.dropna(axis=0, how='any').copy()


    kmf = KaplanMeierFitter()
    T = df_clean['Days_Until_Last_Contact_Or_Death']
    E = df_clean['Vital Status']
    groups = df_clean[omics_gene]
    ix = (groups == 'Lower_25%')
    kmf.fit(T[~ix], E[~ix], label='Upper_75%')
    ax = kmf.plot_survival_function(loc=slice(0.,1100.))

    kmf.fit(T[ix], E[ix], label='Lower_25%')
    ax = kmf.plot_survival_function(ax=ax,loc=slice(0.,1100.))
    # results = multivariate_logrank_test(df_clean['Days_Until_Last_Contact_Or_Death'], df_clean[omics_gene], df_clean['Vital Status'])
    # print(omics_gene,'_',results.p_value)
    ax.get_figure().savefig(omics_gene)
    plt.clf()