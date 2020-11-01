import mysql.connector
# from docutils.nodes import status
from ldap3 import Server, Connection, ALL, SIMPLE, MODIFY_REPLACE
import json
import re
from ldap3.core.exceptions import LDAPException

# from ldap3.core.exceptions import LDAPException
from ldap3.core import exceptions

# Connect to SQL Server:
mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="root1root!",
    auth_plugin='mysql_native_password',
    database="hermod"
)

mycursor = mydb.cursor()

# Connect to AD Server:
server = Server('WIN-P4OIJVR2QDN', get_info=ALL)

conn = Connection(server, user="CN=Administrator,CN=Users,DC=ittaster,DC=local", password="Aa123456",
                  authentication=SIMPLE, auto_bind=True)

userlist = ["mdn", "networkName", "accountId", "subscriptionType", "payType", "corporateName", "subsClientType",
            "pairingInd", "addPackageInfo"]


class Message:

    def __init__(self, m: str):
        self.user = eval(m)

        self.Response = '{"statusCode": "0","message": ""}'
        self.JSONResponse = eval(self.Response)

    def CheckMdn(self):

        if re.search('\d{' + f'{len(self.user["mdn"])}' + '}', self.user["mdn"]) and 11 <= len(
                self.user["mdn"]) < 17:
            return 1

        if re.search('\+\d{' + f'{len(self.user["mdn"]) - 1}' + '}', self.user["mdn"]) and 12 <= len(
                self.user["mdn"]) < 18:
            self.user["mdn"] = self.user["mdn"][1::]
            return 1
        return 0

    def CheckSyntext(self):

        if Message.CheckMdn(self.mdn):
                return 1

        self.JSONResponse["statusCode"] = 1
        self.JSONResponse["message"] = "syntext error "
        self.Response = json.dumps(self.JSONResponse)
        return 0

    def GetUsers(self):
        self.JSONResponse["message"] = "\n\nActive Directory Users: \n"
        conn.search('DC=ittaster,DC=local', '(objectClass=person)')

        for i in range(len(conn.entries)):
            self.JSONResponse["message"] = self.JSONResponse["message"] + conn.entries[i].entry_dn + "\n"

        self.JSONResponse["message"] = self.JSONResponse["message"] + "\nSQL Users: \n"
        mycursor.execute("SELECT mdn FROM hermod.users")
        myresult = mycursor.fetchall()

        for i in range(len(myresult)):
            self.JSONResponse["message"] = self.JSONResponse["message"] + myresult[i][0] + "\n"

    def Create(self):

        statusAD = Message.CreateUserAD(self)
        statusSQL = Message.CreateUserSQL(self)

        if not statusAD:
            self.JSONResponse["statusCode"] = 201
            self.JSONResponse["message"] = f"User {self.user['mdn']} already exist on AD server, "

        if not statusSQL:
            self.JSONResponse["statusCode"] = 201
            self.JSONResponse["message"] = self.JSONResponse["message"] + f"User {self.user['mdn']} already exist on " \
                                                                          f"SQL server"
        if self.JSONResponse["message"] == "":
            self.JSONResponse["message"] = "success"

        self.Response = json.dumps(self.JSONResponse)

    def Delete(self):
        statusAD = Message.DeleteUserAD(self)
        statusSQL = Message.DeleteUserSQL(self)

        if not statusAD:
            self.JSONResponse["statusCode"] = 201
            self.JSONResponse["message"] = f"User {self.user['mdn']} isn't exist on AD server, "
        if not statusSQL:
            self.JSONResponse["statusCode"] = 201
            self.JSONResponse["message"] = self.JSONResponse["message"] + f"User {self.user['mdn']} isn't exist on " \
                                                                          f"SQL server"
        if self.JSONResponse["message"] == "":
            self.JSONResponse["message"] = "success"

        self.Response = json.dumps(self.JSONResponse)

    def Update(self):
        try:
            statusAD = Message.UpdateUserAD(self)
            statusSQL = Message.UpdateUserSQL(self)

            if not statusAD:
                self.JSONResponse["statusCode"] = 201
                self.JSONResponse["message"] = f"User {self.user['mdn']} isn't exist on AD server, "
            if not statusSQL:
                self.JSONResponse["statusCode"] = 201
                self.JSONResponse["message"] = self.JSONResponse["message"] + f"User {self.user['mdn']} isn't exist on " \
                                                                              f"SQL server"
            if self.JSONResponse["message"] == "":
                self.JSONResponse["message"] = "success"

            self.Response = json.dumps(self.JSONResponse)
        except LDAPException as e:
            print(e)
            self.JSONResponse["statusCode"] = 201
            self.JSONResponse["message"] = "AD server is lost"

    def CreateUserSQL(self):
        for x in userlist:
            if x not in self.user:
                userlist.remove(x)

        sql = "INSERT INTO hermod.users ("
        val = ()
        for x in userlist:
            sql = sql + x + ", "
            val = val + (self.user[x],)
        sql = (sql[0:-2] + ") VALUES (" + len(userlist) * "%s, ")[0:-2] + ") "

        try:
            mycursor.execute(sql, val)
        except mysql.connector.errors.IntegrityError:
            print(f"User {self.user['mdn']} already exist on SQL server")
            return 0

        mydb.commit()

        if mycursor.rowcount == 1:
            print(f"User {self.user['mdn']} as been create on SQL server")
            return 1

    def CreateUserAD(self):
        # check if all attributes exist if not put ""
        for x in userlist:
            if x not in self.user:
                self.user[x] = ""

        if not conn.add(f"CN={self.user['mdn']},CN=Users,DC=ittaster,DC=local", 'User',
                        {
                            # 'networkName': {self.user['networkName']},
                            'accountId': {self.user['accountId']},
                            'subscriptionType': {self.user['subscriptionType']},
                            'payType': {self.user['payType']},
                            'corporateName': {self.user['corporateName']},
                            'subsClientType': {self.user['subsClientType']},
                            'pairingInd': {self.user['pairingInd']},
                            'addPackageInfo': {self.user['addPackageInfo']},
                        }):
            print(f"User {self.user['mdn']} is already exists on AD")

            return 0
        else:
            print(f"User {self.user['mdn']} is created on AD")
            return 1

    def DeleteUserSQL(self):
        sql = f"DELETE FROM hermod.users WHERE mdn = {self.user['mdn']}"

        mycursor.execute(sql)

        mydb.commit()

        if mycursor.rowcount == 1:
            print(f"User {self.user['mdn']} as been delete from SQL server")
            return 1
        print(f"User {self.user['mdn']} isn't exists on SQL server")
        return 0

    def DeleteUserAD(self):

        if not conn.delete(f"CN={self.user['mdn']},CN=Users,DC=ittaster,DC=local"):
            print(f"The user {self.user['mdn']} isn't exists on AD Server")
            return 0

        else:
            print(f"The user {self.user['mdn']} is deleted from AD Server")
            return 1

    def UpdateUserSQL(self):

        mycursor.execute(f"SELECT * FROM hermod.users WHERE mdn = {self.user['mdn']}")
        myresult = mycursor.fetchall()
        if len(myresult) == 0:
            print(f"User {self.user['mdn']} isn't exist on SQL server")
            return 0

        userlist = ["mdn", "networkName", "accountId", "subscriptionType", "payType", "corporateName", "subsClientType",
                    "pairingInd", "addPackageInfo"]

        userlist.remove("mdn")
        for x in userlist:
            if x not in self.user:
                userlist.remove(x)
        for x in userlist:
            sql = f"UPDATE hermod.users SET {x} = '{self.user[x]}' WHERE mdn = {self.user['mdn']}"

            mycursor.execute(sql)

            mydb.commit()
            # if mycursor.rowcount == 1:
            # print(x + " as been changed on SQL server")
        print(f"User {self.user['mdn']} is Modified on SQL Server")
        return 1

    def UpdateUserAD(self):
        for x in userlist:
            if x not in self.user:
                if not conn.modify(f"CN={self.user['mdn']},CN=Users,DC=ittaster,DC=local",
                                   {userlist[x]: [(MODIFY_REPLACE, [self.user[userlist[x]]])]}):
                    print(f"User {self.user['mdn']} isn't exist on AD Server")
                    return 0

        else:
            print(f"User {self.user['mdn']} is Modified on AD Server")
            return 1
