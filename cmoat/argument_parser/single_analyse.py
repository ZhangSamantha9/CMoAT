from cmoat.libs import cptac_data as cd
from typing import Optional

from cmoat.libs.analysis_tasks.correlation_curve_task import CorrelationAnalysisAllCancerTask
from cmoat.libs.analysis_tasks.expression_boxplot_task import ExpressionBoxplotTask
from cmoat.libs.analysis_tasks.survival_analysis_task import SurvivalAnalysisTask
from cmoat.libs.analysis_tasks.dual_positive_survival_task import DualSurvivalAnalysisTask
from cmoat.libs.analysis_tasks.normal_tissue_task import NormalTissueTask


def correlation_analysis(cancer_name: str, gene1: str, gene2: str) -> Optional[str]:
    task = CorrelationAnalysisAllCancerTask(cancer_name, gene1, gene2)
    return task.run_task()


def expression_boxplot_analysis(cancer_name: str, gene: str) -> Optional[str]:
    task = ExpressionBoxplotTask(cancer_name, gene)
    return task.run_task()


def normal_tissue_analysis(geneIds: list[str]) -> Optional[str]:
    task = NormalTissueTask(geneIds)
    return task.run_task()


def survival_analysis(cancer_name: str, gene: str) -> Optional[str]:
    task = SurvivalAnalysisTask(cancer_name, gene)
    return task.run_task()


def dual_survival_analysis(cancer_name: str, gene1: str, gene2: str) -> Optional[str]:
    task = DualSurvivalAnalysisTask(cancer_name, gene1, gene2)
    return task.run_task()
