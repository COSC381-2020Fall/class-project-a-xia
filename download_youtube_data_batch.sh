#! /usr/bin/bash

if [ ! -e youtube_data3 ]; then
	mkdir youtube_data3
fi

cd youtube_data3

while read line
do
	python3 ../download_youtube_data.py $line
done < ../video_ids3.txt

