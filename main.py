import cptac
import cptac.utils as ut
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('agg')
import seaborn as sns

en = cptac.Endometrial()
proteomics = pd.DataFrame(en.get_proteomics())
tumorProt = pd.DataFrame(en.join_metadata_to_omics(metadata_df_name="clinical", omics_df_name="proteomics",
                                      metadata_cols='Proteomics_Tumor_Normal'))
tumor_pro_data = tumorProt[tumorProt.Proteomics_Tumor_Normal == 'Tumor']
gene_cor1=tumor_pro_data.A1BG_proteomics
gene_cor2=tumor_pro_data.EGFR_proteomics
sns.set(style="darkgrid")
plot = sns.regplot(x=gene_cor1, y=gene_cor2)
plot.set(xlabel='A1BG', ylabel='EGFR',
         title='gene correlation for the A1BG&EGFR gene')
matplotlib.pyplot.savefig('gene_correlation')
print("done")