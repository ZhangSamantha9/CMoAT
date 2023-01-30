import argparse
import sys
sys.path.append('C:\\Users\\126614\\AppData\\Roaming\\Python\\Python311\\site-packages\\pandas')
import pandas as pd


cancer_list = pd.read_csv('C:\\Users\\126614\\downloads\\datasets.csv')
cancer_list= pd.DataFrame(cancer_list)
print(cancer_list[['Dataset name','Description']])

parser = argparse.ArgumentParser(description='Calculate two gene correlation')
parser.add_argument('cancer name', type=str, help='')
parser.add_argument('gene_1', type=str, help='gene 1')  # 向该对象中添加你要关注的命令行参数和选项
parser.add_argument('gene_2', type=str, help='gene 2')
args = parser.parse_args()

def log1():
    print(1)

def log2():
    print(2)

name = 'log1'

locals()[name]()