import cptac
df=cptac.list_datasets()
print(df[['Description']])


import cptac.utils as ut
cptac.download(dataset="Luad",version="latest")