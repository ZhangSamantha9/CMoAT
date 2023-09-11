import argparse
import cmoa.argument_parser.single_analyse as single_analyse
import cmoa.argument_parser.GUI as GUI

# CLI example: python -m cmoa -ca Luad EGFR MET

parser = argparse.ArgumentParser(description='CMOA Cli')
parser.add_argument('-m', '--mode', type=str, default='single',
                    choices=['single', 'batch', 'GUI'], help='single_cli, batch_cli or gui')
exclusive_group = parser.add_mutually_exclusive_group()

exclusive_group.add_argument(
    '-ca',
    '--correlation',
    nargs=3, metavar=('cancer_name', 'gene1', 'gene2'),
    help='Gene corralation analysis, args: [cancer_name] [gene1] [gene2] e.g. --ca Luad EGFR MET'
)
exclusive_group.add_argument(
    '-bp', '--boxplot', nargs=2, metavar=('cancer_name', 'gene'), help='')
exclusive_group.add_argument(
    '-nt', '--normaltissue', nargs='+', metavar=('geneids'), help='')
exclusive_group.add_argument(
    '-sa', '--survival', nargs=2, metavar=('cancer_name', 'gene'), help='')
exclusive_group.add_argument(
    '-dsa', '--dualsurvival', nargs=3, metavar=('cancer_name', 'gene1', 'gene2'), help='')

args = parser.parse_args()

if args.mode == 'single':
    if args.correlation:
        cancer_name, gene1, gene2 = args.correlation
        single_analyse.correlation_analysis(cancer_name, gene1, gene2)
    if args.boxplot:
        cancer_name, gene = args.boxplot
        single_analyse.expression_boxplot_analysis(cancer_name, gene)
    if args.normaltissue:
        geneids = args.normaltissue
        single_analyse.normal_tissue_analysis(geneids)
    if args.survival:
        cancer_name, gene = args.survival
        single_analyse.survival_analysis(cancer_name, gene)
    if args.dualsurvival:
        cancer_name, gene1, gene2 = args.dualsurvival
        single_analyse.dual_survival_analysis(cancer_name, gene1, gene2)

elif args.mode == 'GUI':
    GUI.show_window()
