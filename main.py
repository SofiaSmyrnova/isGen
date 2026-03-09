from flask import Flask, render_template, request, jsonify
from main import analyze_for_web, load_db

app = Flask(__name__)
DESCRIPTIONS, KNOWN_MUTATIONS = load_db()

from flue import check_patient

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze_api():
    data = request.get_json(silent=True) or {}
    dna = data.get("dna", "")
    report = analyze_for_web(dna, DESCRIPTIONS, KNOWN_MUTATIONS)
    return jsonify(report)

@app.route("/flue-detector")
def flue_detector():
    return render_template("flue_detector.html")

# 
@app.route("/api/flue-detector", methods=["POST"])
def flue_detector_api():
    data = request.get_json(silent=True) or {}
    patients = data.get("patients", [])

    if not isinstance(patients, list):
        return jsonify({"results": []}), 400

    results = []

    for patient in patients:
        if not isinstance(patient, dict):
            results.append({
                "message": "Invalid patient data",
                "status": "error",
                "temperature": None,
                "saturation": None
            })
            continue

        result = check_patient(patient)

        results.append({
            "message": result["message"],
            "status": result["status"],
            "temperature": patient.get("temperature"),
            "saturation": patient.get("saturation")
        })

    return jsonify({"results": results})
#

if __name__ == "__main__":
    app.run(debug=True)
