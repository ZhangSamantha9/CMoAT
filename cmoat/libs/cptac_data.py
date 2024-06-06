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

CANCER_DF_LABLES: dict[str, str] = {
    'Vital_Status': 'vital_status_at_date_of_last_contact',
    'Days_Until_Last_Contact': 'number_of_days_from_date_of_initial_pathologic_diagnosis_to_date_of_last_contact',
    'Days_Until_Death': 'number_of_days_from_date_of_initial_pathologic_diagnosis_to_date_of_death',
}

def load_cancer(cancer_name) -> Optional[Cancer]:
    print(f'loading {cancer_name} data')

    if CANCER_DATASET_DIC.__contains__(cancer_name):
        return CANCER_DATASET_DIC[cancer_name]()
    else:
        return None
