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


def yt_download(d, args):

	yid = d[0]

	aud_path = path.join(args.output_dir, yid)
	# print("Audio path: ", aud_path)

	class_label = d[1][1]
	# print("Class label: ", class_label)
	skip_list = ["female speech", "woman speaking", "female singing", "male speech", "man speaking", "male singing"]

	for i in range(len(skip_list)):
		if skip_list[i] in class_label:
			print("Skipping: ", yid)
			return

	# print("Start Downloading ",yid)
	command = 'youtube-dl -o {} --extract-audio --audio-format mp3 \
				"https://www.youtube.com/watch?v={}"'.format(aud_path+'.mp3', yid)	
	subprocess.call(command, shell=True)

	start = int(d[1][0])
	end = start + 10

	# command = 'ffmpeg -ss {} -to {} -i {} -c:a aac {}'.format(\
	# 			start, end, aud_path+'.mp3', aud_path+'.aac')
	command = 'ffmpeg -hide_banner -loglevel panic -ss {} -to {} -i {} -acodec pcm_s16le -ar 16000 {}'.format(\
				start, end, aud_path+'.mp3', aud_path+'.wav')
	subprocess.call(command, shell=True)
	# print("Completed extracting 10 secs audio ")
	# print("-----------------------------------------------------")

	os.remove(aud_path+'.mp3')

def preprocess(args):

	data = {}

	with open(args.file) as f:
		csv_data = csv.reader(f, delimiter=",")

		for row in csv_data:
			yid = row[0]
			if yid in data:
				data[yid].append(row[1:])
			else:
				data[yid] = row[1:]

	if not path.isdir(args.output_dir):
		os.mkdir(args.output_dir)


	return data


if __name__ == '__main__':


	parser = argparse.ArgumentParser()
	parser.add_argument('-j', '--jobs', help='Number of jobs to run in parallel', default=8, type=int)
	parser.add_argument('-f', '--file', help='CSV file containing data', required=True)
	parser.add_argument('-o', '--output_dir', help="Folder where final videos will be downloaded", required=True)
	args = parser.parse_args()

	data = preprocess(args)

	p = ThreadPoolExecutor(args.jobs)
	threads = [p.submit(yt_download,row,args) for row in data.items()]
	_ = [r.result() for r in tqdm(as_completed(threads), total=len(threads))]