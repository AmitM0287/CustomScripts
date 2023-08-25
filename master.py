import GenerateRandomDataSQL.generateRandomDataSQL as generateRandomDataSQL


if __name__ == '__main__':
    # Required configuration to generate random data for SQL database
    configData = {
        'printData': False,
        'writeData': False,
        'totalRecordsCount': 10**7, # 1B = 10^9  1M = 10^6 
        'randomNameLength': 4,
        'randomSalaryRange': [700000, 70000000],
        'randomYearRange': [1900, 2050],
        'sleepTimeSec': 1,
        'totalWorkers': 8
    }
    generateRandomDataSQL.main(configData)
