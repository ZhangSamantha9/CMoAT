import matplotlib.pyplot as plt
import numpy as np
import requests

from dataclasses import dataclass

@dataclass
class BoxPlotData(object):
    low_bound: float
    q1: float
    median: float
    q3: float
    high_bound: float
    outliers: list[float]

@dataclass
class Disease(object):
    normal: BoxPlotData = None
    tumor: BoxPlotData = None

url_tumors = 'http://firebrowse.org/api/v1/Analyses/mRNASeq/Quartiles?format=json&gene=EGFR&protocol=RSEM&sample_type=tumors'
url_normals = 'http://firebrowse.org/api/v1/Analyses/mRNASeq/Quartiles?format=json&gene=EGFR&protocol=RSEM&sample_type=normals'

tumors_response = requests.get(url_tumors)
normals_response = requests.get(url_normals)
tumors_response_data = tumors_response.json()['mRNASeq_Quartiles']
normals_response_data = normals_response.json()['mRNASeq_Quartiles']

all_data: dict[str, Disease] = {}

for data in tumors_response_data:
    name = data['cohort']
    if name not in all_data:
        all_data[name] = Disease(tumor=BoxPlotData(data['low_bound'], data['q1'], data['median'], data['q3'], data['high_bound'], data['outliers']))
    else:
        all_data[name].tumor = BoxPlotData(data['low_bound'], data['q1'], data['median'], data['q3'], data['high_bound'], data['outliers'])

for data in normals_response_data:
    name = data['cohort']
    if name not in all_data:
        all_data[name] = Disease(normal=BoxPlotData(data['low_bound'], data['q1'], data['median'], data['q3'], data['high_bound'], data['outliers']))
    else:
        all_data[name].normal = BoxPlotData(data['low_bound'], data['q1'], data['median'], data['q3'], data['high_bound'], data['outliers'])

normal_boxplot_data = [[data.normal.low_bound, data.normal.q1, data.normal.median, data.normal.q3, data.normal.high_bound] for data in all_data.values() if data.normal is not None]

tumor_plot_data = [[data.tumor.low_bound, data.tumor.q1, data.tumor.median, data.tumor.q3, data.tumor.high_bound] for data in all_data.values() if data.tumor is not None]

normal_boxplot_positions: list[int] = []
tumor_plotbox_positions: list[int] = []
labels = [key for key in all_data.keys()]
labels_positions = [index * 2 + 1.5 for index in range(len(labels))]

for index, (key, value) in enumerate(all_data.items()):
    if value.normal is not None:
        normal_boxplot_positions.append(index * 2 + 1)
    if value.tumor is not None:
        tumor_plotbox_positions.append(index * 2 + 2)

plt.boxplot(tumor_plot_data, positions=tumor_plotbox_positions, showfliers=True, boxprops={'color': 'red'})
plt.boxplot(normal_boxplot_data, positions=normal_boxplot_positions, showfliers=True, boxprops={'color': 'blue'})

plt.xticks(labels_positions, labels, rotation=60)

outlier_x = []
outlier_y = [[]]

for index, (key, value) in enumerate(all_data.items()):
    if value.normal is not None:
        outlier_x.extend([index * 2 + 1] * len(value.normal.outliers))
        outlier_y.append(value.normal.outliers)
    if value.tumor is not None:
        outlier_x.extend([index * 2 + 2] * len(value.tumor.outliers))
        outlier_y.append(value.tumor.outliers)

plt.scatter(outlier_x, np.concatenate(outlier_y), color='grey', s=1)

plt.show()