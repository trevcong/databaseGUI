from db_helper import StudentDatabase

MIN_CHOICE = 1
MAX_CHOICE = 5
CREATE = 1
READ = 2
UPDATE = 3
DELETE = 4
EXIT = 5



class StudentDatabaseApp:
    #INITIALIZE/FETCH database from db_helper
    def __init__(self):
        self.database = StudentDatabase()
        self.database.loadDatabase()

    #main application loop
    #EXIT when needed
    def runApplication(self):
        while True:
            ...
    

    #process choice made by user from displayMeny
    def processChoice(self, choice):
        #CODE TO PROCESS CHOICE ON IF USER WANTS TO
        choice = 0
        while choice != EXIT:
            displayMenu()
            choice = get_menu_choice()

            if choice == CREATE:
                create()
            elif choice == READ:
                read()
            elif choice == UPDATE:
                update()
            elif choice == DELETE:
                delete()
        ...

    # displayMenu for terminal / when GUI is done
    def displayMenu(self):
            # CODE TO DISPLAY CHOICE
            print('\n----- Student DataBase Menu -----')
            print('1. Create a entry')
            print('2. Read an entry')
            print('3. Update an entry')
            print('4. Delete an entry')
            print('5. Exit the program')


if __name__ == "__main__":
    app = StudentDatabaseApp()
    app.runApplication()