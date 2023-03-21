import maskpass
import mysql.connector
import re

config = {
    'user': 'root',
    'password': 'Shubhankar@123',
    'host': 'localhost',
    'database': 'PythonTraining'
}

conn = mysql.connector.connect(**config)
if (conn.is_connected()):
    print("connection estabilished")
else:
    print("connection not estabilished")


def getData():
    validEmail = False
    validMobile = False
    validPassword = False
    User_name = input("User name : ")
    First_name = input("First Name : ")
    Middle_name = input("Middle Name : ")
    Last_name = input("Last Name : ")
    while(validEmail!=True):
        email = input("Email ID : ")
        if(check_email(email)):
            validEmail = True
        else:
            print("Invalid Email")
            validEmail=False
            
    Address = input("Address : ")
    CountryCode = input("Country Code : ")
    while(validMobile!=True):
        mobile_number = input("Mobile Number : ")
        if(number_validation(mobile_number)):
            validMobile=True
        else:
            print("Invalid Mobile Number")
            validMobile = False

    while(validPassword != True):
        password = maskpass.askpass(prompt="Password :", mask="*")
        confirm_password = maskpass.askpass(prompt="Confirm Password :", mask="*")
        if (password_validation(password, confirm_password)):
            validPassword = True
            tuple = (User_name,First_name,Middle_name,Last_name,email,Address,CountryCode,mobile_number,password)
            database_insertion(tuple)
        else:
            print("Password and Confirm Password doesn't match")
            validPassword = False
    mainMenu()

# email validation


def check_email(email):
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if (re.fullmatch(pattern, email)):
        return True
    else:
        return False

# mobile number validation


def number_validation(phone_number):
    pattern1 = re.compile(r'^\+?91[\-\s][6-9]\d{9}$')
    pattern2 = re.compile(r'^\+?91[6-9]\d{9}$')
    pattern3 = re.compile(r'^[6-9]\d{9}$')

    # Check if the phone number matches the pattern
    if pattern1.match(phone_number):
        return True
    elif pattern2.match(phone_number):
        return True
    elif pattern3.match(phone_number):
        return True
    else:
        return False


# password validation
def password_validation(password, confirmPassword):
    if (password == confirmPassword):
        return 1
    else:
        return 0


def database_insertion(tuple):
    sql = 'INSERT INTO records(recordsUserName,recordsFirstName,recordsMiddleName,recordsLastName,recordsEmail,recordsAddress,recordsCountryCode,recordsMobileNumber,recordsPassword) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)'

    # establishing cursor : a tempory space
    myCursor = conn.cursor()

    # executing querry
    myCursor.execute(sql, tuple)

    conn.commit()
    print(myCursor.rowcount, "rows inserted")
    # closing cursor
    myCursor.close()
    # closing connection




def login():
    print("\n\n********** Welcome to Login**********")
    print(" ")
    print("Please enter username and password to login \n")

    # select querry for database
    select_query = "SELECT * FROM records WHERE recordsUserName=%s AND recordsPassword=%s"
    username = input("Enter your username : ")
    password = maskpass.askpass(prompt="Enter your Password :", mask="*")
    
    myCursor = conn.cursor()
    myCursor.execute(select_query, (username,password))
    x=myCursor.fetchall()
    if(x):
        print("Login Success")
    else:
        print("Sorry ! Login failed")
    myCursor.close()

    mainMenu()




def mainMenu():
    print('''\n\n************Hello Guest*************
    1 - Press 1 if already a user : Login
    2 - Press 2 to sign up as a new user : Sign up\n\n''')

    choice = int(input("Enter your choice : "))

    if(choice == 1):
        login()
    elif(choice == 2):
        getData()
    else:
        print("Wrong Choice")



mainMenu()
conn.close()