from flask import Flask, render_template, request, jsonify
from main import analyze_for_web, load_db

app = Flask(__name__)
DESCRIPTIONS, KNOWN_MUTATIONS = load_db()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/main")
def main():
    return render_template("main.htm")

@app.route("/flu")
def flu():
    return render_template("flu_detector.html")

if __name__ == "__main__":
    app.run(debug=True)


@app.route("/analyze", methods=["POST"])
def analyze_api():
    data = request.get_json(silent=True) or {}
    dna = data.get("dna", "")
    report = analyze_for_web(dna, DESCRIPTIONS, KNOWN_MUTATIONS)
    return jsonify(report)


if __name__ == "__main__":
    app.run(debug=True)
