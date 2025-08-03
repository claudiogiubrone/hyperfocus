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

# Call the function to create database
if __name__ == "__main__":
    create_database()