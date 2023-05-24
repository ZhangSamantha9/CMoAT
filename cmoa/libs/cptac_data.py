import cptac
from typing import Optional

from cptac import dataset

CANCER_DATASET_DIC = {
    'Luad': cptac.Luad,
    'Endometrial': cptac.Endometrial,
    'Brca': cptac.Brca,
    'Ccrcc': cptac.Ccrcc,
    'Colon': cptac.Colon,
    'Gbm': cptac.Gbm,
    'Hnscc': cptac.Hnscc,
    'Lscc': cptac.Lscc,
    'Ovarian': cptac.Ovarian,
    'Pdac': cptac.Pdac,
    'UcecConf': cptac.UcecConf,
    'GbmConf': cptac.GbmConf
}

def load_dataset(cancer_name) -> Optional[dataset.Dataset]:
    print(f'loading {cancer_name} data')

    if CANCER_DATASET_DIC.__contains__(cancer_name):
        cptac.download(dataset=cancer_name, version='latest')
        return CANCER_DATASET_DIC[cancer_name]()
    else:
        return None