from flask import Flask
from mysql.connector import connect
app = Flask(__name__)


def db(sqlquery):
    myhost = 'localhost'
    mydatabase = 'healthInsuranceCompany'
    myuser = 'root'
    mypass = '2510203121'

    con = connect(host=myhost,
                  database=mydatabase,
                  user=myuser,
                  password=mypass)
    cur = con.cursor()
    cur.execute(sqlquery)
    # try:
    #     try:
    #         cur.execute(sqlquery)
    #     # NB : you won't get an IntegrityError when reading
    #     except (Error, Warning) as e:
    #         print('a;sdfjla;lsdjf',e)
    #         return e

    #     try:
    #         user = cur.fetchall()[0]
    #         return user
    #     except TypeError as e:
    #         print('a;ldkfja;ldksfj',e)
    #         return e
    # finally:
    records = cur.fetchall()
    con.commit()
    con.close()
    return records

from company import routes