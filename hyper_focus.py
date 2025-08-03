#this project aims to build an app to keep track of my project and help me improve my focus
import sqlite3
import datetime
from typing import Optional, List, Dict, Any
import json
import os

database_path = "C:/Users/Claudio Giubrone/Documents/workspace/hyper_focus/huperfocus.db" # Change this to your desired path
# fuction to create a database
def create_database():
    print("Function started - creating database...")
    # creates database if it does not exist"
    conn = sqlite3.connect(database_path)
    print(f"Database should be created at: {os.path.abspath('hyperfocus.db')}")
    cursor = conn.cursor()

    #creates the project table
    cursor.execute ('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT,
            created_date TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'backlog'
        )
    ''')
    # creates tasks table
    cursor.execute ('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT NOT NULL DEFAULT 'backlog',
            priority INTEGER DEFAULT 1,
            category TEXT,
            created_date TEXT NOT NULL,
            completed_date TEXT,
            FOREIGN KEY (project_id) REFERENCES projects (id)
        )
    ''')
    conn.commit()
    conn.close()
    print("Database created")

def get_db_connection():
    conn = sqlite3.connect(database_path)
    conn.row_factory = sqlite3.Row # This lets you access columns by name
    return conn
def add_project (name: str, description: str = "", status: str ="backlog"):
    #add new project to database
    conn= get_db_connection()
    cursor = conn.cursor()
    try:
        current_date = datetime.datetime.now().isoformat()
        cursor.execute('''
            INSERT INTO projects (name, description, created_date, status)
            VALUES (?,?,?,?)
        ''', (name, description, current_date, status))

        conn.commit()
        project_id = cursor.lastrowid
        print(f"Project {name} created successfully! (ID: {project_id}), Status: {status}")
    except sqlite3.IntegrityError:
        print(f"Error: Project {name} already exists")
        return None
    finally:
        conn.close()

def add_task (title: str, project_id: int, description: str = "", status: str ="backlog", priority: int =1, category: str =""):
    #add new task to database
    conn= get_db_connection()
    cursor = conn.cursor()

    try:
        # check if a project existss
        cursor.execute("SELECT name FROM projects WHERE id= ?", (project_id,))
        project = cursor.fetchone()
        if not project:
            print("This project does not exist")
            return None
        created_date = datetime.datetime.now().isoformat()
        cursor.execute('''
            INSERT INTO tasks(project_id, title, description, status, priority, created_date, category)
            VALUES (?,?,?,?,?,?,?)
        ''',(project_id, title, description, status, priority, created_date, category))

        conn.commit()
        task_id = cursor.lastrowid
        print(f"Task {title} added to project {project[0]}")
        return task_id
    except Exception as e:  # Add this exception handling
        print(f"Error adding task: {e}")
        return None
    finally:
        conn.close()

def print_database():
    """Print all contents of the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    print("\n=== PROJECTS TABLE ===")
    cursor.execute('SELECT * FROM projects')
    projects = cursor.fetchall()
    
    if projects:
        print("ID | Name | Description | Created Date | Status")
        print("-" * 60)
        for project in projects:
            print(f"{project[0]} | {project[1]} | {project[2]} | {project[3]} | {project[4]}")
    else:
        print("No projects found.")

    print("\n=== TASKS TABLE ===")
    cursor.execute('SELECT * FROM tasks WHERE status in ("to_do", "in_progress") ORDER BY priority')
    tasks = cursor.fetchall()

    if tasks:
        # Add 'Category' to the header
        print("ID | Project_ID | Title | Description | Status | Priority | Created | Completed | Category")
        print("-" * 100) # Adjust line length

        for task in tasks:
            # Access the new column at index 8
            print(f"{task[0]} | {task[1]} | {task[2]} | {task[3]} | {task[4]} | {task[5]} | {task[6]} | {task[7]} | {task[8]}")
    else:
        print("No tasks found.")

    conn.close()

def debug_check():
    """Simple debug to check database contents"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        print("DEBUG: Checking projects...")
        cursor.execute('SELECT COUNT(*) FROM projects')
        project_count = cursor.fetchone()[0]
        print(f"DEBUG: Found {project_count} projects")
        
        cursor.execute('SELECT * FROM projects')
        projects = cursor.fetchall()
        print(f"DEBUG: Projects data: {projects}")
        
        print("DEBUG: Checking tasks...")
        cursor.execute('SELECT COUNT(*) FROM tasks')
        task_count = cursor.fetchone()[0]
        print(f"DEBUG: Found {task_count} tasks")
        
        cursor.execute('SELECT * FROM tasks')
        tasks = cursor.fetchall()
        print(f"DEBUG: Tasks data: {tasks}")
        
        conn.close()
    except Exception as e:
        print(f"DEBUG ERROR: {e}")
def menu():
    while True:
        print("Hyper Focus - menu")
        print("What do you want to do?")
        print("1. Add new project")
        print("2. Add new task to a project")
        print("3. View the all database")
        print("4. View the task you should focus on")
        print("5. Modify project")
        print("6. Modify task")
        print("7. Quit")
        print("8. Debug check")

        selection= input("Enter your choice form 1 to 7: ").strip()
        if selection == "1":
            project_name = input("Project name: ").strip()
            if not project_name:
                print("Error! All projects must have a name!")
                continue
            project_description = input("Describe your project: ").strip()
            project_status= input("Define the status of the project: ").strip()
            if not project_status:
                project_status= "backlog"
            add_project(project_name, project_description, project_status)
        elif selection == "2":
            title = input("What is the task: ").strip()
            if not title:
                print("Please write the tasks")
                continue
            try:
                project_id = int(input("What is the project id linked to this task? "))
                description = input('What do you want to achieve with this task? ')
                status = input('What is the status of the task?: ')
                if not status:
                    status = "backlog"
                priority_input = input("What is the priority (where 1 is Top and 5 is very low)?: ")
                priority = int(priority_input) if priority_input else 1
                category = input("What is the category of this taks? ")
                 # Correct order: title, project_id, description, status, priority
                add_task(title, project_id, description, status, priority, category)
            except ValueError:
                print("Please enter valid numbers for project ID and priority!")
        elif selection == "3":
            print_database()
        elif selection ==  "7":
            print("Great work! Stay focused!")
            break
        elif selection == "8":  # Add this temporarily
            debug_check()
        else:
            print("Please, select a valid choice")


# Call the function to create database
if __name__ == "__main__":
    create_database()
print_database()
menu()

