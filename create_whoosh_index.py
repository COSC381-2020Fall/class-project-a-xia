import os
import sys
import json

from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID
from whoosh.analysis import StemmingAnalyzer

# three fields: youtube id, video title, video description
stem_analyzer = StemmingAnalyzer()
schema = Schema(id=ID(stored=True), title=TEXT(stored=True), description=TEXT(analyzer=stem_analyzer, stored=True))

# create a folder to store index
if not os.path.exists("indexdir"):
    os.mkdir("indexdir")

# create index writer
ix = create_in("indexdir", schema)
writer = ix.writer()

with open('data_for_indexing.json') as f:
    youtube_array = json.load(f)
    for item in youtube_array:
        writer.add_document(id=item['id'], title=item['title'], description=item['description'])

writer.commit()
