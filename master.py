import GenerateRandomDataSQL.generateRandomDataSQL as generateRandomDataSQL


if __name__ == '__main__':
    # Required configuration to generate random data for SQL database
    reqData = {
        'printDataOnly': True,
        'totalRecordsCount': 10**3,
        'randomNameLength': 4,
        'randomSalaryRange': [700000, 70000000],
        'randomYearRange': [1900, 2050]
    }
    generateRandomDataSQL.main(reqData)
