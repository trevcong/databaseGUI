from db_helper import StudentDatabase


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
    
    #displayMenu for terminal / when GUI is done
    def displayMenu(self):
        #CODE TO DISPLAY CHOICES
        ...
    
    #process choice made by user from displayMeny
    def processChoice(self, choice):
        #CODE TO PROCESS CHOICE ON IF USER WANTS TO 
        #EDIT, DELETE, ECT
        ...

if __name__ == "__main__":
    app = StudentDatabaseApp()
    app.runApplication()