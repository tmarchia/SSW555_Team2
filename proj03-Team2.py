"""
   File Name:    proj03-Team2.py
   Authors:      Alan Clark, Timothy Tham, Tyler Marchiano
   Date:         20 Feb 2022
   Description:  Prompt the user for a file name containing GEDCOM data.
                 Parse the data to a Dict of individuals and a Dict of
                 families, each indexed by ID.
"""

# For sys.exit()
import sys
from typing import List, Dict

# Currently not using this
valid_tags = ['INDI', 'NAME', 'SEX', 'BIRT', 'DEAT', 'FAMC', 'FAMS', 'FAM', 'MARR', 'HUSB', 'WIFE', 'CHIL', 'DIV', 'DATE', 'HEAD', 'TRLR', 'NOTE']

# Prompt for the input file and create a handle to it.
fname = input('\nEnter the name of the GEDCOM file:  ')
try:
   fhandle = open(fname)
except:
   print('Cannot open file:  ' + fname)
   # Because using just exit() spawns a traceback error message
   sys.exit()

# Create an empty Dict for names of individuals, and another for members of families.
people : Dict[str, str] = dict()
families : Dict[str, list] = dict()
# Status flags
add_family : bool = False
add_person : bool = False

# Use the file handle to scan the file line by line
for line in fhandle:
   # Strip away any trailing whitespace characters.  If what's left
   # is non-empty, try to treat it as valid.
   line = line.strip()
   if len(line) > 0:
      try:
         # Split it into an array of arguments
         word_array = line.split()

         # Kluge:  Skip lines with too few arguments
         if len(word_array) >= 3:

            # If this is the start of a new individual record, get the ID
            if word_array[0] == '0' and word_array[2] == 'INDI':
               add_person = True
               add_family = False
               identifier = word_array[1]
               
            # Or the start of a new family record, ditto
            elif word_array[0] == '0' and word_array[2] == 'FAM':
               add_family = True
               add_person = False
               identifier = word_array[1]
               # Create an empty list for this family
               families[identifier] = []
               
            # Or, if we're looking for a person's name
            elif add_person == True:
               # Is this it?
               if word_array[0] == '1' and word_array[1] == 'NAME':
                  # Turn any arguments after the first two into a name string
                  name: str = ''
                  for word in word_array[2:]:
                     name = name + word + ' '
                  # Record the name, minus any trailing spaces
                  people[identifier] = name.strip()
                  add_person = False
                  
            # Or, if we're collecting data for a family
            elif add_family == True:
               # Is this a person's ID?
               if word_array[0] == '1' and word_array[1] in ['HUSB', 'WIFE', 'CHIL']:
                  # Add this person's identifier (word_array[2]) to the list for this family.
                  families[identifier].append(word_array[2])

      except:
         print('\nERROR:  File ' + fname + ' contains invalid data\n')
         sys.exit()


# Show what we have

print('\nPEOPLE:')
for key, value in people.items():
   print(key, ':  ', value)

print('\nFAMILIES:')
for key, family_list in families.items():
   print('Family', key, ':  ', family_list)

