class StudentDatabase:
    def __init__(self):
        self.data = []


    #load database from file "database"/students.db
    def loadDatabase(self):
        ...
        print("Database loaded")
    
    #Save data to database 
    def save(self):
        ...
        print("Database saved")

    #Add record to database
    #ONLY ADD DATA IF data is valid
    def addRecordToDatabase(self):
        ...
        print("Record added")
   
   #Edit record from database
   #ONLY EDIT DATA IF record is found, and data is correct 
    def editRecordFromDatabase(self):
        ...
        #if sucess
            #record updated
            #return
        #else
            #Invalid, not updating
            #return
        #If student not found
            #Student not found, try again
    
    #Delete record from database
    #ONLY DELETE DATA IF valid record, "ARE YOU SURE YOU WANT TO DELTE THIS RECORD?"
    def deleteRecordFromDatabase(self):
        ...
        print("Recird delted")

    #View record/s from database
    #View data from different queries (SELECT *, SELECT * FROM -- WHERE gpa > '2.5', ect)
    def viewRecords(self):
        ...