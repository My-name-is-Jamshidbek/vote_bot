"""
data base
"""

import time
import datetime
# from cryptography.fernet import Fernet

from config import *

import sqlite3
from sqlite3 import Connection

if not os.path.exists("database.db"):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    # Create the candidates table
    c.execute("""
                CREATE TABLE candidates (
                id INTEGER PRIMARY KEY, 
                short_name TEXT, 
                full_name TEXT,
                region TEXT, 
                voices INTEGER,
                introduction_url TEXT
                )""")

    # Create the users table with a foreign key reference to candidates
    c.execute("""
        CREATE TABLE users (
            telegram_id INTEGER PRIMARY KEY,
            candidate_id INTEGER,
            fullname TEXT,
            FOREIGN KEY (candidate_id) REFERENCES candidates(id)
        )
    """)
    c.execute(
        "CREATE TABLE channels (id INTEGER PRIMARY KEY, name TEXT, link INTEGER)")

    conn.commit()
    conn.close()

def create_channel(name, link):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("INSERT INTO channels (name, link) VALUES (?, ?)", (name, link))

    conn.commit()
    conn.close()

def read_channels():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("SELECT * FROM channels")
    rows = c.fetchall()

    channels = []
    for row in rows:
        channels.append({"id": row[0], "name": row[1], "link": row[2]})

    return channels

def delete_channel(channel_name):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    # Delete the channel with the specified ID
    c.execute("DELETE FROM channels WHERE name=?", (channel_name,))

    conn.commit()
    conn.close()

def read_regions():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("SELECT DISTINCT region FROM candidates")
    rows = c.fetchall()

    regions = list(set(row[0] for row in rows))

    conn.close()

    return regions

def read_candidates_short_names(region):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("SELECT short_name FROM candidates WHERE region=?", (region,))
    rows = c.fetchall()

    short_names = [row[0] for row in rows]

    conn.close()

    return short_names

def create_candidate(short_name, full_name, region, introduction_url):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    # Insert a new candidate into the candidates table
    c.execute("INSERT INTO candidates (short_name, full_name, region, voices, introduction_url) VALUES (?, ?, ?, ?, ?)",
              (short_name, full_name, region, 0, introduction_url))

    conn.commit()
    conn.close()

def check_exist_user(telegram_id):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM users WHERE telegram_id=?", (telegram_id,))
    result = c.fetchone()[0]

    conn.close()

    return result > 0

def get_candidate_full_name(region, short_name):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("SELECT full_name FROM candidates WHERE region=? AND short_name=?", (region, short_name))
    result = c.fetchone()

    conn.close()

    return result[0] if result else None

def get_candidate_data(region, short_name):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("SELECT introduction_url, voices, id FROM candidates WHERE region=? AND short_name=?", (region, short_name))
    result = c.fetchone()

    conn.close()

    return result if result else None

def get_candidate_data_id(_id):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("SELECT introduction_url, voices, full_name FROM candidates WHERE id=?", (_id,))
    result = c.fetchone()

    conn.close()

    return result if result else None

def add_a_voice_candidate(candidate_id):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    # Increment the voices count for the specified candidate
    c.execute("UPDATE candidates SET voices = voices + 1 WHERE id=?", (candidate_id,))

    conn.commit()
    conn.close()

def add_new_user(user_id, full_name, candidate_id):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    # Insert a new user into the users table
    c.execute("INSERT INTO users (telegram_id, candidate_id, fullname) VALUES (?, ?, ?)",
              (user_id, candidate_id, full_name))

    conn.commit()
    conn.close()

def delete_user(_id):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    # Delete the channel with the specified ID
    c.execute("DELETE FROM users WHERE telegram_id=?", (_id,))

    conn.commit()
    conn.close()