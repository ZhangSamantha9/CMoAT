import argparse

def list_datasets():
    """List all available datasets."""

    dataset_list_url = "https://byu.box.com/shared/static/5vwsvgu8fyzao0pb7rx8lt26huofcdax.tsv"

    try:
        dataset_list_text = _download_text(dataset_list_url)
    except NoInternetError:
        raise NoInternetError("Insufficient internet to download available dataset info. Check your internet connection.") from None

    return pd.read_csv(io.StringIO(dataset_list_text), sep="\t", index_col=0)




parser = argparse.ArgumentParser(description='Calculate two gene correlation')  # 创建一个解析对象
parser.add_argument('gene_1', type=str, help='gene_1')  # 向该对象中添加你要关注的命令行参数和选项
parser.add_argument('gene_2', type=str, help='gene_2')
args = parser.parse_args()

def log1():
    print(1)

def log2():
    print(2)

name = 'log1'

locals()[name]()