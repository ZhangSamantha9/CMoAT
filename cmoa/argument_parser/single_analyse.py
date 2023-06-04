from cmoa.libs import cptac_data as cd
from cmoa.libs import correlation_analysis as ca
from typing import Optional

from cmoa.libs.analysis_tasks.correlation_analysis_task import CorrelationAnalysisTask

def correlation_analysis(cancer_name: str, gene1: str, gene2: str) -> Optional[str]:
    cancer_data = cd.load_dataset(cancer_name)
    if cancer_data:
        # tumor_data = ca.dataset_preprocess(cancer_data)
        # return ca.draw_correlation_curve(gene1, gene2, tumor_data)
        task = CorrelationAnalysisTask(cancer_name, gene1, gene2)
        return task.run_task()
    else:
        print(f'Load dataset {cancer_name} failed.')