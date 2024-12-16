import sqlite3


def main():
    # Connect to the database.
    conn = sqlite3.connect('students.db')

    # Get a database cursor.
    cur = conn.cursor()

    # Add the Students table.
    add_students_table(cur)

    # Add rows to the Students table.
    add_students(cur)

    # Commit the changes.
    conn.commit()

    # Display the Student's info.
    display_students(cur)

    # Close the connection.
    conn.close()


# The add_cities_table adds the Cities table to the database.
def add_students_table(cur):
    # If the table already exists, drop it.
    cur.execute('DROP TABLE IF EXISTS Students')

    # Create the table.
    cur.execute('''CREATE TABLE Students (StudentID INTEGER PRIMARY KEY NOT NULL, 
    First_name TEXT NOT NULL, Last_name TEXT NOT NULL, 
    D_o_B TEXT NOT NULL, Major TEXT, GPA REAL, Email TEXT NOT NULL)''')


# The add_students function adds 10 rows to the Students table.
def add_students(cur):
    students_info = [(129112, 'Luis', 'Amador', "1/8/2005", 'Computer Science', 3.75, "lyamador@students.unwsp.edu"),
                     (129113, 'Emily', 'Johnson', "3/14/2003", 'Biology', 3.82, "emjohnson@students.unwsp.edu"),
                     (129114, 'Michael', 'Smith', "7/22/2004", 'Mathematics', 3.90, "msmith@students.unwsp.edu"),
                     (129115, 'Sophia', 'Brown', "11/11/2005", 'Psychology', 3.68, "sobrown@students.unwsp.edu"),
                     (129116, 'James', 'Davis', "5/19/2003", 'Engineering', 3.45, "jadavis@students.unwsp.edu"),
                     (129117, 'Olivia', 'Martinez', "2/25/2004", 'Nursing', 3.95, "omartinez@students.unwsp.edu"),
                     (129118, 'William', 'Garcia', "10/8/2003", 'Physics', 3.70, "wgarcia@students.unwsp.edu"),
                     (129119, 'Ava', 'Taylor', "6/15/2005", 'History', 3.60, "avataylor@students.unwsp.edu"),
                     (129120, 'Ethan', 'Clark', "4/2/2004", 'Chemistry', 3.88, "eclark@students.unwsp.edu"),
                     (129121, 'Mia', 'Hernandez', "9/30/2003", 'Art', 3.78, "mhernandez@students.unwsp.edu")]

    for row in students_info:
        cur.execute('''INSERT INTO Students (StudentID, First_name, Last_name, D_o_B, Major, GPA, Email)
                       VALUES (?, ?, ?, ?, ?, ?, ?)''', (row[0], row[1], row[2], row[3],row[4], row[5], row[6]))


# The display_Students function displays the contents of
# the Students table.
def display_students(cur):
    print('  ID - FirstN/LastM - DoB   -     Major  -   GPA - EMAIl:')
    cur.execute('SELECT * FROM Students')
    results = cur.fetchall()
    for row in results:
        print(f'{row[0]} {row[1]} {row[2]} {row[3]} {row[4]} {row[5]} {row[6]}')

# Execute the main function.
if __name__ == '__main__':
    main()
