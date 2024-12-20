import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, simpledialog
from tkinter import font as tkFont
from db_helper import StudentDatabase

class StudentDatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Matrix Viewer")
        self.root.geometry("600x700")
        self.root.configure(bg="black")

        # Create a custom style for ttk widgets
        self.style = ttk.Style()
        self.style.configure("TFrame", background="black")
        self.style.configure("TLabel", background="black", foreground="green")
        self.style.configure("TEntry", fieldbackground="black", foreground="green")
        self.style.configure("TButton", background="black", foreground="green")

        # Define custom fonts for a playful look
        self.default_font = tkFont.Font(family="Comic Sans MS", size=12)
        self.label_font = tkFont.Font(family="Comic Sans MS", size=14, weight="bold")

        self.database = StudentDatabase()
        self.database.load()

        self.user_type = None
        self.create_login_screen()

        # Bind the configure event to dynamically adjust font sizes
        self.root.bind('<Configure>', self.adjust_font_size)

    def adjust_font_size(self, event=None):
        # Calculate font size based on window width
        width = self.root.winfo_width()
        font_size = max(12, int(width / 50))  # Adjust divisor for desired scaling

        # Update font sizes dynamically
        self.default_font.config(size=font_size)
        self.label_font.config(size=font_size + 2)

    def create_login_screen(self):
        login_frame = tk.Frame(self.root, bg="black")
        login_frame.pack(expand=True, fill='both')

        label = tk.Label(login_frame, text="Login as:", font=self.label_font, bg="black", fg="green")
        label.pack(pady=20)

        self.user_type_var = tk.StringVar(value="student")
        student_radio = tk.Radiobutton(
            login_frame,
            text="Student",
            variable=self.user_type_var,
            value="student",
            font=self.default_font,
            bg="black",
            fg="green",
            selectcolor="black"
        )
        admin_radio = tk.Radiobutton(
            login_frame,
            text="Admin",
            variable=self.user_type_var,
            value="admin",
            font=self.default_font,
            bg="black",
            fg="green",
            selectcolor="black"
        )
        student_radio.pack(pady=5)
        admin_radio.pack(pady=5)

        login_button = tk.Button(
            login_frame, 
            text="Login", 
            command=self.login, 
            font=self.default_font, 
            bg="black", 
            fg="green"
        )
        login_button.pack(pady=20)

    def login(self):
        self.user_type = self.user_type_var.get()
        self.create_main_interface()

    def create_main_interface(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.notebook = ttk.Notebook(self.root, style='TNotebook')
        self.notebook.pack(expand=True, fill='both')

        self.create_view_tab()

        if self.user_type == "admin":
            self.create_add_tab()
            self.create_edit_tab()
            self.create_delete_tab()

        exit_button = tk.Button(
            self.root, 
            text="Exit", 
            command=self.exit_application, 
            font=self.default_font, 
            bg="black", 
            fg="green"
        )
        exit_button.pack(side=tk.LEFT, padx=5, pady=5)

    def create_view_tab(self):
        view_frame = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(view_frame, text='View Records')

        controls_frame = tk.Frame(view_frame, bg="black")
        controls_frame.pack(fill='x', pady=5)

        self.queries = {
            "All Records": "SELECT * FROM students",
            "Custom Query": ""
        }

        self.query_combobox = ttk.Combobox(
            controls_frame,
            values=list(self.queries.keys()),
            width=30,
            state='readonly'
        )
        self.query_combobox.set("All Records")
        self.query_combobox.pack(side=tk.LEFT, padx=5)

        self.view_button = tk.Button(
            controls_frame,
            text="Refresh Records",
            command=self.view_records,
            font=self.default_font,
            bg="black",
            fg="green"
        )
        self.view_button.pack(side=tk.LEFT, padx=5)

        self.text_area = scrolledtext.ScrolledText(
            view_frame,
            width=70,
            height=20,
            font=self.default_font,
            fg="green",
            bg="black"
        )
        self.text_area.pack(expand=True, fill='both', pady=10)

    def create_add_tab(self):
        add_frame = tk.Frame(self.notebook, bg="black")
        self.notebook.add(add_frame, text='Add Record')

        self.student_id_entry = self.create_label_search(add_frame, "Student ID:")
        self.first_name_entry = self.create_label_search(add_frame, "First Name:")
        self.last_name_entry = self.create_label_search(add_frame, "Last Name:")
        self.dob_entry = self.create_label_search(add_frame, "Date of Birth (YYYY-MM-DD):")
        self.major_entry = self.create_label_search(add_frame, "Major:")
        self.gpa_entry = self.create_label_search(add_frame, "GPA:")
        self.email_entry = self.create_label_search(add_frame, "Email:")

        self.add_button = tk.Button(
            add_frame,
            text="Add Record",
            command=self.add_record,
            font=self.default_font,
            bg="black",
            fg="green"
        )
        self.add_button.pack(pady=5)

    def create_edit_tab(self):
        edit_frame = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(edit_frame, text='Edit Record')

        self.search_id_entry = self.create_label_search(edit_frame, "Search by Student ID:")
        self.search_email_entry = self.create_label_search(edit_frame, "Search by Email:")
        self.search_button = tk.Button(edit_frame, text="Search", command=self.search_record, bg="black", fg="green")
        self.search_button.pack(pady=5)
        
        self.edit_student_id_entry = self.create_label_search(edit_frame, "Student ID:")
        self.edit_first_name_entry = self.create_label_search(edit_frame, "First Name:")
        self.edit_last_name_entry = self.create_label_search(edit_frame, "Last Name:")
        self.edit_dob_entry = self.create_label_search(edit_frame, "Date of Birth (YYYY-MM-DD):")
        self.edit_major_entry = self.create_label_search(edit_frame, "Major:")
        self.edit_gpa_entry = self.create_label_search(edit_frame, "GPA:")
        self.edit_email_entry = self.create_label_search(edit_frame, "Email:")

        self.save_button = tk.Button(edit_frame, text="Save Changes", command=self.save_changes, bg="black", fg="green")
        self.save_button.pack(pady=5)

    def create_delete_tab(self):
        delete_frame = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(delete_frame, text='Delete Record')

        self.delete_entry = self.create_label_search(delete_frame, "Search by Student ID or Email:")
        self.delete_button = tk.Button(delete_frame, text="Search and Delete", command=self.delete_record, bg="black", fg="green")
        self.delete_button.pack(pady=5)

    def create_label_search(self, parent, label_text):
        frame = ttk.Frame(parent, style='TFrame')
        frame.pack(pady=2)
        label = ttk.Label(frame, text=label_text, style="TLabel", font=self.default_font)
        label.pack(side=tk.LEFT)
        entry = ttk.Entry(frame, style="TEntry", font=self.default_font)
        entry.pack(side=tk.RIGHT, fill='x', expand=True)
        return entry


    def view_records(self):
        self.text_area.delete(1.0, tk.END)
        cursor = self.database.connection.cursor()
        
        selected_query = self.query_combobox.get()
        query = self.queries[selected_query]
        
        if selected_query == "Custom Query":
            query = simpledialog.askstring("Input", "Enter your SQL query:")
            if not query:
                self.text_area.insert(tk.END, "No query entered.\n")
                return
        
        try:
            cursor.execute(query)
            records = cursor.fetchall()
            
            self.text_area.insert(tk.END, f"{selected_query}\n")
            self.text_area.insert(tk.END, "-" * 3 + "ID" + "-" * 3 + "First/Last Name" + "-" * 3 +
                                  "Date of Birth" + "-" * 5 + "Major" + "-" * 5 + "GPA" + "-" * 5 + "Email" + "\n\n")
            
            for record in records:
                self.text_area.insert(tk.END, f"{record}\n")
                
        except sqlite3.Error as e:
            self.text_area.insert(tk.END, f"Error executing query: {e}")

    def add_record(self):
        student = {
            "student_id": self.student_id_entry.get(),
            "first_name": self.first_name_entry.get(),
            "last_name": self.last_name_entry.get(),
            "date_of_birth": self.dob_entry.get(),
            "major": self.major_entry.get(),
            "gpa": self.gpa_entry.get(),
            "email": self.email_entry.get()
        }

        validation_error = self.database.validate_student_data(student)
        if validation_error:
            messagebox.showerror("Input Error", validation_error)
            return

        if self.database.add_record(student):
            self.clear_entries()
            messagebox.showinfo("Success", "Record added successfully.")
        else:
            messagebox.showerror("Error", "Failed to add record. Please check your inputs.")
    
    def clear_entries(self):
        self.student_id_entry.delete(0, tk.END)
        self.first_name_entry.delete(0, tk.END)
        self.last_name_entry.delete(0, tk.END)
        self.dob_entry.delete(0, tk.END)
        self.major_entry.delete(0, tk.END)
        self.gpa_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)

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

    def save_changes(self):
        student_id = self.edit_student_id_entry.get()
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

    def exit_application(self):
        self.database.close()
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentDatabaseApp(root)
    root.mainloop()