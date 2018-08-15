import pandas as pd
from pandas.io.json import json_normalize
import sys
import json
from pathlib import Path
import re

# Put the incoming FlowFile into a dataframe
flowFile = sys.stdin.read()
data = json.loads(flowFile)
df = json_normalize(data)

# df = pd.read_csv('/Users/doctor_ew/PycharmProjects/I9PDFExtractor/nocr/results.csv')

attlist = ['citizen', 'alien', 'national', 'resident']
for answer in attlist:
    if bool(re.search(r'^X', df.ix[0, answer])):
        df.ix[0, 'Attestation'] = answer
    df = df.drop(answer, 1)

# Check for previous output and append to it or create a new output file
results_file = Path('/data/fast/hortonworks/I9PDFExtractor/output/results.csv')
if results_file.is_file():
    results = pd.read_csv('/data/fast/hortonworks/I9PDFExtractor/output/results.csv')
    results = results.append(df)
else:
    results = df

results.to_csv(sys.stdout, index=False)
