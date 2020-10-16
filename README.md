# Class Project
## Setup
1. Install necessary Python packages: `python3 -m pip install -r requirements.txt`
2. In config.py:
    - Replace `YOUR API KEY` with your own API key.
    - If you want to use a different search engine, replace the current `cse_id` with another id.
## Obtaining search results
1. Run cse.py with your search term: `python3 cse.py "SEARCH TERM"`.
2. This will create the file google_search.json containing 100 search results.
## Creating a Whoosh index
1. If you have your own list of video ids, replace the contents of the video_ids.txt file. Make sure each id is on its own line.
2. Run: `bash download_youtube_data_batch.sh`. You should now have a directory named youtube_data containing several json files.
3. Run: `python3 create_data_for_indexing.py`. You should now have the file data_for_indexing.json.
4. Run: `python3 create_whoosh_index.py`. This creates the Whoosh index in the directory indexdir.
## Searching the Whoosh index
1. Run query_on_whoosh.py with your search term: `python3 query_on_whoosh.py "SEARCH TERM"`.
2. This gives you the titles of the first 10 videos that have your search term in the video description.
    - If you are using the provided video id list, try searching `imposter` or `crew`.