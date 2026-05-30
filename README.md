<img width="1280" height="640" alt="BodyBoost-Logo" src="https://github.com/user-attachments/assets/b7c0cc1b-2aaf-4a87-b6c1-ccd5fa0f950a" />

# BodyBoost

BodyBoost is a Flask web application that helps users build personalized workout routines based on their fitness goal, experience level, weekly schedule, and body metrics. It combines a local exercise database with routine-generation logic, progress tracking, exercise search, and a user dashboard.

https://github.com/user-attachments/assets/4a4d8b6d-93fb-4d91-9657-377597fcb9af

## Features

- User registration and login with password hashing
- Personalized workout routine generation
- Support for full-body, upper/lower, and body-part split routines
- Fitness goals for hypertrophy, power, and endurance
- Beginner, intermediate, and expert exercise levels
- Weekly schedule management
- Daily workout view with exercise details
- Exercise search powered by a local database
- Workout history and progress tracking
- BMI, BMR, TDEE, and one-rep max related user metrics
- Responsive interface built with Flask templates, Bootstrap, and custom CSS

## Tech Stack

- Python
- Flask
- Flask-Session
- SQLite
- CS50 SQL library
- Jinja templates
- Bootstrap
- Chart.js
- JavaScript

## Project Structure

```text
BodyBoost-main/
|-- app/
|   |-- app.py                 # Main Flask application and routes
|   |-- Routine.py             # Routine generation logic
|   |-- create_db.py           # SQLite database setup and exercise import
|   |-- helpers.py             # Authentication and health metric helpers
|   |-- config.py              # Environment-based configuration
|   |-- data/
|   |   `-- exercises.json     # Local exercise dataset
|   |-- static/
|   |   |-- css/
|   |   |-- images/
|   |   `-- js/
|   `-- templates/             # Jinja HTML templates
|-- db/                        # SQLite database location
|-- requirements.txt
|-- run.py
`-- README.md
```

## Getting Started

### Prerequisites

Make sure you have Python 3 installed.

### Installation

Clone the repository and enter the project folder:

```bash
git clone <repository-url>
cd BodyBoost-main
```

Create and activate a virtual environment:

```bash
python -m venv .venv
```

On Windows:

```bash
.venv\Scripts\activate
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

### Environment Variables

BodyBoost can run with its default configuration, but creating a `.env` file is recommended:

```env
SECRET_KEY=replace-with-a-secure-random-secret
DB_PATH=db/bodyboost.db
DATA_PATH=app/data/exercises.json
FLASK_DEBUG=0
```

`SECRET_KEY` is used by Flask sessions. `DB_PATH` controls where the SQLite database is stored, and `DATA_PATH` points to the local exercise dataset.

### Run the App

Start the development server:

```bash
python run.py
```

Then open:

```text
http://127.0.0.1:5000
```

The SQLite database is created automatically on first run if it does not already exist.

## How It Works

BodyBoost stores user profiles, schedules, workout history, progress data, and exercises in SQLite. The exercise data comes from a local JSON file, which is imported into the database during setup.

The routine generator in `app/Routine.py` builds workouts from three user choices:

- Routine type: `full_body`, `upper_lower`, or `body_part`
- Goal: `hypertrophy`, `power`, or `endurance`
- Level: `beginner`, `intermediate`, or `expert`

The app filters exercises by level, muscle group, category, equipment, force, and mechanics, then selects matching exercises for the user's routine. If an exact match is not available, fallback filtering helps keep routine generation flexible.

## Main Pages

- Dashboard: shows weekly progress, total progress, and user training status
- Daily routine: displays the current day's workout
- Exercise search: lets users find exercises from the local database
- Exercise details: shows muscles, equipment, level, instructions, and images
- History: tracks completed exercises
- Settings: lets users update profile and fitness information
- Help: provides guidance about the app and fitness-related inputs

## Exercise Data

The exercise dataset is based on the open-source [Free Exercise Database](https://github.com/yuhonas/free-exercise-db) by yuhonas, released under the Unlicense. The data is stored locally in `app/data/exercises.json` so the application can work without relying on an external API.

## License

This project is licensed under the GNU Affero General Public License v3.0. See the [LICENSE](LICENSE) file for details.

If you need to use this project under different terms (for example, a more permissive license), please contact me to discuss alternative licensing options.
