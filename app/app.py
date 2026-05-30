# Copyright (C) 2026 Donovan Torres
# Licensed under the GNU Affero General Public License v3.0
# https://www.gnu.org/licenses/agpl-3.0.html

# Fitness web application
# Standard library
import os
from ast import literal_eval
from datetime import datetime
from urllib.parse import urlparse

# Third_party
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, jsonify, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

# Local imports
from . import config
from .helpers import login_required, bmi, bmr, tdee, apology
from .Routine import generate_routine
from .create_db import init_db

# Configure application
app = Flask(__name__)
app.config["SECRET_KEY"] = config.SECRET_KEY
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
if not os.path.exists(config.DB_PATH):
    init_db()
    
db = SQL(f"sqlite:///{config.DB_PATH}")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():

    update_exercise_level()

    user_row = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])[0]

    progress_row = db.execute("SELECT * FROM progress WHERE user_id = ?", session["user_id"])[0]

    # Caculate progress

    week_progress = progress_row["week_progress"]

    week_goal = progress_row["week_goal"]

    total_week_progress = progress_row["total_week_progress"]

    progress_row["pct_week_progress"] = int((week_progress / week_goal) * 100)

    # Expert
    if total_week_progress >= 16:
        progress_row["pct_total_week_progress"] = 100
        progress_row["next_level"] = "Max level"

    # Intermediate
    elif 16 > total_week_progress >= 8:
        progress_row["pct_total_week_progress"] = int(((total_week_progress - 8) / 8) * 100)
        progress_row["next_level"] = "Expert"

    # Beginner
    else:
        progress_row["pct_total_week_progress"] = int((total_week_progress / 8) * 100)
        progress_row["next_level"] = "Intermediate"

    if progress_row["pct_week_progress"] > 100:
        progress_row["pct_week_progress"] = 100

    if progress_row["pct_total_week_progress"] > 100:
        progress_row["pct_total_week_progress"] = 100

    growth = {

        "monday": {},
        "tuesday": {},
        "wednesday": {},
        "thursday": {},
        "friday": {},
        "saturday": {},
        "sunday": {}

    }

    # Count number exercise per day - this snippet of code with help of cs50.ai
    history_rows = db.execute("SELECT CASE strftime('%w', date) "
                              "WHEN '0' THEN 'sunday' "
                              "WHEN '1' THEN 'monday' "
                              "WHEN '2' THEN 'tuesday' "
                              "WHEN '3' THEN 'wednesday' "
                              "WHEN '4' THEN 'thursday' "
                              "WHEN '5' THEN 'friday' "
                              "WHEN '6' THEN 'saturday' "
                              "END AS day_name, COUNT(*) AS count "
                              "FROM history WHERE user_id = ? GROUP BY date, day_name", session["user_id"])
    schedule_row = db.execute("SELECT * FROM schedule WHERE user_id = ?", session["user_id"])[0]

    # Add exercise day
    for day in growth:
        growth[day]["exercise_day"] = schedule_row[day]
        growth[day]["count"] = 0  # Default value

    # Add number of exercises per day
    for history_row in history_rows:
        growth[history_row["day_name"]]["count"] = history_row["count"]

    return render_template("index.html", user_row=user_row, progress_row=progress_row, growth=growth)


@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user_id
    session.clear()

    if request.method == "POST":

        # Check user input
        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            return apology("Missing username")

        elif not password:
            return apology("Missing password")

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", username
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], password
        ):
            return apology("Invalid username/password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        return redirect("/")

    else:

        return render_template("login.html")


@app.route("/logout")
@login_required
def logout():

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        # Check user input
        username = request.form.get("username")
        password = request.form.get("password")
        gender = request.form.get("gender")
        confirmation_pass = request.form.get("confirmation")
        activity_level = request.form.get("activity_level")
        type_routine = request.form.get("type_routine")
        goal = request.form.get("goal")

        try:
            age = int(request.form.get("age"))
            weight = int(request.form.get("weight"))
            height = int(request.form.get("height"))
            onerm = int(request.form.get("onerm"))
        except (ValueError, TypeError):
            return apology("age, weight and height must be numbers")

        if not username:
            return apology("Missing username")

        if not password or not confirmation_pass:
            return apology("Missing password")

        if password != confirmation_pass:
            return apology("Passwords doesn't match")

        if gender not in ["male", "female"]:
            return apology("Invalid gender")

        if activity_level not in ["sedentary", "light", "moderate", "active", "athlete"]:
            return apology("Invalid activity level")

        days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        schedule = []

        for day in days:
            schedule.append(request.form.get(day))

        if len(schedule) != 7:
            return apology("Invalid number of days")

        counter = 0

        if type_routine == "full_body":
            allowed_values = ["rest", "full_body_day"]

            for day in schedule:
                if day not in allowed_values:
                    return apology("Invalid day")

                if day == "rest":
                    counter += 1

            if counter > 4:
                return apology("No more than 4 rest days (full body)")

        elif type_routine == "upper_lower":
            allowed_values = ["rest", "upper_day", "lower_day"]

            for day in schedule:
                if day not in allowed_values:
                    return apology("Invalid day")

                if day == "rest":
                    counter += 1

            if counter > 3:
                return apology("No more than 3 rest days (upper lower)")

        elif type_routine == "body_part":
            allowed_values = ["rest", "chest_day", "back_day",
                              "shoulders_day", "legs_day", "arms_day"]

            for day in schedule:
                if day not in allowed_values:
                    return apology("Invalid day")

                if day == "rest":
                    counter += 1

            if counter > 2:
                return apology("No more than 2 rest days (body part)")

        else:
            return apology("Invalid type of routine")

        if goal not in ["hypertrophy", "power", "endurance"]:
            return apology("Invalid goal")

        if age < 13 or age > 100:
            return apology("Age must be between 13 and 100")

        if weight < 30 or weight > 200:
            return apology("Weight must be between 30 and 200kg")

        if height < 100 or height > 250:
            return apology("Height must be between 100 and 250cm")

        if onerm < 20 or onerm > 500:
            return apology("1RM must be between 20 and 500kg")

        # Insert username and hash
        hash = generate_password_hash(password)

        # Calculate bmi, bmr, tdee
        bmi_result = bmi(weight, height)
        bmr_result = bmr(gender, weight, height, age)
        tdee_result = tdee(activity_level, gender, weight, height, age)

        # Assign exercise_level:
        if activity_level in ["sedentary", "light"]:
            exercise_level = "beginner"

        elif activity_level in ["moderate", "active"]:
            exercise_level = "intermediate"

        else:
            exercise_level = "expert"

        # Load info to users table
        try:
            db.execute("INSERT INTO users (username, hash, gender, age, weight, height, bmi, bmr, tdee, activity_level, type_routine, goal, exercise_level, onerm) "
                       "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       username, hash, gender, age, weight, height, bmi_result, bmr_result, tdee_result, activity_level, type_routine, goal, exercise_level, onerm)
        except ValueError:
            # If username already exists
            return apology("username already exists")

        # Load info to schedule table
        id = db.execute("SELECT id FROM users WHERE username = ?", username)[0]["id"]

        monday = schedule[0]
        tuesday = schedule[1]
        wednesday = schedule[2]
        thursday = schedule[3]
        friday = schedule[4]
        saturday = schedule[5]
        sunday = schedule[6]

        db.execute("INSERT INTO schedule (user_id, monday, tuesday, wednesday, thursday, friday, saturday, sunday)"
                   "VALUES (?, ?, ?, ?, ?, ?, ?, ?)", id, monday, tuesday, wednesday, thursday, friday, saturday, sunday)

        # Load first week goal to progress
        update_week_goal(id)

        return redirect("/")

    else:

        return render_template("register.html")


@app.route("/daily_routine")
@login_required
def daily_routine():

    update_exercise_level()

    # Get routine
    exercises = update_daily_routine()

    # If rest day
    if exercises is None:
        return render_template("daily_routine.html")

    # If exercise day
    else:
        # Query info
        user_and_schedule_rows = db.execute("SELECT * FROM users JOIN schedule ON users.id = schedule.user_id "
                                            "WHERE id = ?", session["user_id"])

        now = datetime.now()
        day_name = now.strftime("%A").lower()
        exercise_day = user_and_schedule_rows[0][day_name]
        type_routine = user_and_schedule_rows[0]["type_routine"]
        goal = user_and_schedule_rows[0]["goal"]
        exercise_level = user_and_schedule_rows[0]["exercise_level"]
        onerm = user_and_schedule_rows[0]["onerm"]

        if goal == "hypertrophy":
            recommendation = f"Recommendation: 3-6 sets, 6-12 reps, 30s-90s rest period and {int(onerm * 0.67)}kg-{int(onerm * 0.85)}kg of 1RM intensity"
        elif goal == "power":
            recommendation = f"Recommendation: 3-5 sets, 1-2 reps, 2min-5min rest period and {int(onerm * 0.80)}kg-{int(onerm * 0.90)}kg of 1RM intensity"
        elif goal == "endurance":
            recommendation = f"Recommendation: 3-4 sets, 12-20+ reps, up to 30s rest period and <{int(onerm * 0.67)}kg of 1RM intensity"
        else:
            return apology("Invalid goal")

        return render_template("daily_routine.html", exercises=exercises, exercise_day=exercise_day, type_routine=type_routine, goal=goal, exercise_level=exercise_level, recommendation=recommendation)


@app.route("/search-exercise")
@login_required
def search_exercise():

    update_exercise_level()

    return render_template("search_exercise.html")


@app.route("/exercise")
@login_required
def exercise():

    update_exercise_level()

    exercise_id = request.args.get('id')

    if not exercise_id:
        return apology("Invalid exercise id")

    # Query database
    exercise_rows = exercises_for_today("exercise", exercise_id)

    # No exercise found
    if exercise_rows is None:
        return apology("Invalid exercise id")

    exercise = exercise_rows[0]

    return render_template("exercise.html", exercise=exercise)


@app.route("/search", methods=['POST'])
@login_required
def search():

    data = request.get_json()

    filters = {}

    # Check user input
    if data.get("name"):
        filters["filter1"] = {"name": data["name"]}
    elif data.get("primaryMuscles"):
        filters["filter1"] = {"primaryMuscles": data["primaryMuscles"]}
    else:
        return jsonify([])

    if data.get("category"):
        filters["filter2"] = {"category": data["category"]}
    else:
        return jsonify([])

    # Get exercises - this snippet of code with help of cs50.ai
    for key in filters["filter1"]:

        if filters["filter2"]["category"] == "all":
            exercises = db.execute("SELECT * FROM exercises WHERE " + key +
                                   " LIKE ? ORDER BY RANDOM() LIMIT 10", "%" + filters["filter1"][key] + "%")
        else:
            exercises = db.execute("SELECT * FROM exercises WHERE " + key + " LIKE ? AND category = ? ORDER BY RANDOM() LIMIT 10",
                                   "%" + filters["filter1"][key] + "%", filters["filter2"]["category"])

    return jsonify(exercises)


@app.route("/history")
@login_required
def history():

    update_exercise_level()

    # Query history table and exercises
    exercises = exercises_for_today("history")

    # No history registered
    if exercises is None:
        now = datetime.now()
        week = now.strftime("%Y-%U")

        return render_template("history.html", week=week)

    history_exercises = {}

    # Seperate by date
    for exercise in exercises:
        # parse string to datetime object
        date_object = datetime.strptime(exercise["date"], "%Y-%m-%d")
        day_name = date_object.strftime("%A")

        if day_name in history_exercises:
            history_exercises[day_name].append(exercise)

        else:
            history_exercises[day_name] = [exercise]

    return render_template("history.html", history_exercises=history_exercises, week=exercises[0]["week"])


@app.route("/settings", methods=["POST", "GET"])
@login_required
def settings():

    update_exercise_level()

    if request.method == "POST":

        form_id = request.form.get("form_id")

        if form_id not in ["form1", "form2"]:
            return apology("Invalid form")

        # Change body info
        if form_id == "form1":

            # Check user input
            gender = request.form.get("gender")
            activity_level = request.form.get("activity_level")

            try:
                age = int(request.form.get("age"))
                weight = int(request.form.get("weight"))
                height = int(request.form.get("height"))
                onerm = int(request.form.get("onerm"))
            except (ValueError, TypeError):
                return apology("age, weight and height must be numbers")

            if gender not in ["male", "female"]:
                return apology("Invalid gender")

            if activity_level not in ["sedentary", "light", "moderate", "active", "athlete"]:
                return apology("Invalid activity level")

            if age < 13 or age > 100:
                return apology("Age must be between 13 and 100")

            if weight < 30 or weight > 200:
                return apology("Weight must be between 30 and 200")

            if height < 100 or height > 250:
                return apology("Height must be between 100 and 250")

            if onerm < 20 or onerm > 500:
                return apology("1RM must be between 20 and 500kg")

            # Calculate bmi, bmr, tdee
            bmi_result = bmi(weight, height)
            bmr_result = bmr(gender, weight, height, age)
            tdee_result = tdee(activity_level, gender, weight, height, age)

            # Update users table
            db.execute("UPDATE users SET gender = ?, age = ?, weight = ?, height = ?, activity_level = ?, bmi = ?, bmr = ?, tdee = ?, onerm = ? "
                       "WHERE id = ? ", gender, age, weight, height, activity_level, bmi_result, bmr_result, tdee_result, onerm, session["user_id"])

            flash("Body info changed!")

            return redirect("/settings")

        # Reset password
        else:

            old_password = request.form.get("old_password")
            new_password = request.form.get("new_password")
            confirmation = request.form.get("confirmation")

            # Check inputs
            if not old_password:
                return apology("Missing old pass")

            if not new_password:
                return apology("Missing new pass")

            if not confirmation:
                return apology("Missing confirmation pass")

            current_hash = db.execute("SELECT hash FROM users WHERE id = ?",
                                      session["user_id"])[0]["hash"]

            if not check_password_hash(current_hash, old_password):
                return apology("Incorrect old password")

            if new_password != confirmation:
                return apology("new password and confirmation do not match")

            # Change password
            new_hash = generate_password_hash(new_password)
            db.execute("UPDATE users SET hash = ? WHERE id = ?", new_hash, session["user_id"])

            # Forget any user_id
            session.clear()

            # Redirect user to login form
            return redirect("/")

    else:

        user_row = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])[0]

        return render_template("settings.html", user_row=user_row)


@app.route("/update_history", methods=["POST"])
@login_required
def update_history():

    # Security measure
    update_exercise_level()

    # Check user input
    referrer_url = request.referrer

    parsed_url = urlparse(referrer_url)

    data = request.get_json()

    action = data["action"]
    exercise_id = data["exercise_id"]

    if action not in ["add", "remove"]:
        return jsonify(success=False, error="Invalid action")

    if action == "add" and parsed_url.path == "/history":
        return jsonify(success=False, error="Can't add from /history")

    if len(db.execute("SELECT * FROM exercises WHERE id = ?", exercise_id)) == 0:
        return jsonify(success=False, error="Invalid exercise_id")

    now = datetime.now()
    formatted_week = now.strftime("%Y-%W")
    formatted_date = now.strftime("%Y-%m-%d")

    try:

        # Adding register
        if action == "add":

            # Insert new register
            db.execute("INSERT INTO history (user_id ,exercise_id, date, week) VALUES (?, ?, ?, ?)",
                       session["user_id"], exercise_id, formatted_date, formatted_week)

            update_progress("add")

        # Removing register
        else:

            # Filter history table by id exercise
            db.execute("DELETE FROM history WHERE user_id = ? AND week = ? AND exercise_id = ?",
                       session["user_id"], formatted_week, exercise_id)

            update_progress("remove")

        return jsonify(success=True)

    except Exception as e:
        return jsonify(success=False, error=str(e))


@app.route("/help")
@login_required
def help():

    return render_template("help.html")

### OTHER FUNCTIONS ###


def update_daily_routine():

    # Info to check if today's routine has been generated
    now = datetime.now()
    formatted_date = now.strftime("%Y-%m-%d")
    daily_routine_rows = db.execute(
        "SELECT * FROM daily_routine WHERE user_id = ? AND date = ?", session["user_id"], formatted_date)

    # Query info
    user_and_schedule_rows = db.execute("SELECT * FROM users JOIN schedule ON users.id = schedule.user_id "
                                        "WHERE id = ?", session["user_id"])

    day_name = now.strftime("%A").lower()
    exercise_day = user_and_schedule_rows[0][day_name]

    # Check if today is a rest day
    if exercise_day == "rest":

        # Delete previous routine
        db.execute("DELETE FROM daily_routine WHERE user_id = ?", session["user_id"])

        return None

    # Routine already generated
    elif len(daily_routine_rows) != 0:

        # Get routine with info parsed
        exercises = exercises_for_today("daily_routine")

    # Generate today's routine
    else:

        # Delete previous routine
        db.execute("DELETE FROM daily_routine WHERE user_id = ?", session["user_id"])

        # Load exercise_id and date to daily_routine
        type_routine = user_and_schedule_rows[0]["type_routine"]
        goal = user_and_schedule_rows[0]["goal"]
        exercise_level = user_and_schedule_rows[0]["exercise_level"]

        routine = generate_routine(type_routine, goal, exercise_level)

        for exercise in routine[exercise_day]:
            db.execute("INSERT INTO daily_routine (user_id, date, exercise_id) VALUES (?, ?, ?) ",
                       session["user_id"], formatted_date,  exercise["id"])

        # Get routine with info parsed
        exercises = exercises_for_today("daily_routine")

    return exercises


def exercises_for_today(query: str, exercise_id: str = None):

    # Query daily_routine table
    if query == "daily_routine":

        exercises_rows = db.execute("SELECT id, name, category, primaryMuscles, secondaryMuscles, instructions, images, force, mechanic, equipment, level "
                                    "FROM daily_routine JOIN exercises ON daily_routine.exercise_id = exercises.id "
                                    "WHERE user_id = ?", session["user_id"])

    # Query history table
    elif query == "history":

        now = datetime.now()
        formatted_week = now.strftime("%Y-%W")

        exercises_rows = db.execute("SELECT id, name, category, primaryMuscles, secondaryMuscles, instructions, images, force, mechanic, equipment, level, week, date "
                                    "FROM history JOIN exercises ON history.exercise_id = exercises.id "
                                    "WHERE user_id = ? AND week = ?", session["user_id"], formatted_week)

        # Check result query
        if len(exercises_rows) == 0:
            return None

    # Query exercises for especific exercise
    elif query == "exercise":

        exercises_rows = db.execute("SELECT * FROM exercises WHERE id = ?", exercise_id)

        # Check result query
        if len(exercises_rows) != 1:
            return None

    # Parse
    for exercise in exercises_rows:
        exercise["primaryMuscles"] = literal_eval(exercise["primaryMuscles"])

        exercise["secondaryMuscles"] = literal_eval(exercise["secondaryMuscles"])

        exercise["instructions"] = literal_eval(exercise["instructions"])

        exercise["images"] = literal_eval(exercise["images"])

        if not exercise["primaryMuscles"]:
            exercise["primaryMuscles"].append("Not found")

        if not exercise["secondaryMuscles"]:
            exercise["secondaryMuscles"].append("Not found")

        if not exercise["instructions"]:
            exercise["instructions"].append("Not found")

        if exercise["force"] is None:

            exercise["force"] = "null"

        if exercise["mechanic"] is None:

            exercise["mechanic"] = "null"

        if exercise["equipment"] is None:

            exercise["equipment"] = "null"

    # Mark exercises done -> exercises["history"] = bool
    exercises_rows = mark_exercises_done(exercises_rows)

    return exercises_rows


def mark_exercises_done(exercises):

    now = datetime.now()
    formatted_date = now.strftime("%Y-%m-%d")

    # Check exercises done today
    history_rows = db.execute(
        "SELECT exercise_id FROM history WHERE user_id = ? AND date = ?", session["user_id"], formatted_date)

    # Extract exercise IDs into a set for faster lookup
    history_exercises_id = {value for exercise in history_rows for value in exercise.values()}

    # Mark exercises as done or not done
    for exercise in exercises:
        exercise["history"] = exercise["id"] in history_exercises_id

    return exercises


def update_exercise_level():

    # RESET EVEY WEEK -> WEEK PROGRESS
    now = datetime.now()
    year_current = int(now.strftime("%Y"))
    week_current = int(now.strftime("%W"))

    progress_row = db.execute("SELECT * FROM progress WHERE user_id = ?", session["user_id"])[0]
    year_last = progress_row["year"]
    week_last = progress_row["week"]
    total_week_progress = progress_row["total_week_progress"]
    week_goal = progress_row["week_goal"]
    week_progress = progress_row["week_progress"]
    weeks_difference = calculate_week_difference(year_current, week_current, year_last, week_last)

    # New week
    if weeks_difference > 0:

        # More than week without working out
        if weeks_difference > 1:
            flash("Since you skipped working out for a week, your progress will be reduced!")

            total_week_progress = max(0, total_week_progress - (weeks_difference - 1))

        # If week goal no completed, decrease total week progress
        if week_progress < week_goal:
            flash("You didn´t complete your week goal, your progress will be reduced!")
            total_week_progress -= 1

        db.execute("UPDATE progress SET total_week_progress = ? WHERE user_id = ?",
                   total_week_progress, session["user_id"])

        # Change exercise level
        if total_week_progress >= 16:
            exercise_level = "expert"

        elif 16 > total_week_progress >= 8:
            exercise_level = "intermediate"

        else:
            exercise_level = "beginner"

        db.execute("UPDATE users SET exercise_level = ? WHERE id = ?",
                   exercise_level, session["user_id"])

        # Reset week progress
        db.execute("UPDATE progress SET week_progress = 0, year = ?, week = ? WHERE user_id = ?",
                   year_current, week_current, session["user_id"])

        update_week_goal()

        # Clear week history
        db.execute("DELETE FROM history WHERE user_id = ?", session["user_id"])


def update_progress(action: str):

    progress_row = db.execute("SELECT * FROM progress WHERE user_id = ?", session["user_id"])[0]
    week_progress = progress_row["week_progress"]
    week_goal = progress_row["week_goal"]
    total_week_progress = progress_row["total_week_progress"]

    was_goal_achieved = week_progress >= week_goal

    # EXERCISE ADDED
    if action == "add":

        # Increment week_progress
        week_progress += 1

        # Check if the goal status changed
        if not was_goal_achieved and week_progress >= week_goal:
            flash("Week goal completed!")
            total_week_progress += 1

    # EXERCISE REMOVED
    elif action == "remove":

        # Decrement week_progress only if it's above 0
        if week_progress > 0:
            week_progress -= 1

            # Check if the goal status changed
            if was_goal_achieved and week_progress < week_goal:
                flash("You didn't complete your week goal!")
                total_week_progress -= 1

    db.execute("UPDATE progress SET week_progress = ?, total_week_progress = ? WHERE user_id = ?",
               week_progress, total_week_progress, session["user_id"])

 # This snippet of code with help of cs50.ai


def calculate_week_difference(year1: int, week1: int, year2: int, week2: int):

    # Number of weeks in a year, considering leap years could affect day of the week
    weeks_per_year = 52

    # Convert both year-week pairs to a total week count from a common reference point
    total_weeks1 = year1 * weeks_per_year + week1
    total_weeks2 = year2 * weeks_per_year + week2

    # Calculate the difference in total weeks
    return total_weeks1 - total_weeks2


def update_week_goal(id: int | None = None):

    if id is None:
        id = session["user_id"]

    # Get exercise_days
    schedule = db.execute(
        "SELECT monday, tuesday, wednesday, thursday, friday, saturday, sunday FROM schedule WHERE user_id = ?", id)[0]

    exercise_days = list(schedule.values())

    # Exclude rest days
    exercise_days = [exercise_day for exercise_day in exercise_days if exercise_day != "rest"]

    # calculate week goal
    user_row = db.execute(
        "SELECT type_routine, goal, exercise_level FROM users WHERE id = ?", id)[0]

    routines = generate_routine(user_row["type_routine"],
                                user_row["goal"], user_row["exercise_level"])

    week_goal = 0

    for exercise_day in exercise_days:
        week_goal += len(routines[exercise_day])

    progress_row = db.execute("SELECT * FROM progress WHERE user_id = ?", id)

    # Update
    if progress_row:
        db.execute("UPDATE progress SET week_goal = ? WHERE user_id = ?", week_goal, id)

    # Insert
    else:
        now = datetime.now()
        year = int(now.strftime("%Y"))
        week = int(now.strftime("%W"))

        exercise_level = user_row["exercise_level"]

        if exercise_level == "beginner":
            total_week_progress = 0

        elif exercise_level == "intermediate":
            total_week_progress = 8

        else:
            total_week_progress = 16

        db.execute("INSERT INTO progress (user_id, week_progress, week_goal, total_week_progress, year, week) "
                   "VALUES (?, 0, ?, ?, ?, ?)", id, week_goal, total_week_progress, year, week)