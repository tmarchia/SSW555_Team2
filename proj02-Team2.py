"""
   File Name:    proj02-Team2.py
   Authors:      Alan Clark, Timothy Tham, Tyler Marchiano
   Date:         20 Feb 2022
   Description:  Prompt the user for a file name containing GEDCOM data.
                 Output each line of data followed by a marked-up version
                 of that line.
"""

# For sys.exit()
import sys

valid_tags = ['INDI', 'NAME', 'SEX', 'BIRT', 'DEAT', 'FAMC', 'FAMS', 'FAM', 'MARR', 'HUSB', 'WIFE', 'CHIL', 'DIV', 'DATE', 'HEAD', 'TRLR', 'NOTE']

# Prompt for the input file
fname = input('\nEnter the name of the GEDCOM file:  ')
try:
   fhandle = open(fname)
except:
   print('Cannot open file:  ' + fname)
   # Because using just exit() spawns a traceback error message
   sys.exit()

# Use the file handle to scan the file line by line
for line in fhandle:
   # Strip away any trailing whitespace characters.  If what's left
   # is non-empty, try to treat it as valid.
   line = line.strip()
   if len(line) > 0:
      try:
         # Split it into an array of arguments
         word_array = line.split()
         
         # Print the raw input line
         print('--> ' + line)
         
         # Get level and tag
         level: str = word_array[0]
         tag: str = word_array[1]
         # Is this a valid tag?
         if tag in valid_tags:
            valid: str = 'Y'
         else:
            valid: str = 'N'
         # Turn any arguments after the first two into a string
         arguments: str = ''
         for word in word_array[2:]:
            arguments = arguments + word + ' '

         # Print the marked-up line
         print('<-- ' + level + '|' + tag + '|' + valid + '|' + arguments.strip())

      except:
         print('\nERROR:  File ' + fname + ' contains invalid data\n')
         sys.exit()
