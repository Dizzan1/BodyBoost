# Copyright (C) 2026 Donovan Torres
# Licensed under the GNU Affero General Public License v3.0
# https://www.gnu.org/licenses/agpl-3.0.html

import json
import os
from . import config
from cs50 import SQL

# Thanks https://github.com/yuhonas/free-exercise-db


def init_db():

    print("Checking / creating database...")

    # Ensure database file exists
    if not os.path.exists(config.DB_PATH):
        open(config.DB_PATH, "w").close()

    # Access my database
    db = SQL(f"sqlite:///{config.DB_PATH}")

    # Create the database
    # Users table
    db.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            username TEXT NOT NULL,
            hash TEXT NOT NULL,
            gender TEXT CHECK(gender IN ('male','female')),
            age INTEGER NOT NULL,
            weight INTEGER NOT NULL,
            height INTEGER NOT NULL,
            onerm INTEGER NOT NULL,
            activity_level TEXT CHECK(activity_level IN('sedentary','light','moderate','active','athlete')),
            bmi FLOAT NOT NULL,
            bmr FLOAT NOT NULL,
            tdee FLOAT NOT NULL,
            type_routine TEXT CHECK(type_routine IN('full_body', 'upper_lower', 'body_part')),
            goal TEXT CHECK(goal IN('hypertrophy','power','endurance')),
            exercise_level TEXT CHECK(exercise_level IN('beginner','intermediate','expert'))
        );
    ''')

    db.execute("CREATE UNIQUE INDEX IF NOT EXISTS username ON users (username);")

    # exercises table
    db.execute('''
        CREATE TABLE IF NOT EXISTS exercises (
            id TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL UNIQUE,
            force TEXT NULL,
            level TEXT NOT NULL,
            mechanic TEXT NULL,
            equipment TEXT NULL,
            primaryMuscles TEXT NOT NULL,
            secondaryMuscles TEXT NOT NULL,
            category TEXT NOT NULL,
            instructions TEXT NOT NULL,
            images TEXT NOT NULL
        );
    ''')

    db.execute("CREATE INDEX IF NOT EXISTS exercises_columns "
               "ON exercises (id, name, force, level, mechanic, equipment, primaryMuscles, secondaryMuscles, category, instructions, images)")

    # Third table users -> daily_routine <- exercises
    db.execute('''
        CREATE TABLE IF NOT EXISTS daily_routine (
            user_id INTEGER NOT NULL,
            exercise_id TEXT NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(exercise_id) REFERENCES exercises(id)
        );
    ''')

    db.execute('''
        CREATE TABLE IF NOT EXISTS schedule (
            user_id INTEGER NOT NULL UNIQUE,
            monday TEXT NOT NULL CHECK(monday IN ('rest', 'full_body_day', 'upper_day', 'lower_day', 'chest_day', 'back_day', 'shoulders_day', 'legs_day', 'arms_day')),
            tuesday TEXT NOT NULL CHECK(tuesday IN ('rest', 'full_body_day', 'upper_day', 'lower_day', 'chest_day', 'back_day', 'shoulders_day', 'legs_day', 'arms_day')),
            wednesday TEXT NOT NULL CHECK(wednesday IN ('rest', 'full_body_day', 'upper_day', 'lower_day', 'chest_day', 'back_day', 'shoulders_day', 'legs_day', 'arms_day')),
            thursday TEXT NOT NULL CHECK(thursday IN ('rest', 'full_body_day', 'upper_day', 'lower_day', 'chest_day', 'back_day', 'shoulders_day', 'legs_day', 'arms_day')),
            friday TEXT NOT NULL CHECK(friday IN ('rest', 'full_body_day', 'upper_day', 'lower_day', 'chest_day', 'back_day', 'shoulders_day', 'legs_day', 'arms_day')),
            saturday TEXT NOT NULL CHECK(saturday IN ('rest', 'full_body_day', 'upper_day', 'lower_day', 'chest_day', 'back_day', 'shoulders_day', 'legs_day', 'arms_day')),
            sunday TEXT NOT NULL CHECK(sunday IN ('rest', 'full_body_day', 'upper_day', 'lower_day', 'chest_day', 'back_day', 'shoulders_day', 'legs_day', 'arms_day')),
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
    ''')

    db.execute("CREATE INDEX IF NOT EXISTS schedule_columns "
               "ON schedule (monday, tuesday, wednesday, thursday, friday, saturday, sunday)")

    # History table
    db.execute('''
        CREATE TABLE IF NOT EXISTS history (
                user_id INTEGER NOT NULL,
                exercise_id TEXT NOT NULL,
                date TEXT NOT NULL,
                week TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY(exercise_id) REFERENCES exercises(id)
        );
    ''')

    db.execute('''
        CREATE TABLE IF NOT EXISTS progress (
               user_id INTEGER NOT NULL,
               week_progress INTEGER NOT NULL,
               week_goal INTEGER NOT NULL,
               total_week_progress INTEGER NOT NULL,
               year INTEGER NOT NULL,
               week INTEGER NOT NULL,
               FOREIGN KEY(user_id) REFERENCES users(id)
        );
    ''')

    load_exercises(db)


def load_exercises(db):
    existing_exercises = db.execute("SELECT COUNT(*) AS count FROM exercises")[0]["count"]

    if existing_exercises > 0:
        return
    
    with open(config.DATA_PATH, "r") as file:
        data = json.load(file)

    # Insert JSON data
    for item in data:
        # Convert the primaryMuscles list to a JSON string
        primary_muscles_json = json.dumps(item['primaryMuscles'])
        secondary_muscles_json = json.dumps(item['secondaryMuscles'])
        instructions_json = json.dumps(item['instructions'])
        images_json = json.dumps(item['images'])

        db.execute('''
            INSERT INTO exercises (
                   id, name, force, level, mechanic, equipment,
                   primaryMuscles, secondaryMuscles, category,
                   instructions, images
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        ''',
        item["id"],
        item['name'],
        item['force'],
        item['level'],
        item['mechanic'],
        item['equipment'],
        primary_muscles_json,
        secondary_muscles_json,
        item['category'],
        instructions_json,
        images_json)


if __name__ == "__main__":
    init_db()
