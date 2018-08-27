import sys
import json
import re

# Put the incoming FlowFile into a dataframe
flowFile = sys.stdin.read()
data = json.loads(flowFile)

attlist = ['citizen', 'alien', 'national', 'resident']
for answer in attlist:
    if bool(re.search(r'^X', data[answer])):
        data['Attestation'] = answer
    del data[answer]

data = json.dumps(data)
sys.stdout.write(data)
