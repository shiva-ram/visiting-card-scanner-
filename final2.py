#importing libraries
import sys
import cv2
import pytesseract
import re
import sqlite3
from PIL import Image

#Getting the image data
image_fullpath=sys.argv[1]
image_name=sys.argv[2]
img= Image.open(str(image_fullpath))
# image_save_path=image_fullpath.replace(image_name,"temp.png")
# img.rotate(90).convert("LA").save(image_save_path)
# print("/media/temp.png")

#location of pytesseract file
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

#converting image to text
text=pytesseract.image_to_string(img)
# print(text)

# This is to get each line as a seperate text
text_lst = text.splitlines() 
text_lst = [word for word in text_lst if len(word)!= 0]

#functions to identify different fields
def get_full_name(lst):
    for idx in lst:
        full_name = re.match(r"(?P<first_name>\w+) (?P<last_name>\w+)", idx)
        if full_name is not None:
            return idx

def get_email(lst):
    for idx in lst:
        mail = re.search(r'[\w\.-]+@[\w\.-]+', idx)
        if mail is not None:
            return idx

def get_phone_number(lst):
    for idx in lst:
        for i in range(0, len(idx)):
            if idx[i][0] == "+":
                return idx
            elif idx[i][0] == "0":
                return idx



#Assagning values to variables
Name=get_full_name(text_lst)
Telephone=get_phone_number(text_lst)
Email=get_email(text_lst)
print(Name)
print(Telephone)
print(Email)

#inserting values into sqllite database

def insertVaribleIntoTable( name, phone, email):
    try:
        sqliteConnection = sqlite3.connect('python.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_insert_with_param = """INSERT INTO SqliteDb_developers
                          ( name,phone, email) 
                          VALUES ( ?, ?, ?);"""

        data_tuple = ( name,phone, email)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqliteConnection.commit()
        print("Python Variables inserted successfully into SqliteDb_developers table")

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed")

insertVaribleIntoTable( Name, Telephone, Email)
