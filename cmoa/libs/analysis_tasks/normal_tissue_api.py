import requests
import json

url='https://gtexportal.org/api/v2/expression/medianGeneExpression'
parms={
    "gencodeId":["ENSG00000146648.15","ENSG00000132432.13","ENSG00000132434.9"],
    "tissueSiteDetailId":['Adipose_Subcutaneous', 'Adipose_Visceral_Omentum', 'Adrenal_Gland', 'Artery_Aorta']
}
x=requests.get(url,params=parms)
print (x.text)