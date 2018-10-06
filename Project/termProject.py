import os
import string
import copy
from sklearn.naive_bayes import GaussianNB
from sklearn import svm
import re
import time
import sched
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import game1
testingFile = open('testingCode.py', 'r+')
trainingFile = open('trainingCode.py', 'r+')
def startingTabs(line): #Number of starting tabs
	numTabs = 0
	numSpaces = 0
	for character in line:
		if character == " ":
			numSpaces+=1
			if numSpaces%4 == 0:
				numTabs+=1
		elif character == "\t":
			numTabs+=1
		else:
			break
	return numTabs

############Magic Number Checker####################
def isMagic(line, index):
	try:
		test = int(line[index])
		return False
	except:
		pass
	if line[index] == "=" and line[index-1] != "=":
		return False
	elif line[index] in string.whitespace:
		isMagic(line, index-1)
	else:
		return True
def getNumber(line, charIndex):
	for index in range(charIndex+1, len(line)):
		try:
			possibleInt = int(line[index])
		except:
			return line[charIndex:index]
def checkMagic(lines):
	magicLines = []
	originalCopy = copy.deepcopy(lines)
	for lineIndex in range(len(lines)):
		if not "#Magic Numbers" in lines[lineIndex]:
			for charIndex in range(len(lines[lineIndex])):
				try:
					possibleMagic = int(lines[lineIndex][charIndex])
					possibleMagic = getNumber(lines[lineIndex], charIndex)
					#pre-determined, non-magic nums
					if int(possibleMagic) not in [-1, 0, 1, 2, 10] and\
					 isMagic(lines[lineIndex], charIndex-1):
						magicLines.append(lineIndex)
						break
				except:
					pass
	return magicLines
###############Global Variable Checker###################
def globalChecker(lines):
	globalLines = []
	for lineIndex in range(len(lines)):
		if "=" in lines[lineIndex] and not "==" in lines[lineIndex]:
			if startingTabs(lines[lineIndex]) == 0:
				if not '#Global Variable' in lines[lineIndex]:
					globalLines.append(lineIndex)
	return globalLines



############Snake Case to Camel Case################
def findSnakeCase(lines):
	snakeCaseLines = []
	for line in lines:
		if "def " in line:
			functionName = line.split(" ")[1]
			if "_" in functionName and not "__" == functionName[:2]:
				snakeCaseLines.append((functionName, lines.index(line)))
	return snakeCaseLines
def suggestCamelCase(snakeCaseLines):
	for line in snakeCaseLines:
		name = line[0]
		lineNum = line[1]
		newName = name
		for charIndex in range(len(name)):
			if name[charIndex] == "_" and name[charIndex+1].isalpha():
				newName = name[:charIndex] + name[charIndex+1].upper() + name[charIndex+2:]
	return newName
# snakeCaseLines = findSnakeCase(file.readlines())
# print(suggestCamelCase(snakeCaseLines))




############## Comments Suggestor #######################
def wordDict(lines):
	wordSet = set()
	for line in lines:
		for word in re.split("\(|\t|\n| |,|:|\)", line):
			if not word in wordSet:
				wordSet.add(word)
	return list(wordSet)
def makeData(wordList, line):
	hasComment = 0
	data = [0]*len(wordList)
	if '#' in line:
		if commentedLine(line):
			return None
		hasComment = 1
	data = makeVector(wordList, line, data)
	return data, hasComment
def makeVector(wordList, line, frequencyList, isTraining = False):
	data = [0]*(len(wordList)+1)
	for word in re.split("\(|\t|\n| |,|:|\)", line):
		data[wordList.index(word)] += 1
	data[-1] = len(line)
	if isTraining:
		for index in range(len(data)-1):
			frequencyList[index][data[index]] +=1
		frequencyList[-1][len(line)%5]+=1
	return data
def commentedLine(line):
	if line == "":
		return False
	elif line[0] in string.whitespace:
		return commentedLine(line[1:])
	elif line[0] == '#':
		return True
	else:
		return False
def commentBefore(lineIndex, lines):
	if lineIndex == 0:
		return False
	elif commentedLine(lines[lineIndex-1]):
		return True
	return False
def allCommentLines(lines):
	commentLines = []
	for lineIndex in range(len(lines)):
		if not commentedLine(lines[lineIndex]) and '#' in lines[lineIndex]: #commented line of code
			commentLines.append(lineIndex)
		elif commentBefore(lineIndex, lines):
			commentLines.append(lineIndex)
	return commentLines
def probabilityComment(lines):
	i = 0
	j = 0
	for lineIndex in range(len(lines)):
		if not commentedLine(lines[lineIndex]) and '#' in lines[lineIndex]: #commented line of code
			i+=1
		elif commentBefore(lineIndex, lines):
			i+=1
			j-=1
		j+=1
	return i/j
def commentLineVectors(wordList, commentLines, lines, frequencyListC, isTraining = False):
	vectors = []
	for line in commentLines:
		vector = makeVector(wordList, lines[line], frequencyListC, isTraining)
		vectors.append(vector)
	return vectors
def probabilityElement(lineData, elementNum, testVectors):
	found = 0
	checked = 0
	for commentIndex in range(len(testVectors)):
		if testVectors[commentIndex][elementNum] == lineData[elementNum]: #if same (maybe change to >=)
			found+=1
		checked+=1
	return found/checked
def probCommentLine(lineVector, commentVectors, frequencyListC):
	totalProb = 1
	for elementIndex in range(len(lineVector)):
		#P(x_i | commented line)
		elementCommentProb = frequencyListC[elementIndex][lineVector[elementIndex]]/len(commentVectors)
		if elementCommentProb == 0:
			elementCommentProb = 0.01 #avoid 0s
		totalProb *= elementCommentProb
	return totalProb
def probUncommentLine(lineVector, uncommentVectors, frequencyListU):
	totalProb = 1
	for elementIndex in range(len(lineVector)):
		#P(x_i | uncommented line)
		elementCommentProb = frequencyListU[elementIndex][lineVector[elementIndex]]/len(uncommentVectors)
		if elementCommentProb == 0:
			elementCommentProb = 0.01 #avoid 0s
		totalProb *= elementCommentProb
	return totalProb
def uncommentLineVectors(wordList, commentLines, lines, frequencyListU, isTraining = False):
	vectors = []
	for lineIndex in range(len(lines)):
		if not lineIndex in commentLines: #uncommented line
			vector = makeVector(wordList, lines[lineIndex], frequencyListU, isTraining)
			vectors.append(vector)
	return vectors

def testAlgorithm(trainingLines, testingLines):
	wordList = wordDict(trainingLines + testingLines) #use same wordlist for training and testing
	##Create Training Data##
	lst = []
	for i in range(len(wordList)+1):
		lst.append([0]*100)
	frequencyListC = copy.deepcopy(lst)
	frequencyListU = copy.deepcopy(lst)
	trainingComments = allCommentLines(trainingLines) #indices of commented lines in training set
	commentVectors = commentLineVectors(wordList, trainingComments, trainingLines, frequencyListC, True)
	uncommentVectors = uncommentLineVectors(wordList, trainingComments, trainingLines, frequencyListU, True)
	commentProbability = probabilityComment(trainingLines)
	##Testing##
	i = 0
	j = 0
	commentLines = []
	for lineIndex in range(len(testingLines)):
		line = testingLines[lineIndex]
		lineVector = makeVector(wordList, line, frequencyListC)
		probIsComment = commentProbability * probCommentLine(lineVector, commentVectors, frequencyListC)
		probNotComment = (1-commentProbability) * probUncommentLine(lineVector, uncommentVectors, frequencyListU)
		difference = probIsComment - probNotComment
		if probIsComment >= probNotComment - 10**(-10):
			if '#' in testingLines[lineIndex]:
			#10**(-9) chosen since it worked well, not for statistical reasons
				i+=1
			commentLines.append(lineIndex)
		j+=1
	print(i /j)
	return commentLines
#If you want to test it on a testing file (for efficiency), uncomment below
# testAlgorithm(trainingFile.readlines(), testingFile.readlines())

def commentTypes(commentLines, lines):
	commentTypes = []
	for comment in commentLines:
		if "print" in lines[comment]:
			commentTypes.append("Explain what is being printed on line ")
		elif "return" in lines[comment]:
			commentTypes.append("Explain what is being returned on line ")
		elif "def" in lines[comment]:
			commentTypes.append("Explain the function on line ")
		elif "for" in lines[comment] or "while" in lines[comment]:
			commentTypes.append("Explain the loop on line ")
		else:
			commentTypes.append("Comment on line ")
	return commentTypes



############Formatting Lines#############
def lineWidthCheck(lines):
	longLines = []
	for line in lines:
		numTabs = line.count("\t")
		tabSize = 4
		lineLength = numTabs*(tabSize-1) + len(line)
		maxLength = 80
		if lineLength>maxLength and not '#Long Line' in line:
			longLines.append(lines.index(line))
	return longLines



def functionLength(lines, length):
	longFunctions = []
	inFunction = False
	lineCount = 0
	functionTabs = 0
	for lineIndex in range(len(lines)):
		if "def " in lines[lineIndex] and not inFunction: #start of new function
			inFunction = True
			functionTabs = startingTabs(lines[lineIndex])
			currentFunction = lineIndex
		elif startingTabs(lines[lineIndex]) > functionTabs and inFunction: #during the function
			lineCount+=1
		elif startingTabs(lines[lineIndex]) == functionTabs and inFunction: #finish function
			inFunction = False
			lineCount+=1
			if lineCount > length:
				if not '#Long Function' in lines[currentFunction]:
					longFunctions.append((lines[currentFunction], currentFunction))
			lineCount = 0
			currentFunction = ""
	return longFunctions

############RunTime Analysis##############
def importTime(lines):
	lines.insert(0, "import time #import time --v\n")
	return lines
def addTimers(lines):
	lines = importTime(lines)
	inFunction = False
	functionTabs = 0
	newLines = []
	for lineIndex in range(len(lines)):
		newLines.append(lines[lineIndex])
		tabs = startingTabs(lines[lineIndex])
		if "return" in lines[lineIndex]:
			inFunction = False
			#string formatting for adding timers
			newLines.insert(-1, "\t"*(tabs) +  functionName + \
				"EndTime = time.time()" + "\n")
			newLines.insert(-1, "\t"*(tabs) +  "print(" + \
				functionName + "EndTime - " + functionName + "StartTime)\n")
		elif lineIndex == len(lines)-1 and inFunction and tabs == functionTabs:
			inFunction = False
			newLines.insert(-1, "\t"*(tabs+1) +  functionName +\
			 "EndTime = time.time()" + "\n")
			newLines.insert(-1, "\t"*(tabs+1) +  "print(" + functionName \
				+ "EndTime - " + functionName + "StartTime)\n")
		elif lineIndex == len(lines)-1 and inFunction and tabs != functionTabs:
			inFunction = False
			newLines.insert(-1, "\t"*(tabs) +  functionName + \
				"EndTime = time.time()" + "\n")
			newLines.insert(-1, "\t"*(tabs) +  "print(" + functionName + \
				"EndTime - " + functionName + "StartTime)\n")
		elif tabs == functionTabs and inFunction:
			inFunction = False
			newLines.insert(-1, "\t"*(tabs+1) +  functionName + \
				"EndTime = time.time()" + "\n")
			newLines.insert(-1, "\t"*(tabs+1) +  "print(" + functionName +\
			 "EndTime - " + functionName + "StartTime)\n")
		if "def " in lines[lineIndex]:
			if not inFunction:
				functionTabs = tabs
				functionName = re.split(" |\(|\t", lines[lineIndex])[1]
				newLines.append("\t"*(tabs+1) +  functionName + \
					"StartTime = time.time()" + "\n")
			inFunction = True
	return newLines

############### UI ###################
def quit(window):
	window.destroy()
def changeFile(lines, file):
	file.seek(0)
	file.truncate()
	file.writelines(lines)
def okBox(text):
	okWindow = Tk()
	okWindow.geometry('400x400')
	textWindow = Label(okWindow, text = text)
	textWindow.place(relx = 0.5, rely = 0.5, anchor = 'c')
	okButton = Button(okWindow, text = "OK", command = lambda: quit(okWindow))
	okButton.place(relx = 0.5, rely = 1.0, anchor = 's')
#next few functions are wrappers
def runMagic(lines, file):
	magicLines = checkMagic(lines)
	if magicLines == []:
		okBox("No Magic Numbers that I haven't checked!")
	for index in magicLines:
		printLine = lines[index].strip()
		changeLine = messagebox.askyesno("Do you want to change the\
		 following line?",printLine)
		if changeLine:
			lines[index] = lines[index][:-1] + " #Magic Numbers" + "\n"
def runGlobal(lines, file):
	globalLines = globalChecker(lines)
	if globalLines == []:
		okBox("No Global Variables that I haven't checked!")
	for index in globalLines:
		printLine = lines[index].strip()
		changeLine = messagebox.askyesno("Do you want to change the \
			following line?",printLine)
		if changeLine:
				lines[index] = lines[index][:-1] + " #Global Variable" + "\n"
	
def commentSuggestor(lines, file):
	linesTraining = trainingFile.readlines()
	commentSuggestions = testAlgorithm(linesTraining, lines)
	commentStrings = commentTypes(commentSuggestions, lines)
	for line in commentSuggestions:
		if not "#" in lines[line]:
			changeLine = messagebox.askyesno("Suggestion!",\
				commentStrings[commentSuggestions.index(line)] + str(line))
			if changeLine:
				lines[line] = lines[line][:-1] + '#' + commentStrings[commentSuggestions.index(line)] + '\n'
def doLines(lines, file):
	longLines = lineWidthCheck(lines)
	if longLines == []:
		okBox("No Long Lines that I haven't checked!")
	for index in longLines:
		changeLine = messagebox.askyesno("Issue!","Line " + str(index) + \
			" is too long! Want to comment?")
		if changeLine:
				lines[index] = lines[index][:-1] + " #Long Line" + "\n"
def runFunctionLength(lines, file, length):
	longFunctions  = functionLength(lines, length)
	if longFunctions == []:
		okBox("No Long Functions that I haven't checked!")
	for function in longFunctions:
		changeLine = messagebox.askyesno("Issue!","Function " +\
		 function[0] + " is too long! Want to comment?")
		if changeLine:
			lines[function[1]] = lines[function[1]][:-1] +\
			 " #Long Function" + "\n"
	

def runTimers(lines, file):
	if not '#import time --v' in lines[0]:
		lines = addTimers(lines)
		if not lines == []:
			return lines
	else:
		okBox("Timers should be entered!")
		return lines


def homeScreen(canvas, data):
	canvas.create_image(data.width//2, data.height//2, image = data.background)
	canvas.create_text(data.width//2, data.height//2, text =\
	 'Welcome to the Style Editor \n Click which one you want to do!',\
	 font = ('Times', 20, 'bold'), fill = 'white')
	canvas.create_rectangle(10, 3*data.height//4, 110, 3*data.height//4 + 50,  fill = 'black')
	canvas.create_text(60, 3*data.height//4 + 25, text = "Game",  fill = 'white', font = ('Times', 12, 'bold'))
	canvas.create_rectangle(data.width - 110, 3*data.height//4, data.width - 10, 3*data.height//4 + 50, fill = 'black')
	canvas.create_text(data.width - 60, 3*data.height//4 + 25, text = "Editor",  fill = 'white', font = ('Times', 12, 'bold'))
def clickInBox(x, y, boxDim):
	if boxDim[0] <= x <= boxDim[2] and boxDim[1] <= y <= boxDim[3]:
		return True
	else:
		return False
#main menu
def mainMenu(canvas, data):
	titleRectWidth = 100
	titleRectHeight = 20
	canvas.create_image(data.width//2, data.height//2, image = data.background)
	canvas.create_rectangle(data.width//2 - titleRectWidth,\
	 data.height//20 - titleRectHeight, data.width//2 + titleRectWidth,\
	 data.height//20 + titleRectHeight, width = 5, fill = 'grey', outline = 'pink')
	canvas.create_text(data.width//2, data.height//20, \
		text = 'Main Menu', font = ('Times', 20, 'bold'), fill = 'white')
	for itemIndex in range(len(data.menu)):
		numItems = len(data.menu)+1
		item = data.menu[itemIndex]
		canvas.create_rectangle(10, data.height*(itemIndex+1)//numItems + 10,\
		 10 + 200, data.height*(itemIndex+1)//numItems + 40, width = 0, fill = 'grey')

		data.menuItemBox.append((10, data.height*(itemIndex+1)//numItems + 10,\
		 10 + 200, data.height*(itemIndex+1)//numItems + 40))

		canvas.create_text(10+200//2, data.height*(itemIndex+1)//numItems+25, \
			text = item, font = ('Times', 12, 'bold'), fill = 'pink')
def init(data):
	# load data.xyz as appropriate
	data.background = PhotoImage(file = "background.png")
	data.home = True
	data.menuBool = False
	data.menu = ['Magic Numbers', 'Global Variables', 'Line Length', 'Comment Suggestor',\
	'Function Length', 'Add Timers']
	root = Tk()
	root.withdraw()
	data.filename = filedialog.askopenfilename(initialdir = "/",title = "Select file")
	root.destroy()
	data.file = open(data.filename, 'r+')
	data.gameFile = open('game1.py', 'r+') #load different game files here
	data.gameWrite = open('gameWrite.py', 'w+')
	data.linesGame = data.gameFile.readlines()
	data.lines = data.file.readlines()
	data.commentSuggested = False
	data.menuItemBox = []
	data.game = False
	pass
def saveValue(root,box, data):
	data.length = int(box.get())
	root.destroy()
#input integers
def inputLineBox(text, data):
	root = Tk()
	label = Label(root, text = text)
	label.pack()
	box = Entry(root)
	box.pack()
	box.delete(0, END)
	box.insert(0, "20")
	button = Button(root, text = "OK", command= lambda: saveValue(root,box, data)).pack()
def mousePressed(event, data, root):
	# use event.x and event.y
	if data.home:
		if clickInBox(event.x, event.y, (data.width - 110, 3*data.height//4, data.width - 10, 3*data.height//4 + 50)):
			data.length = inputLineBox("How many Lines per function?", data)
			data.home = False
			data.menuBool = True
		elif clickInBox(event.x, event.y, (10, 3*data.height//4, 110, 3*data.height//4 + 50)):
			game(data.linesGame, data, root)

	if data.menuBool:
		for boxIndex in range(len(data.menuItemBox)):
			box = data.menuItemBox[boxIndex]
			if clickInBox(event.x, event.y, box):
				data.menuBool = False
				if boxIndex == 0:
					runMagic(data.lines, data.file)
				elif boxIndex == 1:
					runGlobal(data.lines, data.file)
				elif boxIndex == 2:
					doLines(data.lines, data.file)
				elif boxIndex == 3:
					if not data.commentSuggested:
						commentSuggestor(data.lines, data.file)
						data.commentSuggested = True
					else:
						okBox("Comments already suggested!")
				elif boxIndex == 4:
					runFunctionLength(data.lines, data.file, data.length)
				elif boxIndex == 5:
					data.lines = copy.deepcopy(runTimers(data.lines, data.file))
				data.menuBool = True
	pass

def keyPressed(event, data):
	# use event.char and event.keysym
	pass

def timerFired(data):
	pass

def redrawAll(canvas, data):
	# draw in canvas
	if data.home:
		homeScreen(canvas, data)
	else:
		mainMenu(canvas, data)
 

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

	def mousePressedWrapper(event, canvas, data, root):
		mousePressed(event, data, root)
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
	root = Tk()
	init(data)
	# create the root and the canvas
	canvas = Canvas(root, width=data.width, height=data.height)
	canvas.pack()
	# set up events
	root.bind("<Button-1>", lambda event:
							mousePressedWrapper(event, canvas, data, root))
	root.bind("<Key>", lambda event:
							keyPressedWrapper(event, canvas, data))
	timerFiredWrapper(canvas, data)
	# and launch the app
	root.mainloop()  # blocks until window is closed
	if not data.game:
		changeFile(data.lines, data.file)
	print("bye!")



################## Game Using above#####################
def goodStyle(lines, data):
	#check lines if they have good style
	lengthCheck = False
	nameCheck = False
	length = 20
	if functionLength(lines, length) == [] and lineWidthCheck(lines) == []:
		lengthCheck = True
	if globalChecker(lines) == [] and checkMagic(lines) == [] and\
	 findSnakeCase(lines) == []:
		nameCheck = True
	outputCheck = False
	data.gameWrite.writelines(lines)
	data.gameWrite.close()
	try:
		realOutput = game1.blahLong()
		import gameWrite
		newOutput = gameWrite.blahLong()
		if realOutput == newOutput:
			outputCheck = True
	except:
		pass
	data.gameWrite = open('gameWrite', 'w+')
	return nameCheck and lengthCheck and outputCheck
def createTextBox(lines, text):
	text.delete(1.0, END)
	for line in lines:
		text.insert(END, line)
def getText(text):
	newText = text.get(1.0, END)
	return newText
def winScreen(text):
	okBox("You're a nerd")
def ok(gameRoot, timerRoot, text, currLines, originalTime, data, root):
	#what to do with the ok button in the main game window
	currLines = []
	newText = getText(text)
	for line in newText.split("\n"):
		currLines.append(line+"\n")
	if goodStyle(currLines, data):
		okWindow = okBox("You won! \n Time Taken: " + str(int(time.time()\
		 - originalTime)) + " seconds")
		timerRoot.destroy()
		gameRoot.destroy()
		data.game = False
		
	else:
		createTextBox(currLines, text)
def game(lines, data, root):
	root.destroy()
	data.game = True
	currLines = []
	gameRoot = Tk()
	text = Text(gameRoot)
	text.pack()
	createTextBox(lines, text)
	timerRoot = Tk()
	timer = Label(timerRoot, text = "")
	timer.pack()
	originalTime = time.time()
	button = Button(gameRoot, text = "ok", command = \
		lambda: ok(gameRoot, timerRoot, text, currLines, originalTime, data, root))
	button.pack()
	def update():
		gameRoot.after(1000, update)
		timeString = "Time Taken: " + str(int(time.time() - originalTime)) + " seconds"
		timer.configure(text = timeString)
	if data.game:
		gameRoot.after(0, update)
	gameRoot.mainloop()
# lines = file.readlines()
# game(lines)
run(500, 500) #arbitrary