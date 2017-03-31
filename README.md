# TextAnonymizer
A python-based tool to replace all matching names (and other word-based items such as emails) in text and html files. It is useful first step when anonymizing IRB human subject research data.

## Features

* Only replaces matching complete words (so the Tom in "Tom's" will be replaced but not "atom" or "tomato")
* Case insensitive (matches Tom tom TOM toM)
* Word-based matching: From the example mapping below, the exact match "Bertrand Russel" but also just "Russel" and "Bertrand" are all potential matches
* Does not overwrite original file (creates a new file with '-replace' as part of the filename)

## How to set up your textmap file

The textmap file contains a list of names (or words, or email addresses) that you want to replace. 
Create a *plain text* file 'textmap.txt' in the same directory as your original text data.
Here's an example textmap. The last word on each line is used as the replacement value.
Words can be separated using comma, tab or spaces:
````
Illinois	1234560
Tom,1234569
mary a. smith 1234561
Mary R clarke,1234562
Bertrand Russel	1234568
Berty 1234568
brussel@gm.com brussel@yahu.com 1001
````
Blank lines and lines that start with # character are ignored, all other lines have at least two words.

## Example use

Suppose we have a file `example.html` that includes the following source text

````
On Monday's Bertrand enjoyed looking over the University of Illinois.
Bertrand Russel was his full name and it sometimes appeared twice on the same line, like this line has Bertrand Russel twice.
Sometimes he was known as Russel too.
"bertrand" 
"Russel Bertrand" 
"Bertrand,  russel" 
and "berty Russel" or just
berty
And don't forget Mary
and Mary R clarke who liked to email brussel@yahu.com.
Tom met with tOm
Tom,tom!  tom  , tom's Tom;tom
But Atom and tomato and aToms should not be replaced nor stom
````

Run the script by including the filename (or full filepath) of the original text file. The program looks for the textmap file is in the same directory as this original text file.
In the example below we've already used "cd" to navigate to the directory that includes the original text file, the textmap and textanonymizer.

````
python textanonymizer.py example.html` 

Input file  : example.html
Mapper file : textmap.txt
Output file : example-replace.html
Finished processing. 18 lines. 17 lines modified. 24 replacements.
````

The original text file is read but not modified. Instead a new file `example-replace.html` is created-

````
On Monday's 1234568 enjoyed looking over the University of 1234560.
1234568 was his full name and it sometimes appeared twice on the same line, like this line has 1234568 twice.
Sometimes he was known as 1234568 too.
"1234568" 
"1234568 1234568" 
"1234568,  1234568" 
and "1234568 1234568" or just
1234568
And don't forget [[[1234561,1234562]]]
and 1234562 who liked to email 1001.
1234569 met with 1234569
1234569,1234569!  1234569  , 1234569's 1234569;1234569
But Atom and tomato and aToms should not be replaced nor stom
````

## FAQ

* Can I use or cite this for IRB / research purposes e.g. to help anonymize discussion text?
Yes. An acknowledgement or citation of this work would be appreciated. 
A typical citation would include the following: TextAnonymizer by Lawrence Angrave, 'https://github.com/angrave/TextAnonymizer' (2017).

* Can I use textanonymizer to anonymize a known set of email addresses?
Yes if you can add list of known email addresses to the textmap. 

* Can you make textanonymizer do ... for me?
Sorry this software is provided "as-is" and is not actively supported. It is open source and freely available. It's small enough that you can probably tweak to do what you want.

* Does this script understand html?
No - it just treats all files as plain files.

* Can I use this with my Microsoft .doc .zip or .pdf binary files?
No - only plain text files will work. In practice this means .html and .txt text files are suitable.

## Notes

* Individual words need to be at least two characters to be elgible for matching. The reasoning here is that full names may include initials for middle names.
* If a word maps to multiple values then the matching word will be replaced with [[[...,...,...]]]. For example Mary will be replaced with `[[[1234561,1234562]]]`.
* The script treats html files as if they are plain text.
