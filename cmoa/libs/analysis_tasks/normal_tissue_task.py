import os
import json

import requests
import matplotlib
import matplotlib.pyplot as plt

from .analysis_task_base import AnalysisTaskBase, PreprocessError, ProcessError


class NormalTissueTask(AnalysisTaskBase):

    url: str = 'https://gtexportal.org/api/v2/expression/medianGeneExpression'

    @property
    def params(self) -> dict[str, list[str]]:
        return {
            "gencodeId": self.genecodeIds,
            "tissueSiteDetailId": ["Adipose_Subcutaneous", "Adipose_Visceral_Omentum", "Adrenal_Gland", "Artery_Aorta", "Artery_Coronary", "Artery_Tibial",
                                   "Bladder", "Brain_Amygdala", "Brain_Anterior_cingulate_cortex_BA24", "Brain_Caudate_basal_ganglia",
                                   "Brain_Cerebellar_Hemisphere", "Brain_Cerebellum", "Brain_Cortex", "Brain_Frontal_Cortex_BA9",
                                   "Brain_Hippocampus", "Brain_Hypothalamus", "Brain_Nucleus_accumbens_basal_ganglia",
                                   "Brain_Putamen_basal_ganglia", "Brain_Spinal_cord_cervical_c-1", "Brain_Substantia_nigra",
                                   "Breast_Mammary_Tissue", "Cells_Cultured_fibroblasts", "Cells_EBV-transformed_lymphocytes",
                                   "Cells_Transformed_fibroblasts", "Cervix_Ectocervix", "Cervix_Endocervix", "Colon_Sigmoid",
                                   "Colon_Transverse", "Esophagus_Gastroesophageal_Junction", "Esophagus_Mucosa", "Esophagus_Muscularis",
                                   "Fallopian_Tube", "Heart_Atrial_Appendage", "Heart_Left_Ventricle", "Kidney_Cortex", "Kidney_Medulla",
                                   "Liver", "Lung", "Minor_Salivary_Gland", "Muscle_Skeletal", "Nerve_Tibial", "Ovary", "Pancreas",
                                   "Pituitary", "Prostate", "Skin_Not_Sun_Exposed_Suprapubic", "Skin_Sun_Exposed_Lower_leg",
                                   "Small_Intestine_Terminal_Ileum", "Spleen", "Stomach", "Testis", "Thyroid", "Uterus", "Vagina",
                                   "Whole_Blood"]
        }
    
    @property
    def pretty_geneids(self) -> str:
        return f"[{','.join(self.genecodeIds)}]"
    
    @property
    def result(self):
        return self.figPath

    def __init__(self, genecodeIds: list[str]) -> None:
        super().__init__()
        self.genecodeIds: list[str] = genecodeIds

    def preprocess(self) -> None:
        if len(self.genecodeIds) > 1:
            raise PreprocessError('Gene count is more than 1, multiply gene is not supported yet.')

        api_rsp = requests.get(NormalTissueTask.url, params=self.params)
        self.data = json.loads(api_rsp.text)['data']

    def process(self) -> None:
        matplotlib.use('Agg')

        # 输出转换后的 Python 对象
        # print(x_python)
        # print(data)
        organs = [entry['tissueSiteDetailId'] for entry in self.data]
        values = [entry['median'] for entry in self.data]

        # 创建一个新的画布
        plt.figure(figsize=(10, 6))

        # 绘制条形图
        plt.bar(organs, values, color='#FF5733')

        # 添加标签和标题
        plt.xlabel('Organ')
        plt.ylabel('Median Value')
        plt.title(f'Median Values of Organs. Gene: {self.pretty_geneids}')

        # 旋转横坐标标签以避免重叠
        plt.xticks(rotation=90)

        # 保存图表
        plt.tight_layout()
        self.figPath = os.path.join(os.getcwd(), f'normal_tissue_{self.genecodeIds[0]}.png')
        plt.savefig(self.figPath)

# test

if __name__ == '__main__':
    task = NormalTissueTask(['ENSG00000132432.13'])
    task.run_task()
    print(task.result)
