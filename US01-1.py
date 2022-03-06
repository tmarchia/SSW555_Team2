"""
US01
SSW 555
03/05/2022
"""

"""This is a program that checks the dates of a GEDCOM files
and makes sure the dates are not after the current date"""
from time import monotonic, strptime
import datetime

def US01_DateBeforeCurrentDate(key, value):
    """This function checks to make sure their
    are no dates before the current date"""
    
    #Get the current date
    today = datetime.date.today()    
    
    for tag in ['BIRT', 'DEAT', 'DIV','MARR']:
        if tag in value:
            gedcomDate = value[tag]
            
            #Separate the day, month and year from the input
            gedcomDate = gedcomDate.split()
            day = int(gedcomDate[0])
            month = gedcomDate[1]
            year = int(gedcomDate[2])
            
            #Convert the month from text to number
            month = int(strptime(month,'%b').tm_mon)
            
            gedcomDate = datetime.date(year, month, day)
            
            if gedcomDate > today:
                if tag == 'BIRT':
                    tag = 'BIRTH'
                elif tag == 'DEAT':
                    tag = 'DEATH'
                elif tag == 'DIV':
                    tag = 'DIVORCE'
                elif tag == 'MARR':
                    tag = 'MARRIAGE'
                print("ERROR US01: "+tag+ " date of "+key+" occurs in the future")