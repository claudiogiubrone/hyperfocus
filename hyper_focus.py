#this project aims to build an app to keep track of my project and help me improve my focus
import sqlite3
import datetime
from typing import Optional, List, Dict, Any
import json
import os

# fuction to create a database
def create_database():
    print("Function started - creating database...")
    # creates database if it does not exist"
    conn = sqlite3.connect("hyperfocus.db")
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
            created_date TEXT NOT NULL,
            completed_date TEXT,
            FOREIGN KEY (project_id) REFERENCES projects (id)
        )
    ''')
    conn.commit()
    conn.close()
    print("Database created")

def add_project (name: str, description: str = "", status: str ="backlog"):
    #add new project to database
    conn= sqlite3.connect("hyperfocus.db")
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

def add_task (title: str, project_id: int, description: str = "", status: str ="backlog", priority: int =1):
    #add new task to database
    conn= sqlite3.connect("hyperfocus.db")
    cursor = conn.cursor()

    try:
        # check if a project existss
        cursor.execute("SELECT name FROM projects WHERE id= ?", (project_id,))
        project = cursor.fetchone()
        if not project:
            print("This project does not exist")
            return None
        current_date = datetime.datetime.now().isoformat()
        cursor.execute('''
            INSERT INTO tasks(project_id, title, description, status, priority, created_at)
            VALUES (?,?,?,?,?,?)
        ''',(project_id, title, description, status, priority, current_date))

        conn.commit()
        task_id = cursor.lastrowid
        print(f"Task {title} added to project {project[0]}")
        return task_id
    finally:
        conn.close()

def print_database():
    """Print all contents of the database."""
    conn = sqlite3.connect("hyperfocus.db")
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
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    
    if tasks:
        print("ID | Project_ID | Title | Description | Status | Priority | Created | Completed")
        print("-" * 80)
        for task in tasks:
            print(f"{task[0]} | {task[1]} | {task[2]} | {task[3]} | {task[4]} | {task[5]} | {task[6]} | {task[7]}")
    else:
        print("No tasks found.")
    
    conn.close()

def menu():
    while True:
        print("Hyper Focus - menu")
        print("What do you want to do?")
        print("1. Add new project")
        print("2. Add new task to a project")
        print("3. View dashboard")
        print("4. Modify project")
        print("5. Modify task")
        print("6. Quit")

        selection= input("Enter your choice form 1 to 6: ").strip()
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
        elif selection == "3":
            print_database()
        elif selection ==  "6":
            print("Great work! Stay focused!")
        else:
            print("Please, select a valid choice")
# Call the function to create database
if __name__ == "__main__":
    create_database()
    menu()


