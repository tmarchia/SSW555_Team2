"""
Main file that will run all of the user stories
"""
from GedcomClass import Gedcom
from US01 import US01_DateBeforeCurrentDate
from US05 import US05_MarriageBeforeDeath

def Main():
    #set up the class based on an input file
    ged : Gedcom = Gedcom('/Users/tylermarchiano/Documents/Stevens/SSW555/Project/User Stories/Input_TylerMarchiano.ged')
    individuals = ged.people.keys()
    families = ged.families.keys()
    
    #Run US01
    for person in individuals:
        key = person
        value = ged.people[person]
        dateTags = ['BIRT', 'DEAT', 'DIV','MARR']
        US01_DateBeforeCurrentDate(key, value)
    
    for family in families:
        key = family
        value = ged.families[family]
        dateTags = ['BIRT', 'DEAT', 'DIV','MARR']
        US01_DateBeforeCurrentDate(key, value)
    
    #Run US05
    for family in families:
        key = family
        value = ged.families[family]
        husb_id = value['HUSB']
        wife_id = value['WIFE']
        husb_info = ged.people[husb_id]
        wife_info = ged.people[wife_id]
        US05_MarriageBeforeDeath(key, value, husb_info, wife_info)

Main()