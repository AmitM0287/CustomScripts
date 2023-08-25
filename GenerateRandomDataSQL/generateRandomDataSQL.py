import random
import string
import traceback
import time
import threading
from Common.connections import * 
from Common.models import * 
from sqlalchemy import func 


# GetRandomChar function
def getRandomChar(_upper=False, _len=1):
    if _upper:
        return ''.join(random.choices(string.ascii_uppercase, k=_len))
    else:
        return ''.join(random.choices(string.ascii_lowercase, k=_len))


# GetRandomNumber function
def getRandomNumber(_start=0, _end=9):
    return random.randrange(_start, _end+1)


def getMaxID(session):
    maxID = session.query(func.coalesce(func.max(Employees.id), 0)).first()
    return maxID[0]


def generateRandomData(configData, idxStart, idxEnd):
    if configData['writeData']:
        session = getPostgresConnections()
    # Generating random data with in the range has been given
    for idx in range(idxStart, idxEnd):
        fname = "{}{}".format(getRandomChar(True, 1), getRandomChar(False, configData['randomNameLength']))
        lname = "{}{}".format(getRandomChar(True, 1), getRandomChar(False, configData['randomNameLength']))
        email = "{}.{}@{}.{}".format(fname.lower(), lname.lower(), getRandomChar(False, getRandomNumber(3, 7)), getRandomChar(False, getRandomNumber(2, 3)))
        salary = getRandomNumber(configData['randomSalaryRange'][0], configData['randomSalaryRange'][1])
        yearJoined = getRandomNumber(configData['randomYearRange'][0], configData['randomYearRange'][1])
        if configData['writeData']:
            # Creating employee object
            employee = Employees(
                id = idx,
                first_name = fname,
                last_name = lname,
                email = email,
                salary = salary,
                year_joined = yearJoined
            )
            session.add(employee)
        if configData['printData']:
            _dict = {
                "id": idx,
                "first_name": fname,
                "last_name": lname,
                "email": email,
                "salary": salary,
                "year_joined": yearJoined
            }
            print(_dict)
    if configData['writeData']:
        session.commit()
        session.close()
    time.sleep(configData['sleepTimeSec'])


# Main function
def main(configData):
    try:
        PROCESSING_TIME = time.time()*1000
        print("\nSCRIPT STARTED ...")

        maxID = 0
        if configData['writeData']:
            session = getPostgresConnections()
            maxID = getMaxID(session)
            session.close()

        eachWorkerTaskCount = configData['totalRecordsCount'] // configData['totalWorkers']
        extraTaskCount = 0
        if configData['totalRecordsCount'] != configData['totalRecordsCount'] * configData['totalWorkers']:
            extraTaskCount = configData['totalRecordsCount'] - (eachWorkerTaskCount * configData['totalWorkers'])
        
        print("\nTotal task count: {}".format(configData['totalRecordsCount']))
        print("\nTotal workers planned: {}".format(configData['totalWorkers']))
        print("\nEach worker task count: {}".format(eachWorkerTaskCount))
        taskList = []
        idxStart = maxID + 1
        idxEnd = eachWorkerTaskCount + maxID + 1

        # Assign tasks to wrokers
        for workerID in range(configData['totalWorkers']):
            print("\nworker {} => {} to {} [{}]".format(workerID+1, idxStart, idxEnd, (idxEnd-idxStart)))
            worker = threading.Thread(target=generateRandomData, args=(configData, idxStart, idxEnd))
            taskList.append(worker)
            taskList[-1].start()
            if workerID == configData['totalWorkers']-1:
                break
            idxStart += eachWorkerTaskCount
            idxEnd += eachWorkerTaskCount
            time.sleep(configData['sleepTimeSec'])
        
        # Collecting all tasks
        for task in taskList:
            task.join()
        
        # Doing extra task if any
        if extraTaskCount != 0:
            print("\nExtra task count: {} => {} to {} ".format(extraTaskCount, idxStart, idxEnd+extraTaskCount))
            generateRandomData(configData, idxStart, idxEnd)
        
        print("\nPROCESSING_TIME: {} ms\n".format(round((time.time()*1000 - PROCESSING_TIME), 2) ))
    except Exception as exc:
        traceback.print_exc(exc)
