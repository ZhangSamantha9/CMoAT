import cptac
import cptac.utils as ut
cptac.download(dataset="Luad",version="latest")
cptac.download(dataset="endometrial",version="latest")
cptac.download(dataset="Ccrcc",version="latest")
cptac.download(dataset="Brca",version="latest")
cptac.download(dataset="Colon",version="latest")
cptac.download(dataset="Gbm",version="latest")
cptac.download(dataset="Hnscc",version="latest")
cptac.download(dataset="Lscc",version="latest")
cptac.download(dataset="Ovarian",version="latest")
cptac.download(dataset="Pdac",version="latest")


def check(cancer):
    clinical = cancer.get_clinical()
    if 'Sample_Tumor_Normal' in clinical.columns:
        print(cancer.__class__.__name__)
    else:
        print(cancer.__class__.__name__,"false")

check(cptac.Luad())
check(cptac.Endometrial())
check(cptac.Ccrcc())
check(cptac.Brca())
check(cptac.Colon())
check(cptac.Gbm())
check(cptac.Hnscc())
check(cptac.Lscc())
check(cptac.Ovarian())
check(cptac.Pdac())
