# Copyright (C) 2026 Donovan Torres
# Licensed under the GNU Affero General Public License v3.0
# https://www.gnu.org/licenses/agpl-3.0.html

from flask import redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

# Fuctions related to health

# BMI (Body mass index)


def bmi(weight: int, height: int):

    # cm to m
    height = height / 100

    bmi_result = weight / (height ** 2)

    bmi_result = round(bmi_result, 2)

    return bmi_result

# BMR (Basal metabolic rate)


def bmr(gender: str, weight: int, height: int, age: int):

    if "male" == gender:

        bmr_result = 10 * weight + 6.25 * height - 5 * age + 5

    elif "female" == gender:

        bmr_result = 10 * weight + 6.25 * height - 5 * age - 161

    # Limit to 2 decimals
    bmr_result = round(bmr_result, 2)

    return bmr_result

# TDEE (total daily energy expenditure) BMR + activity


def tdee(activity_level: str, gender: str, weight: int, height: int, age: int):

    # Calculates BMR
    bmr_result = bmr(gender, weight, height, age)

    if activity_level == "sedentary":

        tdee_result = bmr_result * 1.2

    elif activity_level == "light":

        tdee_result = bmr_result * 1.375

    elif activity_level == "moderate":

        tdee_result = bmr_result * 1.55

    elif activity_level == "active":

        tdee_result = bmr_result * 1.725

    elif activity_level == "athlete":

        tdee_result = bmr_result * 1.9

    # Limit to 2 decimals
    tdee_result = round(tdee_result, 2)

    return tdee_result
