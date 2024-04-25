
import os

import pyodbc

def get_data(num):
    server = os.environ.get('SERVER')
    database = os.environ.get('DATABASE')
    username = os.environ.get('NAME')
    password = os.environ.get('PASSWORD')

    num = str(num[1:])
    conn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = conn.cursor()

    cursor.execute(f"""SELECT * FROM user_demographics WHERE user_demographics.Phone_Number_1 = {num}""")

    row = cursor.fetchone()

    print(row)

    if row:
        return True, row[12]
    else:
        # print("NO PHONE NUMBER 1")
        cursor.execute(f"""SELECT * FROM user_demographics WHERE user_demographics.Phone_Number_2 = {num}""")
        row = cursor.fetchone()
        if row:
            return True, row[11]

        return False, 0

if __name__ == "__main__":
    num = "+27822205729"
    # num = "+27639447541"
    print(get_data(num))
