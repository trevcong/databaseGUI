import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, simpledialog
from db_helper import StudentDatabase

class StudentDatabaseApp:
    #CONSTRUCTOR
    #Root: THE MAIN TKINTER WINDOW
    #INIT database GUI components
    def __init__(self, root):
        self.root = root
        self.root.title("Student Database App")
        self.database = StudentDatabase()
        self.database.load()

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both')

        # Create tabs: View Records, Add Record, Edit Record, and Delete Record.
        self.create_view_tab()
        self.create_add_tab()
        self.create_edit_tab()
        self.create_delete_tab()

        # Exit button tab: Exit application
        self.exit_button = tk.Button(self.root, text="Exit", command=self.exit_application)
        self.exit_button.pack(side=tk.LEFT, padx=5, pady=5)


    #Displays all student records in a scrollable text area
    #Button: "Refresh Records" to reload data
    def create_view_tab(self):
        #This creates the VIEW RECORDS tab
        #This is for viewing student records
        view_frame = ttk.Frame(self.notebook)
        self.notebook.add(view_frame, text='View Records')

        #Create a frame for the controls
        controls_frame = ttk.Frame(view_frame)
        controls_frame.pack(fill='x', pady=5)
       

        #Predefined SQL queries
        self.queries = {
            "All Records": "SELECT * FROM students",
            "Custom Query": ""  # Custom SQL query
        }
        
        #Combobox for selecting queries
        self.query_combobox = ttk.Combobox(
            controls_frame, 
            values=list(self.queries.keys()),
            width=30,
            state='readonly'
        )
        self.query_combobox.set("All Records")  #Default selection
        self.query_combobox.pack(side=tk.LEFT, padx=5)

        #Button to refresh the records
        self.view_button = tk.Button( 
            controls_frame, 
            text="Refresh Records", 
            command=self.view_records
        )
        self.view_button.pack(side=tk.LEFT, padx=5)

        #Text area for displaying results
        self.text_area = scrolledtext.ScrolledText(view_frame, width=50, height=15)
        self.text_area.pack(pady=10)

    #Input fields:
        #Student ID, First Name, Last Name, Date of Birth, Major, GPA, Email.
    #Button: "Add Record" to add a student
    def create_add_tab(self):
        #Creates the ADD RECORD tab
        #Allows for adding new student records
        add_frame = ttk.Frame(self.notebook)
        self.notebook.add(add_frame, text='Add Record')

        #Entry fields for student data
        self.student_id_entry = self.create_label_search(add_frame, "Student ID:") #ADD LABEL 
        self.first_name_entry = self.create_label_search(add_frame, "First Name:")
        self.last_name_entry = self.create_label_search(add_frame, "Last Name:")
        self.dob_entry = self.create_label_search(add_frame, "Date of Birth (YYYY-MM-DD):")
        self.major_entry = self.create_label_search(add_frame, "Major:")
        self.gpa_entry = self.create_label_search(add_frame, "GPA:")
        self.email_entry = self.create_label_search(add_frame, "Email:")

        #Button to add a new record
        self.add_button = tk.Button(add_frame, text="Add Record", command=self.add_record)
        self.add_button.pack(pady=5)

    #SEARCH FIELDS: 
        #StudentID or email
    #Editable fields
        #Edit the fields needed, they will be populated with a successful search
    #Button/s:
        #'Search": Finds the record
        #"Save changes": Updates the record
    def create_edit_tab(self):
        #Creates the EDIT RECORD tab
        #Allows searching for and editing existing student records
        edit_frame = ttk.Frame(self.notebook)
        self.notebook.add(edit_frame, text='Edit Record')

        #Search fields for student data
        self.search_id_entry = self.create_label_search(edit_frame, "Search by Student ID:")
        self.search_email_entry = self.create_label_search(edit_frame, "Search by Email:")
        self.search_button = tk.Button(edit_frame, text="Search", command=self.search_record)
        self.search_button.pack(pady=5)
        
        #Editable fields for student data
        self.edit_student_id_entry = self.create_label_search(edit_frame, "Student ID:")
        self.edit_first_name_entry = self.create_label_search(edit_frame, "First Name:")
        self.edit_last_name_entry = self.create_label_search(edit_frame, "Last Name:")
        self.edit_dob_entry = self.create_label_search(edit_frame, "Date of Birth (YYYY-MM-DD):")
        self.edit_major_entry = self.create_label_search(edit_frame, "Major:")
        self.edit_gpa_entry = self.create_label_search(edit_frame, "GPA:")
        self.edit_email_entry = self.create_label_search(edit_frame, "Email:")

        #Button to save changes
        self.save_button = tk.Button(edit_frame, text="Save Changes", command=self.save_changes)
        self.save_button.pack(pady=5)

    # Input field: Student ID or Email
    # Button: "Search and Delete" to delete a record after confirmation 
    def create_delete_tab(self):
        #Creates the DELETE RECORD tab
        #Allows users to search for and delete student records
        delete_frame = ttk.Frame(self.notebook)
        self.notebook.add(delete_frame, text='Delete Record')

        #Entry field for student ID or email
        self.delete_entry = self.create_label_search(delete_frame, "Search by Student ID or Email:")
        self.delete_button = tk.Button(delete_frame, text="Search and Delete", command=self.delete_record)
        self.delete_button.pack(pady=5)

    # Creates a labeled text entry field for user input.
    def create_label_search(self, parent, label_text):
        #Creates a labeled text entry field for user input based on parent

        #Parameters
            #parent (Frame): The parent frame to which the entry field belongs.
            #label_text (str): The text for the label.

        #Returns
            #Entry: The created entry widget.
        frame = ttk.Frame(parent)
        frame.pack(pady=2)
        label = ttk.Label(frame, text=label_text)
        label.pack(side=tk.LEFT)
        entry = ttk.Entry(frame)
        entry.pack(side=tk.RIGHT)
        return entry
    
    # Fetches and displays all student records from the database
    def view_records(self):
        #Fetches and displays all student records from the dfatabase
        #Allows for predefined or custome SQL queries
        self.text_area.delete(1.0, tk.END)
        cursor = self.database.connection.cursor()
        
        #Get the selected query
        selected_query = self.query_combobox.get()
        query = self.queries[selected_query]
        
        if selected_query == "Custom Query":
            #Prompt user for custom SQL input
            query = simpledialog.askstring("Input", "Enter your SQL query:")
            if not query:
                self.text_area.insert(tk.END, "No query entered.\n")
                return
        
        try:
            cursor.execute(query)
            records = cursor.fetchall()
            
            #Add header showing which query was executed
            self.text_area.insert(tk.END, f"Executing: {selected_query}\n")
            self.text_area.insert(tk.END, "-" * 50 + "\n\n")
            
            #Display records
            for record in records:
                self.text_area.insert(tk.END, f"{record}\n")
                
        except sqlite3.Error as e:
            self.text_area.insert(tk.END, f"Error executing query: {e}")

    # Collects input data, validates it, and adds a new student record
    def add_record(self):
        #Collect stundet data
        student = {
            "student_id": self.student_id_entry.get(),
            "first_name": self.first_name_entry.get(),
            "last_name": self.last_name_entry.get(),
            "date_of_birth": self.dob_entry.get(),
            "major": self.major_entry.get(),
            "gpa": self.gpa_entry.get(),
            "email": self.email_entry.get()
        }

        #Validate student data
        validation_error = self.database.validate_student_data(student)
        if validation_error:
            messagebox.showerror("Input Error", validation_error)
            return

        #Attempt to add the record
        if self.database.add_record(student):
            self.clear_entries()
            messagebox.showinfo("Success", "Record added successfully.")
        else:
            messagebox.showerror("Error", "Failed to add record. Please check your inputs.")
    
    # Clears all input fields after successful addition
    def clear_entries(self):
        self.student_id_entry.delete(0, tk.END)
        self.first_name_entry.delete(0, tk.END)
        self.last_name_entry.delete(0, tk.END)
        self.dob_entry.delete(0, tk.END)
        self.major_entry.delete(0, tk.END)
        self.gpa_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)

    # Searches for a student by student_id or email
    def search_record(self):
        student_id = self.search_id_entry.get()
        email = self.search_email_entry.get()
        cursor = self.database.connection.cursor()

        if student_id:
            cursor.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
        elif email:
            cursor.execute("SELECT * FROM students WHERE email = ?", (email,))
        else:
            messagebox.showwarning("Input Error", "Please enter a Student ID or Email to search.")
            return

        record = cursor.fetchone()
        if record:
            self.edit_student_id_entry.delete(0, tk.END)
            self.edit_student_id_entry.insert(0, record[0])
            self.edit_first_name_entry.delete(0, tk.END)
            self.edit_first_name_entry.insert(0, record[1])
            self.edit_last_name_entry.delete(0, tk.END)
            self.edit_last_name_entry.insert(0, record[2])
            self.edit_dob_entry.delete(0, tk.END)
            self.edit_dob_entry.insert(0, record[3])
            self.edit_major_entry.delete(0, tk.END)
            self.edit_major_entry.insert(0, record[4])
            self.edit_gpa_entry.delete(0, tk.END)
            self.edit_gpa_entry.insert(0, record[5])
            self.edit_email_entry.delete(0, tk.END)
            self.edit_email_entry.insert(0, record[6])
        else:
            messagebox.showinfo("Not Found", "No student found with the given ID or Email.")

    # Updates student data for the searched record
    def save_changes(self):
        student_id = self.edit_student_id_entry.get()
        #updated student records
        updated_student = {
            "first_name": self.edit_first_name_entry.get(),
            "last_name": self.edit_last_name_entry.get(),
            "date_of_birth": self.edit_dob_entry.get(),
            "major": self.edit_major_entry.get(),
            "gpa": self.edit_gpa_entry.get(),
            "email": self.edit_email_entry.get()
        }

        for field, new_value in updated_student.items():
            if not new_value:
                messagebox.showwarning("Input Error", f"Please fill in the {field.replace('_', ' ').title()} field.")
                return

        for field, new_value in updated_student.items():
            self.database.edit_record(student_id, field, new_value)

        messagebox.showinfo("Success", "Record updated successfully.")

    # Deletes a student record after user confirmation.
    def delete_record(self):
        student_id_or_email = self.delete_entry.get()
        if not student_id_or_email:
            messagebox.showwarning("Input Error", "Please enter a Student ID or Email to delete.")
            return

        confirmation = messagebox.askyesno("Confirm", "Are you sure you want to delete this record?")
        if confirmation:
            cursor = self.database.connection.cursor()
            cursor.execute("DELETE FROM students WHERE student_id = ? OR email = ?", (student_id_or_email, student_id_or_email))
            if cursor.rowcount > 0:
                self.database.connection.commit()
                messagebox.showinfo("Success", "Record deleted successfully.")
            else:
                messagebox.showinfo("Not Found", "No student found with the given ID or Email.")
   
    # Closes the database connection and exits the application
    def exit_application(self):
        self.database.close()
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentDatabaseApp(root)
    root.mainloop()
