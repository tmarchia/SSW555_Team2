"""
   File Name:   US12.py
   Authors:      Alan Clark
   Date:         7 Mar 2022
   Description:  Test the data stored by the Gedcom class in GedcomClass.py.
"""

from GedcomClass import Gedcom
# Need these for data storage
from typing import List, Dict
# For dealing with dates
from datetime import date, timedelta
# And this for testing
import unittest

class US12Test(unittest.TestCase):
   """ Class for testing Gedcom class """

   MONTHS : dict = {'JAN':1, 'FEB':2, 'MAR':3, 'APR':4, 'MAY':5, 'JUN':6, 'JUL':7, 'AUG':8, 'SEP':9, 'OCT':10, 'NOV':11, 'DEC':12}
   # Timedelta doesn't support "years" because leap years
   SIXTY_YEARS  : timedelta = timedelta(days = 60*365)
   EIGHTY_YEARS : timedelta = timedelta(days = 80*365)

   # Create an instance of the class from a GEDCOM data file
   my_fam : Gedcom = Gedcom('amc.ged')
   print('\n')
   # Debug purposes only
   #my_fam.display_people()
   #my_fam.display_families()

   def string_to_date(self, instring: str) -> date:
      """ Turn a GEDCOM-format date string into a datetime.date """
      # Split into sub-strings
      d = instring.split()
      # Convert to integers.
      # It could be DD MMM YYYY, or MMM YYYY, or just YYYY.  If necessary,
      # pad it out to DD MMM YYYY, using 28 Jun as the default because it's
      # approximately the middle of the year and every month >= 28 days.
      # THIS IS NOT AN IDEAL SOLUTION.
      if len(d) == 1:
         d = [28, 6, int(d[0])]
      elif len(d) == 2:
         d = [28, self.MONTHS[d[0]], int(d[1])]
      else:
         d = [int(d[0]), self.MONTHS[d[1]], int(d[2])]
      # Pass it to the date method in (y, m, d) order
      return date(d[2], d[1], d[0])
      

   def test_parents_not_too_old(self):
      """ Test parental ages in GedcomClass.py structures """
      print('\n')
      # For each individual...
      #for key, person in self.my_fam.people.items():
      for key, person in self.my_fam.people.items():
         # Does this person have a family of origin and date of birth?
         if 'FAMC' in person.keys() and 'BIRT' in person.keys():
            # Record them
            child_date : date = self.string_to_date(person['BIRT'])
            family_id : str = person['FAMC']
            # Get and test mother's data
            if 'WIFE' in self.my_fam.families[family_id].keys():
               mother_id = self.my_fam.families[family_id]['WIFE']
               mom_date : date = self.string_to_date(self.my_fam.people[mother_id]['BIRT'])
               print('Testing child ' + key + ' of mother ' + mother_id)
               self.assertTrue(child_date - mom_date < self.SIXTY_YEARS)
            # Get and test father's data
            if 'HUSB' in self.my_fam.families[family_id].keys():
               father_id = self.my_fam.families[family_id]['HUSB']
               dad_date : date = self.string_to_date(self.my_fam.people[father_id]['BIRT'])
               print('Testing child ' + key + ' of father ' + father_id)
               self.assertTrue(child_date - dad_date < self.EIGHTY_YEARS)


# This runs all the unittest functions from the test class.
# I don't understand how.
if __name__ == '__main__':
   unittest.main(exit=False, verbosity=2)
