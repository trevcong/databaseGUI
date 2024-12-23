#Created by Trevor Conger & Luis Amador
#Database Python GUI
#Useable by students and admins of a school
#DATE: 12/19/24
import sqlite3
import re
import datetime

#StudentDatabase class:
#This class will serve as the database helper class
class StudentDatabase:
    #CONSTRUCTOR
    #name of DATABASE defaults to DB='stundents.db'
    #Initialize the database connection and creates the students TABLE if it doesnt exist
    def __init__(self, db="students.db"):
        self.db = db
        self.connection = None
        self._initialize_database()


    #Creates the STUDENTS table
    def _initialize_database(self):
        self.connection = sqlite3.connect(self.db)
        cursor = self.connection.cursor()
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY,
                first_name TEXT,
                last_name TEXT,
                date_of_birth TEXT,
                major TEXT,
                gpa REAL,
                email TEXT
            )
            '''
        )
        self.connection.commit()
    
    #CLOSEs the database connection
    def close(self):
        if self.connection:
            self.connection.close()
            print("Database connection closed.") #NOT NEEDED 

    #opens a connection to the database
    def load(self):
        self.connection = sqlite3.connect(self.db)
        print("Database connection opened.") #NOT NEEDED 

    #Validate Student Data
    # PARAM: STUDENT in the form of a dictionary
    # IF RETURN NONE THEN IT IS VALID DATA, otherwise return an error message.   
    def validate_student_data(self, student):
        if not student["student_id"].isalnum(): 
            return "Error: Student ID must be alphanumeric."

        if not student["first_name"].isalpha():
            return "Error: First Name must contain only letters."

        if not student["last_name"].isalpha():
            return "Error: Last Name must contain only letters."
                        
        if not re.match(r"\d{4}-\d{2}-\d{2}", student["date_of_birth"]):
            return "Error: Date of Birth must be in YYYY-MM-DD format."

        try:
            datetime.datetime.strptime(student["date_of_birth"], "%Y-%m-%d")
        except ValueError:
            return "Error: Date of Birth is not a valid date."
        #THIS CHECK IS REDUNDANT ** IT IS FINE AS IT HAS NOT BROKEN THE APPLICATION YET
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", student["email"]):
            return "Error: Email format is invalid."

        try:
            gpa = float(student["gpa"])
            if not 0.0 <= gpa <= 4.0:
                return "Error: GPA must be between 0.0 and 4.0."
        except ValueError:
            return "Error: GPA must be a valid number."

        return None
    
    #Adds a new student record to the database.
    #Returns True if successful; otherwise, handles errors.
    def add_record(self, student):
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                '''
                INSERT INTO students (student_id, first_name, last_name, date_of_birth, major, gpa, email)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''',
                (
                    student["student_id"],
                    student["first_name"],
                    student["last_name"],
                    student["date_of_birth"],
                    student["major"],
                    student["gpa"],
                    student["email"]
                )
            )
            self.connection.commit()
            print("Record added successfully.") #NOT NEEDED 
            return True
        except sqlite3.IntegrityError:
            print("Error: Student ID already exists.") #NOT NEEDED 
            return False
        except sqlite3.Error as e:
            print(f"An error occurred: {e}") #NOT NEEDED 
            return False
   
   #Updates a specified field for the given student_id.
   #ONLY EDIT DATA IF record is found, and data is correct 
   #SMALL PARTS OF LOGIC KEPT, WE DONT NEED TO VERIFY THE FIELD NOW SINCE WE ARE USING THE GUI
    def edit_record(self, student_id, field, new_value):
        valid_fields = {"first_name", "last_name", "date_of_birth", "major", "gpa", "email"}
        if field not in valid_fields:
            print("Error: Invalid field name.") #NOT NEEDED 
            return

        cursor = self.connection.cursor()
        try:
            cursor.execute(
                f"UPDATE students SET {field} = ? WHERE student_id = ?",
                (new_value, student_id)
            )
            if cursor.rowcount > 0:
                self.connection.commit()
                print("Record updated successfully.") #NOT NEEDED  
            else:
                print("Error: Student not found.") #NOT NEEDED 
        except sqlite3.Error as e:
            print(f"An error occurred: {e}") #NOT NEEDED 
    
    #Deletes a student record by student_id
    #ONLY DELETE DATA IF valid record, "ARE YOU SURE YOU WANT TO DELTE THIS RECORD?"
    def delete_record(self, student_id):
        cursor = self.connection.cursor()
        try:
            cursor.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
            if cursor.rowcount > 0:
                self.connection.commit()
                print("Record deleted successfully.") #NOT NEEDED 
            else:
                print("Error: Student not found.") #NOT NEEDED 
        except sqlite3.Error as e:
            print(f"An error occurred: {e}") #NOT NEEDED 

  


