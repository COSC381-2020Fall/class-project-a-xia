from pathlib import Path
import json

paths = [str(x) for x in Path('./youtube_data3').glob('**/*.json')]
results = []
for path in paths:
    with open(path, 'r') as f:
        data = json.load(f)
        
        if data: # if data is not empty
            info = {
                'id': data[0]['id'],
                'title': data[0]['snippet']['title'],
                'description': data[0]['snippet']['description'],
                'topic': 'Antichamber'
            }
            
            results.append(info)

with open('data_for_indexing3.json', 'w') as dump_file:
    json.dump(results, dump_file)

