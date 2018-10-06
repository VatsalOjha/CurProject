
def pigLatin5(s):
    result=""
    for word in s.split():
        result += (word+"yay ")
    return result.strip()

def testTestPigLatin():
    print("Testing testPigLatin()...")

    successCount = 0
    try:
        testPigLatin(pigLatin1)
        print("pigLatin1: passed")
        successCount += 1
    except:
        print("pigLatin1: failed")

    try:
        testPigLatin(pigLatin2)
        print("pigLatin2: passed")
        successCount += 1
    except:
        print("pigLatin2: failed")

    try:
        testPigLatin(pigLatin3)
        print("pigLatin3: passed")
        successCount += 1
    except:
        print("pigLatin3: failed")

    try:
        testPigLatin(pigLatin4)
        print("pigLatin4: passed")
        successCount += 1
    except:
        print("pigLatin4: failed")

    try:
        testPigLatin(pigLatin5)
        print("pigLatin5: passed")
        successCount += 1
    except:
        print("pigLatin5: failed")

    # Only one pigLatin function should pass the test cases, and it should
    # be the correct one!
    assert(successCount == 1)
    print("Passed!")

def testHasLetterC():
    print("Testing hasLetterC()...", end="")
    assert(hasLetterC("cookie") == True)
    assert(hasLetterC("banana") == False)
    assert(hasLetterC("ace") == True)
    assert(hasLetterC("attorney") == False)
    print("Passed!")

def testFindShortFruits():
    print("Testing findShortFruits()...", end="")
    assert(findShortFruits("apple-banana-kiwi-pumpkin") == 2)
    assert(findShortFruits("") == 0)
    assert(findShortFruits("cucumber-grapefruit-pineapple") == 0)
    assert(findShortFruits("fig-lemon-lime") == 3)
    assert(findShortFruits("berry") == 1)
    print("Passed!")

def testHasConsecutiveDigits():
    print("Testing hasConsecutiveDigits()...", end="")
    assert(hasConsecutiveDigits(0) == False)
    assert(hasConsecutiveDigits(123456789) == False)
    assert(hasConsecutiveDigits(1212) == False)
    assert(hasConsecutiveDigits(1212111212) == True)
    assert(hasConsecutiveDigits(33) == True)
    print("Passed!")

def testnthUndulatingNumber():
    print ("Testing nthUndulatingNumber()", end='')
    assert(nthUndulatingNumber(0) == 101)
    assert(nthUndulatingNumber(1) == 121)
    assert(nthUndulatingNumber(10) == 212)
    assert(nthUndulatingNumber(6) == 171)
    assert(nthUndulatingNumber(100) == 3131)
    print ("Passed!")

def testNthPradishNumber():
    print("Testing nthPradishNumber()...", end="")
    assert(nthPradishNumber(0) == 11)
    assert(nthPradishNumber(1) == 1102)
    assert(nthPradishNumber(2) == 1111)
    assert(nthPradishNumber(3) == 1120)
    assert(nthPradishNumber(4) == 2002)
    assert(nthPradishNumber(5) == 2011)
    assert(nthPradishNumber(6) == 2020)
    assert(nthPradishNumber(7) == 102003)
    print("Passed!")

def testLongestSubpalindrome():
    print("Testing longestSubpalindrome()...", end="")
    assert(longestSubpalindrome("ab-4-be!!!") == "b-4-b")
    assert(longestSubpalindrome("abcbce") == "cbc")
    assert(longestSubpalindrome("aba") == "aba")
    assert(longestSubpalindrome("m") == "m")
    assert(longestSubpalindrome("when he said madamimadam i laughed") == \
                                " madamimadam ")
    print("Passed!")

def testBonusGetEvalSteps():
    print("Testing getEvalSteps()...", end="")
    assert(getEvalSteps("0") == "0 = 0")
    assert(getEvalSteps("2") == "2 = 2")
    assert(getEvalSteps("3+2") == "3+2 = 5")
    assert(getEvalSteps("3-2") == "3-2 = 1")
    assert(getEvalSteps("3**2") == "3**2 = 9")
    assert(getEvalSteps("31%16") == "31%16 = 15")
    assert(getEvalSteps("31*16") == "31*16 = 496")
    assert(getEvalSteps("32//16") == "32//16 = 2")
    assert(getEvalSteps("2+3*4") == "2+3*4 = 2+12\n      = 14")
    assert(getEvalSteps("2*3+4") == "2*3+4 = 6+4\n      = 10")
    assert(getEvalSteps("2+3*4-8**3%3") == """\
2+3*4-8**3%3 = 2+3*4-512%3
             = 2+12-512%3
             = 2+12-2
             = 14-2
             = 12""")
    assert(getEvalSteps("2+3**4%2**4+15//3-8") == """\
2+3**4%2**4+15//3-8 = 2+81%2**4+15//3-8
                    = 2+81%16+15//3-8
                    = 2+1+15//3-8
                    = 2+1+5-8
                    = 3+5-8
                    = 8-8
                    = 0""")
    print("Passed!")

#################################################
# Hw3 Main
#################################################

def testAll():
    testTestPigLatin()
    testHasLetterC()
    testFindShortFruits()
    testHasConsecutiveDigits()
    testnthUndulatingNumber()
    testNthPradishNumber()
    testLongestSubpalindrome()
    testBonusGetEvalSteps()

def main():
    cs112_s18_week3_linter.lint() # check style rules
    testAll()

if __name__ == '__main__':
    main()
#################################################
# Hw4
#################################################

import cs112_s18_week4_linter
import math
import string
import copy

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
# Hw4 problems
#################################################

"""
Fill in your answers to the List Function Table problem here.

a = a + b destructive
a += b destructive
a.append(x) destructive
a.insert(0, x) destructive
a.extend(b) destructive
a.remove(x) destructive
a.pop(0) destructive
del a[0] destructive
a.reverse() destructive
reversed(a) non destructive
a.sort() destructive
sorted(a) non destructive
copy.copy(a) non destructive
"""

def inverseLookAndSay(a):
    say = []
    for Tuple in a:
        repeatCount=Tuple[0]
        while repeatCount>0: #adds n copies of number
            say.append(Tuple[1])
            repeatCount-=1
    return say

def inHand(hand,word): #checks if dictionary word is in hand
    for letter in word:
        if word.count(letter) > hand.count(letter):
            return False
        elif letter not in hand:
            return False
    return True
    
def allWords(hand, dictionary): #makes a list of all dictionary words in hand
    hand = ''.join(hand)
    wordList = []
    for word in dictionary:
        if inHand(hand,word):
            wordList.append(word)
    return wordList

def wordScore(word, letterScores):
    alphabet='abcdefghijklmnopqrstuvwxyz'
    score = 0
    for letter in word: #adds value of letter to word score
        letterScore = letterScores[alphabet.find(letter)]
        score+= letterScore
    return score
        
def bestScrabbleScore(dictionary, letterScores, hand):
    wordList = allWords(hand,dictionary)
    bestScore = 0
    bestWord = []
    for word in wordList:
        score = wordScore(word,letterScores)
        if score > bestScore: 
            bestScore=score #updates highest scoring word
            bestWord = []
            bestWord.append(word)
        elif score == bestScore and bestWord != []:
            bestWord.append(word) #special case with multiple equal words
    if bestWord == []:
        return None
    elif len(bestWord) == 1: #removes string from bestword list
        return (bestWord[0], bestScore)
    else:
        return (bestWord, bestScore)

######################################################################
# ignore_rest: The autograder will ignore all code below here
######################################################################

from tkinter import *

def drawChessboard(winWidth=640, winHeight=640):
    root = Tk()
    canvas = Canvas(root, width=winWidth, height=winHeight)
    canvas.pack()
    lX = winWidth/8 #length of single column
    lY = winHeight/8 #length of single row
    beigeStatus=True
    for col in range(8): #drawing board
        for row in range(8):
            if beigeStatus:
                color = 'beige'
            elif not beigeStatus:
                color = 'dimgray'
            canvas.create_rectangle(col*lX,row*lY,(col+1)*lX,(row+1)*lY, 
                fill=color)
            beigeStatus=not beigeStatus
        beigeStatus = not beigeStatus
    blackStatus=True
    radius=lX/3
    for row in range(2): #drawing pawns
        if blackStatus:
            color='black'
        elif not blackStatus:
            color='white'
        for col in range(8):
            trianglePoints=[]
            centerX=lX/2+lX*col #columns 1-8
            centerY=lY/2+lY*row*5+lY #rows 2,7
            for i in range(3):
                xCor=centerX-radius*math.sin(2*math.pi*i/3)
                trianglePoints.append(xCor)
                yCor=centerY-radius*math.cos(2*math.pi*i/3)
                trianglePoints.append(yCor)
            canvas.create_polygon(trianglePoints,fill=color,
                outline='black',width=1)
        blackStatus=not blackStatus
    pieces=['R','H','B','Q','K','B','H','R']
    blackStatus=True
    for row in range(2): #drawing other pieces
        if blackStatus:
            color='black'
            textColor='white'
        elif not blackStatus:
            color='white'
            textColor='black'
        for col in range(8):
            centerX=lX/2+lX*col #columns 1-8
            centerY=lY/2+lY*row*7 #rows 1,8
            canvas.create_oval(centerX-radius,centerY-radius,
                centerX+radius,centerY+radius, fill=color)
            canvas.create_text(centerX,centerY,text=pieces[col],
                font='Helvetica %d bold' %radius, fill=textColor)
        blackStatus=not blackStatus

    root.mainloop()

##### Bonus #####


#################################################
# Hw4 Test Functions
#################################################

def _verifyInverseLookAndSayIsNondestructive():
    a = [(1,2), (2,3)]
    b = copy.copy(a)
    inverseLookAndSay(a) # ignore result, just checking for destructiveness here
    return (a == b)

def testInverseLookAndSay():
    print("Testing inverseLookAndSay()...", end="")
    assert(_verifyInverseLookAndSayIsNondestructive() == True)
    assert(inverseLookAndSay([]) == [])
    assert(inverseLookAndSay([(3,1)]) == [1,1,1])
    assert(inverseLookAndSay([(1,-1),(1,2),(1,7)]) == [-1,2,7])
    assert(inverseLookAndSay([(2,3),(1,8),(3,-10)]) == [3,3,8,-10,-10,-10])
    assert(inverseLookAndSay([(5,2), (2,5)]) == [2]*5 + [5]*2)
    assert(inverseLookAndSay([(2,5), (5,2)]) == [5]*2 + [2]*5)
    print("Passed!")

def testBestScrabbleScore():
    print("Testing bestScrabbleScore()...", end="")
    def dictionary1(): return ["a", "b", "c"]
    def letterScores1(): return [1] * 26
    def dictionary2(): return ["xyz", "zxy", "zzy", "yy", "yx", "wow"] 
    def letterScores2(): return [1+(i%5) for i in range(26)]
    assert(bestScrabbleScore(dictionary1(), letterScores1(), list("b")) ==
                                        ("b", 1))
    assert(bestScrabbleScore(dictionary1(), letterScores1(), list("ace")) ==
                                        (["a", "c"], 1))
    assert(bestScrabbleScore(dictionary1(), letterScores1(), list("b")) ==
                                        ("b", 1))
    assert(bestScrabbleScore(dictionary1(), letterScores1(), list("z")) ==
                                        None)
    # x = 4, y = 5, z = 1
    # ["xyz", "zxy", "zzy", "yy", "yx", "wow"]
    #    10     10     7     10    9      -
    assert(bestScrabbleScore(dictionary2(), letterScores2(), list("xyz")) ==
                                         (["xyz", "zxy"], 10))
    assert(bestScrabbleScore(dictionary2(), letterScores2(), list("xyzy")) ==
                                        (["xyz", "zxy", "yy"], 10))
    assert(bestScrabbleScore(dictionary2(), letterScores2(), list("xyq")) ==
                                        ("yx", 9))
    assert(bestScrabbleScore(dictionary2(), letterScores2(), list("yzz")) ==
                                        ("zzy", 7))
    assert(bestScrabbleScore(dictionary2(), letterScores2(), list("wxz")) ==
                                        None)
    print("Passed!")

def testDrawChessboard():
    print("Testing drawChessboard()...")
    print("Since this is graphics, this test is not interactive.")
    print("Inspect each of these results manually to verify them.")
    drawChessboard()
    drawChessboard(winWidth=400, winHeight=400)
    print("Done!")



#################################################
# Hw4 Main
#################################################

def testAll():
    testInverseLookAndSay()
    testBestScrabbleScore()
    testDrawChessboard()

def main():
    cs112_s18_week4_linter.lint() # check style rules
    testAll()

if __name__ == '__main__':
    main()
#Teddy Warner tcwarner


import copy
'''
Slow 1:
A. Destructively modifies a list to switch the first and last values.
B.
def slow1(lst): #n=len(lst)
    assert(len(lst) >= 2)
    a = lst.pop() #O(1)
    b = lst.pop(0) #O(n)
    lst.insert(0, a) #O(n)
    lst.append(b) #O(1)
    
    #Total = O(n)
C and D.
def fast1(lst):
    assert(len(lst)) >=2
    n=len(lst)-1 #O(1)
    temp=lst[0] #O(1)
    lst[0]=lst[n] #O(1)
    lst[n]=lst[temp] #O(1)
    
    #Total = O(1)

Slow 2:
A. Returns how many times a value has occurred previously in a list.
B.
def slow2(lst): # N is the length of the list lst
    counter = 0
    for i in range(len(lst)): #O(n)
        if lst[i] not in lst[:i]: #O(n)
            counter += 1
    return counter
    
    #Total= O(n**2)
    
C and D.
def fast2(lst):
    return len(lst)-len(set(lst)) #O(1),O(n)
    
    #Total = O(n)
    

Slow 3:
A. Returns the letter with the highest count. Ties are broken by ord value.
B.
import string
def slow3(s): # N is the length of the string s
    maxLetter = ""
    maxCount = 0
    for c in s: #O(n)
        for letter in string.ascii_lowercase: #O(n)
            if c == letter:
                if s.count(c) > maxCount or \
                   s.count(c) == maxCount and c < maxLetter: #O(N)
                    maxCount = s.count(c) #O(n), not nested
                    maxLetter = c
    return maxLetter
    
    #Total=O(n**3)
    
C and D.
import string
def fast3(s):
    maxLetter=''
    maxCount=0
    for c in s: #O(n)
        if c.isalpha() and (s.count(c) > maxCount or \
            s.count(c) == maxCount and c < maxLetter): #O(1), O(n)
                maxCount = s.count(c) #O(n), not nested
                maxLetter = c
    return maxLetter
    
    #Total=O(n**2)
'''

def friendsOfFriends(d):
    newDict={}
    for key in d: #creates blank dictionary of friends
        newDict.update({key: set()})
    
    for person in d:
        for friend in d[person]:
            for friendOfFriend in d[friend]: #friends of person's friends
                if friendOfFriend not in d[person] and friendOfFriend!=person:
                    #person not friends with them
                    #person cannot be friends with self
                    newDict[person].add(friendOfFriend)

    return newDict
    
def movieAwards(oscarResults):
    awards={}
    for tupl in oscarResults: #makes dict of movie:{}
        awards[tupl[1]]=set()
    for tupl in oscarResults: #adds awards to each movie
        awards[tupl[1]].add(tupl[0])
    return awards

def containsPythagoreanTriple(a):
    for A in range(len(a)):
        for B in range(len(a)):
            if A==B: #don't double count values
                continue
            value=(a[A]**2+a[B]**2)**0.5
            if value==int(value) and value in set(a):
                #in sets have O(1)
                return True
    return False
    #O(n**2)

def instrumentedLinearSearch(lst,n):
    valuesChecked=[]
    for i in range(len(lst)):
        valuesChecked.append(i)
        if lst[i]==n:
            break
    return valuesChecked
    
def instrumentedBinarySearch(lst,n):
    valuesChecked=[]
    valueOffset=0
    beginning=True
    unModCount=0
    while unModCount<2:
        checked=len(lst)//2 #middle value
        if beginning and len(lst)%2==0: #i dont know why this is needed
            checked-=1
        if checked not in valuesChecked:
            valuesChecked.append(checked+valueOffset)
        if lst[checked]==n:
            break
        elif lst[checked]<n:
            lst=lst[checked:len(lst)]
            valueOffset+=checked #lst is destructively modified
            beginning=False
        else:
            lst=lst[0:checked]
        if len(lst)==1:
            unModCount+=1
    
    return valuesChecked
    
def testFriendsOfFriends():
    print("Testing friendsOfFriends", end='...')
    d = { }
    d["jon"] = set(["arya", "tyrion"])
    d["tyrion"] = set(["jon", "jaime", "pod"])
    d["arya"] = set(["jon"])
    d["jaime"] = set(["tyrion", "brienne"])
    d["brienne"] = set(["jaime", "pod"])
    d["pod"] = set(["tyrion", "brienne", "jaime"])
    d["ramsay"] = set()
    
    solution={
 'tyrion': {'arya', 'brienne'}, 
 'pod': {'jon'}, 
 'brienne': {'tyrion'}, 
 'arya': {'tyrion'}, 
 'jon': {'pod', 'jaime'}, 
 'jaime': {'pod', 'jon'}, 
 'ramsay': set()
}
    assert(friendsOfFriends(d)==solution)
    print("Complete")

def testMovieAwards():
    print("Testing movieAwards", end="...")
    d= { 
    ("Best Picture", "The Shape of Water"), 
    ("Best Actor", "Darkest Hour"),
    ("Best Actress", "Three Billboards Outside Ebbing, Missouri"),
    ("Best Director", "The Shape of Water")
}
    solution= {"Darkest Hour" : { "Best Actor" },
    "Three Billboards Outside Ebbing, Missouri" : { "Best Actress" },
    "The Shape of Water" : { "Best Director", "Best Picture" }
}
    assert(movieAwards(d)==solution)
    print("Complete")
    
def testContainsPythagoreanTriple():
    print("Testing pythagoreanTriple",end='...')
    assert(containsPythagoreanTriple([1,3,6,2,5,1,4]))
    assert(not containsPythagoreanTriple([1,2,3,4,6]))
    print("Complete")
    
def testInstrumentedLinearSearch():
    print("Testing instrumentedLinearSearch",end='...')
    assert(instrumentedLinearSearch([2, 4, 6, 8, 10, 12],8)==[0,1,2,3])
    print('Complete')
    
def testInstrumentedBinarySearch():
    print("Testing instrumentedBinarySearch",end='...')
    assert(instrumentedBinarySearch([2, 4, 6, 8, 10, 12, 14],12)==[3,5])
    assert(instrumentedBinarySearch(['a', 'b', 'c', 'd'], 'a')==[1,0])
    assert(instrumentedBinarySearch(['here', 'not'], 'look')==[0,1])
    print('Complete')
    
def testAll():
    testFriendsOfFriends()
    testMovieAwards()
    testContainsPythagoreanTriple()
    testInstrumentedLinearSearch()
    testInstrumentedBinarySearch()
    
testAll()
#Teddy Warner tcwarner

def powerSum(n, k):
    if n<=0 or k<0:
        return 0
    else:
        return n**k + (powerSum(n-1,k))
    
def generateLetterString(s,depth=0):
    if len(s)!=2 or s[0]==s[1]:
        if depth!=0: #puts last letter in
            return s[0]
        else:
            return ''
    else:
        if ord(s[0])<ord(s[1]): #forwards
            return s[0]+generateLetterString(chr(ord(s[0])+1)+s[1],depth+1)
        else: #backwards
            return s[0]+generateLetterString(chr(ord(s[0])-1)+s[1],depth+1)

class VendingMachine:
    def __init__(self,numberOfBottles,price):
        self.numberOfBottles=numberOfBottles
        self.price=price
        self.moneyPaid=0
        self.owed=0
    def __repr__(self):
        if self.numberOfBottles==1:
            plural=''
        else:
            plural='s'
        #avoids 0.00
        if (self.moneyPaid/100)%1==0 and (self.price/100)%1!=0:
            return "Vending Machine:<%d bottle%s; $%0.2f each; $%d paid>"\
                %(self.numberOfBottles, plural,self.price/100, self.moneyPaid)
        elif (self.price/100)%1==0:
            return "Vending Machine:<%d bottle%s; $%d each; $%d paid>"\
                %(self.numberOfBottles, plural,self.price/100, self.moneyPaid)
        else:
            return "Vending Machine:<%d bottle%s; $%0.2f each; $%0.2f paid>"\
                %(self.numberOfBottles,plural,self.price/100,\
                    self.moneyPaid/100)
    def isEmpty(self):
        return self.numberOfBottles==0
    def getBottleCount(self):
        return self.numberOfBottles
    def stillOwe(self):
        self.owed=self.price-self.moneyPaid
        return self.owed
    def insertMoney(self,money):
        if self.numberOfBottles==0:
            return ("Machine is empty", money)
        self.moneyPaid+=money
        self.owed=self.price-self.moneyPaid
        if self.owed<=0:
            self.numberOfBottles-=1
            self.moneyPaid=0
            if self.owed==0:
                change=0
            else:
                change=abs(self.owed) #extra amount paid
            return ("Got a bottle!",change)
        elif (self.owed/100)%1==0:
            return (("Still owe $%d" %(self.owed/100),0))
        else:
            return (("Still owe $%0.2f" %(self.owed/100),0))
    def stockMachine(self,units):
        self.numberOfBottles+=units
    
    def getHashables(self):
        return (self.numberOfBottles,self.price, self.moneyPaid,self.owed)
    def __hash__(self):
        return hash(self.getHashables())
    def __eq__(self,other):
        return (isinstance(other,VendingMachine) and (str(self)==str(other)))
#!/usr/bin/env python
"""Setup configuration for the python grr modules."""

# pylint: disable=unused-variable
# pylint: disable=g-multiple-import
# pylint: disable=g-import-not-at-top
import ConfigParser
import os
import subprocess

from setuptools import find_packages, setup, Extension
from setuptools.command.develop import develop
from setuptools.command.install import install
from setuptools.command.sdist import sdist

IGNORE_GUI_DIRS = ["node_modules", "tmp"]


def find_data_files(source, ignore_dirs=None):
  ignore_dirs = ignore_dirs or []
  result = []
  for directory, dirnames, files in os.walk(source):
    dirnames[:] = [d for d in dirnames if d not in ignore_dirs]

    files = [os.path.join(directory, x) for x in files]
    result.append((directory, files))

  return result


def run_make_files(make_ui_files=True, sync_artifacts=True):
  """Builds necessary assets from sources."""

  if sync_artifacts:
    # Sync the artifact repo with upstream for distribution.
    subprocess.check_call(["python", "makefile.py"], cwd="grr/artifacts")

  if make_ui_files:
    subprocess.check_call(["npm", "install"], cwd="grr/gui/static")
    subprocess.check_call(
        ["npm", "install", "-g", "gulp"], cwd="grr/gui/static")
    subprocess.check_call(["gulp", "compile"], cwd="grr/gui/static")


def get_config():
  config = ConfigParser.SafeConfigParser()
  config.read(
      os.path.join(os.path.dirname(os.path.realpath(__file__)), "version.ini"))
  return config


VERSION = get_config()


class Develop(develop):

  def run(self):
    run_make_files()
    develop.run(self)
class Sdist(sdist):
  """Build sdist."""

  user_options = sdist.user_options + [
      ("no-make-ui-files", None, "Don't build UI JS/CSS bundles (AdminUI "
       "won't work without them)."),
      ("no-sync-artifacts", None,
       "Don't sync the artifact repo. This is unnecessary for "
       "clients and old client build OSes can't make the SSL connection."),
  ]

  def initialize_options(self):
    self.no_sync_artifacts = None
    self.no_make_ui_files = None
    sdist.initialize_options(self)

  def run(self):
    run_make_files(
        make_ui_files=not self.no_make_ui_files,
        sync_artifacts=not self.no_sync_artifacts)
    sdist.run(self)


data_files = (
    find_data_files("executables") + find_data_files("install_data") +
    find_data_files("scripts") + find_data_files("grr/artifacts") +
    find_data_files("grr/checks") + find_data_files(
        "grr/gui/static", ignore_dirs=IGNORE_GUI_DIRS) + find_data_files(
            "grr/gui/local/static", ignore_dirs=IGNORE_GUI_DIRS) +
    ["version.ini"])

if "VIRTUAL_ENV" not in os.environ:
  print "*****************************************************"
  print "  WARNING: You are not installing in a virtual"
  print "  environment. This configuration is not supported!!!"
  print "  Expect breakage."
  print "*****************************************************"

setup_args = dict(
    name="grr-response-core",
    version=VERSION.get("Version", "packageversion"),
    description="GRR Rapid Response",
    license="Apache License, Version 2.0",
    url="https://github.com/google/grr",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    ext_modules=[Extension("grr._semantic", ["accelerated/accelerated.c"])],
    cmdclass={
        "develop": Develop,
        "install": install,
        "sdist": Sdist,
    },
    install_requires=[
        "binplist==0.1.4",
        "cryptography==2.0.3",
        "fleetspeak==0.0.7",
        "grr-response-proto==%s" % VERSION.get("Version", "packagedepends"),
        "ipaddr==2.2.0",
        "ipython==5.0.0",
        "pip>=8.1.1",
        "psutil==5.4.3",
        "python-dateutil==2.6.1",
        "pytsk3==20170802",
        "pytz==2017.3",
        "PyYAML==3.12",
        "requests==2.9.1",
        "virtualenv==15.0.3",
        "wheel==0.30",
        "Werkzeug==0.11.3",
        "yara-python==3.6.3",
    ],
    extras_require={
        # The following requirements are needed in Windows.
        ':sys_platform=="win32"': [
            "WMI==1.4.9",
            "pypiwin32==219",
        ],
    },

    # Data files used by GRR. Access these via the config_lib "resource" filter.
    data_files=data_files)

setup(**setup_args)
#!/usr/bin/env python
"""A module that configures the behaviour of pytest runner."""
import sys

import pytest

from grr.lib import flags
from grr.test_lib import testing_startup

SKIP_BENCHMARK = pytest.mark.skip(
    reason="benchmark tests are executed only with --benchmark flag")

test_args = None


def pytest_cmdline_preparse(config, args):
  """A pytest hook that is called during command-line argument parsing."""
  del config  # Unused.

  try:
    separator = args.index("--")
  except ValueError:
    separator = len(args)

  global test_args
  test_args = args[separator + 1:]
  del args[separator:]


def pytest_cmdline_main(config):
  """A pytest hook that is called when the main function is executed."""
  del config  # Unused.
  sys.argv = ["pytest"] + test_args


last_module = None


def pytest_runtest_setup(item):
  """A pytest hook that is called before each test item is executed."""
  # We need to re-initialize flags (and hence also testing setup) because
  # various modules might have various flags defined.
  global last_module
  if last_module != item.module:
    flags.Initialize()
    testing_startup.TestInit()
  last_module = item.module


def pytest_addoption(parser):
  """A pytest hook that is called during the argument parser initialization."""
  parser.addoption(
      "-B",
      "--benchmark",
      dest="benchmark",
      default=False,
      action="store_true",
      help="run tests marked as benchmarks")


def pytest_collection_modifyitems(session, config, items):
  """A pytest hook that is called when the test item collection is done."""
  del session  # Unused.

  benchmark = config.getoption("benchmark")
  for item in items:
    if not benchmark and item.get_marker("benchmark"):
      item.add_marker(SKIP_BENCHMARK)