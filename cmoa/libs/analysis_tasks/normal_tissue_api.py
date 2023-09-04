import requests
import json
import matplotlib.pyplot as plt

url='https://gtexportal.org/api/v2/expression/medianGeneExpression'
parms={
    "gencodeId":["ENSG00000132432.13"],
    "tissueSiteDetailId":["Adipose_Subcutaneous", "Adipose_Visceral_Omentum", "Adrenal_Gland" ,"Artery_Aorta", "Artery_Coronary", "Artery_Tibial" ,
                          "Bladder" ,"Brain_Amygdala", "Brain_Anterior_cingulate_cortex_BA24", "Brain_Caudate_basal_ganglia",
                          "Brain_Cerebellar_Hemisphere", "Brain_Cerebellum" ,"Brain_Cortex" ,"Brain_Frontal_Cortex_BA9",
                          "Brain_Hippocampus" ,"Brain_Hypothalamus" ,"Brain_Nucleus_accumbens_basal_ganglia",
                          "Brain_Putamen_basal_ganglia", "Brain_Spinal_cord_cervical_c-1" ,"Brain_Substantia_nigra",
                          "Breast_Mammary_Tissue", "Cells_Cultured_fibroblasts" ,"Cells_EBV-transformed_lymphocytes",
                          "Cells_Transformed_fibroblasts", "Cervix_Ectocervix" ,"Cervix_Endocervix" ,"Colon_Sigmoid",
                          "Colon_Transverse" ,"Esophagus_Gastroesophageal_Junction" ,"Esophagus_Mucosa", "Esophagus_Muscularis" ,
                          "Fallopian_Tube", "Heart_Atrial_Appendage" ,"Heart_Left_Ventricle", "Kidney_Cortex","Kidney_Medulla",
                          "Liver" ,"Lung" ,"Minor_Salivary_Gland", "Muscle_Skeletal" ,"Nerve_Tibial" ,"Ovary" ,"Pancreas",
                          "Pituitary" ,"Prostate", "Skin_Not_Sun_Exposed_Suprapubic", "Skin_Sun_Exposed_Lower_leg" ,
                          "Small_Intestine_Terminal_Ileum", "Spleen", "Stomach" ,"Testis" ,"Thyroid" ,"Uterus" ,"Vagina",
                          "Whole_Blood"]
}
x=requests.get(url,params=parms)
print (x.text)
# 使用 json.loads() 将 JSON 字符串转换为 Python 对象

x_python=json.loads(x.text)
data = x_python['data']

# 输出转换后的 Python 对象
print(x_python)
print(data)
organs = [entry['tissueSiteDetailId'] for entry in data]
values = [entry['median'] for entry in data]

# 创建一个新的画布
plt.figure(figsize=(10, 6))

# 绘制条形图
plt.bar(organs, values, color='#FF5733')

# 添加标签和标题
plt.xlabel('Organ')
plt.ylabel('Median Value')
plt.title('Median Values of Organs')

# 旋转横坐标标签以避免重叠
plt.xticks(rotation=90)

# 显示图表
plt.tight_layout()
plt.show()












