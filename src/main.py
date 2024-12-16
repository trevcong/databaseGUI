from db_helper import StudentDatabase


class StudentDatabaseApp:
    #INITIALIZE/FETCH database from db_helper
    def __init__(self):
        self.database = StudentDatabase()
        self.database.load()

    #main application loop
    #EXIT when needed
    def runApplication(self):
        while True:
            choice = self.display_menu()
            
            self.process_choice(choice)
            if choice == 5:
                break
    
    #displayMenu for terminal / when GUI is done
    def display_menu(self):
        print("1. View Records")
        print("2. Add Record")
        print("3. Edit Record")
        print("4. Delete Record")
        print("5. Exit")
        return int(input("Enter your choice: "))
    
    def add_record(self):
        student = {
            "student_id": input("Enter Student ID: "),
            "first_name": input("Enter First Name: "),
            "last_name": input("Enter Last Name: "),
            "date_of_birth": input("Enter Date of Birth (YYYY-MM-DD): "),
            "major": input("Enter Major: "),
            "gpa": input("Enter GPA: "),
            "email": input("Enter Email: ")
        }
        self.database.add_record(student)

    def edit_record(self):
        student_id = input("Enter Student ID to edit: ")
        field = input("Enter field to edit (e.g., 'first_name'): ")
        new_value = input(f"Enter new value for {field}: ")
        self.database.edit_record(student_id, field, new_value)    

    def delete_record(self):
        student_id = input("Enter Student ID to delete: ")
        confirmation = input("Are you sure you want to delete this record? (yes/no): ")
        if confirmation.lower() == 'yes':
            self.database.delete_record(student_id)
        else:
            print("Deletion cancelled.")
       
    #process choice made by user from displayMeny
    def process_choice(self, choice):
        try:
            if choice == 1:
                self.database.view_records()
            elif choice == 2:
                self.add_record()
            elif choice == 3:
                self.edit_record()
            elif choice == 4:
                self.delete_record()
            elif choice == 5:
                if isinstance(self.database, StudentDatabase):
                    self.database.close()
                    print("Goodbye!")
                else:
                    print("Error: Database is not properly initialized.")
                exit(0)
            else:
                print("Invalid choice. Please try again.")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    app = StudentDatabaseApp()
    app.runApplication()