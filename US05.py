"""
US01
SSW 555
03/05/2022
"""

"""This is a program that checks the dates of a GEDCOM files
and makes sure the marriage date is not after the death of either spouse"""
from time import monotonic, strptime
import datetime

def US05_MarriageBeforeDeath(key, value, husb_info, wife_info):
    """This function checks to make sure the marriage date is not
    after the death of either spouse"""
    if 'MARR' in value:
        marriage_date = value['MARR']
        marriage_date = marriage_date.split()
        day = int(marriage_date[0])
        month = marriage_date[1]
        year = int(marriage_date[2])
        
        #Convert the month from text to number
        month = int(strptime(month,'%b').tm_mon)
        
        #format the date
        marriage_date = datetime.date(year, month, day)
        
        #Get the death date
        for info in [husb_info, wife_info]:
            if 'DEAT' in info:
                death_date = info['DEAT']
                death_date = death_date.split()
                day = int(death_date[0])
                month = death_date[1]
                year = int(death_date[2])

                #Convert the month from text to number
                month = int(strptime(month,'%b').tm_mon)

                #format the date
                death_date = datetime.date(year, month, day)
            
                if marriage_date > death_date:
                    if info['SEX'] == 'M':
                        member = 'husband'
                    else:
                        member = 'wife'
                    print("ERROR US05: Family "+key+" marriage date "+str(marriage_date)+" occurs after the death of "+member+" "+str(death_date))