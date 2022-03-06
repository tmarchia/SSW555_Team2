"""
   File Name:    US11.py
   Authors:      Alan Clark
   Date:         27 Feb 2022
   Description:  Test the data stored by the Gedcom class in GedcomClass.py.
"""

from GedcomClass import Gedcom
# Need these for data storage
from typing import List, Dict
# For dealing with dates
from datetime import date
# And this for testing
import unittest

class US11Test(unittest.TestCase):
   """ Class for testing Gedcom class """

   MONTHS : dict = {'JAN':1, 'FEB':2, 'MAR':3, 'APR':4, 'MAY':5, 'JUN':6, 'JUL':7, 'AUG':8, 'SEP':9, 'OCT':10, 'NOV':11, 'DEC':12}

   # Create an instance of the class from a GEDCOM data file
   my_fam : Gedcom = Gedcom('amc.ged')

   def string_to_date(self, instring: str) -> date:
      """ Turn a GEDCOM-format date string into a datetime.date """
      # Turn the sub-strings into integers
      d = instring.split()
      # Convert the year into an integer
      d[0] = int(d[0])
      # It could be DD MMM YYYY, or MMM YYYY, or just YYYY.  If necessary,
      # pad it out to DD MMM YYYY, using 28 Jun as the default because it's
      # approximately the middle of the year and every month >= 28 days.
      # THIS IS NOT AN IDEAL SOLUTION.
      # First months...
      if len(d) == 1:
         d.append(6)
      else:
         d[1] = self.MONTHS[d[1]]
      # ...then days.
      if len(d) == 2:
         d.append(28)
      else:
         d[2] = int(d[2])
      return date(d[2], d[1], d[0])
      

   def test_no_bigamy(self):
      """ Verify that there are no overlapping marriages """
      marriages : dict = dict()
      spousal_families : list = list()
      print('\n')
      # Scrutinize each person for the crime of bigamy!
      # Remember, "key" is the person's ID and "person" is a Dict of their data
      for key, person in self.my_fam.people.items():
         spousal_families.clear()
         # Get the list of all families they were a spouse in, if any
         if 'FAMS' in person.keys():
            spousal_families = person['FAMS']
            sex : str = person['SEX']
            # If this person was in more than one marriage, did
            # each marriage end (in death or divorce) before the
            # next one began?
            if len(spousal_families) > 1:
               marriages.clear()
               # Create records of all the marriages
               for fam_id in spousal_families:
                  marriages[fam_id] = {}
                  # Identify the spouse -- we're being very traditional here
                  if self.my_fam.people[key]['SEX'] == 'M':
                     spouse_id = self.my_fam.families[fam_id]['WIFE']
                  else:
                     spouse_id = self.my_fam.families[fam_id]['HUSB']
                  marriages[fam_id]['spouse'] = spouse_id
                  # When did the marriage start?
                  marriages[fam_id]['start'] = self.string_to_date(self.my_fam.families[fam_id]['MARR'])
                  # Trickier question:  When did it end?
                  if 'DIV' in self.my_fam.families[fam_id].keys():
                     marriages[fam_id]['end'] = self.string_to_date(self.my_fam.families[fam_id]['DIV'])
                  elif 'DEAT' in self.my_fam.people[spouse_id]:
                     marriages[fam_id]['end'] = self.string_to_date(self.my_fam.people[spouse_id]['DEAT'])
                     
               # Okay, that's all the marriages of record for this person.
               # Now compare the dates.
               for fam_id1 in spousal_families:
                  print('\nTesting marriages of ' + person['NAME'])
                  for fam_id2 in spousal_families:
                     # Don't compare a family to itself
                     if fam_id1 != fam_id2:
                        print('   Married to ' + marriages[fam_id1]['spouse'])
                        self.assertTrue(marriages[fam_id1]['start'] > marriages[fam_id2]['end'] or\
                                        marriages[fam_id1]['end'] < marriages[fam_id2]['start'])


# This runs all the unittest functions from HW05Test.
# I don't understand how.
if __name__ == '__main__':
   unittest.main(exit=False, verbosity=2)
