import sys
import json

from whoosh.qparser import QueryParser
from whoosh import scoring
from whoosh.query import Term
from whoosh.index import open_dir
from whoosh.lang.porter import stem

ix = open_dir("indexdirectory")

def query(query_str, topic, items_per_page=10, current_page=1):
    query_str = stem(query_str)
    with ix.searcher(weighting=scoring.Frequency) as searcher:
        qp = QueryParser("description", ix.schema).parse(query_str)
        allow_topic = Term("topic", topic)
        results = searcher.search(qp, filter=allow_topic, limit=None)
        num_query_results = len(results)
        query_results = []
        start_index = (current_page -1) * items_per_page
        end_index = start_index + items_per_page

        for i in range(start_index, min(len(results), end_index)):
            d = {}
            d['url'] = "https://www.youtube.com/watch?v=%s" % results[i]['id']
            d['title'] = results[i]['title']
            d['description'] = results[i]['description']
            d['topic'] = results[i]['topic']
            d['score'] = results[i].score
            query_results.append(d)
    
    return query_results, num_query_results

if __name__ == "__main__":
    query_str = sys.argv[1]
    items_per_page = int(sys.argv[2])
    current_page = int(sys.argv[3])
    topic = sys.argv[4]
    query_results, num_query_results = query(query_str, topic, items_per_page=items_per_page, current_page=current_page)
    print(json.dumps(query_results))