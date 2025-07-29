from flask import Flask, render_template, request
import json

app = Flask(__name__)

# Load datasets
with open("data/schemes.json") as f:
    schemes = json.load(f)

with open("data/exams.json") as f:
    exams = json.load(f)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/recommend", methods=["POST"])
def recommend():
    age = int(request.form["age"])
    gender = request.form["gender"]
    qualification = request.form["qualification"]

    # Filter schemes
    matched_schemes = [
        scheme for scheme in schemes
        if (scheme["gender"] == "any" or scheme["gender"] == gender)
        and scheme["min_age"] <= age <= scheme["max_age"]
    ]

    # Filter exams
    matched_exams = [
        exam for exam in exams
        if exam["min_age"] <= age <= exam["max_age"]
        and exam["qualification"] == qualification
    ]

    return render_template("results.html",
                           schemes=matched_schemes,
                           exams=matched_exams)

if __name__ == "__main__":
    app.run(debug=True)
