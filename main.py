# import cptac
import correlation_analysis

# import argparse
#
#
# parser = argparse.ArgumentParser(description='Calculate two gene correlation')
# parser.add_argument('cancer_name', type=str, help='Choose from: Brca,Ccrcc,Colon,Endometrial,Gbm,Hnscc,Lscc,Luad,Ovarian,Pdac,UcecConf,GbmConf')
# parser.add_argument('gene_1', type=str, help='gene 1')  # 向该对象中添加你要关注的命令行参数和选项
# parser.add_argument('gene_2', type=str, help='gene 2')
# args = parser.parse_args()
#
# cancername = args.cancer_name
# gene1 = args.gene_1
# gene2 = args.gene_2

# correlation_analysis.analysis(cancername,gene1,gene2)

# correlation_analysis.analysis("Luad","EGFR","MET")

correlation_analysis.user_cancername("Endometrial")