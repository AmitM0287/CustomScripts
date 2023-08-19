import random
import string
import traceback
from common.connections import * 

# GetRandomChar function
def getRandomChar(_upper=True, _len=1):
    if _upper:
        return ''.join(random.choices(string.ascii_uppercase, k=_len))
    else:
        return ''.join(random.choices(string.ascii_lowercase, k=_len))


# GetRandomNumber function
def getRandomNumber(_start=0, _end=9):
    return random.randrange(_start, _end)


# Main function
def main():
    session = getPostgresConnections()
    employee = {
    }
    print(session)

