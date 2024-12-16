# Program 4
# by Luis Amador
# 12/5/24

import sqlite3

MIN_CHOICE = 1
MAX_CHOICE = 5
CREATE = 1
READ = 2
UPDATE = 3
DELETE = 4
EXIT = 5

def main():
     choice = 0
     while choice != EXIT:
       display_menu()
       choice = get_menu_choice()

       if choice == CREATE:
             create()
       elif choice == READ:
                 read()
       elif choice == UPDATE:
                 update()
       elif choice == DELETE:
                  delete()

# The display_menu function displays the main menu.

def display_menu():
      print('\n----- Student DataBase Menu -----')
      print('1. Create a entry')
      print('2. Read an entry')
      print('3. Update an entry')
      print('4. Delete an entry')
      print('5. Exit the program')

  # The get_menu_choice function gets the user's menu choice.
def get_menu_choice():
      # Get the user's choice.
     choice = int(input('Enter your choice: '))

    # Validate the input.
     while choice < MIN_CHOICE or choice > MAX_CHOICE:
              print(f'Valid choices are {MIN_CHOICE} through {MAX_CHOICE}.')
              choice = int(input('Enter your choice: '))

     return choice

  # The create function creates a new item.
def create():
    print('Create New Entry')
    student_id = int(input("Enter Student ID: "))
    first_name = input('First Name: ')
    last_name = input("Last Name: ")
    d_o_b = input("Date of Birth (xx/xx/xxxx format): ")
    major= input("Major: ")
    gpa = float(input("GPA (in decimal form): "))
    email = input("Email: ")



    insert_row(student_id, first_name, last_name, d_o_b, major, gpa, email)

  # The read function reads an existing item.
def read():
    last_name = input('Enter an item name to search for: ')
    num_found = display_item(last_name)
    print(f'{num_found} row(s) found.')

  # The update function updates an existing item's data.
def update():
      # First let the user search for the row.
      read()

      # Get the ID of the selected item.
      selected_id = int(input('Select an enter a specific ID: '))

      # Get the new values for item name and price.
      first_name = input('First Name: ')
      last_name = input("Last Name: ")
      d_o_b = input("Date of Birth (xx/xx/xxxx format): ")
      major = input("Major: ")
      gpa = float(input("GPA (in decimal form): "))
      email = input("Email: ")

      # Update the row.
      num_updated = update_row(selected_id, first_name, last_name, d_o_b, major, gpa, email)
      print(f'{num_updated} row(s) updated.')

  # The delete function deletes an item.
def delete():
      # First let the user search for the row.
      read()

      # Get the ID of the selected item.
      selected_id = int(input('Enter a specific StudentID to delete: '))

      # Confirm the deletion.
      sure = input('Are you sure you want to delete this item? (y/n): ')
      if sure.lower() == 'y':
          num_deleted = delete_row(selected_id)
          print(f'{num_deleted} row(s) deleted.')

  # The insert_row function inserts a row into the Inventory table.
def insert_row(studentID, first_name, last_name, d_o_b, major, gpa, email):
        conn = None
        try:
          conn = sqlite3.connect('student.db')
          cur = conn.cursor()
          cur.execute('''INSERT INTO Students (StudentID, First_name, Last_name, D_o_B, Major, GPA, Email)
                         VALUES (?, ?, ?, ?, ? ?)''',
                      (studentID, first_name, last_name, d_o_b, major, gpa, email))
          conn.commit()
        except sqlite3.Error as err:
          print('Database Error', err)

        finally:
            if conn is not None:
                conn.close()

 # The display_item function displays all items
  # with a matching ItemName.
def display_item(last_name):
    conn = None
    results = []
    try:
        conn = sqlite3.connect('students.db')
        cur = conn.cursor()
        cur.execute('''SELECT * FROM Students WHERE Last_name = ?''', (last_name,))
        results = cur.fetchall()

        for row in results:
            print(f'ID: {row[0]:<3} Name: {row[1]:<15} Phone Number: {row[2]:<10}')

    except sqlite3.Error as err:
        print('Database Error', err)

    finally:
        if conn is not None:
            conn.close()

    return len(results)


  # The update_row function updates an existing row with a new
  # ItemName and Price. The number of rows updated is returned.

def update_row(first_name, last_name, d_o_b, major, gpa, email ):
    conn = None
    num_updated = 0
    try:
        conn = sqlite3.connect('students.db')
        cur = conn.cursor()
        cur.execute('''UPDATE Students
                       SET First_name = ?, Last_name = ?, D_o_B = ?, Major = ?, GPA = ?, Email = ?, 
                        WHERE StudentID == ?''',
                      (first_name, last_name, d_o_b, major, gpa, email))
        conn.commit()
        num_updated = cur.rowcount

    except sqlite3.Error as err:
            print('Database Error', err)

    finally:
        if conn is not None:
            conn.close()

    return num_updated

  # The delete_row function deletes an existing item.
  # The number of rows deleted is returned.
def delete_row(studentID):
    conn = None
    try:
        conn = sqlite3.connect('students.db')
        cur = conn.cursor()
        cur.execute('''DELETE FROM students
                         WHERE StudentID == ?''',
                      (studentID))
        conn.commit()
        num_deleted = cur.rowcount
    except sqlite3.Error as err:
            print('Database Error', err)

    finally:
        if conn is not None:
           conn.close()

    return num_deleted

  # Execute the main function.
if __name__ == '__main__':
      main()
