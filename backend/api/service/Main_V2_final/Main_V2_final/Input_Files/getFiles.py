import os
import pandas as pd

path = os.path.dirname(os.path.realpath(__file__))
def getFileByName(folder, fileName):
    return pd.read_csv(os.path.join(path, folder, fileName))

def getMappingFileByName(fileName):
    return pd.read_csv(os.path.join(path, "Mapping Tables", fileName))

def getRegulatoryFileByName(fileName):
    return pd.read_csv(os.path.join(path, "Regulatory Tables", fileName))
