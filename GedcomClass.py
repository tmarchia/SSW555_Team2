"""
   File Name:    GedcomClass.py
   Authors:      Alan Clark, Timothy Tham, Tyler Marchiano
   Date:         26 Feb 2022
   Description:  Prompt the user for a file name containing GEDCOM data.
                 Parse the data to a Dict of individuals and a Dict of
                 families, each indexed by ID.
"""

# For access to sys.exit() function
import sys
# Need these for data storage
from typing import List, Dict

class Gedcom:
   """ A class for reading data from a GEDCOM file into a pair of Dict structures """

   # Valid tags for individual records and family records
   PEOPLE_TAGS = ['NAME', 'BIRT', 'DEAT', 'DATE', 'SEX', 'FAMC', 'FAMS']
   FAMILY_TAGS = ['HUSB', 'WIFE', 'MARR', 'DIV', 'DATE', 'CHIL']

   # Create an empty Dict for individuals, and another for families.
   people : dict = dict()
   families : dict = dict()
      
   def __init__(self, fname: str) -> None:
      """ Function to initialize an instance of the Gedcom class """
      # Try to create a handle to the GEDCOM file
      try:
         fhandle = open(fname)
      except:
         print('Cannot open file:  ' + fname)
         # Because using just exit() spawns a traceback error message
         sys.exit()

      # Status flags
      add_family : bool = False
      add_person : bool = False
      date_birth : bool = False
      date_death : bool = False
      date_marriage : bool = False
      date_divorce : bool = False

      # Use the file handle to scan the file line by line
      for line in fhandle:
         # Strip away any trailing whitespace characters.  If what's left
         # is non-empty, try to process it as valid.
         line = line.strip()
         if len(line) > 0:
            try:
               # Split it into an array of arguments
               word_array = line.split()

               # Look for the start of an individual or family record
               if word_array[0] == '0' and len(word_array) > 2:
                  
                  if word_array[2] == 'INDI':
                     # Start an empty dict for this person
                     identifier = word_array[1]
                     self.people[identifier] = {}
                     # Set the loop-control flags
                     add_person = True
                     add_family = False
                     
                  elif word_array[2] == 'FAM':
                     # Start an empty dict for this family
                     identifier = word_array[1]
                     self.families[identifier] = {}
                     # Set the loop-control flags
                     add_family = True
                     add_person = False

               # Continue collecting data for an individual
               elif add_person and len(word_array) > 1:
                  tag = word_array[1]
                  if tag in self.PEOPLE_TAGS:
                     if tag == 'BIRT':
                        # The next line will have the date
                        date_birth = True
                     elif tag == 'DEAT':
                        # The next line will have the date
                        date_death = True
                     else:
                        # Turn everything after the tag into a space-separated string
                        input_string = word_array[2]
                        for word in word_array[3:]:
                           input_string = input_string + ' ' + word
                        # If this is a date we were waiting for, store it
                        # and clear its flag
                        if date_birth and tag == 'DATE':
                           self.people[identifier]['BIRT'] = input_string
                           date_birth = False
                        elif date_death and tag == 'DATE':
                           self.people[identifier]['DEAT'] = input_string
                           date_death = False
                        # Add a family this person started
                        elif tag == 'FAMS':
                           if not 'FAMS' in self.people[identifier]:
                              self.people[identifier]['FAMS'] = list()
                           self.people[identifier]['FAMS'].append(input_string)
                        # If it's other data, just store it
                        else:
                           self.people[identifier][tag] = input_string
                     
               # Continue collecting data for a family
               elif add_family and len(word_array) > 1:
                  tag = word_array[1]
                  if tag in self.FAMILY_TAGS:
                     if tag == 'MARR':
                        # The next line will have the date
                        date_marriage = True
                     elif tag == 'DIV':
                        # The next line will have the date
                        date_divorce = True
                     else:
                        # Turn everything after the tag into a space-separated string
                        input_string = word_array[2]
                        for word in word_array[3:]:
                           input_string = input_string + ' ' + word
                        # If this is a date we were waiting for, store it
                        # and clear its flag
                        if date_marriage and tag == 'DATE':
                           self.families[identifier]['MARR'] = input_string
                           date_marriage = False
                        elif date_divorce and tag == 'DATE':
                           self.families[identifier]['DIV'] = input_string
                           date_divorce = False
                        # Add a child, starting the list of children for this
                        # family if there isn't one yet
                        elif tag == 'CHIL':
                           if not 'CHIL' in self.families[identifier]:
                              self.families[identifier]['CHIL'] = list()
                           self.families[identifier]['CHIL'].append(input_string)
                        # If it's other valid data, just store it
                        else:
                           self.families[identifier][tag] = input_string

            except:
               print('\nERROR:  File ' + fname + ' contains invalid data\n')
               sys.exit()

   def display_people(self):
      """ Print the contents of the Dict that has details of each individual """
      print('\nPEOPLE:')
      for key, value in self.people.items():
         print(key, ':  ', value)

   def display_families(self):
      """ Print the contents of the Dict that has details of each family """
      print('\nFAMILIES:')
      for key, family_list in self.families.items():
         print('Family', key, ':  ', family_list)
