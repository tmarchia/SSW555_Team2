"""
Main file that will run all of the user stories
"""
from GedcomClass import Gedcom
from US01 import US01_DateBeforeCurrentDate

def Main():
    ged : Gedcom = Gedcom('/Users/tylermarchiano/Documents/Stevens/SSW555/Project/User Stories/Input_TylerMarchiano.ged')
    individuals = ged.people.keys()
    families = ged.families.keys()
    
    #Run US01
    for person in individuals:
        key = person
        value = ged.people[person]
        dateTags = ['BIRT', 'DEAT', 'DIV','MARR']
        if any(tag in value for tag in dateTags):
            US01_DateBeforeCurrentDate(key, value)
    
    for family in families:
        key = family
        value = ged.families[family]
        dateTags = ['BIRT', 'DEAT', 'DIV','MARR']
        if any(tag in value for tag in dateTags):
            US01_DateBeforeCurrentDate(key, value)

Main()