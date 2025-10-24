import os
import json
from flask import Flask, render_template, request

app = Flask(__name__)

# --- Safe file paths for Render ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
schemes_path = os.path.join(BASE_DIR, "data", "schemes.json")
exams_path = os.path.join(BASE_DIR, "data", "exams.json")

# --- Load JSON files safely ---
try:
    with open(schemes_path, encoding="utf-8") as f:
        schemes = json.load(f)
    with open(exams_path, encoding="utf-8") as f:
        exams = json.load(f)
except Exception as e:
    print("❌ Error loading JSON files:", e)
    schemes = []
    exams = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/recommend", methods=["POST"])
def recommend():
    try:
        age = int(request.form["age"])
        gender = request.form["gender"]
        qualification = request.form["qualification"]

        # Filter schemes
        matched_schemes = [
            s for s in schemes
            if (s["gender"] == "any" or s["gender"] == gender)
            and s["min_age"] <= age <= s["max_age"]
        ]

        # Filter exams
        matched_exams = [
            e for e in exams
            if e["min_age"] <= age <= e["max_age"]
            and e["qualification"] == qualification
        ]

        return render_template("results.html",
                               schemes=matched_schemes,
                               exams=matched_exams)

    except Exception as e:
        # If anything goes wrong, show the error on screen
        return f"<h2 style='color:red;'>Server Error: {e}</h2>"

if __name__ == "__main__":
    app.run(debug=True)
