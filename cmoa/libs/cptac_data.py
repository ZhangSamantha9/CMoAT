import cptac
from typing import Optional

from cptac.cancers.cancer import Cancer


CANCER_DATASET_DIC = {
    'Luad': cptac.Luad,
    # 'Endometrial': cptac.Endometrial, removed at cptac 1.5.5
    'Brca': cptac.Brca,
    'Ccrcc': cptac.Ccrcc,
    'Coad': cptac.Coad,
    'Gbm': cptac.Gbm,
    'Hnscc': cptac.Hnscc,
    'Lscc': cptac.Lscc,
    'Ov': cptac.Ov,
    'Pdac': cptac.Pdac,
    'Ucec': cptac.Ucec,
    # 'GbmConf': cptac.GbmConf, removed at cptac 1.5.5
}

def load_cancer(cancer_name) -> Optional[Cancer]:
    print(f'loading {cancer_name} data')

    if CANCER_DATASET_DIC.__contains__(cancer_name):
        return CANCER_DATASET_DIC[cancer_name]()
    else:
        return None
