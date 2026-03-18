import sqlite3

conn = sqlite3.connect("healnet.db", check_same_thread=False)
cursor = conn.cursor()

# ----------------------------
# CREATE TABLES
# ----------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS organizations(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
username TEXT,
password TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
org_id INTEGER,
name TEXT,
username TEXT,
password TEXT,
role TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS patients(
id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER,
name TEXT,
age INTEGER,
scan_type TEXT,
disease TEXT,
confidence REAL
)
""")

conn.commit()

# ----------------------------
# ORGANIZATION FUNCTIONS
# ----------------------------

def register_org(name, username, password):
    cursor.execute(
        "INSERT INTO organizations(name,username,password) VALUES(?,?,?)",
        (name,username,password)
    )
    conn.commit()

def login_org(username,password):
    cursor.execute(
        "SELECT * FROM organizations WHERE username=? AND password=?",
        (username,password)
    )
    return cursor.fetchone()

# ----------------------------
# USER FUNCTIONS
# ----------------------------

def add_user(org_id,name,username,password,role):
    cursor.execute(
        "INSERT INTO users(org_id,name,username,password,role) VALUES(?,?,?,?,?)",
        (org_id,name,username,password,role)
    )
    conn.commit()

def login_user(username,password):
    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username,password)
    )
    return cursor.fetchone()

# ----------------------------
# PATIENT FUNCTIONS
# ----------------------------

def add_patient(user_id,name,age,scan_type,disease,confidence):
    cursor.execute(
        "INSERT INTO patients(user_id,name,age,scan_type,disease,confidence) VALUES(?,?,?,?,?,?)",
        (user_id,name,age,scan_type,disease,confidence)
    )
    conn.commit()

def get_patients(user_id):
    cursor.execute(
        "SELECT * FROM patients WHERE user_id=?",
        (user_id,)
    )
    return cursor.fetchall()