import random
import string
import traceback
import time
from Common.connections import * 
from Common.models import * 


# GetRandomChar function
def getRandomChar(_upper=False, _len=1):
    if _upper:
        return ''.join(random.choices(string.ascii_uppercase, k=_len))
    else:
        return ''.join(random.choices(string.ascii_lowercase, k=_len))


# GetRandomNumber function
def getRandomNumber(_start=0, _end=9):
    return random.randrange(_start, _end)


# Main function
def main(reqData):
    try:
        PROCESSING_TIME = time.time()*1000
        if not reqData['printDataOnly']:
            session = getPostgresConnections()
        # Generating random data with in the range has been given
        for idx in range(reqData['totalRecordsCount']):
            fname = "{}{}".format(getRandomChar(True, 1), getRandomChar(False, reqData['randomNameLength']))
            lname = "{}{}".format(getRandomChar(True, 1), getRandomChar(False, reqData['randomNameLength']))
            email = "{}.{}@{}.{}".format(fname.lower(), lname.lower(), getRandomChar(False, getRandomNumber(3, 7)), getRandomChar(False, getRandomNumber(2, 3)))
            salary = getRandomNumber(reqData['randomSalaryRange'][0], reqData['randomSalaryRange'][1])
            yearJoined = getRandomNumber(reqData['randomYearRange'][0], reqData['randomYearRange'][1])
            if not reqData['printDataOnly']:
                # Creating employee object
                employee = Employees(
                    id = idx+1,
                    first_name = fname,
                    last_name = lname,
                    email = email,
                    salary = salary,
                    year_joined = yearJoined
                )
                session.add(employee)
            else:
                _dict = {
                    "id": idx+1,
                    "first_name": fname,
                    "last_name": lname,
                    "email": email,
                    "salary": salary,
                    "year_joined": yearJoined
                }
                print(_dict)
        if not reqData['printDataOnly']:
            session.commit()
            session.close()
        print("\nPROCESSING_TIME: {} ms\n".format(round((time.time()*1000 - PROCESSING_TIME), 2) ))
    except Exception as exc:
        traceback.print_exc(exc)
