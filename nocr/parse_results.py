import pandas as pd
from pandas.io.json import json_normalize
import sys
import json
from pathlib import Path

# Put the incoming FlowFile into a dataframe
flowFile = sys.stdin.read()
data = json.loads(flowFile)
df = json_normalize(data)

# Check for previous output and append to it or create a new output file
results_file = Path('/data/fast/hortonworks/PDF-Data-Extraction/output/results.csv')
if results_file.is_file():
    results = pd.read_csv('/data/fast/hortonworks/PDF-Data-Extraction/output/results.csv')
    results = results.append(df)
else:
    results = df

results.to_csv(sys.stdout, index=False)