import os
import cptac.utils as ut
import pandas as pd
import numpy as np
from lifelines import KaplanMeierFitter
from lifelines.statistics import logrank_test

gene1_name = 'MUC1'
gene2_name = 'EGFR'
cancer_name='Ov'

expression_data = 'D:\\doc\\data\\Ov\\OV_tumor.xlsx'  # 替换为你的Excel文件路径
expression_data= pd.read_excel(expression_data)
# 打印DataFrame
expression_data.set_index("patiens", inplace=True)
expression_data=expression_data.T
expression_data = expression_data.replace('NA', float('NaN'))

if gene1_name not in expression_data.columns:
    raise (f'Gene [{gene1_name}] not in dataframe')
if gene2_name not in expression_data.columns:
    raise (f'Gene [{gene2_name}] not in dataframe')
genes_series = expression_data[[gene1_name,gene2_name]]

clinical_data='D:\\doc\\data\\Ov\\OV_tumor.xlsx'
clinical_data=pd.read_excel(clinical_data)
clinical_data.set_index("patiens", inplace=True)

clin_prot_follow= pd.merge(expression_data, clinical_data, on="patiens")


