import argparse
import argument_parser.single_analyse as single_analyse

# Single example: Luad EGFR MET

parser = argparse.ArgumentParser(description='CMOA Cli')
parser.add_argument('-m', '--mode', type=str, default='single', choices=['single', 'batch', 'GUI'], help='single_cli, batch_cli or gui')
exclusive_group = parser.add_mutually_exclusive_group()

exclusive_group.add_argument('--ca', nargs=3, metavar=('cancer_name', 'gene1', 'gene2'), help='Gene corralation analysis, args: [cancer_name] [gene1] [gene2] e.g. --ca Luad EGFR MET')

args = parser.parse_args()

if args.mode == 'single':
    if args.ca:
        cancer_name, gene1, gene2 = args.ca
        single_analyse.correlation_analysis(cancer_name, gene1, gene2)

# parser.add_argument('cancer_name', type=str, help='Choose from: Brca,Ccrcc,Colon,Endometrial,Gbm,Hnscc,Lscc,Luad,Ovarian,Pdac,UcecConf,GbmConf')
# parser.add_argument('gene_1', type=str, help='gene 1')  # 向该对象中添加你要关注的命令行参数和选项
# parser.add_argument('gene_2', type=str, help='gene 2')
# parser.add_argument('-m', '--mode', type=str, default='single', help='single or multiple')

# args = parser.parse_args()

# cancer_name = args.cancer_name
# gene1 = args.gene_1
# gene2 = args.gene_2

# cancer_data = cptac_data.load_dataset(cancer_name)
# if cancer_data:
#     tumor_data = correlation_analysis.dataset_preprocess(cancer_data)
#     correlation_analysis.draw_correlation_curve(gene1,gene2,tumor_data)