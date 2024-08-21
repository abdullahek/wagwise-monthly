
import os
import pyodbc


def del_from_db(num):
    server = os.environ.get('SERVER')
    database = os.environ.get('DATABASE')
    username = os.environ.get('NAME')
    password = os.environ.get('PASSWORD')

    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 18 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM users where number={num}")

    row = cursor.fetchone()
    id = row[0]
    if row:
        cursor.execute(f"DELETE FROM baseline_answers WHERE user_id = {id}")
        cursor.execute(f"DELETE FROM monthly_answers WHERE user_id = {id}")
        cursor.execute(f"DELETE FROM users WHERE id = {id}")
        cursor.commit()

def update_response(msg, num):
    server = os.environ.get('SERVER')
    database = os.environ.get('DATABASE')
    username = os.environ.get('NAME')
    password = os.environ.get('PASSWORD')

    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 18 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    cursor = conn.cursor()
    cursor.execute(f"UPDATE Campaign_Responses SET Responses = ? WHERE PhoneNumber = ?", (msg, int(num)))
    conn.commit()
    cursor.close()
    conn.close()
    print(msg)
    print(num)
    return True 
def validate_num(num):
    print(num)
    server = os.environ.get('SERVER')
    database = os.environ.get('DATABASE')
    username = os.environ.get('NAME')
    password = os.environ.get('PASSWORD')

    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 18 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
  
  
    cursor = conn.cursor()

    cursor.execute("SELECT PhoneNumber, ID FROM Campaign_Responses WHERE PhoneNumber=?", (num,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    print(row)    
   
    if not row:
        return False
    else:
         return True


def get_data_ud(num, cursor):

    num = str(num[1:])


    cursor.execute(f"""SELECT * FROM user_demographics WHERE user_demographics.Phone_Number_1 = {num}""")

    row = cursor.fetchone()


    if not row:
        cursor.execute(f"""SELECT * FROM user_demographics WHERE user_demographics.Phone_Number_2 = {num}""")
        row = cursor.fetchone()
        # print(row)
        return row[8]

    return row[8]

            # print(f"User: {id} with number {num} not in demos")

if __name__ == "__main__":
    server = os.environ.get('SERVER')
    database = os.environ.get('DATABASE')
    username = os.environ.get('NAME')
    password = os.environ.get('PASSWORD')


    conn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users where id>400")

    rows = cursor.fetchall()

    # row = cursor.fetchone()
    # print(row[1])
    # get_data_ud(row[0], row[1], cursor)
    count = 1

    for row in rows:
        print(count)
        print(f"User_id: {row[0]}")
        get_data_ud(row[0], row[1], cursor)
        count +=1

