import cptac
from typing import Optional

from cptac.cancers.cancer import Cancer


CANCER_DATASET_DIC = {
    'Luad': cptac.Luad,
    # 'Endometrial': cptac.Endometrial,
    'Brca': cptac.Brca,
    'Ccrcc': cptac.Ccrcc,
    'Coad': cptac.Coad,
    'Gbm': cptac.Gbm,
    'Hnscc': cptac.Hnscc,
    'Lscc': cptac.Lscc,
    'Ov': cptac.Ov,
    'Pdac': cptac.Pdac,
    'Ucec': cptac.Ucec,
    # 'GbmConf': cptac.GbmConf
}

# {
#     # 'brca': 'Breast invasive carcinoma',
#     # 'ccrcc': 'Clear cell renal cell carcinoma',
#     # 'coad': 'Colon adenocarcinoma',
#     # 'gbm': 'Glioblastoma multiforme',
#     # 'hnscc': 'Head and Neck squamous cell carcinoma',
#     # 'lscc': 'Lung squamous cell carcinoma',
#     # 'luad': 'Lung adenocarcinoma',
#     # 'ov': 'Ovarian serous cystadenocarcinoma',
#     'pda': 'Pancreatic ductal adenocarcinoma',
#     # 'pdac': 'Pancreatic ductal adenocarcinoma',
#     # 'ucec': 'Uterine Corpus Endometrial Carcinoma'
# }


def load_dataset(cancer_name) -> Optional[Cancer]:
    print(f'loading {cancer_name} data')

    if CANCER_DATASET_DIC.__contains__(cancer_name):
        # cptac.download(dataset=cancer_name, version='latest')
        return CANCER_DATASET_DIC[cancer_name]()
    else:
        return None
