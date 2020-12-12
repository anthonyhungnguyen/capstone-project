import pickle
import json

with open('mappingNameToId.json') as mappingFile:
    mappingNameToId = json.load(mappingFile)
print(mappingNameToId)
