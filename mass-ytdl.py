#!/usr/bin/env python3

import os
import subprocess
import sys
import time
import xlrd

def print_help():

	print("Usage: ./mass-mus-ydl <SPREADSHEET>")
	print("Make sure <SPREADSHEET> is a path to a valid spreadsheet.")

def download(data):

	data["Title"] = str(data["Title"]).replace("/", "-")
	data["Artist"] = str(data["Artist"]).replace("/", "-")
	output = f"output/{data['Artist']}/{data['Album']}/{data['Artist']} - {data['Title']}-R-.%(ext)s"

	print(f"==> [..........]   0% Downloading: {data['Artist']} - {data['Title']}.ogg", end=" ")

	if os.path.exists(f"output/{data['Artist']}/{data['Album']}/{data['Artist']} - {data['Title']}.ogg"):
		print("- Already exists. Skipping.", end=" ")
		return 0

	print(f"\r==> [#.........]  10% Downloading: {data['Artist']} - {data['Title']}.ogg", end=" ")

	process = subprocess.run(
		[
			"youtube-dl", "-x", "--audio-format", "vorbis",
			data["Target URL"],	"-o", output
		],
		stdout=open(os.devnull, "wb"),
		stderr=open(os.devnull, "wb")
	)

	if process.returncode != 0:
		return -1

	print(f"\r==> [#######...]  70% Downloading: {data['Artist']} - {data['Title']}.ogg", end=" ")

	finput = f"output/{data['Artist']}/{data['Album']}/{data['Artist']} - {data['Title']}-R-.ogg"
	output = f"output/{data['Artist']}/{data['Album']}/{data['Artist']} - {data['Title']}.ogg"

	cliargs = [
		"ffmpeg", "-i", finput, "-acodec", "copy",
		"-map_metadata", "-1",
		"-metadata", "title=%s" % data['Title'],
		"-metadata", "artist=%s" % data['Artist'],
		"-metadata", "album=%s" % data['Album'],
	]

	if data["Track #"] != "" and data["out of"] != "":
		cliargs.append("-metadata")
		cliargs.append("track=%s/%s" % (data["Track #"], data["out of"]))

	cliargs.append(output)

	process = subprocess.run(cliargs, stdout=open(os.devnull, "wb"), stderr=open(os.devnull, "wb"))

	if process.returncode != 0:
		return -1

	print(f"\r==> [#########.]  90% Downloading: {data['Artist']} - {data['Title']}.ogg", end=" ")

	process = subprocess.run(
		[
			"rm", "-f", finput
		],
		stdout=open(os.devnull, "wb"),
		stderr=open(os.devnull, "wb")
	)

	if process.returncode != 0:
		return -1

	print(f"\r==> [##########] 100% Downloading: {data['Artist']} - {data['Title']}.ogg", end=" ")

def main(args):

	start = time.time()

	# Argument checking.
	if len(args) != 1 or "-h" in args or "--help" in args:
		print_help()
		return -1
	else:
		fname = args[0]

	# Making sure the supplied path exists.
	try:
		assert os.path.exists(fname) and os.path.isfile(fname)
	except:
		print(f"Path {fname} is invalid.")
		return -1

	# Variables.
	data = []
	template = {}
	headers = {}
	spreadsheet = xlrd.open_workbook(fname).sheet_by_index(0)

	# Creating a template.
	for column in range(len(spreadsheet.row(0))):
		header = spreadsheet.row(0)[column].value
		template[header] = None
		headers[column] = header

	# Populating data.
	for row in range(1, spreadsheet.nrows):
		item = template.copy()
		for column in range(len(spreadsheet.row(row))):
			value = spreadsheet.cell(row, column).value
			if type(value) == float:
				if value == int(value):
					value = str(int(value))
				else:
					value = str(value)
			item[headers[column]] = value
		data.append(item)

	# Download the music from the video and set its metadata.
	for item in data:
		if download(item) == -1:
			print("ERROR ENCOUNTERED! See alerts.txt.")
			open("alerts.txt", "a+").write(str(item)+"\n")
		print()

	print(f"Done with {len(data)} items in {int(time.time()-start)} seconds elapsed.")

if __name__ == "__main__":
	main(sys.argv[1::])
