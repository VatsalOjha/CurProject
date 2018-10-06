#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2014 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Copy files from source to dest expanding symlinks along the way.
"""

from shutil import copytree

import argparse
import sys


# Ignore these files and directories when copying over files into the snapshot.
IGNORE = set(['.hg', 'httplib2', 'oauth2', 'simplejson', 'static'])

# In addition to the above files also ignore these files and directories when
# copying over samples into the snapshot.
IGNORE_IN_SAMPLES = set(['googleapiclient', 'oauth2client', 'uritemplate'])

parser = argparse.ArgumentParser(description=__doc__)

parser.add_argument('--source', default='.',
					help='Directory name to copy from.')

parser.add_argument('--dest', default='snapshot',
					help='Directory name to copy to.')


def _ignore(path, names):
  retval = set()
  if path != '.':
	retval = retval.union(IGNORE_IN_SAMPLES.intersection(names))
  retval = retval.union(IGNORE.intersection(names))
  return retval


def main():
  copytree(FLAGS.source, FLAGS.dest, symlinks=True,
			ignore=_ignore)


if __name__ == '__main__':
  FLAGS = parser.parse_args(sys.argv[1:])
  main()

"""Build wiki page with a list of all samples.
The information for the wiki page is built from data found in all the README
files in the samples. The format of the README file is:
   Description is everything up to the first blank line.
   api: plus  (Used to look up the long name in discovery).
   keywords: appengine (such as appengine, oauth2, cmdline)
   The rest of the file is ignored when it comes to building the index.
"""
from __future__ import print_function

import httplib2
import itertools
import json
import os
import re

BASE_HG_URI = ('http://code.google.com/p/google-api-python-client/source/'
			   'browse/#hg')

http = httplib2.Http('.cache')
r, c =  http.request('https://www.googleapis.com/discovery/v1/apis')
if r.status != 200:
  raise ValueError('Received non-200 response when retrieving Discovery.')

# Dictionary mapping api names to their discovery description.
DIRECTORY = {}
for item in json.loads(c)['items']:
  if item['preferred']:
	DIRECTORY[item['name']] = item

# A list of valid keywords. Should not be taken as complete, add to
# this list as needed.
KEYWORDS = {
	'appengine': 'Google App Engine',
	'oauth2': 'OAuth 2.0',
	'cmdline': 'Command-line',
	'django': 'Django',
	'threading': 'Threading',
	'pagination': 'Pagination',
	'media': 'Media Upload and Download'
	}


def get_lines(name, lines):
  """Return lines that begin with name.
  Lines are expected to look like:
	 name: space separated values
  Args:
	name: string, parameter name.
	lines: iterable of string, lines in the file.
  Returns:
	List of values in the lines that match.
  """
  retval = []
  matches = itertools.ifilter(lambda x: x.startswith(name + ':'), lines)
  for line in matches:
	retval.extend(line[len(name)+1:].split())
  return retval


def wiki_escape(s):
  """Detect WikiSyntax (i.e. InterCaps, a.k.a. CamelCase) and escape it."""
  ret = []
  for word in s.split():
	if re.match(r'[A-Z]+[a-z]+[A-Z]', word):
	  word = '!%s' % word
	ret.append(word)
  return ' '.join(ret)


def context_from_sample(api, keywords, dirname, desc, uri):
  """Return info for expanding a sample into a template.
  Args:
	api: string, name of api.
	keywords: list of string, list of keywords for the given api.
	dirname: string, directory name of the sample.
	desc: string, long description of the sample.
	uri: string, uri of the sample code if provided in the README.
  Returns:
	A dictionary of values useful for template expansion.
  """
  if uri is None:
	uri = BASE_HG_URI + dirname.replace('/', '%2F')
  else:
	uri = ''.join(uri)
  if api is None:
	return None
  else:
	entry = DIRECTORY[api]
	context = {
		'api': api,
		'version': entry['version'],
		'api_name': wiki_escape(entry.get('title', entry.get('description'))),
		'api_desc': wiki_escape(entry['description']),
		'api_icon': entry['icons']['x32'],
		'keywords': keywords,
		'dir': dirname,
		'uri': uri,
		'desc': wiki_escape(desc),
		}
	return context


def keyword_context_from_sample(keywords, dirname, desc, uri):
  """Return info for expanding a sample into a template.
  Sample may not be about a specific api.
  Args:
	keywords: list of string, list of keywords for the given api.
	dirname: string, directory name of the sample.
	desc: string, long description of the sample.
	uri: string, uri of the sample code if provided in the README.
  Returns:
	A dictionary of values useful for template expansion.
  """
  if uri is None:
	uri = BASE_HG_URI + dirname.replace('/', '%2F')
  else:
	uri = ''.join(uri)
  context = {
	  'keywords': keywords,
	  'dir': dirname,
	  'uri': uri,
	  'desc': wiki_escape(desc),
	  }
  return context


def scan_readme_files(dirname):
  """Scans all subdirs of dirname for README files.
  Args:
	dirname: string, name of directory to walk.
  Returns:
	(samples, keyword_set): list of information about all samples, the union
	  of all keywords found.
  """
  samples = []
  keyword_set = set()

  for root, dirs, files in os.walk(dirname):
	if 'README' in files:
	  filename = os.path.join(root, 'README')
	  with open(filename, 'r') as f:
		content = f.read()
		lines = content.splitlines()
		desc = ' '.join(itertools.takewhile(lambda x: x, lines))
		api = get_lines('api', lines)
		keywords = get_lines('keywords', lines)
		uri = get_lines('uri', lines)
		if not uri:
		  uri = None

		for k in keywords:
		  if k not in KEYWORDS:
			raise ValueError(
				'%s is not a valid keyword in file %s' % (k, filename))
		keyword_set.update(keywords)
		if not api:
		  api = [None]
		samples.append((api[0], keywords, root[1:], desc, uri))

  samples.sort()

  return samples, keyword_set


def main():
  # Get all the information we need out of the README files in the samples.
  samples, keyword_set = scan_readme_files('./samples')

  # Now build a wiki page with all that information. Accumulate all the
  # information as string to be concatenated when were done.
  page = ['<wiki:toc max_depth="3" />\n= Samples By API =\n']

  # All the samples, grouped by API.
  current_api = None
  for api, keywords, dirname, desc, uri in samples:
	context = context_from_sample(api, keywords, dirname, desc, uri)
	if context is None:
	  continue
	if current_api != api:
	  page.append("""
=== %(api_icon)s %(api_name)s ===
%(api_desc)s
Documentation for the %(api_name)s in [https://google-api-client-libraries.appspot.com/documentation/%(api)s/%(version)s/python/latest/ PyDoc]
""" % context)
	  current_api = api

	page.append('|| [%(uri)s %(dir)s] || %(desc)s ||\n' % context)

  # Now group the samples by keywords.
  for keyword, keyword_name in KEYWORDS.iteritems():
	if keyword not in keyword_set:
	  continue
	page.append('\n= %s Samples =\n\n' % keyword_name)
	page.append('<table border=1 cellspacing=0 cellpadding=8px>\n')
	for _, keywords, dirname, desc, uri in samples:
	  context = keyword_context_from_sample(keywords, dirname, desc, uri)
	  if keyword not in keywords:
		continue
	  page.append("""
<tr>
  <td>[%(uri)s %(dir)s] </td>
  <td> %(desc)s </td>
</tr>""" % context)
	page.append('</table>\n')

  print(''.join(page))


if __name__ == '__main__':
  main()
from __future__ import print_function

import httplib2
import itertools
import json
import os
import re

BASE_HG_URI = ('http://code.google.com/p/google-api-python-client/source/'
			   'browse/#hg')

http = httplib2.Http('.cache')
r, c =  http.request('https://www.googleapis.com/discovery/v1/apis')
if r.status != 200:
  raise ValueError('Received non-200 response when retrieving Discovery.')

# Dictionary mapping api names to their discovery description.
DIRECTORY = {}
for item in json.loads(c)['items']:
  if item['preferred']:
	DIRECTORY[item['name']] = item

# A list of valid keywords. Should not be taken as complete, add to
# this list as needed.
KEYWORDS = {
	'appengine': 'Google App Engine',
	'oauth2': 'OAuth 2.0',
	'cmdline': 'Command-line',
	'django': 'Django',
	'threading': 'Threading',
	'pagination': 'Pagination',
	'media': 'Media Upload and Download'
	}


def get_lines(name, lines):
  """Return lines that begin with name.
  Lines are expected to look like:
	 name: space separated values
  Args:
	name: string, parameter name.
	lines: iterable of string, lines in the file.
  Returns:
	List of values in the lines that match.
  """
  retval = []
  matches = itertools.ifilter(lambda x: x.startswith(name + ':'), lines)
  for line in matches:
	retval.extend(line[len(name)+1:].split())
  return retval


def wiki_escape(s):
  """Detect WikiSyntax (i.e. InterCaps, a.k.a. CamelCase) and escape it."""
  ret = []
  for word in s.split():
	if re.match(r'[A-Z]+[a-z]+[A-Z]', word):
	  word = '!%s' % word
	ret.append(word)
  return ' '.join(ret)


def context_from_sample(api, keywords, dirname, desc, uri):
  """Return info for expanding a sample into a template.
  Args:
	api: string, name of api.
	keywords: list of string, list of keywords for the given api.
	dirname: string, directory name of the sample.
	desc: string, long description of the sample.
	uri: string, uri of the sample code if provided in the README.
  Returns:
	A dictionary of values useful for template expansion.
  """
  if uri is None:
	uri = BASE_HG_URI + dirname.replace('/', '%2F')
  else:
	uri = ''.join(uri)
  if api is None:
	return None
  else:
	entry = DIRECTORY[api]
	context = {
		'api': api,
		'version': entry['version'],
		'api_name': wiki_escape(entry.get('title', entry.get('description'))),
		'api_desc': wiki_escape(entry['description']),
		'api_icon': entry['icons']['x32'],
		'keywords': keywords,
		'dir': dirname,
		'uri': uri,
		'desc': wiki_escape(desc),
		}
	return context


def keyword_context_from_sample(keywords, dirname, desc, uri):
  """Return info for expanding a sample into a template.
  Sample may not be about a specific api.
  Args:
	keywords: list of string, list of keywords for the given api.
	dirname: string, directory name of the sample.
	desc: string, long description of the sample.
	uri: string, uri of the sample code if provided in the README.
  Returns:
	A dictionary of values useful for template expansion.
  """
  if uri is None:
	uri = BASE_HG_URI + dirname.replace('/', '%2F')
  else:
	uri = ''.join(uri)
  context = {
	  'keywords': keywords,
	  'dir': dirname,
	  'uri': uri,
	  'desc': wiki_escape(desc),
	  }
  return context


def scan_readme_files(dirname):
  """Scans all subdirs of dirname for README files.
  Args:
	dirname: string, name of directory to walk.
  Returns:
	(samples, keyword_set): list of information about all samples, the union
	  of all keywords found.
  """
  samples = []
  keyword_set = set()

  for root, dirs, files in os.walk(dirname):
	if 'README' in files:
	  filename = os.path.join(root, 'README')
	  with open(filename, 'r') as f:
		content = f.read()
		lines = content.splitlines()
		desc = ' '.join(itertools.takewhile(lambda x: x, lines))
		api = get_lines('api', lines)
		keywords = get_lines('keywords', lines)
		uri = get_lines('uri', lines)
		if not uri:
		  uri = None

		for k in keywords:
		  if k not in KEYWORDS:
			raise ValueError(
				'%s is not a valid keyword in file %s' % (k, filename))
		keyword_set.update(keywords)
		if not api:
		  api = [None]
		samples.append((api[0], keywords, root[1:], desc, uri))

  samples.sort()

  return samples, keyword_set


def main():
  # Get all the information we need out of the README files in the samples.
  samples, keyword_set = scan_readme_files('./samples')

  # Now build a wiki page with all that information. Accumulate all the
  # information as string to be concatenated when were done.
  page = ['<wiki:toc max_depth="3" />\n= Samples By API =\n']

  # All the samples, grouped by API.
  current_api = None
  for api, keywords, dirname, desc, uri in samples:
	context = context_from_sample(api, keywords, dirname, desc, uri)
	if context is None:
	  continue
	if current_api != api:
	  page.append("""
=== %(api_icon)s %(api_name)s ===
%(api_desc)s
Documentation for the %(api_name)s in [https://google-api-client-libraries.appspot.com/documentation/%(api)s/%(version)s/python/latest/ PyDoc]
""" % context)
	  current_api = api

	page.append('|| [%(uri)s %(dir)s] || %(desc)s ||\n' % context)

  # Now group the samples by keywords.
  for keyword, keyword_name in KEYWORDS.iteritems():
	if keyword not in keyword_set:
	  continue
	page.append('\n= %s Samples =\n\n' % keyword_name)
	page.append('<table border=1 cellspacing=0 cellpadding=8px>\n')
	for _, keywords, dirname, desc, uri in samples:
	  context = keyword_context_from_sample(keywords, dirname, desc, uri)
	  if keyword not in keywords:
		continue
	  page.append("""
<tr>
  <td>[%(uri)s %(dir)s] </td>
  <td> %(desc)s </td>
</tr>""" % context)
	page.append('</table>\n')

  print(''.join(page))


if __name__ == '__main__':
  main()
from sudoku import *
import copy
from tkinter import *

def init(data):
	data.rows = data.sideLength
	data.cols = data.sideLength
	data.margin = 5 # margin around grid
	data.selection = [-1, -1]

#NOTE: these functions are taken from website

def pointInGrid(x, y, data):
	# return True if (x, y) is inside the grid defined by data.
	return ((data.margin <= x <= data.width-data.margin) and
			(data.margin <= y <= data.height-data.margin))

def getCell(x, y, data):
	# aka "viewToModel"
	# return (row, col) in which (x, y) occurred or (-1, -1) if outside grid.
	if (not pointInGrid(x, y, data)):
		return (-1, -1)
	gridWidth  = data.width - 2*data.margin
	gridHeight = data.height - 2*data.margin
	cellWidth  = gridWidth / data.cols
	cellHeight = gridHeight / data.rows
	row = (y - data.margin) // cellHeight
	col = (x - data.margin) // cellWidth
	# triple-check that we are in bounds
	row = min(data.rows-1, max(0, row))
	col = min(data.cols-1, max(0, col))
	return (row, col)

def getCellBounds(row, col, data):
	# aka "modelToView"
	# returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
	gridWidth  = data.width - 2*data.margin
	gridHeight = data.height - 2*data.margin
	columnWidth = gridWidth / data.cols
	rowHeight = gridHeight / data.rows
	x0 = data.margin + col * columnWidth
	x1 = data.margin + (col+1) * columnWidth
	y0 = data.margin + row * rowHeight
	y1 = data.margin + (row+1) * rowHeight
	return (x0, y0, x1, y1)

def mousePressed(event, data):
	(row, col) = getCell(event.x, event.y, data)
	# select this (row, col) unless it is selected
	if (data.selection == [row, col]):
		data.selection = [-1, -1]
	else:
		data.selection = [row, col]
		
#end copied functions

def keyPressed(event, data):
	if event.keysym == "Up":
		data.selection[0]-=1
	elif event.keysym == "Down":
		data.selection[0]+=1
	elif event.keysym == "Left":
		data.selection[1]-=1
	elif event.keysym == "Right":
		data.selection[1]+=1
	data.selection[0]=int(data.selection[0]%data.sideLength)
	#floats cannot be list indices
	data.selection[1]=int(data.selection[1]%data.sideLength)
	try: #only allow int inputs
		if int(event.keysym) in range(1,data.sideLength+1)\
			and data.board[data.selection[1]][data.selection[0]]\
				==0:
			#valid number and allowed space
			data.newBoard[data.selection[1]][data.selection[0]]=\
				int(event.keysym)
			if not isLegalSudoku(data.newBoard): #illegal move
				data.newBoard[data.selection[1]][data.selection[0]]= 0
	except:
		pass
	if event.keysym=='BackSpace' and\
			data.board[data.selection[1]][data.selection[0]]==0:
		data.newBoard[data.selection[1]][data.selection[0]]= 0 #deletes

def winCheck(board):
	for row in range(len(board)):
		#no isvalid is needed, only valid inputs are allowed
		for col in range(len(board[row])):
			if board[row][col]==0:
				return False
	return True

def redrawAll(canvas, data):
	for row in range(data.rows):
		for col in range(data.cols):
			(x0, y0, x1, y1) = getCellBounds(row, col, data)
			fill = "orange" if (data.selection == [row, col]) else "white"
			canvas.create_rectangle(x0, y0, x1, y1, fill=fill)
			length=data.sideLength
			centerX=col*data.width/length+data.width/(length*2)
			centerY=row*data.height/length+data.height/(length*2)
			if data.newBoard[col][row]==0: #dont draw 0
				continue
			if data.newBoard[col][row]==data.board[col][row]:
				color='black' #given nums
			else:
				color='red' #new nums
			canvas.create_text(centerX,centerY,text=data.newBoard[col][row],
				font=('Comic Sans MS' ,26 ,'bold'), fill=color)
	for i in range(1,data.blockLength):
		canvas.create_line(data.width/data.blockLength*i,5,
			data.width/data.blockLength*i,data.height-5,width=4)
	for j in range(1,data.blockLength):
		canvas.create_line(5,data.height/data.blockLength*j,
			data.width-5,data.height/data.blockLength*j,width=4)
	if winCheck(data.newBoard):
		canvas.create_rectangle(data.width/4,data.height/4,
			3*data.width/4,3*data.width/4,fill='white')
		canvas.create_text(data.width/2,data.height/2,
			text="YOU'RE\nWINNER!", font=('Comic Sans MS', 30, 'bold'))

#copied run functions

def runSudoku(width, height, board):
	if not isLegalSudoku(board):
		return None
	def redrawAllWrapper(canvas, data):
		canvas.delete(ALL)
		canvas.create_rectangle(0, 0, data.width, data.height,
								fill='white', width=0)
		redrawAll(canvas, data)
		canvas.update()    

	def mousePressedWrapper(event, canvas, data):
		mousePressed(event, data)
		redrawAllWrapper(canvas, data)

	def keyPressedWrapper(event, canvas, data):
		keyPressed(event, data)
		redrawAllWrapper(canvas, data)

	# Set up data and call init
	class Struct(object): pass
	data = Struct()
	data.width = width
	data.height = height
	data.board = board
	data.newBoard= copy.deepcopy(board) #to check against given board
	data.sideLength= len(board)
	data.blockLength= int(data.sideLength**0.5)
	init(data)
	# create the root and the canvas
	root = Tk()
	canvas = Canvas(root, width=data.width, height=data.height)
	canvas.pack()
	# set up events
	root.bind("<Button-1>", lambda event:
							mousePressedWrapper(event, canvas, data))
	root.bind("<Key>", lambda event:
							keyPressedWrapper(event, canvas, data))
	redrawAll(canvas, data)
	# and launch the app
	root.mainloop()  # blocks until window is closed
	print("bye!")

def starterBoard(n):
	if n==0:
		board=[
  [ 1, 2, 3, 4, 5, 6, 7, 8, 9],
  [ 5, 0, 8, 1, 3, 9, 6, 2, 4],
  [ 4, 9, 6, 8, 7, 2, 1, 5, 3],
  [ 9, 5, 2, 3, 8, 1, 4, 6, 7],
  [ 6, 4, 1, 2, 9, 7, 8, 3, 5],
  [ 3, 8, 7, 5, 6, 4, 0, 9, 1],
  [ 7, 1, 9, 6, 2, 3, 5, 4, 8],
  [ 8, 6, 4, 9, 1, 5, 3, 7, 2],
  [ 2, 3, 5, 7, 4, 8, 9, 1, 6]
]
	elif n==1:
		board=[[0]]
	elif n==2:
		board=[[0,0,0,0,],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
	elif n==3:
		board=[
	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
]
	return board
runSudoku(600, 600,starterBoard(0))
# Mode Demo
from tkinter import *
import random

####################################
# init
####################################

def init(data):
	data.timerDelay=50
	data.score=0
	data.time=20
	data.timerCalls=0
	
	data.mode = "start" #start inits
	data.score = 0
	data.iconLocation=[data.width//2,data.height//2] 
	loadIcon(data)
	data.iconSpeed=[6,4]
	data.radius=data.icon.width()//2
	
	#game inits
	data.cameraCenter=[data.width,data.height]
	#center of screen
	data.window=[-data.width,-data.height,
		data.width,data.height]
	data.icons=[]
	
def loadIcon(data):
	filename = "eyluo.gif"
	data.icon=PhotoImage(file=filename)


####################################
# mode dispatcher
####################################

def mousePressed(event, data):
	if (data.mode == "start"):
		startMousePressed(event, data)
	elif (data.mode == "playGame"):
		playGameMousePressed(event, data)
	elif (data.mode == "gameOver"):
		gameOverMousePressed(event, data)

def keyPressed(event, data):
	if (data.mode == "start"):
		startKeyPressed(event, data)
	elif (data.mode == "playGame"):
		playGameKeyPressed(event, data)
	elif (data.mode == "gameOver"):
		gameOverKeyPressed(event, data)

def timerFired(data):
	if (data.mode == "start"):
		startTimerFired(data)
	elif (data.mode == "playGame"):
		playGameTimerFired(data)
	elif (data.mode == "gameOver"):
		gameOverTimerFired(data)

def redrawAll(canvas, data):
	if (data.mode == "start"):
		startRedrawAll(canvas, data)
	elif (data.mode == "playGame"):
		playGameRedrawAll(canvas, data)
	elif (data.mode == "gameOver"):
		gameOverRedrawAll(canvas, data)

####################################
# start mode
####################################

def startMousePressed(event, data):
	pass

def startKeyPressed(event, data):
	if event.keysym=='p':
		data.mode = "playGame"

def startTimerFired(data):
	data.iconLocation[0]+=data.iconSpeed[0]
	#off edge in x
	if data.iconLocation[0]+data.radius>data.width\
		or data.iconLocation[0]-data.radius<0:
		data.iconSpeed[0]=-data.iconSpeed[0]
	data.iconLocation[1]+=data.iconSpeed[1]
	#off edge in y
	if data.iconLocation[1]+data.radius>data.height\
		or data.iconLocation[1]-data.radius<0:
		data.iconSpeed[1]=-data.iconSpeed[1]

def startRedrawAll(canvas, data):
	canvas.create_text(data.width/2,data.height/4,
		text='     The 112\nClicker Game!', font='Arial 30')
	canvas.create_text(data.width/2,data.height/4*3
		,text='Press p to play', font='Arial 20')
	canvas.create_image(data.iconLocation[0]
		,data.iconLocation[1],image=data.icon)

####################################
# gameOver mode
####################################

def gameOverMousePressed(event, data):
	pass

def gameOverKeyPressed(event, data):
	if event.keysym=='s':
		data.mode='start'

def gameOverTimerFired(data):
	pass

def gameOverRedrawAll(canvas, data):
	canvas.create_rectangle(0,0,data.width,
		data.height,fill='red')
	canvas.create_text(data.width/2,data.height/6,
		text='GAME OVER!',fill='white',font='Arial 34')
	canvas.create_text(data.width/2,data.height/2,
		text='Final Score: '+str(data.score),fill='white',
		font='Arial 20')
	canvas.create_text(data.width/2,data.height/6*5,
		text="Press 's' to start again",fill='white',
		font='Arial 20')

####################################
# playGame mode
####################################

def playGameMousePressed(event, data):
	#x and y in relation to top left of window
	x=event.x-data.cameraCenter[0]+data.width
	y=event.y-data.cameraCenter[1]+data.height
	for icon in reversed(data.icons): #top image first
		if abs(x-icon[0])<data.radius and abs(y-icon[1])<data.radius:
			data.icons.remove(icon)
			data.score+=1
			if data.score%5==0:
				data.time+=1
			break #only removes one

def playGameKeyPressed(event, data):
	if event.keysym=='Down':
		data.cameraCenter[1]-=20
	if event.keysym=='Up':
		data.cameraCenter[1]+=20
	if event.keysym=='Right':
		data.cameraCenter[0]-=20
	if event.keysym=='Left':
		data.cameraCenter[0]+=20

def playGameTimerFired(data):
	data.timerCalls+=1 #50ms
	if data.timerCalls%10==0:
		newIcon(data)
	if data.timerCalls%20==0:
		data.time-=1
	if data.time==0:
		data.mode='gameOver'
	
def newIcon(data):
	#fully appears on screen
	x=random.randint(data.radius,2*data.width-data.radius)
	y=random.randint(data.radius,2*data.height-data.radius)
	data.icons.append([x,y])

def playGameRedrawAll(canvas, data):
	canvas.create_rectangle(0,0,data.width,data.height,fill='dimgray')
	x=data.cameraCenter[0]
	y=data.cameraCenter[1]
	canvas.create_rectangle(x-data.width,y-data.height,
		x+data.width,y+data.height,fill='white')
	
	for icon in data.icons:
		canvas.create_image(icon[0]+x-data.width,
			icon[1]+y-data.height,image=data.icon)
		
	canvas.create_text(0,data.height/10,text="Time Left: "+str(data.time),
		font='Arial 12 bold',anchor='w')
	canvas.create_text(0,data.height/10*9,text="Score "+str(data.score),
		font='Arial 12 bold',anchor='w')

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
	def redrawAllWrapper(canvas, data):
		canvas.delete(ALL)
		canvas.create_rectangle(0, 0, data.width, data.height,
								fill='white', width=0)
		redrawAll(canvas, data)
		canvas.update()    

	def mousePressedWrapper(event, canvas, data):
		mousePressed(event, data)
		redrawAllWrapper(canvas, data)

	def keyPressedWrapper(event, canvas, data):
		keyPressed(event, data)
		redrawAllWrapper(canvas, data)

	def timerFiredWrapper(canvas, data):
		timerFired(data)
		redrawAllWrapper(canvas, data)
		# pause, then call timerFired again
		canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
	# Set up data and call init
	class Struct(object): pass
	data = Struct()
	data.width = width
	data.height = height
	data.timerDelay = 100 # milliseconds
	init(data)
	# create the root and the canvas
	root = Toplevel()
	canvas = Canvas(root, width=data.width, height=data.height)
	canvas.pack()
	# set up events
	root.bind("<Button-1>", lambda event:
							mousePressedWrapper(event, canvas, data))
	root.bind("<Key>", lambda event:
							keyPressedWrapper(event, canvas, data))
	timerFiredWrapper(canvas, data)
	# and launch the app
	root.mainloop()  # blocks until window is closed
	print("bye!")

run(300, 300)
#Teddy Warner tcwarner Section O

#################################################
# Hw3
#################################################

import cs112_s18_week3_linter
import math
import string

#################################################
# Helper functions
#################################################

def almostEqual(d1, d2, epsilon=10**-7):
	# note: use math.isclose() outside 15-112 with Python version 3.5 or later
	return (abs(d2 - d1) < epsilon)

import decimal
def roundHalfUp(d):
	# Round to nearest with ties going away from zero.
	rounding = decimal.ROUND_HALF_UP
	# See other rounding options here:
	# https://docs.python.org/3/library/decimal.html#rounding-modes
	return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

#################################################
# Hw3 problems
#################################################

### TESTING PROBLEM ###

def testPigLatin(pigLatin):
	print ("Testing pigLatin(s)...", end='')
	assert(pigLatin('hello') == 'ellohay') # some don't work at all
	assert(pigLatin('apple') == 'appleyay')
	assert(pigLatin('integer') == 'integeryay')
	assert(pigLatin('a') == 'ayay')
	assert(pigLatin('') == '')# some do not handle blank string
	assert(pigLatin('ship') == 'ipshay')
	assert(pigLatin('this is programming') == 'isthay isyay ogrammingpray')
	assert(pigLatin('under') == 'underyay') #1 forgets u

### DEBUGGING PROBLEMS ###
### NOTE: remove the triple-quotes before you start debugging. ###

def hasLetterC(s):
	s = s.lower()
	for i in range(len(s)):
		if s[i] == 'c': #==, not =
			return True
	return False

def findShortFruits(fruits):
	count = 0
	for fruit in fruits.split("-"):
		if len(fruit) < 6 and len(fruit) > 0:
			count += 1
	return count

def hasConsecutiveDigits(n):
	if n < 0:
		return hasConsecutiveDigits(-n)
	while n > 0:
		nextN = n // 10 #returned as float
		if n % 10 == nextN % 10:
			return True
		n = nextN
	return False

### STYLE PROBLEM ###
#added test cases
#better variable names
#got rid of blah
#changed if to elif
#added comments

def is_undulating(n):
	if n < 100: #only undulating if 3 digits, pos
		return False
	odddigit = n % 10 
	evendigit = (n // 10) % 10 
	n = n // 100
	digitcount = 0
	while n > 0:
		digit = n % 10
		if digitcount % 2 == 0:
		  if digit != odddigit:
			  return False
		elif digitcount % 2 == 1:
			if digit != evendigit:
				return False
		digitcount+=1
		n = n // 10
	return odddigit - evendigit != 0

def nthUndulatingNumber(n):
	count= 0
	check =0 
	while count<= n :
		check+=1
		if is_undulating(check):
			count += 1 #increases if check is undulating
	return check

### ALGORITHMIC THINKING PROBLEM ###

def hasEvenDigits(n):
	return len(str(n)) % 2 == 0

def sumOfDigits(n):
	n = str(n)
	digitsum = 0
	for digit in n:
		digitsum += int(digit)
	return digitsum
	
def equalHalves(n):
	n = str(n)
	midpoint = len(n)//2
	return sumOfDigits(n[0:midpoint]) == sumOfDigits(n[midpoint::])
	
def isPradishNumber(n):
	if not hasEvenDigits(n): #evendigits
		return False
	elif not sumOfDigits(n) == len(str(n)):
		return False #sum = number of digits
	elif not equalHalves(n):
		return False #1st half = second half
	return True

def nthPradishNumber(n):
	count = 0
	check = 10
	while count <=n:
		check += 1
		if isPradishNumber(check):
			count+=1
	return check

def ispalindrome(s):
	return str(s) == str(s[::-1])

def longestSubpalindrome(s):
	longest=''
	for begin in range(len(s)):
		for end in range(len(s)+1):
			splitstring = s[begin:end]
			if ispalindrome(splitstring):
				if len(splitstring) > len(longest):
					longest = splitstring
				elif len(splitstring) == len(longest):
					if splitstring > longest:
						longest = splitstring
	return longest
		

##### Bonus #####
#Don't grade this, I didn't finish
'''def exponentterm(slic):
	num1 = 0
	num2 = 0
	lower = 0
	upper = len(slic)
	while slic[0:lower+1].isnumeric():
		lower+=1
	num1 = int(slic[0:lower])
	while slic[upper-1:len(slic)].isnumeric():
		upper -=1
	num2 = int(slic[upper:len(slic)])
	return (num1 ** num2)
	
def modterm(slic):
	num1 = 0
	num2 = 0
	lower = 0
	upper = len(slic)
	while slic[0:lower+1].isnumeric():
		lower+=1
	num1 = int(slic[0:lower])
	while slic[upper-1:len(slic)].isnumeric():
		upper -=1
	num2 = int(slic[upper:len(slic)])
	return (num1 % num2)
	
def intdevideterm(slic):
	num1 = 0
	num2 = 0
	lower = 0
	upper = len(slic)
	while slic[0:lower+1].isnumeric():
		lower+=1
	num1 = int(slic[0:lower])
	while slic[upper-1:len(slic)].isnumeric():
		upper -=1
	num2 = int(slic[upper:len(slic)])
	return (num1 // num2)
	
def devideterm(slic):
	num1 = 0
	num2 = 0
	lower = 0
	upper = len(slic)
	while slic[0:lower+1].isnumeric():
		lower+=1
	num1 = int(slic[0:lower])
	while slic[upper-1:len(slic)].isnumeric():
		upper -=1
	num2 = int(slic[upper:len(slic)])
	return (num1 / num2)
	
def multiplyterm(slic):
	num1 = 0
	num2 = 0
	lower = 0
	upper = len(slic)
	while slic[0:lower+1].isnumeric():
		lower+=1
	num1 = int(slic[0:lower])
	while slic[upper-1:len(slic)].isnumeric():
		upper -=1
	num2 = int(slic[upper:len(slic)])
	return (num1 ** num2)
	
def addterm(slic):
	num1 = 0
	num2 = 0
	lower = 0
	upper = len(slic)
	while slic[0:lower+1].isnumeric():
		lower+=1
	num1 = int(slic[0:lower])
	while slic[upper-1:len(slic)].isnumeric():
		upper -=1
	num2 = int(slic[upper:len(slic)])
	return (num1 ** num2)
	
def subtractterm(slic):
	num1 = 0
	num2 = 0
	lower = 0
	upper = len(slic)
	while slic[0:lower+1].isnumeric():
		lower+=1
	num1 = int(slic[0:lower])
	while slic[upper-1:len(slic)].isnumeric():
		upper -=1
	num2 = int(slic[upper:len(slic)])
	return (num1 ** num2)

def expression(operation, expr):
	location = -1
	max = -1
	min = -1
	location = expr.find(operation)
	if location != -1:
		min = location-1
		max = location+1
		if operation == "**" or operation == "//":
			max +=1
		while expr[min-1].isnumeric():
			min-=1
		while expr[max].isnumeric():
			max+=1
	return (min,max)

def firstofstep2(expr):
	multindex = expr.find('*')
	if multindex == -1:
		multindex = 100000
	divindex = expr.find('/')
	if expr[divindex:divindex+1]== '//':
		divindex=-1
	if divindex == -1:
		divindex = 100000
	modindex = expr.find('%')
	if modindex == -1:
		modindex = 100000
	intdivindex = expr.find('//')
	if intdivindex == -1:
		intdivindex = 100000
	wantedindex = min(multindex,divindex,modindex,intdivindex)
	if wantedindex == intdivindex:
		return '//',wantedindex
	return expr[wantedindex],wantedindex
	
def firstofstep3(expr):
	addindex = expr.find('+')
	if addindex == -1:
		addindex = 100000
	subtindex = expr.find('-')
	if subtindex == -1:
		subtindex = 100000
	wantedindex = min(addindex,subtindex)
	return expr[wantedindex],wantedindex

def getEvalSteps(expr):
	if expr.isnumeric():
		return expr
	initexpr = expr
	finalexpr = expr
	while expr.find('**') != -1:
		sliceindex = expression('**', expr)
		slic = expr[sliceindex[0]:sliceindex[1]]
		solve = str(exponentterm(slic))
		expr = expr.replace(slic,solve)
		finalexpr += '=' +expr +'\n'
	return finalexpr'''

#################################################
# Hw3 Test Functions
#################################################

def pigLatin1(s):
	if s == "":
		return ""
	result = ""
	for word in s.split():
		index = 0
		for i in range(len(word)):
			if word[i] in 'aeio':
				index = i
				break
		if index == 0:
			newWord = word + "yay"
		else:
			newWord = word[index:] + word[:index] + "ay"
		result += newWord + " "
	return result[:-1]

def pigLatin2(sent):
  res = ""
  for s in sent.split(" "):
	if(s[0] in "aeiou"):
	  res += s + "yay "
	else:
	  i = 0
	  while(s[i] not in "aeiou"):
		i += 1
	  res += s[i:] + s[0:i]
	  res += "ay "
  return res[:-1]

def findFirstVowel(word):
	vowels = "aeiou"
	for i in range(len(word)):
		c = word[i]
		if c in vowels:
			break
	return i
def pigLatin3(sentence):
	vowels = "aeiou"
	result = ""
	for word in sentence.split(" "):
		if word[0] not in vowels:
			i = findFirstVowel(word)
			result += word[i:] + word[:i] + "ay" + " "
		else:
			result += word + "yay" + " "
	return result

def findVowel(word):
	vowels = "aeiou"
	for i in range(len(word)): 
		if word[i] in vowels:
			return i
def pigLatin4(s):
	result = ""
	vowels = "aeiou"
	for word in s.split():
		if word.isalpha() and word == word.lower():
			if word[0] in vowels: 
				toAdd = word + "yay"
			else: 
				consonantIndex = findVowel(word)
				toAdd = word[consonantIndex:] + word[:consonantIndex] + "ay"
			result += toAdd + " "
	return result.strip()
