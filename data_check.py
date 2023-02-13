import cptac
import cptac.utils as ut


def check(cancer):
    clinical = cancer.get_clinical()
    print(cancer.__class__.__name__)

check(cptac.Luad())