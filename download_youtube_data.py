import sys
import json
import config

from googleapiclient.discovery import build

my_api_key = config.api_key

def video_data(video_id):
    request = build("youtube", "v3", developerKey=my_api_key)
    res = request.videos().list(part='snippet', id=video_id).execute()
    return res['items']

if __name__ ==  '__main__':
    vid_id = sys.argv[1]
    results = video_data(vid_id)
    file_name = vid_id + '.json'
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)


