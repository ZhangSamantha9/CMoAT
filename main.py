import argparse
import cptac


parser = argparse.ArgumentParser(description='Calculate two gene correlation')
parser.add_argument('cancer_name', type=str, help='Choose from: Brca,Ccrcc,Colon,Endometrial,Gbm,Hnscc,Lscc,Luad,Ovarian,Pdac,UcecConf,GbmConf')
parser.add_argument('gene_1', type=str, help='gene 1')  # 向该对象中添加你要关注的命令行参数和选项
parser.add_argument('gene_2', type=str, help='gene 2')
args = parser.parse_args()

def input_cancer(cancer_name):
    cancer = cancer_name
    return cancer
locals()[input_cancer()]()
 #uhdihf
def log1():
    print(1)

def log2():
    print(2)

name = 'log1'

locals()[name]()