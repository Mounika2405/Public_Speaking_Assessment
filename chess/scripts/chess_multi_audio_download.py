import multiprocessing as mp
from concurrent.futures import ThreadPoolExecutor, as_completed
from os import listdir, path
import numpy as np
import argparse, os
import csv
import subprocess
import sys
import time
from tqdm import tqdm
import pandas as pd
import os

def yt_download(d, args):
	# print('in yt_download')
	yid = d
	# print('yid is', yid)
	aud_path = path.join(args.output_dir, yid)
	# print("Audio path: ", aud_path)

	# class_label = d[1][1]
	# # print("Class label: ", class_label)
	# skip_list = ["female speech", "woman speaking", "female singing", "male speech", "man speaking", "male singing"]

	# for i in range(len(skip_list)):
	# 	if skip_list[i] in class_label:
	# 		print("Skipping: ", yid)
	# 		return

	# print("Start Downloading ",yid)
	cmd = 'youtube-dl --extract-audio --audio-format mp3 --no-progress --match-filter "duration > 300" \
				-g "https://www.youtube.com/watch?v={}"'.format(yid)	
	# print('url', url)
	# url = subprocess.call(cmd, shell=True)
	url = os.popen(cmd).read()
	url = url[:-1]
	# start = 00:00:00
	# end = 00:05

	# command = 'ffmpeg -ss {} -to {} -i {} -c:a aac {}'.format(\
	# 			start, end, aud_path+'.mp3', aud_path+'.aac')	
	
	#command = 'ffmpeg -re -ss 00:00:00 -t 00:05:00 -i {} {}'.format('"'+url+'"', '"' + aud_path+'.mp3' + '"')
	command = 'ffmpeg -loglevel panic -ss 00:00:00 -t 00:05:00 -i "' + url + '"' + ' ' + '"' +  aud_path + '.mp3' + '"'
	os.system(command)
	# print("Completed extracting 10 secs audio ")
	# print("-----------------------------------------------------")

def preprocess(args):

	data = {}
	yid = []

	# with open(args.file) as f:
	# 	csv_data = csv.reader(f, delimiter=",")
	csv_data = pd.read_csv(args.file)

	for i, row in csv_data.iterrows():
		yid.append(row['videoid'])
		# if yid in data:
		# 	data[yid].append(row[1:])
		# else:
		# 	data[yid] = row[1:]

	if not path.isdir(args.output_dir):
		os.mkdir(args.output_dir)


	return yid


if __name__ == '__main__':


	parser = argparse.ArgumentParser()
	parser.add_argument('-j', '--jobs', help='Number of jobs to run in parallel', default=20, type=int)
	parser.add_argument('-f', '--file', help='CSV file containing data', required=True)
	parser.add_argument('-o', '--output_dir', help="Folder where final videos will be downloaded", required=True)
	args = parser.parse_args()

	data = preprocess(args)

	p = ThreadPoolExecutor(args.jobs)
	print('starting...')
	# print('data.items', data.items())
	threads = [p.submit(yt_download,row,args) for row in data]
	_ = [r.result() for r in tqdm(as_completed(threads), total=len(threads))]
