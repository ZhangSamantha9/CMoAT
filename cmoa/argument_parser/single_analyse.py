from cmoa.libs import cptac_data as cd
from cmoa.libs import correlation_analysis as ca
from typing import Optional

from cmoa.libs.analysis_tasks.correlation_analysis_task import CorrelationAnalysisTask
from cmoa.libs.analysis_tasks.expression_boxplot_task import ExpressionBoxplotTask
from cmoa.libs.analysis_tasks.survival_plot import SurvivalAnalysisTask

def correlation_analysis(cancer_name: str, gene1: str, gene2: str) -> Optional[str]:
    try:
        task = CorrelationAnalysisTask(cancer_name, gene1, gene2)
        return task.run_task()
    except Exception:
        return None

def expression_boxplot_analysis(cancer_name: str, gene: str) -> Optional[str]:
    try:
        task = ExpressionBoxplotTask(cancer_name, gene)
        return task.run_task()
    except Exception:
        return None

def survival_analysis(cancer_name: str, gene: str) -> Optional[str]:
    try:
        task = SurvivalAnalysisTask(cancer_name, gene)
        return task.run_task()
    except Exception:
        return None

