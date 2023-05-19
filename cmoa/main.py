import argparse
import libs.correlation_analysis as correlation_analysis
import libs.cptac_data as cptac_data

parser = argparse.ArgumentParser(description='Calculate two gene correlation')
parser.add_argument('cancer_name', type=str, help='Choose from: Brca,Ccrcc,Colon,Endometrial,Gbm,Hnscc,Lscc,Luad,Ovarian,Pdac,UcecConf,GbmConf')
parser.add_argument('gene_1', type=str, help='gene 1')  # 向该对象中添加你要关注的命令行参数和选项
parser.add_argument('gene_2', type=str, help='gene 2')
args = parser.parse_args()

cancer_name = args.cancer_name
gene1 = args.gene_1
gene2 = args.gene_2

# tumor_data = correlation_analysis.get_cancer_data("Luad")
# correlation_analysis.gene_correlation_curve('EGFR', 'MET', tumor_data)

cancer_data = cptac_data.load_dataset(cancer_name)
if cancer_data:
    tumor_data = correlation_analysis.dataset_preprocess(cancer_data)
    correlation_analysis.draw_correlation_curve(gene1,gene2,tumor_data)