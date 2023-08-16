import sqlite3
import os
from datetime import datetime

class VideoDatabase:
    def __init__(self, db_name='video_data.db'):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connect()

    def create_database(self):
        if not os.path.exists(self.db_name):
            self.conn = sqlite3.connect(self.db_name)
            self.conn.close()
            print("Database created.")
        else:
            print("Database already exists.")

    def connect(self):
        if os.path.exists(self.db_name):
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
        else:
            print("Database does not exist.")
            self.create_database()

    def create_table(self):
        if self.conn is not None:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS videos (
                    id INTEGER PRIMARY KEY,
                    video_id TEXT UNIQUE,
                    username TEXT,
                    likes REAL,
                    shares REAL,
                    plays REAL,
                    thumbnail TEXT,
                    description TEXT,
                    hashtags TEXT,
                    region TEXT,
                    timestamp TEXT
                )
            ''')
            self.conn.commit()
            print("Table created.")

    def insert_data(self, data):
        if self.conn is not None:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.cursor.execute('''
                INSERT OR IGNORE INTO videos (video_id, username, likes, shares, plays, thumbnail, description, hashtags, region, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                data['video_id'], data['username'], data['likes'], data['shares'], data['plays'],
                data['thumbnail'], data['description'], data['hashtags'], data['region'], timestamp
            ))
            self.conn.commit()
            print("Data Inserted")

    def select_all(self):
        if self.conn is not None:
            self.cursor.execute("SELECT * FROM videos")
            return self.cursor.fetchall()

    def close(self):
        if self.conn is not None:
            self.conn.close()

if __name__ == "__main__":
   
    db = VideoDatabase()
    db.connect()

    selected_data = db.select_all()
    if selected_data:
        for row in selected_data:
            print(row)
    else:
        print("No data found.")

    db.close()
