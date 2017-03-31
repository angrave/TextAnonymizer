# TextAnonymizer V0.0.2
# Original version by Lawrence Angrave (angrave@illinois.edu) March 29, 2017.

# MIT License
#
# Copyright (c) 2017 Lawrence Angrave
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys, re
import os.path

def readTextMap(textmapFilepath):
    rules = []
    linecount = 0
    with open(textmapFilepath) as fp:
        for line in fp:
            linecount = linecount + 1
            line = line.rstrip() # drop trailing newline
            if line.startswith('#'): continue
            if len( line ) == 0 : continue
            words = line.replace(',',' ').split()
            if len(words) == 1:
                message = "Only one word on line %d" % (linecount)
                printUsageAndQuit(message)
            searchWords = words[:-1]
            replaceWord = words[-1]
            upto =len(replaceWord) + 1
            searchExact = line[:-upto]
            rules.append([searchExact,replaceWord])
#            print "Exact '"+ searchExact + "'->'" + replaceWord +"'"
            for word in searchWords:
                if len(word) > 1:
                    rules.append([word,replaceWord])
#                   print "Word '"+ word + "'->'" + replaceWord +"'"
    return toReplacementMap(rules)

def toReplacementMap(rules):
    multiMap = dict()
    allKeys = []
    for rule in rules:
        key,value = rule
        key = key.lower()
        if(not multiMap.has_key(key)):
            multiMap[key] = [value]
            allKeys.append(key)
        else:
            existing = multiMap[key]
            if( value not in existing):
                multiMap[key].append(value)
                
    subList = []
    for key in reversed(sorted(allKeys,key=len)):
        replaceWith = multiMap[key]
#        print key, replaceWith
        if( len(replaceWith) == 1) :
          replacement= replaceWith[0]
        else:
          replacement= '[[[' + (','.join(replaceWith)) + ']]]'
        subList.append([key, replacement])
    return subList

#  Inspired by the (buggy  +len(old)) ireplace
# http://stackoverflow.com/questions/919056/case-insensitive-replace 
def wordReplace(old, new, text):
    startingIndex = 0
    replaceCount = 0
    while startingIndex < len(text):
        index = text.lower().find(old.lower(), startingIndex)
        if index == -1:
            break
            
# Only match complete words i.e. if the characters immediately before and after (if valid) are not letters, otherwise skip
        before, after = [ '.', '.' ]
        
        if index >1: 
            before = text[index-1]
        if index + len(old) < len(text):
            after = text[index + len(old)]
            
        if before.isalpha() or after.isalpha():
            startingIndex = startingIndex + len(old)
        else:
            text = text[ : index ] + new + text[ index + len(old) : ]
            startingIndex = index + len(new)
            replaceCount = replaceCount + 1
            
    return [ text, replaceCount ] 
        
def process(rules,sourceFile,outputFile):
    lineCount = 0
    lineModificationCount = 0
    wordReplacementCount = 0
    
    for line in sourceFile:
        
        lineCount = lineCount + 1
        replacedLine = line
        
        for rule in rules:
            
            replacedLine, wordsReplaced = wordReplace( rule[0], rule[1], replacedLine) 
            
            if wordsReplaced >0: 
                lineModificationCount = lineModificationCount + 1
                wordReplacementCount = wordReplacementCount + wordsReplaced
            
        outputFile.write( replacedLine )
        
    return [ lineCount, lineModificationCount, wordReplacementCount ]
    
def printUsageAndQuit(message):
    print message
    print "Usage: textreplacer.py path-to-text-file-to-read"
    print "textreplacer looks for a file named textmap.txt in the same directory as the original text"
    print "Open the example textmap.txt to see how to create your textmap.txt file"
    print "The original text file is unchanged but a new file with '-replaced' as part of the filename is created"
    sys.exit(1)
    
def toOutputFilepath(sourceFilepath):
    lastDotPosition = sourceFilepath.rfind('.')
    if lastDotPosition == -1:
        outputFilepath = sourceFilepath + "-replaced"
    else :
        outputFilepath = sourceFilepath[:lastDotPosition] + "-replace" + sourceFilepath[lastDotPosition:]
#    print "Output file:" + outputFilepath
    return outputFilepath

def toTextMapFilepath(sourceFilepath):
    return os.path.join( os.path.dirname(sourceFilepath) , "textmap.txt")

    
def main():
    if len(sys.argv) != 2:
        printUsageAndQuit("What text file should I process?")

    sourceFilepath= sys.argv[1]
    outputFilepath = toOutputFilepath( sourceFilepath )
    textmapFilepath = toTextMapFilepath( sourceFilepath )

    if not os.path.isfile(sourceFilepath): 
        printUsageAndQuit("Please provide a filepath to the source text")
    if not os.path.isfile(textmapFilepath):
        print "Expected to find " + textmapFilepath 
        printUsageAndQuit("Couldnt find text map file in the same directory")

    print "Input file  : " + sourceFilepath
    print "Mapper file : " + textmapFilepath
    print "Output file : " + outputFilepath
    
    rules = readTextMap(textmapFilepath)
    sourceFile = open(sourceFilepath, "r")
    outputFile = open(outputFilepath, "w")
    
    lineCount, lineModificationCount, wordReplacementCount = process(rules,sourceFile,outputFile)
    
    sourceFile.close()
    outputFile.close()
    print "Finished processing. %d lines. %d lines modified. %d replacements." % ( lineCount, lineModificationCount, wordReplacementCount)
    print "Review output file %s for errors and ommissions " % outputFilepath

if __name__ == "__main__":
    main()