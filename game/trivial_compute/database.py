"""
Madeline Gyllenhoff
database.py

GUI to add questions to the database. Database is specified in database.env.
"""

# Import everything needed to make GUI and load in .env file
import tkinter as tk
from tkinter import ttk, messagebox
import pymysql
from dotenv import load_dotenv
import os

class Database:
    """
    Database class to handle the database UI and interactions.
    """
    def __init__(self, app, screen=None):
        self.app = app
        self.root = tk.Tk()
        self.db_config = {
            'host': os.getenv('DB_HOST'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'database': os.getenv('DB_NAME')
            }

    # Function to fetch categories from the database
    def fetch_categories(self):
        try:
            connection = pymysql.connect(**self.db_config)
            cursor = connection.cursor()
            cursor.execute("SELECT categoryID, categoryName FROM Categories")
            categories = cursor.fetchall()
            cursor.close()
            connection.close()
            return categories
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            return []

    # Function to add a question to the database
    def add_question(self, category_id, question_content, answer_content):
        try:
            # Connect to the database
            connection = pymysql.connect(**self.db_config)
            cursor = connection.cursor()

            # Insert the new question into the Questions table
            insert_query = """
                INSERT INTO Questions (questionContent, answerContent, categoryID)
                VALUES (%s, %s, %s)
            """
            cursor.execute(insert_query, (question_content, answer_content, category_id))

            # Commit the transaction
            connection.commit()

            # Close the cursor and connection
            cursor.close()
            connection.close()

            print("Question added successfully!")
        except Exception as e:
            print(f"An error occurred: {e}")

    def get_category_id(self, category_name):
        try:
            # Connect to the database
            connection = pymysql.connect(**self.db_config)
            cursor = connection.cursor()

            # Execute the query to fetch the categoryID
            query = "SELECT categoryID FROM Categories WHERE categoryName = %s"
            cursor.execute(query, (category_name,))
            result = cursor.fetchone()

            # If the categoryID is found, return it
            if result:
                category_id = result[0]
            else:
                # Insert the new category into the Categories table
                insert_query = "INSERT INTO Categories (categoryName) VALUES (%s)"
                cursor.execute(insert_query, (category_name,))
                connection.commit()

                # Retrieve the new categoryID
                cursor.execute(query, (category_name,))
                result = cursor.fetchone()
                category_id = result[0]

            # Close the cursor and connection
            cursor.close()
            connection.close()

            return category_id
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    # Function to handle the button click and print the inputs
    def make_question(self):
        category_name = self.category_var.get()
        question_content = self.question_entry.get()
        answer_content = self.answer_entry.get()

        if category_name and question_content and answer_content:
            category_id = self.get_category_id(category_name)
            self.add_question(category_id, question_content, answer_content)
            messagebox.showinfo("Success", "Question added to database!")
        else:
            messagebox.showwarning("Input Error", "All fields are required!")

    # Function to handle the exit button click
    def exit_gui(self):
        self.root.destroy()

    def run(self):
        """
        Add function docstring here.
        """
        # Create the main window
        self.root.title("Add Question to Database")

        # Fetch categories from the database
        categories = self.fetch_categories()
        category_names = [cat[1] for cat in categories]

        # Create and place the widgets
        tk.Label(self.root, text="Category").grid(row=0, column=0, padx=10, pady=10)
        category_var = tk.StringVar()
        category_dropdown = ttk.Combobox(self.root, textvariable=category_var, values=category_names)
        category_dropdown.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Question").grid(row=1, column=0, padx=10, pady=10)
        question_entry = tk.Entry(self.root)
        question_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Answer").grid(row=2, column=0, padx=10, pady=10)
        answer_entry = tk.Entry(self.root)
        answer_entry.grid(row=2, column=1, padx=10, pady=10)

        # Add the new question
        tk.Button(self.root, text="Add Question", command=self.make_question).grid(row=3, column=0, columnspan=2, pady=10)
        tk.Button(self.root, text="Exit", command=self.exit_gui).grid(row=4, column=0, columnspan=2, pady=10)

        # Run the main event loop
        self.root.mainloop()
