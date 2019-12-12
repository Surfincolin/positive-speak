'''
SentimentHelper.py - Designed to help with parsing and analyzing
the president speech corpus.
'''

import pandas as pd
import re
import datetime
from os import listdir
from os.path import isfile, join
from IPython.display import clear_output
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# matches the string: title="anything here"
title_rx = re.compile(r'title="(.*)"')
# matches the string: date="anything here"
date_rx = re.compile(r'date="(.*)"')
# matches the string: January 12, 1990
date_format_rx = re.compile(r'[ADFJMNOS]\w* [\d]{1,2}, [\d]{4}')
# matches anything in double quotes
quoted_rx = re.compile(r'\"(.+?)"')
# matches anything in angle brackets
angle_bracket_rx = re.compile(r'<(.*)>')

vader = SentimentIntensityAnalyzer()

def vaderAnalyze(sentence):
	'''
	Analyzes a sentence's positivity.

	Parameters
	----------
	sentence: str
			String of words to analyze.
			
	Returns
	----------
	return: float
			A positivity score between -1.0 and 1.0.
			-1.0 is negative, 1.0 is positive
	'''
	analysis = vader.polarity_scores(sentence)
	raw_score = analysis['compound']
			
	return raw_score

class SpeechData:
	'''
	SpeechData is used to help keep speech info together.
	'''
	def __init__(self, date, name, title, positivity):
		self.date = date
		self.person = name
		self.title = title
		self.positivity = positivity
			
	def get_dict(self):
		'''
		Returns a print friendly version of the info.
		'''
		return {
			'date': self.date,
			'person': self.person,
			'title': self.title,
			'positivity': self.positivity
		}

def batch_process_files(speech_files, df):
	count = 0

	for speech in speech_files:

		# progress status
		complete = count * 100 / len(speech_files)
		clear_output(True)
		print('Processing: %.2f%% Complete' % complete)
		count += 1

		result = process_speech_file(
			speech['filename'],
			speech['folder'])
		
		if result is not None:
			df = df.append(result.get_dict(), ignore_index=True)

	clear_output(True)
	
	return df


def process_speech_file(file_str, president_name):
		
	file = open(file_str, 'r')

	title = find_title(file)
	date = find_date(file)

	if not date:
		# close file to prevent mem leaks!!!
		file.close()
		print('Warning: File had bad formatting.')
		print('file: {}'.format(file_str))
		return None

	'''
	Loop through the sentences and average the positivity
	score. For iteration beyond the first we divide by two,
	for a moving average.
	'''
	divider = 1
	score = 0
	for line in file:
		line = angle_bracket_rx.sub('', line)

		sentences = line.split('. ')
		for sentence in sentences:
			if len(sentence) < 2:
				continue
							
			sentence = sentence.rstrip()
			raw_score = vaderAnalyze(sentence)
			score += raw_score
			score = score / divider
			divider = 2 
						
	speech_data = SpeechData(date, president_name, title, score)

	# close file to prevent mem leaks!!!
	file.close()
		
	return speech_data
			

def find_title(file):
	'''
	Loops through the file looking for a title.
	title="title here"

	Parameters
	----------
	file: file
			Text file to search line by line.
			
	Returns
	----------
	return: str
			Returns the title of the document if found.
			Otherwise None
	'''
	title = None

	for line in file:
		clean_line = line.rstrip()
		title_match = title_rx.search(clean_line)
		if clean_line and title_match:
			title = quoted_rx.findall(clean_line)[0]
			break

	return title

def find_date(file):
	'''
	Loops through the file looking for a date.
	date="date here" (or date here works too)

	Parameters
	----------
	file: file
			Text file to search line by line.
			
	Returns
	----------
	return: datetime
			Returns the date of the string if found.
			Otherwise None
	'''
	date = None

	for line in file:
		clean_line = line.rstrip()
		date_match = date_rx.search(clean_line)
		if clean_line and date_match:
			date = date_format_rx.findall(clean_line)[0]
			break

	try:
		date = datetime.datetime.strptime(date, '%B %d, %Y')
	except:
		raise Exception('Trouble parsing the date in "{}"'.format(file.name))

	return date

def get_all_files_in_subfolders(base_directory):
	'''
	Returns a list of all the files one subdirectory deep.

	Parameters
	----------
	base_directory: str
			Folder to start looking in.

	Returns
	----------
	return: list
			Returns a list of dicts { filename, folder }
	'''
	base_list = listdir(base_directory)
	found_files = []
	
	for f in base_list:
		loc = join(base_directory, f)
		if not isfile(loc):
			for file_name in listdir(loc):
				file_str = join(loc, file_name)
				if isfile(file_str):
					found_files.append({'filename': file_str, 'folder': f})

	return found_files