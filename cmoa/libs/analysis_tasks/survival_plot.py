import os

import pandas as pd
import cptac
import cptac.utils as ut
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from lifelines import KaplanMeierFitter

from cmoa.libs import cptac_data as cd
from .analysis_task_base import AnalysisTaskBase, PreprocessError, ProcessError

class SurvivalAnalysisTask(AnalysisTaskBase):

    def __init__(self, cancer: str, gene: str) -> None:
        super().__init__()
        self.cancer_name = cancer
        self.gene_name = gene
