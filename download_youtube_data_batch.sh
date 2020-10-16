#! /usr/bin/bash

if [ ! -e youtube_data ]; then
	mkdir youtube_data
fi

cd youtube_data

while read line
do
	python3 ../download_youtube_data.py $line
done < ../video_ids.txt

