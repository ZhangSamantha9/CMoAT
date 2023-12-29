from cmoa.libs import cptac_data as cd
from typing import Optional

from cmoa.libs.analysis_tasks.correlation_analysis_task import CorrelationAnalysisTask
from cmoa.libs.analysis_tasks.expression_boxplot_task import ExpressionBoxplotTask
from cmoa.libs.analysis_tasks.survival_analysis_task import SurvivalAnalysisTask
from cmoa.libs.analysis_tasks.dual_positive_survival_task import DualSurvivalAnalysisTask
from cmoa.libs.analysis_tasks.normal_tissue_task import NormalTissueTask
from cmoa.libs.analysis_tasks.correlation_heatmap_task import CorrelationHeatmapTask


def correlation_analysis(cancer_name: str, gene1: str, gene2: str) -> Optional[str]:
    task = CorrelationAnalysisTask(cancer_name, gene1, gene2)
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


def correlation_heatmap(cancer_name: str, gene1: str, gene2: str,gene3:str, gene4:str, gene5:str, gene6:str, gene7:str) -> Optional[str]:
    task = CorrelationHeatmapTask(cancer_name, gene1, gene2,gene3, gene4, gene5, gene6, gene7)
    return task.run_task()
